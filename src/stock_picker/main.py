#!/usr/bin/env python

import os
import sys
import json
import warnings
from datetime import datetime

from stock_picker.crew import StockPicker
from stock_picker.tools.send_email import send_email

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the Stock Picker crew and email the final report.
    """

    inputs = {
        "sector": "Technology",
        "current_date": str(datetime.now().date()),
    }

    try:
        result = StockPicker().crew().kickoff(inputs=inputs)

        print("\n" + "=" * 70)
        print("FINAL RESULT")
        print("=" * 70)
        print(result)

        report_path = "output/decision.md"

        if os.path.exists(report_path):

            subject = f"Investment Recommendation - {datetime.now().date()}"

            message = """
Hello,

Your Stock Picker AI investment analysis has been completed successfully.

The detailed investment report has been attached with this email.

Inside the report you will find:

• Executive Summary
• Recommended Company
• Investment Thesis
• Financial Analysis
• Growth Opportunities
• Competitive Advantages
• Investment Risks
• Comparison with Other Companies
• Final Recommendation

This report is based on publicly available information and should not be considered personalized financial advice.

Best regards,

Stock Picker AI
Powered by CrewAI
"""

            status = send_email(
                subject=subject,
                message=message,
            )

            print("\n" + "=" * 70)
            print("EMAIL STATUS")
            print("=" * 70)
            print(status)

        else:
            print("\nWarning: output/decision.md was not found.")
            print("Skipping email notification.")

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew.
    """

    inputs = {
        "sector": "Technology",
        "current_date": str(datetime.now().date()),
    }

    try:
        StockPicker().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay a previous crew execution.
    """

    try:
        StockPicker().crew().replay(
            task_id=sys.argv[1]
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew.
    """

    inputs = {
        "sector": "Technology",
        "current_date": str(datetime.now().date()),
    }

    try:
        StockPicker().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew using a trigger payload.
    """

    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])

    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload.")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "sector": "Technology",
        "current_date": str(datetime.now().date()),
    }

    try:
        result = StockPicker().crew().kickoff(inputs=inputs)
        print(result)
        return result

    except Exception as e:
        raise Exception(
            f"An error occurred while running the crew with trigger: {e}"
        )