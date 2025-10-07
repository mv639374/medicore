import sys
import os

def test_sys_path():
    """
    This is a diagnostic test. It will print the Python path and current
    working directory from within the pytest environment and then fail
    on purpose so we can see the output.
    """
    print("\n\n--- DIAGNOSTIC INFORMATION ---")
    print(f"Current Working Directory: {os.getcwd()}")
    print("\nPython sys.path:")
    for p in sys.path:
        print(f"  - {p}")
    print("--- END DIAGNOSTIC ---")

    # This assertion will fail intentionally so pytest shows us the print statements.
    assert False, "Stopping test to display diagnostic path info."