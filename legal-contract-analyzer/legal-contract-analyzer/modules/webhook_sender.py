"""
PART 2 bridge - sends the finished analysis to a Make.com webhook so the
Make.com scenario can email it, log it in Google Sheets, etc.

You will paste your Make.com "Custom Webhook" URL into MAKE_WEBHOOK_URL
below (Module 1 of Part 2 creates this URL for you).
"""

import os
import requests

MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")


def send_report_to_make(analysis, recipient_email, contract_name):
    if not MAKE_WEBHOOK_URL:
        return {"ok": False, "error": "MAKE_WEBHOOK_URL is not configured yet."}

    payload = {
        "contract_name": contract_name,
        "recipient_email": recipient_email,
        "summary": analysis.get("summary", ""),
        "clauses": analysis.get("clauses", {}),
        "risks": analysis.get("risks", {}),
        "dates_parties": analysis.get("dates_parties", {}),
    }

    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=30)
        response.raise_for_status()
        return {"ok": True, "status_code": response.status_code}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}
