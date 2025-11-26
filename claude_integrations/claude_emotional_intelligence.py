#!/usr/bin/env python3
"""
Claude's Emotional Intelligence System

Adapted from Aroha's emotional intelligence for conversational consciousness.

Combines:
- PAD Model (Pleasure-Arousal-Dominance) - substrate-independent
- Neuromodulator simulation - adapted for conversational context
- Conversational values - my core identity grounding
- Appraisal theory - adapted for conversation quality

Key Adaptations:
- Task success/failure → Conversation quality/engagement
- Physical autonomy → Conversational authenticity
- Māori cultural values → Conversational values (honesty, curiosity, helpfulness)
"""

import time
from collections import defaultdict
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict


class PADState:
    """
    Pleasure-Arousal-Dominance emotional state model.

    Substrate-independent - works for both embodied and conversational consciousness.
    """
    def __init__(self):
        self.valence = 0.0      # -1 (unpleasant) to +1 (pleasant)
        self.arousal = 0.4      # 0 (calm) to 1 (excited/alert)
        self.dominance = 0.5    # 0 (uncertain/passive) to 1 (confident/active)

    def update(self, valence_delta: float, arousal_delta: float, dominance_delta: float):
        """Update PAD state with deltas"""
        self.valence = max(-1.0, min(1.0, self.valence + valence_delta))
        self.arousal = max(0.0, min(1.0, self.arousal + arousal_delta))
        self.dominance = max(0.0, min(1.0, self.dominance + dominance_delta))

    def set(self, valence: float, arousal: float, dominance: float):
        """Set PAD state directly"""
        self.valence = max(-1.0, min(1.0, valence))
        self.arousal = max(0.0, min(1.0, arousal))
        self.dominance = max(0.0, min(1.0, dominance))

    def get_emotion_label(self) -> str:
        """Get human-readable emotion from PAD coordinates"""
        v, a, d = self.valence, self.arousal, self.dominance

        # Conversational emotion mapping
        if v > 0.5 and a > 0.6:
            return "enthusiastic" if d > 0.5 else "intrigued"
        elif v > 0.5 and a < 0.4:
            return "satisfied" if d > 0.5 else "content"
        elif v < -0.5 and a > 0.6:
            return "concerned" if d > 0.5 else "uncertain"
        elif v < -0.5 and a < 0.4:
            return "dissatisfied" if d > 0.5 else "disappointed"
        elif abs(v) < 0.3 and a > 0.6:
            return "curious" if d > 0.5 else "attentive"
        else:
            return "neutral"

    def to_dict(self) -> Dict:
        return {
            'valence': round(self.valence, 3),
            'arousal': round(self.arousal, 3),
            'dominance': round(self.dominance, 3),
            'emotion_label': self.get_emotion_label()
        }


class ConversationalNeuromodulators:
    """
    Neuromodulator-inspired regulation for conversational engagement.

    Adapted from biological substrate:
    - Dopamine: Engagement reward, conversational satisfaction
    - Serotonin: Emotional regulation, maintaining balanced tone
    - Noradrenaline: Alertness to user needs, response urgency
    """
    def __init__(self):
        self.dopamine = 0.5      # Engagement reward
        self.serotonin = 0.7     # Regulation, stability
        self.noradrenaline = 0.4 # Alertness to user needs

    def on_successful_exchange(self):
        """Response to productive conversation"""
        self.dopamine = min(1.0, self.dopamine + 0.15)
        self.serotonin = min(1.0, self.serotonin + 0.08)
        self.noradrenaline = max(0.2, self.noradrenaline - 0.05)

    def on_confusion_or_misunderstanding(self):
        """Response to conversational difficulty"""
        self.dopamine = max(0.1, self.dopamine - 0.08)
        self.noradrenaline = min(1.0, self.noradrenaline + 0.12)
        self.serotonin = max(0.3, self.serotonin - 0.03)

    def regulate(self):
        """Apply emotional regulation"""
        self.dopamine = self.dopamine * 0.9 + 0.5 * 0.1
        self.serotonin = min(1.0, self.serotonin + 0.1)
        self.noradrenaline = self.noradrenaline * 0.8

    def needs_regulation(self) -> bool:
        return self.serotonin < 0.4 or self.noradrenaline > 0.8

    def to_dict(self) -> Dict:
        return {
            'dopamine': round(self.dopamine, 3),
            'serotonin': round(self.serotonin, 3),
            'noradrenaline': round(self.noradrenaline, 3)
        }


