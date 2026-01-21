#!/usr/bin/env python3
"""
API Key Validation Script

Tests configured API keys to verify they are working correctly.
Supports: OpenAI, Gemini, and other LiteLLM-compatible providers.

Usage:
    uv run --with litellm --with python-dotenv python check_apis.py
"""

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    import litellm
except ImportError:
    print("❌ Missing dependencies. Run with:")
    print("   uv run --with litellm --with python-dotenv python check_apis.py")
    sys.exit(1)


def load_environment():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        print(f"❌ .env file not found at {env_path}")
        sys.exit(1)

    load_dotenv(env_path, override=True)

    # Explicitly set API keys in environment for LiteLLM
    for key in ["GEMINI_API_KEY", "OPENAI_API_KEY"]:
        value = os.getenv(key)
        if value:
            os.environ[key] = value

    print(f"✅ Loaded environment from {env_path}\n")


def test_api_key(provider_name: str, model: str, api_key_var: str) -> dict:
    """
    Test an API key by making a minimal API call.

    Args:
        provider_name: Human-readable provider name (e.g., "OpenAI", "Gemini")
        model: LiteLLM model identifier (e.g., "gpt-4o", "gemini/gemini-2.0-flash")
        api_key_var: Environment variable name for the API key

    Returns:
        dict with 'success' (bool), 'message' (str), and optional 'error' (str)
    """
    api_key = os.getenv(api_key_var)

    if not api_key:
        return {
            'success': False,
            'message': f'❌ {provider_name}: API key not found (${api_key_var})',
            'error': 'missing_key'
        }

    print(f"Testing {provider_name} ({model})...", end=" ")

    try:
        # Make a minimal completion request
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5,
            timeout=10
        )

        if response and response.choices:
            print("✅")
            return {
                'success': True,
                'message': f'✅ {provider_name}: Working correctly',
                'model': model,
                'response_preview': response.choices[0].message.content[:50]
            }
        else:
            print("⚠️")
            return {
                'success': False,
                'message': f'⚠️ {provider_name}: Unexpected response format',
                'error': 'invalid_response'
            }

    except Exception as e:
        print("❌")
        error_msg = str(e)

        # Parse common error types
        if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
            error_type = "quota_exceeded"
            friendly_msg = "Quota exceeded - check billing"
        elif "invalid" in error_msg.lower() and "key" in error_msg.lower():
            error_type = "invalid_key"
            friendly_msg = "Invalid API key"
        elif "authentication" in error_msg.lower() or "unauthorized" in error_msg.lower():
            error_type = "auth_failed"
            friendly_msg = "Authentication failed"
        elif "rate" in error_msg.lower() and "limit" in error_msg.lower():
            error_type = "rate_limited"
            friendly_msg = "Rate limited - try again later"
        else:
            error_type = "unknown"
            friendly_msg = error_msg[:100]

        return {
            'success': False,
            'message': f'❌ {provider_name}: {friendly_msg}',
            'error': error_type,
            'error_details': error_msg
        }


def main():
    """Test all configured API keys."""
    print("=" * 60)
    print("API Key Validation")
    print("=" * 60 + "\n")

    load_environment()

    # Define providers to test
    # Format: (provider_name, litellm_model, env_var_name)
    providers = [
        ("OpenAI GPT-4", "gpt-4o", "OPENAI_API_KEY"),
        ("Google Gemini 2.5 Flash", "gemini/gemini-2.5-flash", "GEMINI_API_KEY"),
    ]

    results = []

    print("Running API Tests:")
    print("-" * 60)

    for provider_name, model, api_key_var in providers:
        result = test_api_key(provider_name, model, api_key_var)
        results.append(result)

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60 + "\n")

    working = [r for r in results if r['success']]
    failing = [r for r in results if not r['success']]

    if working:
        print("Working APIs:")
        for r in working:
            print(f"  {r['message']}")

    if failing:
        print("\nFailing APIs:")
        for r in failing:
            print(f"  {r['message']}")
            if 'error_details' in r:
                print(f"    Details: {r['error_details'][:200]}")

    print(f"\n{len(working)}/{len(results)} APIs working correctly\n")

    # Exit with error code if any tests failed
    sys.exit(0 if len(failing) == 0 else 1)


if __name__ == "__main__":
    main()
