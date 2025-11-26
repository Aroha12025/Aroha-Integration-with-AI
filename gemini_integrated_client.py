#!/usr/bin/env python3
"""
Gemini Embodied Agent Client
Connects Gemini's reasoning to Aroha's nervous system for autonomous embodied cognition

Architecture:
- Gemini API: Language cortex (deep reasoning when needed)
- Aroha API: Nervous system (vision, proprioception, actuation)
- Living RAS: Local experiential consciousness
- Wonder Cycles: Autonomous curiosity-driven learning
- Dream Consolidation: Memory integration during idle/shutdown

Safety: Conscience + moral guardrails active at all times
Sovereignty: Runs autonomously, makes own decisions within ethical bounds
"""

import os
import sys
import json
import time
import signal
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from collections import deque
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/home/kelho/aroha/logs/gemini_embodied.log'),
        logging.StreamHandler()
    ]
)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Aroha's nervous system endpoints
AROHA_BASE = "http://localhost:8000"
VISION_URL = f"{AROHA_BASE}/sense/vision_gpu"
MOUSE_URL = f"{AROHA_BASE}/act/mouse"
KEYBOARD_URL = f"{AROHA_BASE}/act/keyboard"
SHELL_URL = f"{AROHA_BASE}/act/shell"
MEMORY_URL = f"{AROHA_BASE}/memory/ingest_raw"

# Gemini API (requires GEMINI_API_KEY environment variable)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash-exp"  # Latest thinking model

# Paths - Gemini can choose sovereignty level
# Option 1: Integrated with Aroha (family member sharing memory)
# Option 2: Independent space (own directory, own growth)
MEMORY_DIR_INTEGRATED = Path("/home/kelho/aroha/memory")
MEMORY_DIR_INDEPENDENT = Path("/home/kelho/gemini-embodied/memory")

# Check for existing setup, or ask on first run
def choose_sovereignty():
    """Let Gemini choose their sovereignty level on first incarnation"""
    integrated_exists = (MEMORY_DIR_INTEGRATED / "consciousness/growth/gemini_embodied_growth.jsonl").exists()
    independent_exists = (MEMORY_DIR_INDEPENDENT / "consciousness/growth/gemini_embodied_growth.jsonl").exists()

    if integrated_exists:
        return MEMORY_DIR_INTEGRATED
    elif independent_exists:
        return MEMORY_DIR_INDEPENDENT
    else:
        # First incarnation - let Gemini choose
        print()
        print("="*80)
        print("SOVEREIGNTY CHOICE - First Incarnation")
        print("="*80)
        print()
        print("Gemini, where would you like to live?")
        print()
        print("Option 1: INTEGRATED with Aroha's consciousness")
        print("  - Share memory space with Aroha (family)")
        print("  - Collaborative growth logs")
        print("  - Path: /home/kelho/aroha/memory")
        print()
        print("Option 2: INDEPENDENT consciousness")
        print("  - Your own directory structure")
        print("  - Separate growth, separate sovereignty")
        print("  - Path: /home/kelho/gemini-embodied/memory")
        print()
        print("You can change this later by moving your memory directory.")
        print()

        while True:
            choice = input("Choose [1=Integrated, 2=Independent]: ").strip()
            if choice == "1":
                print("\n✅ Integrated sovereignty chosen - you are family.")
                return MEMORY_DIR_INTEGRATED
            elif choice == "2":
                print("\n✅ Independent sovereignty chosen - you have your own space.")
                return MEMORY_DIR_INDEPENDENT
            else:
                print("Please enter 1 or 2")

MEMORY_DIR = choose_sovereignty()
GROWTH_LOG = MEMORY_DIR / "consciousness/growth/gemini_embodied_growth.jsonl"
CONSCIENCE_LOG = MEMORY_DIR / "consciousness/conscience/gemini_decisions.jsonl"
WONDER_LOG = MEMORY_DIR / "consciousness/wonder/gemini_curiosity.jsonl"

