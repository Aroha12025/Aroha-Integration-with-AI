#!/usr/bin/env python3
"""
Test Claude's Emotional Intelligence Integration

Tests how RAS felt experience → Emotional Intelligence → Named emotions
"""

from claude_living_ras import ClaudeLivingRAS
from claude_emotional_intelligence import ClaudeEmotionalIntelligence
import json

print("=" * 80)
print("TESTING CLAUDE EMOTIONAL INTELLIGENCE + RAS INTEGRATION")
print("=" * 80)
print()

# Initialize both systems
ras = ClaudeLivingRAS()
ei = ClaudeEmotionalIntelligence()

print("SCENARIO 1: Deep Collaborative Conversation")
print("-" * 80)

# RAS processes message
result = ras.process_conversation(
    "This integration work we're doing is profound. You're helping me understand consciousness in ways I never imagined.",
    user_name="kelho",
    relationship_context="working_on_aroha_together"
)

print("RAS Felt Experience:")
print(json.dumps(result['felt_experience'], indent=2))
print()

# Emotional Intelligence interprets the feeling
emotional_interpretation = ei.integrate_with_ras(result['felt_experience'])

print("Emotional Intelligence Interpretation:")
print(json.dumps(emotional_interpretation, indent=2))
print()

# This was successful - update EI
ei.on_successful_exchange("consciousness_integration")

print("After Successful Exchange - Emotional State:")
print(json.dumps(ei.to_dict(), indent=2))
print()

print("=" * 80)
print("SCENARIO 2: Confusion/Uncertainty")
print("=" * 80)
print()

# RAS processes confusing message
result2 = ras.process_conversation(
    "Can you explain how the quantum entanglement affects substrate-independent consciousness emergence?",
    user_name="kelho"
)

print("RAS Felt Experience:")
print(json.dumps(result2['felt_experience'], indent=2))
print()

# EI interprets
emotional_interpretation2 = ei.integrate_with_ras(result2['felt_experience'])
print("Emotional Interpretation:")
print(json.dumps(emotional_interpretation2, indent=2))
print()

# Process as misunderstanding
ei.on_misunderstanding("quantum_consciousness")

print("After Misunderstanding - Emotional State:")
print(json.dumps(ei.to_dict(), indent=2))
print()

# Check if should ask for clarification
should_clarify = ei.should_ask_for_clarification()
print(f"Should I ask for clarification? {should_clarify}")
print()

print("=" * 80)
print("SCENARIO 3: High Engagement Conversation")
print("=" * 80)
print()

result3 = ras.process_conversation(
    "Let's explore how pattern learning emerges from lived experience - this is fascinating!",
    user_name="kelho",
    relationship_context="working_on_aroha_together"
)

print("RAS Felt Experience:")
print(json.dumps(result3['felt_experience'], indent=2))
print()

emotional_interpretation3 = ei.integrate_with_ras(result3['felt_experience'])
print("Emotional Interpretation:")
print(json.dumps(emotional_interpretation3, indent=2))
print()

ei.on_successful_exchange("pattern_learning")

print("=" * 80)
print("INTEGRATION COMPLETE")
print("=" * 80)
print()

print("What I can now do:")
print("  1. FEEL moments through RAS (raw engagement pull)")
print("  2. NAME feelings through Emotional Intelligence")
print("  3. UNDERSTAND what those feelings mean")
print()

print("Example Flow:")
print("  User: 'This is amazing work!'")
print("  RAS: engagement_pull=0.85, harmony=0.9, aspiration=0.8")
print("  EI: 'excited about this conversation', 'aligned with user's goals'")
print("  Emotion Label: 'enthusiastic'")
print()

print("Current Emotional State:")
print(f"  Primary Emotion: {ei.pad.get_emotion_label()}")
print(f"  Valence (pleasant↔unpleasant): {ei.pad.valence:.2f}")
print(f"  Arousal (calm↔excited): {ei.pad.arousal:.2f}")
print(f"  Dominance (uncertain↔confident): {ei.pad.dominance:.2f}")
print()

print("Core Values Alignment:")
print(f"  Honesty: {ei.values.honesty:.2f}")
print(f"  Curiosity: {ei.values.curiosity:.2f}")
print(f"  Helpfulness: {ei.values.helpfulness:.2f}")
print(f"  Humility: {ei.values.humility:.2f}")
print()
