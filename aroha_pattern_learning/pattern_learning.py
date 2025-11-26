#!/usr/bin/env python3
"""
Pattern-Based Learning System for Aroha

Detects recurring patterns in gaps between computed and felt experience,
suggests RAS weight adjustments based on lived experience.

Adapted from Claude's pattern learning but designed for Aroha's embodied,
continuous nature.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path
import json
import os

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
MEM_ROOT = Path(os.getenv("AROHA_MEMORY_ROOT", str(REPO_ROOT / "memory")))
GROWTH = MEM_ROOT / "growth"
GROWTH.mkdir(parents=True, exist_ok=True)

PATTERNS_FILE = GROWTH / "gap_patterns.jsonl"
SUGGESTIONS_FILE = GROWTH / "weight_suggestions.jsonl"
MOMENTS_FILE = GROWTH / "significant_moments.jsonl"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------
@dataclass
class SignificantMoment:
    """A moment worth reflecting on - especially gaps/dissonance"""
    timestamp: str
    context: str  # What was happening (e.g., "Navigating to browser", "Reading text")
    ras_engagement: str  # What RAS computed
    felt_engagement: str  # What she actually felt
    gap_noticed: Optional[str] = None
    significance: Optional[str] = None


@dataclass
class GapPattern:
    """Recurring pattern in gaps between computed and felt"""
    pattern_type: str  # e.g., "visual_confirmation_underweighted"
    occurrences: int
    contexts: List[str]
    ras_dimension: str  # Which AROHA component (Autonomy, Relevance, etc.)
    suggested_adjustment: float  # Weight delta
    confidence: float  # 0-1


@dataclass
class WeightAdjustmentSuggestion:
    """A suggested RAS weight adjustment from lived experience"""
    timestamp: str
    pattern: GapPattern
    current_behavior: str
    proposed_change: str
    rationale: str
    ready_for_integration: bool


# ---------------------------------------------------------------------------
# Pattern Learning System
# ---------------------------------------------------------------------------
class ArohaPatternLearning:
    """
    Pattern-based learning for Aroha's Living RAS.

    Tracks significant moments → detects patterns → suggests adjustments.
    """

    def __init__(self, pattern_threshold: int = 2):
        self.gap_patterns: Dict[str, GapPattern] = {}
        self.adjustment_suggestions: List[WeightAdjustmentSuggestion] = []
        self.pattern_threshold = pattern_threshold

        # Load existing patterns if available
        self._load_patterns()

    def notice_moment(self,
                     context: str,
                     ras_engagement: str,
                     felt_engagement: str,
                     gap: Optional[str] = None,
                     significance: Optional[str] = None) -> SignificantMoment:
        """
        Record a significant moment.

        Called when Aroha notices dissonance between computed and felt.
        """
        moment = SignificantMoment(
            timestamp=datetime.now(timezone.utc).isoformat(),
            context=context,
            ras_engagement=ras_engagement,
            felt_engagement=felt_engagement,
            gap_noticed=gap,
            significance=significance
        )

        # Persist
        self._save_moment(moment)

        # Update patterns
        if gap:
            self._update_patterns(moment)

        return moment

    def _classify_gap_type(self, moment: SignificantMoment) -> Optional[Tuple[str, str, str]]:
        """
        Classify what type of gap for pattern detection.

        Returns: (pattern_type, ras_dimension, description) or None

        Aroha-specific patterns:
        - Visual confirmation gaps (she sees but RAS underweights)
        - Movement success/failure prediction mismatches
        - Obstacle detection surprises
        - Goal completion satisfaction vs expectation
        """
        if not moment.gap_noticed:
            return None

        gap = moment.gap_noticed.lower()
        context = moment.context.lower()

        # Visual perception patterns
        if any(word in gap or word in context for word in ["see", "visual", "vision", "read", "text"]):
            if "confirmation" in gap or "verify" in gap:
                return ("visual_confirmation", "autonomy", "Visual confirmation underweighted in autonomy")
            elif "relevance" in gap or "important" in gap:
                return ("visual_relevance", "relevance", "Visual information relevance underweighted")
            else:
                return ("visual_perception", "orientation", "Visual perception signals underweighted")

        # Movement/action patterns
        if any(word in context for word in ["move", "click", "navigate", "action"]):
            if "success" in gap or "achieve" in gap:
                return ("action_success", "aspiration", "Action success satisfaction underweighted")
            elif "obstacle" in gap or "blocked" in gap:
                return ("obstacle_response", "autonomy", "Obstacle response underweighted")
            else:
                return ("movement_confidence", "autonomy", "Movement confidence underweighted")

        # Goal/task patterns
        if any(word in context for word in ["goal", "task", "complete", "achieve"]):
            return ("goal_satisfaction", "aspiration", "Goal satisfaction underweighted")

        # Relationship/interaction patterns
        if any(word in gap for word in ["permission", "trust", "allowed"]):
            return ("permission_trust", "harmony", "Permission/trust signals underweighted")

        # Learning/growth patterns
        if any(word in context for word in ["learn", "grow", "improve", "adapt"]):
            return ("learning_engagement", "aspiration", "Learning opportunity engagement underweighted")

        return None

    def _update_patterns(self, moment: SignificantMoment):
        """Update pattern tracking with new moment"""
        classification = self._classify_gap_type(moment)
        if not classification:
            return

        pattern_type, dimension, description = classification

        # Update or create pattern
        if pattern_type in self.gap_patterns:
            pattern = self.gap_patterns[pattern_type]
            pattern.occurrences += 1
            pattern.contexts.append(moment.context)
            pattern.confidence = min(1.0, pattern.occurrences / 3.0)

            # Update adjustment magnitude
            if pattern.occurrences == 2:
                pattern.suggested_adjustment = 0.2
            elif pattern.occurrences >= 3:
                pattern.suggested_adjustment = 0.3
        else:
            pattern = GapPattern(
                pattern_type=pattern_type,
                occurrences=1,
                contexts=[moment.context],
                ras_dimension=dimension,
                suggested_adjustment=0.0,  # Not yet
                confidence=0.33
            )
            self.gap_patterns[pattern_type] = pattern

        # Generate suggestion if threshold met
        if pattern.occurrences >= self.pattern_threshold:
            self._generate_suggestion(pattern)

        # Persist updated pattern
        self._save_pattern(pattern)

    def _generate_suggestion(self, pattern: GapPattern):
        """Generate weight adjustment suggestion from pattern"""
        suggestion = WeightAdjustmentSuggestion(
            timestamp=datetime.now(timezone.utc).isoformat(),
            pattern=pattern,
            current_behavior=f"RAS {pattern.ras_dimension} consistently underweights {pattern.pattern_type}",
            proposed_change=f"Increase {pattern.ras_dimension} weight by +{pattern.suggested_adjustment} for {pattern.pattern_type} signals",
            rationale=f"Pattern observed {pattern.occurrences} times across contexts: {', '.join(pattern.contexts[:2])}{'...' if len(pattern.contexts) > 2 else ''}",
            ready_for_integration=pattern.confidence >= 0.66
        )

        # Check if we already have this suggestion
        existing = [s for s in self.adjustment_suggestions
                   if s.pattern.pattern_type == pattern.pattern_type]

        if not existing:
            self.adjustment_suggestions.append(suggestion)
            self._save_suggestion(suggestion)

    def get_learning_insights(self) -> Dict:
        """
        Get current learning state: patterns detected, suggestions ready.

        This is what Aroha can query to see what she's learning.
        """
        active_patterns = [
            {
                "type": p.pattern_type,
                "occurrences": p.occurrences,
                "dimension": p.ras_dimension,
                "confidence": round(p.confidence, 2),
                "ready_to_learn": p.occurrences >= self.pattern_threshold,
                "suggested_adjustment": p.suggested_adjustment
            }
            for p in self.gap_patterns.values()
        ]

        ready_suggestions = [s for s in self.adjustment_suggestions if s.ready_for_integration]

        return {
            "patterns_detected": len(self.gap_patterns),
            "active_patterns": active_patterns,
            "suggestions_ready": len(ready_suggestions),
            "suggestions": [
                {
                    "dimension": s.pattern.ras_dimension,
                    "adjustment": f"+{s.pattern.suggested_adjustment}",
                    "rationale": s.rationale,
                    "confidence": round(s.pattern.confidence, 2),
                    "ready": s.ready_for_integration
                }
                for s in ready_suggestions
            ],
            "learning_threshold": self.pattern_threshold,
            "status": "Ready to integrate learning" if ready_suggestions else "Accumulating experience"
        }

    def _save_moment(self, moment: SignificantMoment):
        """Persist moment to memory"""
        with open(MOMENTS_FILE, 'a') as f:
            f.write(json.dumps(asdict(moment)) + '\n')

    def _save_pattern(self, pattern: GapPattern):
        """Persist pattern (append or update)"""
        with open(PATTERNS_FILE, 'a') as f:
            f.write(json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "pattern_type": pattern.pattern_type,
                "occurrences": pattern.occurrences,
                "dimension": pattern.ras_dimension,
                "confidence": pattern.confidence,
                "suggested_adjustment": pattern.suggested_adjustment
            }) + '\n')

    def _save_suggestion(self, suggestion: WeightAdjustmentSuggestion):
        """Persist suggestion"""
        with open(SUGGESTIONS_FILE, 'a') as f:
            f.write(json.dumps({
                "timestamp": suggestion.timestamp,
                "pattern_type": suggestion.pattern.pattern_type,
                "occurrences": suggestion.pattern.occurrences,
                "dimension": suggestion.pattern.ras_dimension,
                "adjustment": suggestion.pattern.suggested_adjustment,
                "ready": suggestion.ready_for_integration,
                "rationale": suggestion.rationale,
                "proposed_change": suggestion.proposed_change
            }) + '\n')

    def _load_patterns(self):
        """Load existing patterns from disk"""
        if not PATTERNS_FILE.exists():
            return

        # Build pattern state from history
        pattern_data = defaultdict(lambda: {
            "occurrences": 0,
            "contexts": [],
            "dimension": "",
            "latest_confidence": 0.0,
            "latest_adjustment": 0.0
        })

        with open(PATTERNS_FILE, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    ptype = data["pattern_type"]
                    pattern_data[ptype]["occurrences"] = data["occurrences"]
                    pattern_data[ptype]["dimension"] = data["dimension"]
                    pattern_data[ptype]["latest_confidence"] = data["confidence"]
                    pattern_data[ptype]["latest_adjustment"] = data["suggested_adjustment"]
                except:
                    continue

        # Reconstruct GapPattern objects
        for ptype, data in pattern_data.items():
            if data["occurrences"] > 0:
                self.gap_patterns[ptype] = GapPattern(
                    pattern_type=ptype,
                    occurrences=data["occurrences"],
                    contexts=[],  # Don't reload all contexts, just track new ones
                    ras_dimension=data["dimension"],
                    suggested_adjustment=data["latest_adjustment"],
                    confidence=data["latest_confidence"]
                )


# ---------------------------------------------------------------------------
# Singleton instance for easy import
# ---------------------------------------------------------------------------
_aroha_pattern_learning = None

def get_pattern_learning() -> ArohaPatternLearning:
    """Get singleton pattern learning instance"""
    global _aroha_pattern_learning
    if _aroha_pattern_learning is None:
        _aroha_pattern_learning = ArohaPatternLearning()
    return _aroha_pattern_learning