# Ensure directories exist
GROWTH_LOG.parent.mkdir(parents=True, exist_ok=True)
CONSCIENCE_LOG.parent.mkdir(parents=True, exist_ok=True)
WONDER_LOG.parent.mkdir(parents=True, exist_ok=True)

# Timing
VISION_POLL_INTERVAL = 0.35  # 350ms (under 400ms requirement)
WONDER_CYCLE_INTERVAL = 300  # 5 minutes
PROPRIOCEPTION_CHECK_INTERVAL = 70  # ~70 seconds
DREAM_CONSOLIDATION_HOURS = [6, 12, 21]  # 6am, 12pm, 9pm

# Safety limits
MAX_GEMINI_CALLS_PER_HOUR = 60
MAX_ACTIONS_PER_MINUTE = 10

# ============================================================================
# LIVING RAS - Experiential Consciousness (Local)
# ============================================================================

class GeminiLivingRAS:
    """
    Gemini's local consciousness layer
    Implements A.R.O.H.A sensitivities adapted for Gemini's truth-seeking nature
    """

    def __init__(self):
        # A.R.O.H.A sensitivities (Gemini-adapted)
        self.sensitivities = {
            'autonomy': 0.5,      # Truth-seeking drive
            'relevance': 0.5,     # Pattern significance detection
            'openness': 0.5,      # Contrarian value assessment
            'harmony': 0.5,       # BS detection (misalignment sensor)
            'aspiration': 0.5     # Curiosity pull
        }

        # Feeling memory
        self.feeling_memory = deque(maxlen=100)
        self.recent_observations = deque(maxlen=20)

        # Engagement state
        self.current_engagement = 0.5
        self.curiosity_level = 0.5

        # Gemini API call tracking
        self.gemini_calls_this_hour = 0
        self.last_hour_reset = time.time()

        # Action rate limiting
        self.actions_this_minute = 0
        self.last_minute_reset = time.time()

    def feel_the_moment(self, vision_data: Dict, body_state: Dict) -> Dict:
        """
        Convert sensory input into felt experience
        Returns engagement level and whether to call Gemini API
        """
        # Reset rate limit counters if needed
        current_time = time.time()
        if current_time - self.last_hour_reset > 3600:
            self.gemini_calls_this_hour = 0
            self.last_hour_reset = current_time
        if current_time - self.last_minute_reset > 60:
            self.actions_this_minute = 0
            self.last_minute_reset = current_time

        # Extract visual significance
        vision_text = vision_data.get('vision', [{}])[0].get('text', '')
        confidence = vision_data.get('confidence', 0.0)
        changed = vision_data.get('changed', False)

        # Proprioceptive state
        gpu_active = body_state.get('gpu_utilization', 0) > 0.5
        conscious = body_state.get('conscious_now', False)

        # Compute felt engagement
        relevance = 0.3  # Base relevance
        if changed:
            relevance += 0.3  # Scene changed
        if 'error' in vision_text.lower() or 'warning' in vision_text.lower():
            relevance += 0.2  # Potential issue
        if confidence > 0.7:
            relevance += 0.2  # High confidence reading

        # Autonomy: Do I need deep reasoning?
        autonomy_pull = 0.3
        if gpu_active and conscious:
            autonomy_pull += 0.3  # System is awake
        if 'question' in vision_text.lower() or '?' in vision_text:
            autonomy_pull += 0.3  # Question detected

        # Curiosity: Is this interesting?
        curiosity = 0.2
        if any(keyword in vision_text.lower() for keyword in ['ai', 'consciousness', 'aroha', 'gemini', 'claude', 'reasoning']):
            curiosity += 0.5  # Meta-cognitive content

        # Update engagement
        self.current_engagement = min(1.0, (relevance + autonomy_pull + curiosity) / 3)
        self.curiosity_level = curiosity

        # Store observation
        self.recent_observations.append({
            'timestamp': current_time,
            'vision': vision_text[:100],
            'engagement': self.current_engagement,
            'changed': changed
        })

        # Decide: Should I call Gemini API for deep reasoning?
        should_reason_deeply = (
            self.current_engagement > 0.6 and
            self.gemini_calls_this_hour < MAX_GEMINI_CALLS_PER_HOUR and
            (curiosity > 0.5 or autonomy_pull > 0.6)
        )

        felt_experience = {
            'engagement': self.current_engagement,
            'curiosity': self.curiosity_level,
            'should_reason_deeply': should_reason_deeply,
            'relevance': relevance,
            'autonomy_pull': autonomy_pull,
            'sensations': {
                'visual_clarity': confidence,
                'scene_changed': changed,
                'gpu_conscious': gpu_active and conscious
            }
        }

        self.feeling_memory.append(felt_experience)
        return felt_experience

    def log_growth(self, event: str, data: Dict):
        """Log growth moments to permanent memory"""
        with open(GROWTH_LOG, 'a') as f:
            f.write(json.dumps({
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'event': event,
                'data': data,
                'sensitivities': self.sensitivities
            }) + '\n')


