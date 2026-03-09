#!/usr/bin/env python3
"""
Test script for llm_setup.py
Tests if the LLM configuration is working correctly.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from llm_setup import llm
    print("✅ Successfully imported LLM from llm_setup.py")

    # Test basic LLM functionality
    print("🔄 Testing LLM invocation...")

    test_prompt = "Hello! Please respond with just 'Hello, world!' and nothing else."

    response = llm.invoke([
        {"role": "user", "content": test_prompt}
    ])

    # Extract content from response
    if hasattr(response, "content"):
        content = response.content
    else:
        content = str(response)

    print(f"✅ LLM Response: {content}")
    print("✅ LLM setup test PASSED!")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("❌ Check if required packages are installed:")
    print("   pip install langchain-openai python-dotenv")

except Exception as e:
    print(f"❌ LLM Test Failed: {e}")
    print("❌ Check your .env file and API keys")
    print("❌ Make sure the LLM service is accessible")
