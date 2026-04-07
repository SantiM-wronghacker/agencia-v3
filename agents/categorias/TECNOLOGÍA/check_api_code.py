#!/usr/bin/env python
"""Check which api_agencia.py file is being used"""
import sys
import os

# Add current dir to path
sys.path.insert(0, os.getcwd())

# Check file location
api_path = os.path.join(os.getcwd(), 'api_agencia.py')
print(f"Current directory: {os.getcwd()}")
print(f"API file path: {api_path}")
print(f"File exists: {os.path.exists(api_path)}")

# Check for /test-19-cats in the file
if os.path.exists(api_path):
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()

    has_test = '/test-19-cats' in content
    print(f"\n/test-19-cats endpoint exists: {has_test}")

    # Find the position
    if has_test:
        idx = content.find('/test-19-cats')
        section = content[max(0, idx-200):idx+500]
        print(f"\nContext around /test-19-cats:")
        print(section)
