#!/usr/bin/env python
"""Test backend imports"""
import sys
sys.path.insert(0, '.')

try:
    from app.main import app
    print("OK: Backend imports successful")
    print(f"OK: FastAPI app created: {app.title}")
except Exception as e:
    print(f"ERROR: Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

