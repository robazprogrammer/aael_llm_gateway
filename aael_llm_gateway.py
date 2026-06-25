# aael_llm_gateway.py
# AAEL Labs Project 01: Multi-Provider LLM Gateway

import os
import requests
from datetime import datetime


class LLMGatewayError(Exception):
    pass


DEFAULT_MAX_TOKENS = 500
DEFAULT_TIMEOUT = 45

PROVIDERS = {
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "api_key_env": "OPENAI_API_KEY",
        "default_model": "gpt-4o-mini",
    },
    "together": {
        "url": "https://api.together.xyz/v1/chat/completions",
        "api_key_env": "TOGETHER_API_KEY",
        "default_model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    },
    "anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "api_key_env": "ANTHROPIC_API_KEY",
        "default_model": "claude-3-5-sonnet-latest",
    },
}


def generate(provider, messages, model=None, max_tokens=DEFAULT_MAX_TOKENS):
    provider = provider.lower().strip()

    if provider not in PROVIDERS:
        raise LLMGatewayError(f"Unsupported provider: {provider}")

    if provider == "anthropic":
        return _call_anthropic(provider, messages, model, max_tokens)

    return _call_openai_compatible(provider, messages, model, max_tokens)


def _call_openai_compatible(provider, messages, model, max_tokens):
    config = PROVIDERS[provider]
    api_key = os.getenv(config["api_key_env"])

    if not api_key:
        raise LLMGatewayError(f"Missing environment variable: {config['api_key_env']}")

    payload = {
        "model": model or config["default_model"],
        "messages": messages,
        "max_tokens": max_tokens,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        config["url"],
        headers=headers,
        json=payload,
        timeout=DEFAULT_TIMEOUT,
    )

    if response.status_code != 200:
        raise LLMGatewayError(f"{provider} error: {response.text}")

    data = response.json()
    text = data["choices"][0]["message"]["content"]

    return _normalize(provider, payload["model"], text)


def _call_anthropic(provider, messages, model, max_tokens):
    config = PROVIDERS[provider]
    api_key = os.getenv(config["api_key_env"])

    if not api_key:
        raise LLMGatewayError(f"Missing environment variable: {config['api_key_env']}")

    system_text = None
    cleaned_messages = []

    for message in messages:
        if message["role"] == "system":
            system_text = message["content"]
        else:
            cleaned_messages.append(message)

    payload = {
        "model": model or config["default_model"],
        "messages": cleaned_messages,
        "max_tokens": max_tokens,
    }

    if system_text:
        payload["system"] = system_text

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    response = requests.post(
        config["url"],
        headers=headers,
        json=payload,
        timeout=DEFAULT_TIMEOUT,
    )

    if response.status_code != 200:
        raise LLMGatewayError(f"{provider} error: {response.text}")

    data = response.json()
    text = data["content"][0]["text"]

    return _normalize(provider, payload["model"], text)


def _normalize(provider, model, text):
    return {
        "provider": provider,
        "model": model,
        "text": text,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def aael_task(prompt, provider="openai"):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AAEL Labs assistant. Use the Ask, Adapt, "
                "Evaluate, Learn framework. Be practical, structured, and concise."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    return generate(provider=provider, messages=messages)


if __name__ == "__main__":
    task = """
    Scenario: Create a Phoenix housing market report.
    Use AAEL:
    1. Ask: clarify the task
    2. Adapt: identify data and tools
    3. Evaluate: explain how to check quality
    4. Learn: explain what the user should take away
    """

    result = aael_task(task, provider="openai")

    print("\n--- AAEL LABS OUTPUT ---")
    print(f"Provider: {result['provider']}")
    print(f"Model: {result['model']}")
    print(f"Time: {result['timestamp']}")
    print("\nResponse:\n")
    print(result["text"])
