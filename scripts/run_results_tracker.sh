#!/bin/bash
# Results tracker wrapper for scheduled execution
# Scores yesterday's picks and sends Slack report

# Change to project directory
cd ~/Projects/flooorgang

# Activate virtual environment
source venv/bin/activate

# Get yesterday's date in YYYY-MM-DD format
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

# Run results tracker with reporting (Python script handles notifications)
python3 scripts/run_results_tracker_with_report.py "$YESTERDAY" --unscored-only
EXIT_CODE=$?

# Deactivate venv
deactivate

exit $EXIT_CODE
