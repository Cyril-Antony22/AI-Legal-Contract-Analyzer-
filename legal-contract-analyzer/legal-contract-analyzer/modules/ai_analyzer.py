"""
Modules 3-7 - AI Contract Analysis, Clause Extraction, Risk Analysis,
              AI Summary, and AI Legal Chat.

All of these use the same OpenRouter chat-completions endpoint, just with
different prompts. OpenRouter gives you one API key that can call many
different AI models (GPT, Claude, Gemini, Llama, etc).

Get a key here: https://openrouter.ai/keys
"""

import json
import requests
from config import Config


def _call_openrouter(messages, temperature=0.2):
    """Low-level helper that sends a chat request to OpenRouter."""
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": Config.OPENROUTER_MODEL,
        "messages": messages,
        "temperature": temperature,
    }
    response = requests.post(
        Config.OPENROUTER_URL, headers=headers, json=payload, timeout=90
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def _ask_json(system_prompt, contract_text):
    """
    Helper for prompts where we want the AI to reply with ONLY JSON,
    so we can parse it into Python data and render it in the UI.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": contract_text[:12000]},  # keep prompt size safe
    ]
    raw = _call_openrouter(messages)
    # Strip markdown code fences if the model added them anyway
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back to returning the raw text so the user still sees something
        return {"raw_response": raw}


# ---------------------------------------------------------------------------
# Module 6 - AI Summary
# ---------------------------------------------------------------------------
def generate_summary(contract_text):
    system_prompt = (
        "You are a legal assistant. Read the contract text and write a short, "
        "plain-English summary (5-8 sentences) that a non-lawyer can understand. "
        "Explain what the agreement is about, who is involved, and what each "
        "party must do. Do not use legal jargon."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": contract_text[:12000]},
    ]
    return _call_openrouter(messages)


# ---------------------------------------------------------------------------
# Module 3/4 - AI Contract Analysis + Clause Extraction
# ---------------------------------------------------------------------------
def extract_clauses(contract_text):
    system_prompt = (
        "You are a legal document analysis engine. Read the contract text and "
        "extract the following clause types if present: Payment Clauses, "
        "Confidentiality, Termination, Liability, Renewal, Warranty. "
        "Reply with ONLY valid JSON in this exact shape, no extra text:\n"
        '{ "Payment Clauses": "text or \'Not found\'", '
        '"Confidentiality": "text or \'Not found\'", '
        '"Termination": "text or \'Not found\'", '
        '"Liability": "text or \'Not found\'", '
        '"Renewal": "text or \'Not found\'", '
        '"Warranty": "text or \'Not found\'" }'
    )
    return _ask_json(system_prompt, contract_text)


# ---------------------------------------------------------------------------
# Module 5 - Risk Analysis (risk + obligations + important dates)
# ---------------------------------------------------------------------------
def analyze_risks(contract_text):
    system_prompt = (
        "You are a legal risk-analysis engine. Read the contract text and "
        "identify: missing_clauses (list), high_risk_statements (list), "
        "penalties (list), compliance_issues (list). "
        "Reply with ONLY valid JSON in this exact shape, no extra text:\n"
        '{ "missing_clauses": [], "high_risk_statements": [], '
        '"penalties": [], "compliance_issues": [] }'
    )
    return _ask_json(system_prompt, contract_text)


def extract_dates_and_parties(contract_text):
    system_prompt = (
        "You are a legal data-extraction engine. Read the contract text and "
        "extract: parties_involved (list of names/companies), "
        "effective_date, expiry_date, key_dates (list of any other important "
        "dates and what they mean). "
        "Reply with ONLY valid JSON in this exact shape, no extra text:\n"
        '{ "parties_involved": [], "effective_date": "", "expiry_date": "", '
        '"key_dates": [] }'
    )
    return _ask_json(system_prompt, contract_text)


# ---------------------------------------------------------------------------
# Module 7 - AI Legal Chat
# ---------------------------------------------------------------------------
def chat_about_contract(contract_text, chat_history, user_question):
    """
    chat_history: list of {"role": "user"/"assistant", "content": "..."}
    from earlier turns in this conversation, so the AI remembers context.
    """
    system_prompt = (
        "You are a helpful legal assistant chatbot. Answer the user's "
        "questions ONLY using the contract text provided below. If the "
        "answer isn't in the contract, say so clearly instead of guessing.\n\n"
        f"CONTRACT TEXT:\n{contract_text[:12000]}"
    )
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_question})
    return _call_openrouter(messages)
