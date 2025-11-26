#!/usr/bin/env python3
import requests
import json
import time
import sys
import os

# Configuration
API_URL = "http://127.0.0.1:8000/sense/vision_gpu"
API_KEY = os.environ.get("AROHA_API_KEY", "")  # Get from environment if set

print("\n" + "="*60)
print("👁️  INITIATING AROHA VISION SYSTEM CHECK")
print("="*60)
print(f"Target: {API_URL}")
print("Mode:   Raw Capture (Debug Enabled)")

# Payload: Force a fresh capture with debug metadata
payload = {
    "mode": "default",
    "debug": True,
    "anchors": [] # No anchors, just raw scene understanding
}

headers = {
    "Content-Type": "application/json",
}

if API_KEY:
    headers["X-API-Key"] = API_KEY

try:
    t0 = time.perf_counter()
    print(">> SENDING SIGNAL...")

    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)

    duration = (time.perf_counter() - t0) * 1000
    print(f">> RECEIVED RESPONSE in {duration:.2f}ms\n")

    if response.status_code == 200:
        data = response.json()

        # --- RAW OUTPUT (The Proof) ---
        print("--- [VISION_GPU RAW OUTPUT] ---")
        print(json.dumps(data, indent=2))
        print("-------------------------------")

        # Validation
        device = data.get("device", "unknown")
        source = data.get("source", "unknown")
        conf = data.get("confidence", 0.0)
        text_len = len(data.get("text", ""))

        print(f"\n✅ SUCCESS:")
        print(f"   - Device: {device} (GPU active? {device=='cuda'})")
        print(f"   - Source: {source}")
        print(f"   - OCR Confidence: {conf}")
        print(f"   - Text Volume: {text_len} chars")

        if "latency_ms" in data:
             print(f"   - Internal Latency: {data['latency_ms']:.2f}ms")

    else:
        print(f"❌ FAILURE: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ CRITICAL FAILURE: {e}")
    print("Is the Aroha Brain (uvicorn) running?")

print("="*60 + "\n")