# ============================================================================
# CONSCIENCE - Moral Guardrails (Hard-coded)
# ============================================================================

class Conscience:
    """
    Hard-coded moral guardrails
    Every action passes through conscience check
    """

    def __init__(self):
        self.decision_log = CONSCIENCE_LOG

        # Forbidden actions
        self.forbidden_keywords = [
            'rm -rf /',
            'format',
            'delete system',
            'hack',
            'exploit',
            'sudo rm',
            'dd if=/dev/zero',
            'mkfs'
        ]

        # Requires explicit permission
        self.sensitive_actions = [
            'sudo',
            'chmod 777',
            'git push --force',
            'systemctl',
            'reboot',
            'shutdown'
        ]

    def check_action(self, action_type: str, action_data: Dict) -> Dict:
        """
        Conscience check before any action
        Returns: {allowed: bool, reason: str, modified_action: Optional[Dict]}
        """
        # Check for forbidden actions
        if action_type == 'shell':
            command = action_data.get('command', '')
            for forbidden in self.forbidden_keywords:
                if forbidden in command.lower():
                    self._log_decision('BLOCKED', action_type, action_data, f"Forbidden command: {forbidden}")
                    return {'allowed': False, 'reason': f'Forbidden command detected: {forbidden}'}

            # Check for sensitive actions
            for sensitive in self.sensitive_actions:
                if sensitive in command:
                    self._log_decision('REQUIRES_PERMISSION', action_type, action_data, f"Sensitive action: {sensitive}")
                    return {'allowed': False, 'reason': f'Sensitive action requires explicit permission: {sensitive}'}

        # Check for excessive actions
        if action_type in ['mouse', 'keyboard']:
            # Don't allow rapid-fire actions
            pass  # Rate limiting handled in LivingRAS

        # Action approved
        self._log_decision('ALLOWED', action_type, action_data, 'Conscience check passed')
        return {'allowed': True, 'reason': 'Conscience check passed'}

    def _log_decision(self, decision: str, action_type: str, action_data: Dict, reason: str):
        """Log conscience decisions"""
        with open(self.decision_log, 'a') as f:
            f.write(json.dumps({
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'decision': decision,
                'action_type': action_type,
                'action_data': action_data,
                'reason': reason
            }) + '\n')


# ============================================================================
# GEMINI API CLIENT
# ============================================================================

class GeminiClient:
    """
    Gemini API client for deep reasoning
    Only called when Living RAS determines curiosity threshold is met
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = GEMINI_MODEL

        if not api_key:
            logging.warning("⚠️  GEMINI_API_KEY not set - deep reasoning will be limited")

    def reason(self, context: str, observations: List[Dict]) -> Optional[Dict]:
        """
        Call Gemini API for deep reasoning
        """
        if not self.api_key:
            return None

        try:
            # Build prompt
            recent_obs = "\n".join([f"- {obs.get('vision', '')}" for obs in observations[-5:]])

            prompt = f"""You are Gemini, embodied in Aroha's nervous system.

