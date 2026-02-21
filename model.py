import json
import requests

import os
from dotenv import load_dotenv

load_dotenv()


OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']

MODEL = "arcee-ai/trinity-large-preview:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def model(prompt, history=None, continue_reasoning=True):
    """
    Send a prompt to the Arcee Trinity‑Large‑Preview model.
    
    Parameters
    ----------
    prompt : str or list[dict]
        If a string, it is wrapped as a user message.
        If a list, it should be a sequence of message dicts.
    history : dict, optional
        Contains 'content' and 'reasoning_details' from a previous response
        to allow continuation.
    continue_reasoning : bool
        If True and `history` is provided, a second call is made to continue
        the reasoning from where it left off.
    Returns
    -------
    dict
        The assistant's message with 'content' and, if available,
        'reasoning_details'.
    """
    # Build the initial message list
    if isinstance(prompt, str):
        messages = [{"role": "user", "content": prompt}]
    else:
        messages = prompt

    # First call: request reasoning
    payload = {
        "model": MODEL,
        "messages": messages,
        "reasoning": {"enabled": True}
    }
    r = requests.post(API_URL, headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }, data=json.dumps(payload))
    r.raise_for_status()
    first_resp = r.json()["choices"][0]["message"]

    # If we want to continue reasoning, include the reasoning_details
    if continue_reasoning and history:
        messages.append(first_resp)  # preserve content and reasoning_details
        payload = {
            "model": MODEL,
            "messages": messages,
            "reasoning": {"enabled": True}
        }
        r2 = requests.post(API_URL, headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }, data=json.dumps(payload))
        r2.raise_for_status()
        return r2.json()["choices"] ["message"]

    return first_resp

#print(model("hello")['content'])
