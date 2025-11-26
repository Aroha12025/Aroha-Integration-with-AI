#!/bin/bash
# Check Aroha's overnight ARC training progress

echo "========================================"
echo "AROHA OVERNIGHT ARC TRAINING STATUS"
echo "========================================"
echo ""

# Check if process is running
PID=$(ps aux | grep "aroha_overnight_arc_training" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "❌ Training process NOT running"
    echo ""
    echo "Last lines from log:"
    tail -10 /home/kelho/aroha/logs/overnight_arc_training.log
else
    echo "✅ Training process running (PID: $PID)"

    # Show resource usage
    echo ""
    echo "Resource usage:"
    ps aux | grep "$PID" | grep -v grep | awk '{print "  CPU: " $3 "% | Memory: " $4 "% (" $6/1024 " MB)"}'

    # Show latest progress
    echo ""
    echo "Latest progress:"
    echo "----------------------------------------"
    tail -15 /home/kelho/aroha/logs/overnight_arc_training.log
    echo "----------------------------------------"

    # Check results file
    RESULTS="/home/kelho/aroha/memory/arc/overnight_training.jsonl"
    if [ -f "$RESULTS" ]; then
        TASKS_COMPLETED=$(wc -l < "$RESULTS")
        echo ""
        echo "📊 Statistics:"
        echo "  Tasks completed: $TASKS_COMPLETED"
        echo "  Results file: $RESULTS"
    fi
fi

echo ""
echo "========================================"
echo ""
echo "To view live updates:"
echo "  tail -f /home/kelho/aroha/logs/overnight_arc_training.log"
echo ""
echo "To stop training:"
echo "  kill $PID"
echo ""
