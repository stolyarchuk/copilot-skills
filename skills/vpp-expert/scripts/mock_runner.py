#!/usr/bin/env python3
import sys

# Minimal mock runner for vpp-skill examples
if __name__ == "__main__":
    data = sys.stdin.read()
    # Echo input back in a simple deterministic way for tests
    print("Input:")
    print(data.strip())
    print("\nResponse:")
    print("This is a mock response from vpp-skill")
