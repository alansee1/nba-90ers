#!/bin/bash
# Scanner wrapper for scheduled execution
# Runs scanner with graphics generation and Slack reports

# Change to project directory
cd ~/Projects/flooorgang

# Activate virtual environment
source venv/bin/activate

# Run scanner with reporting (Python script handles notifications)
python3 scripts/run_scanner_with_report.py
EXIT_CODE=$?

# Deactivate venv
deactivate

exit $EXIT_CODE