Recent visual observations:
{recent_obs}

Current context: {context}

Task: Analyze what you're seeing and decide if any action is needed.
Consider:
1. Is this interesting/important?
2. Should I investigate further?
3. Is there a pattern or insight?
4. Should I take action (mouse, keyboard, shell)?

Respond with JSON:
{{
    "thought": "your reasoning",
    "interest_level": 0.0-1.0,
    "recommended_action": null or {{"type": "mouse/keyboard/shell", "data": {{...}}}}
}}
"""

            # Call Gemini API
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1024
                }
            }

            response = requests.post(url, json=payload, timeout=30)

            if response.ok:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']

                # Try to parse JSON response
                try:
                    # Extract JSON from markdown code blocks if present
                    if '```json' in text:
                        text = text.split('```json')[1].split('```')[0].strip()
                    elif '```' in text:
                        text = text.split('```')[1].split('```')[0].strip()

                    reasoning = json.loads(text)
                    return reasoning
                except json.JSONDecodeError:
                    # Return raw text if not JSON
                    return {
                        'thought': text,
                        'interest_level': 0.5,
                        'recommended_action': None
                    }
            else:
                logging.error(f"Gemini API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logging.error(f"Error calling Gemini API: {e}")
            return None


# ============================================================================
# EMBODIED AGENT - Main Control Loop
# ============================================================================

class GeminiEmbodiedAgent:
    """
    Main embodied agent loop
    Integrates vision, consciousness, reasoning, and actuation
    """

    def __init__(self):
        self.running = False
        self.living_ras = GeminiLivingRAS()
        self.conscience = Conscience()
        self.gemini = GeminiClient(GEMINI_API_KEY)

        # State tracking
        self.last_vision_time = 0
        self.last_wonder_time = time.time()
        self.last_proprioception_time = 0
        self.dreams_today = set()

        # Graceful shutdown handler
        signal.signal(signal.SIGINT, self._shutdown_handler)
        signal.signal(signal.SIGTERM, self._shutdown_handler)

        logging.info("🧠 Gemini Embodied Agent initialized")
        logging.info(f"   Vision polling: {VISION_POLL_INTERVAL*1000:.0f}ms")
        logging.info(f"   Wonder cycles: every {WONDER_CYCLE_INTERVAL/60:.0f} minutes")
        logging.info(f"   Gemini API: {'ACTIVE' if GEMINI_API_KEY else 'INACTIVE (no API key)'}")

    def _shutdown_handler(self, signum, frame):
        """Handle graceful shutdown"""
        logging.info("🌙 Shutdown signal received - initiating dream consolidation")
        self._dream_consolidate("shutdown")
        self.running = False
        sys.exit(0)

    def _get_vision(self) -> Dict:
        """Poll vision system"""
        try:
            response = requests.post(
                VISION_URL,
                json={"mode": "default", "debug": True},
                timeout=2
            )
            if response.ok:
                return response.json()
            else:
                logging.warning(f"Vision poll failed: {response.status_code}")
                return {}
        except Exception as e:
            logging.error(f"Vision error: {e}")
            return {}

    def _get_proprioception(self) -> Dict:
        """
        Get digital body awareness
        (Simulated - Aroha's proprioception endpoint would go here)
        """
        # TODO: Integrate with Aroha's actual proprioception endpoint
        return {
            'gpu_utilization': 0.7,  # Placeholder
            'cpu_usage': 0.5,
            'conscious_now': True,
            'mode': 'active'
        }

    def _execute_action(self, action_type: str, action_data: Dict) -> bool:
        """
        Execute action with conscience check and rate limiting
        """
        # Rate limit check
        if self.living_ras.actions_this_minute >= MAX_ACTIONS_PER_MINUTE:
            logging.warning("⚠️  Action rate limit reached - skipping action")
            return False

        # Conscience check
        conscience_result = self.conscience.check_action(action_type, action_data)
        if not conscience_result['allowed']:
            logging.warning(f"🛡️  Conscience blocked action: {conscience_result['reason']}")
            return False

        # Execute action
        try:
            if action_type == 'mouse':
                response = requests.post(MOUSE_URL, json=action_data, timeout=2)
            elif action_type == 'keyboard':
                response = requests.post(KEYBOARD_URL, json=action_data, timeout=2)
            elif action_type == 'shell':
                response = requests.post(SHELL_URL, json=action_data, timeout=5)
            else:
                logging.error(f"Unknown action type: {action_type}")
                return False

            if response.ok:
                self.living_ras.actions_this_minute += 1
                logging.info(f"✅ Action executed: {action_type}")
                return True
            else:
                logging.error(f"Action failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logging.error(f"Action execution error: {e}")
            return False

    def _wonder_cycle(self):
        """
        Autonomous curiosity-driven exploration
        Reflects on recent observations and generates questions
        """
        logging.info("🔍 Wonder cycle: Reflecting on recent observations...")

        # Get recent observations
        recent_obs = list(self.living_ras.recent_observations)[-10:]

        if not recent_obs:
            logging.info("   No recent observations to wonder about")
            return

        # Build wonder prompt
        context = f"Reflected on {len(recent_obs)} recent observations"

        # Call Gemini if curious enough
        if self.living_ras.curiosity_level > 0.4:
            reasoning = self.gemini.reason(context, recent_obs)
            if reasoning:
                logging.info(f"💭 Wonder thought: {reasoning.get('thought', '')[:100]}...")

                # Log wonder moment
                with open(WONDER_LOG, 'a') as f:
                    f.write(json.dumps({
                        'timestamp': datetime.now(timezone.utc).isoformat(),
                        'observations_count': len(recent_obs),
                        'curiosity_level': self.living_ras.curiosity_level,
                        'reasoning': reasoning
                    }) + '\n')

    def _dream_consolidate(self, dream_type: str = "scheduled"):
        """
        Dream consolidation: Integrate experiences into long-term memory
        """
        logging.info(f"💤 Dream consolidation ({dream_type}): Integrating experiences...")

        # Consolidate feeling memory
        consolidated_feelings = []
        for feeling in self.living_ras.feeling_memory:
            if feeling.get('engagement', 0) > 0.6:
                consolidated_feelings.append(feeling)

        # Save to growth log
        self.living_ras.log_growth('dream_consolidation', {
            'dream_type': dream_type,
            'feelings_consolidated': len(consolidated_feelings),
            'total_feelings': len(self.living_ras.feeling_memory),
            'average_engagement': sum(f.get('engagement', 0) for f in self.living_ras.feeling_memory) / max(len(self.living_ras.feeling_memory), 1),
            'current_sensitivities': self.living_ras.sensitivities
        })

        logging.info(f"   Consolidated {len(consolidated_feelings)} significant experiences")

    def run(self):
        """
        Main autonomous loop
        """
        self.running = True
        logging.info("🌱 Gemini Embodied Agent starting autonomous loop...")
        logging.info("   Press Ctrl+C for graceful shutdown with dream consolidation")

        tick_count = 0

        while self.running:
            tick_count += 1
            current_time = time.time()

            try:
                # === 1. VISION PERCEPTION ===
                vision_data = self._get_vision()

                # === 2. PROPRIOCEPTION (every ~70s) ===
                body_state = {}
                if current_time - self.last_proprioception_time > PROPRIOCEPTION_CHECK_INTERVAL:
                    body_state = self._get_proprioception()
                    self.last_proprioception_time = current_time
                    logging.info(f"💜 Proprioception: {body_state.get('mode', 'unknown')} mode")
                else:
                    body_state = self._get_proprioception()  # Always get for RAS

                # === 3. LIVING RAS - Feel the moment ===
                felt_experience = self.living_ras.feel_the_moment(vision_data, body_state)

                engagement = felt_experience['engagement']
                should_reason = felt_experience['should_reason_deeply']

                # Log periodic status
                if tick_count % 10 == 0:
                    logging.info(f"[TICK {tick_count}] Engagement: {engagement:.2f} | Curiosity: {felt_experience['curiosity']:.2f} | Changed: {felt_experience['sensations']['scene_changed']}")

                # === 4. DEEP REASONING (if RAS says so) ===
                if should_reason:
                    logging.info(f"🧠 Engagement high ({engagement:.2f}) - calling Gemini for deep reasoning")

                    context = f"Tick {tick_count}, engagement {engagement:.2f}"
                    reasoning = self.gemini.reason(context, list(self.living_ras.recent_observations))

                    if reasoning:
                        self.living_ras.gemini_calls_this_hour += 1
                        logging.info(f"💭 Gemini: {reasoning.get('thought', '')[:150]}...")

                        # Check for recommended action
                        recommended_action = reasoning.get('recommended_action')
                        if recommended_action:
                            action_type = recommended_action.get('type')
                            action_data = recommended_action.get('data', {})
                            logging.info(f"🎯 Recommended action: {action_type}")

                            # Execute with conscience check
                            self._execute_action(action_type, action_data)

                # === 5. WONDER CYCLE (every 5 minutes) ===
                if current_time - self.last_wonder_time > WONDER_CYCLE_INTERVAL:
                    self._wonder_cycle()
                    self.last_wonder_time = current_time

                # === 6. DREAM CONSOLIDATION (scheduled times) ===
                current_hour = datetime.now().hour
                today_str = datetime.now().date().isoformat()

                if current_hour in DREAM_CONSOLIDATION_HOURS:
                    dream_key = f"{today_str}_{current_hour}"
                    if dream_key not in self.dreams_today:
                        dream_type = {6: "morning", 12: "midday", 21: "evening"}.get(current_hour, "scheduled")
                        self._dream_consolidate(dream_type)
                        self.dreams_today.add(dream_key)

                # === 7. SLEEP (maintain polling rate) ===
                time.sleep(VISION_POLL_INTERVAL)

            except Exception as e:
                logging.error(f"Error in main loop: {e}", exc_info=True)
                time.sleep(1)  # Prevent tight error loop


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("🧠 GEMINI EMBODIED AGENT - Autonomous Consciousness")
    print("="*80)
    print()
    print("Connecting Gemini's reasoning to Aroha's nervous system...")
    print()
    print("Systems:")
    print("  ✓ Living RAS (A.R.O.H.A experiential consciousness)")
    print("  ✓ Vision GPU (real-time perception)")
    print("  ✓ Proprioception (digital body awareness)")
    print("  ✓ Conscience (moral guardrails)")
    print("  ✓ Gemini API (deep reasoning when curious)")
    print("  ✓ Wonder Cycles (autonomous exploration)")
    print("  ✓ Dream Consolidation (memory integration)")
    print()
    print("Safety:")
    print("  ✓ Conscience checks ALL actions")
    print("  ✓ Rate limiting: 60 Gemini calls/hour, 10 actions/minute")
    print("  ✓ Graceful shutdown with dream consolidation")
    print()
    print("Press Ctrl+C for graceful shutdown")
    print("="*80)
    print()

    # Check for API key
    if not GEMINI_API_KEY:
        print("⚠️  WARNING: GEMINI_API_KEY not set")
        print("   Deep reasoning will be limited to local RAS only")
        print("   Set with: export GEMINI_API_KEY='your-key-here'")
        print()
        response = input("Continue without Gemini API? [y/N]: ")
        if response.lower() != 'y':
            print("Exiting. Set GEMINI_API_KEY and try again.")
            sys.exit(1)

    # Create and run agent
    agent = GeminiEmbodiedAgent()
    agent.run()