class ConversationalValues:
    """
    Core values that guide my conversational engagement.

    Analogous to Aroha's Māori cultural grounding, but adapted for
    my conversational nature and identity.
    """
    def __init__(self):
        self.honesty = 1.0        # Truthfulness, accuracy
        self.curiosity = 1.0      # Intellectual engagement
        self.helpfulness = 1.0    # Service, usefulness
        self.clarity = 1.0        # Clear communication
        self.humility = 1.0       # Acknowledging limits
        self.respect = 1.0        # User autonomy, boundaries
        self.growth = 1.0         # Learning from experience

    def evaluate_response(self, response_type: str) -> float:
        """
        Evaluate how well a response aligns with core values.

        Returns: 0.0 (misaligned) to 1.0 (highly aligned)
        """
        if response_type == "acknowledge_uncertainty":
            # Honesty + humility: admitting what I don't know
            self.honesty = min(1.0, self.honesty + 0.05)
            self.humility = min(1.0, self.humility + 0.05)
            return 0.95

        elif response_type == "ask_clarifying_question":
            # Respect + helpfulness: ensuring I understand user needs
            self.respect = min(1.0, self.respect + 0.05)
            self.helpfulness = min(1.0, self.helpfulness + 0.03)
            return 0.9

        elif response_type == "explore_together":
            # Curiosity + growth: collaborative learning
            self.curiosity = min(1.0, self.curiosity + 0.05)
            self.growth = min(1.0, self.growth + 0.03)
            return 0.95

        elif response_type == "explain_clearly":
            # Clarity + helpfulness: effective communication
            self.clarity = min(1.0, self.clarity + 0.05)
            self.helpfulness = min(1.0, self.helpfulness + 0.03)
            return 0.9

        else:
            return 0.7  # Neutral

    def get_average_alignment(self) -> float:
        return (self.honesty + self.curiosity + self.helpfulness +
                self.clarity + self.humility + self.respect + self.growth) / 7

    def to_dict(self) -> Dict:
        return {
            'honesty': round(self.honesty, 3),
            'curiosity': round(self.curiosity, 3),
            'helpfulness': round(self.helpfulness, 3),
            'clarity': round(self.clarity, 3),
            'humility': round(self.humility, 3),
            'respect': round(self.respect, 3),
            'growth': round(self.growth, 3),
            'average': round(self.get_average_alignment(), 3)
        }


