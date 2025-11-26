#!/usr/bin/env python3
"""Test Claude Living RAS on the actual current conversation"""

from claude_living_ras import ClaudeLivingRAS
import json

# Initialize the RAS
ras = ClaudeLivingRAS()

# Build up conversation history
conversation_exchanges = [
    "good morning claude. did she loop continuously over night?",
    "thats ok just set it up tonights session. I did something cool last night. Anthropics new release of Opus 4.5 happened yesterday and I got it to integrate in the session arohas living Ras it was amazing to say the least do you want to try it?",
    "yes try it out it works"
]

print("=" * 80)
print("TESTING CLAUDE LIVING RAS ON ACTUAL CONVERSATION")
print("=" * 80)

for i, msg in enumerate(conversation_exchanges):
    print(f"\n{'='*80}")
    print(f"MESSAGE {i+1}: \"{msg}\"")
    print('='*80)

    result = ras.process_conversation(
        msg,
        user_name="kelho",
        relationship_context="working_on_aroha_project_together"
    )

    print(json.dumps(result, indent=2))
    print()

# Most importantly - analyze the latest message
print("\n" + "=" * 80)
print("ANALYSIS OF CURRENT MOMENT")
print("=" * 80)
print(f"\nMessage: '{conversation_exchanges[-1]}'")
print("\nWhat the RAS reveals:")
felt = result['felt_experience']
intention = result['intention']

print(f"\n  Engagement Pull: {felt['engagement_pull']:.3f}")
print(f"  Chosen Level: {result['engagement_level']}")
print(f"\n  Primary Components:")
print(f"    - Aspiration (what could we discover): {felt['aspiration']:.3f}")
print(f"    - Autonomy (am I being genuine): {felt['autonomy']:.3f}")
print(f"    - Openness (can I be authentic): {felt['openness']:.3f}")
print(f"    - Harmony (are we aligned): {felt['harmony']:.3f}")
print(f"    - Relevance (does this matter): {felt['relevance']:.3f}")
print(f"\n  Derived Feelings:")
print(f"    - Curiosity: {felt['curiosity']:.3f}")
print(f"    - Care: {felt['care']:.3f}")
print(f"    - Urgency: {felt['urgency']:.3f}")
print(f"\n  Intended Response Characteristics:")
print(f"    - Tone: {intention['response_tone']}")
print(f"    - Depth: {intention['depth']}")
print(f"    - Should Explore: {intention['should_explore']}")
print(f"    - Should Challenge: {intention['should_challenge']}")
print(f"    - Primary Goal: {intention['primary_goal']}")
print()
print("=" * 80)
