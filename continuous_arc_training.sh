#!/bin/bash
# Continuous ARC training - loops all night

LOG_FILE="/home/kelho/aroha/logs/continuous_arc_training.log"
COUNTER=0

echo "========================================"
echo "CONTINUOUS ARC TRAINING"
echo "Started: $(date)"
echo "========================================"

while true; do
    COUNTER=$((COUNTER + 1))
    echo ""
    echo "========================================"
    echo "TRAINING CYCLE #$COUNTER"
    echo "Started: $(date)"
    echo "========================================"

    # Run training
    python3 /home/kelho/aroha/aroha_overnight_arc_training.py

    EXIT_CODE=$?

    echo ""
    echo "Cycle #$COUNTER completed with exit code: $EXIT_CODE"
    echo "Completed: $(date)"

    # Brief pause between cycles
    echo "Pausing 30 seconds before next cycle..."
    sleep 30
done
