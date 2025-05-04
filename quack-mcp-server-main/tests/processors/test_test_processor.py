"""
Test File: tests/processor/test_test_processor.py
Purpose: Simulate a code submission and verify the functionality of the processors/test_job_processor module.
"""

import os
import tempfile
import pytest
import asyncio

# Import the module to be tested (make sure the processors directory is in PYTHONPATH)
from quack.processors.test_job_processor import TestJobProcessor

# Create an instance of TestJobProcessor
test_job_processor = TestJobProcessor()

# Simulate a valid single-file submission (includes solution code and test code)
valid_submission = '''"""
Submission for Quack Testing Tool Example

This file includes both solution code and embedded tests.
"""

# ======= Solution Code =======
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

# ======= Test Code =======
def test_add():
    assert add(2, 3) == 5, "2 + 3 should equal 5"

# ======= Main Block =======
if __name__ == "__main__":
    import sys
    if "test" in sys.argv:
        import pytest
        sys.exit(pytest.main([__file__]))
    else:
        print("Demo: 2 + 3 =", add(2, 3))
'''

# Simulate a submission with a test failure (assertion error in the test)
failing_submission = '''"""
Submission for Quack Testing Tool Example with Failure

This file includes both solution code and embedded tests.
"""

# ======= Solution Code =======
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

# ======= Test Code =======
def test_add():
    # Intentionally set an incorrect result
    assert add(2, 3) == 6, "2 + 3 should equal 6"

# ======= Main Block =======
if __name__ == "__main__":
    import sys
    if "test" in sys.argv:
        import pytest
        sys.exit(pytest.main([__file__]))
    else:
        print("Demo: 2 + 3 =", add(2, 3))
'''

# Simulate a submission with a syntax error
syntax_error_submission = '''"""
Submission with Syntax Error

This file includes both solution code and embedded tests.
"""

# ======= Solution Code =======
def add(a, b):
    """Return the sum of two numbers."""
    return a + b

# The following intentionally contains a syntax error
def broken_function():
    print("This is broken"

# ======= Test Code =======
def test_add():
    assert add(2, 3) == 5, "2 + 3 should equal 5"

# ======= Main Block =======
if __name__ == "__main__":
    import sys
    if "test" in sys.argv:
        import pytest
        sys.exit(pytest.main([__file__]))
    else:
        print("Demo: 2 + 3 =", add(2, 3))
'''

@pytest.fixture
def temp_submission_file():
    """
    Temporary file factory: creates a temporary file, writes the given content, returns the file path, and cleans up after the test.
    """
    def _create_file(content):
        fd, path = tempfile.mkstemp(suffix=".py", text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        return path
    return _create_file

def test_valid_submission(temp_submission_file):
    file_path = temp_submission_file(valid_submission)
    result = test_job_processor.run_pytest_sync(file_path)
    # Expect all tests to pass (failure count should be 0)
    assert result.get("failed") == 0, f"Expected 0 failures, got: {result}"
    os.remove(file_path)

def test_failing_submission(temp_submission_file):
    file_path = temp_submission_file(failing_submission)
    result = test_job_processor.run_pytest_sync(file_path)
    # Check the returned error message or failure count to ensure the error is detected
    assert result.get("failed", 0) > 0 or "error" in result, f"Expected failures, got: {result}"
    os.remove(file_path)

def test_syntax_error_submission(temp_submission_file):
    file_path = temp_submission_file(syntax_error_submission)
    result = test_job_processor.run_pytest_sync(file_path)
    # When a syntax error occurs, pytest may not capture test results,
    # so the returned result should contain an error message or have a failure count greater than 0

    assert "error" in result or result.get("failed", 0) > 0, f"Expected error or failures, got: {result}"
    os.remove(file_path)

@pytest.mark.asyncio
async def test_async_valid_submission(temp_submission_file):
    file_path = temp_submission_file(valid_submission)
    result = await test_job_processor.run_pytest_async(file_path)
    assert result.get("failed") == 0, f"Expected 0 failures in async execution, got: {result}"
    os.remove(file_path)