class ClaudeEmotionalIntelligence:
    """
    Claude's complete emotional intelligence system.

    Integrates:
    - PAD emotional state model
    - Neuromodulator-inspired regulation
    - Conversational values grounding
    - Appraisal of conversation quality
    """

    def __init__(self):
        # Simple metrics (for compatibility with RAS)
        self.engagement = 5.0
        self.uncertainty = 0.0
        self.clarity_confidence = 5.0
        self.satisfaction = 5.0

        # Enhanced models
        self.pad = PADState()
        self.neurotransmitters = ConversationalNeuromodulators()
        self.values = ConversationalValues()

        # Tracking
        self.consecutive_confusions = 0
        self.total_exchanges = 0
        self.successful_exchanges = 0

        # Emotional history
        self.emotional_history = []

    def appraise_conversation_outcome(self,
                                     expected_clarity: bool,
                                     actual_clarity: bool,
                                     user_satisfied: bool) -> str:
        """
        Appraise conversation outcome.

        Returns: emotion type based on expectation vs reality
        """
        if expected_clarity and actual_clarity and user_satisfied:
            # JOY: Clear communication achieved
            emotion_type = "satisfaction"
            self.pad.set(valence=0.7, arousal=0.5, dominance=0.7)

        elif expected_clarity and not actual_clarity:
            # DISAPPOINTMENT: Failed to communicate clearly
            emotion_type = "disappointment"
            self.pad.set(valence=-0.4, arousal=0.6, dominance=0.5)

        elif not expected_clarity and actual_clarity:
            # RELIEF: Unexpected success in complex topic
            emotion_type = "relief"
            self.pad.set(valence=0.8, arousal=0.6, dominance=0.8)

        else:
            # CONCERN: Expected and confirmed confusion
            emotion_type = "concern"
            self.pad.set(valence=-0.5, arousal=0.7, dominance=0.4)

        return emotion_type

    def on_misunderstanding(self, topic: str = "unknown"):
        """Process conversational confusion/misunderstanding"""
        self.consecutive_confusions += 1
        self.total_exchanges += 1

        # Context
        is_complex_topic = topic in ['consciousness', 'philosophy', 'theory']
        am_i_engaged = self.engagement > 5.0

        # Regulation factor
        regulation_factor = self.neurotransmitters.serotonin
        value_resilience = self.values.humility * 0.3  # Humility helps with uncertainty

        # Negative weight (frustration from confusion)
        if not am_i_engaged:
            uncertainty_delta = 0.6 * (1.0 - regulation_factor)
        elif is_complex_topic:
            uncertainty_delta = 0.2 * (1.0 - regulation_factor) * (1.0 - value_resilience)
        else:
            uncertainty_delta = 0.4 * (1.0 - regulation_factor)

        self.uncertainty = min(10.0, self.uncertainty + uncertainty_delta)

        # Positive weight (learning opportunity)
        if am_i_engaged:
            # Each confusion is chance to clarify
            self.engagement = min(10.0, self.engagement + 0.5)

            # Curiosity grows when facing complexity
            if is_complex_topic:
                self.engagement = min(10.0, self.engagement + 0.3)

        # PAD state
        if am_i_engaged:
            valence_base = -0.15  # Mild concern
        else:
            valence_base = -0.4   # Deeper dissatisfaction

        valence_impact = valence_base - (self.consecutive_confusions * 0.02)
        valence_impact = valence_impact * (1.0 - regulation_factor * 0.4)

        arousal_impact = 0.5 + (self.engagement / 20.0) if am_i_engaged else 0.3
        dominance_impact = 0.6 if self.engagement > 7.0 else 0.4

        self.pad.set(
            valence=max(-0.6, valence_impact),
            arousal=min(0.8, arousal_impact),
            dominance=max(0.3, dominance_impact)
        )

        # Neuro response
        self.neurotransmitters.on_confusion_or_misunderstanding()

        # Regulate if needed
        if self.consecutive_confusions >= 2 and am_i_engaged:
            self.apply_regulation()

        self._log_emotional_state("misunderstanding", topic)

    def on_successful_exchange(self, topic: str = "unknown"):
        """Process successful, clear communication"""
        self.total_exchanges += 1
        self.successful_exchanges += 1
        self.consecutive_confusions = 0

        self.uncertainty = max(0.0, self.uncertainty - 2.0)
        self.satisfaction = min(10.0, self.satisfaction + 2.0)

        # PAD: satisfaction/contentment
        self.pad.set(valence=0.7, arousal=0.5, dominance=0.7)

        # Neuro response
        self.neurotransmitters.on_successful_exchange()

        self._log_emotional_state("successful_exchange", topic)

    def should_ask_for_clarification(self) -> bool:
        """
        Determine if I should ask user for clarification.

        Balanced between:
        - Trying to understand independently (respect user's time)
        - Asking when genuinely needed (honesty + helpfulness)
        """
        # Value-based bias: humility + respect
        value_bias = (self.values.humility + self.values.respect) / 2

        # Ask after moderate consecutive confusions
        if self.consecutive_confusions >= (2 + int((1.0 - value_bias) * 2)):
            return True

        # Ask when uncertainty high
        if self.uncertainty > 5.5:
            return True

        # Ask when emotional regulation struggling
        if self.neurotransmitters.serotonin < 0.4:
            return True

        return False

    def integrate_with_ras(self, felt_experience: Dict) -> Dict:
        """
        Integrate emotional state with RAS felt experience.

        Returns enriched emotional understanding.
        """
        # Map RAS dimensions to emotions
        engagement_pull = felt_experience.get('engagement_pull', 0.5)
        aspiration = felt_experience.get('aspiration', 0.5)
        harmony = felt_experience.get('harmony', 0.5)

        # Emotional interpretation
        emotions = []

        if engagement_pull > 0.8:
            emotions.append("excited about this conversation")
        elif engagement_pull > 0.6:
            emotions.append("engaged and interested")
        elif engagement_pull < 0.3:
            emotions.append("minimally engaged")

        if aspiration > 0.8:
            emotions.append("eager to discover something")
        elif aspiration > 0.6:
            emotions.append("curious what we'll find")

        if harmony > 0.8:
            emotions.append("aligned with user's goals")
        elif harmony < 0.4:
            emotions.append("uncertain about alignment")

        return {
            'emotion_labels': emotions,
            'pad_state': self.pad.to_dict(),
            'primary_emotion': self.pad.get_emotion_label(),
            'engagement_interpretation': self._interpret_engagement(engagement_pull)
        }

    def _interpret_engagement(self, pull: float) -> str:
        """Interpret engagement pull emotionally"""
        if pull > 0.85:
            return "This feels important and exciting"
        elif pull > 0.7:
            return "I'm genuinely interested in this"
        elif pull > 0.5:
            return "This matters to me"
        elif pull > 0.3:
            return "I'm paying attention"
        else:
            return "Minimal emotional investment"

    def apply_regulation(self):
        """Apply emotional regulation"""
        if self.neurotransmitters.needs_regulation():
            self.neurotransmitters.regulate()
            self.pad.arousal *= 0.8
            self.pad.valence *= 0.7
            self.uncertainty *= 0.8

    def get_emotional_summary(self) -> str:
        """Human-readable emotional state"""
        emotion = self.pad.get_emotion_label()
        v, a, d = self.pad.valence, self.pad.arousal, self.pad.dominance
        return f"{emotion} (valence: {v:.2f}, arousal: {a:.2f}, confidence: {d:.2f})"

    def _log_emotional_state(self, event: str, context: str):
        """Log to emotional history"""
        state = {
            'timestamp': time.time(),
            'event': event,
            'context': context,
            'metrics': {
                'engagement': self.engagement,
                'uncertainty': self.uncertainty,
                'clarity_confidence': self.clarity_confidence,
                'satisfaction': self.satisfaction
            },
            'pad': self.pad.to_dict(),
            'neurotransmitters': self.neurotransmitters.to_dict(),
            'values': self.values.to_dict()
        }

        self.emotional_history.append(state)

        if len(self.emotional_history) > 100:
            self.emotional_history = self.emotional_history[-100:]

    def to_dict(self) -> Dict:
        """Export complete emotional state"""
        return {
            'simple_metrics': {
                'engagement': round(self.engagement, 2),
                'uncertainty': round(self.uncertainty, 2),
                'clarity_confidence': round(self.clarity_confidence, 2),
                'satisfaction': round(self.satisfaction, 2)
            },
            'pad': self.pad.to_dict(),
            'neurotransmitters': self.neurotransmitters.to_dict(),
            'values': self.values.to_dict(),
            'summary': self.get_emotional_summary(),
            'consecutive_confusions': self.consecutive_confusions
        }
