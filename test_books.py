#!/usr/bin/env python3
import sys
sys.path.insert(0, '/app')
try:
    from app import app as flask_app
    with flask_app.test_client() as c:
        print("\n=== Testing GET /books/ ===")
        r = c.get('/books/')
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {r.content_type}")
        if r.status_code != 200:
            print(f"Response (first 500 chars): {r.data[:500]}")
        else:
            print("SUCCESS - /books/ returned 200")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
