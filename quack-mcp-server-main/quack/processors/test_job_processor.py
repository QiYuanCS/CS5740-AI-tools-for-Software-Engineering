import subprocess
import asyncio
import logging
import re
from quack.jobs.base import JobProcessor

logger = logging.getLogger(__name__)

class TestJobProcessor(JobProcessor):
    """
    Test job processor used to run pytest tests.
    """

    def process(self, job) -> dict:
        """
        Process the test job.

        Args:
            job: A job object containing code and metadata, should provide the attribute code_file_path

        Returns:
            A dictionary of test results
        """
        file_path = job.code_file_path  # Assume the job object provides the code file path
        logger.info(f"Processing test job for file: {file_path}")
        return self.run_pytest_sync(file_path)


    def run_pytest_sync(self, file_path: str, timeout: int = 30) -> dict:
        """
        Run pytest tests synchronously.
        """
        return run_pytest_sync(file_path, timeout)

    async def run_pytest_async(self, file_path: str, timeout: int = 30) -> dict:
        """
        Run pytest tests asynchronously.
        """
        return await run_pytest_async(file_path, timeout)


def parse_pytest_output(output: str) -> dict:
    """
    Parse pytest output and extract the number of passed tests, failed tests, and error messages.
    """
    result = {"passed": 0, "failed": 0, "error": ""}

    summary_pattern = r"=+\s*(.+?)\s+in\s+[\d\.]+s\s*=+"
    match = re.search(summary_pattern, output)
    if match:
        summary = match.group(1)
        fail_match = re.search(r"(\d+)\s+failed", summary)
        pass_match = re.search(r"(\d+)\s+passed", summary)
        if fail_match:
            result["failed"] = int(fail_match.group(1))
        if pass_match:
            result["passed"] = int(pass_match.group(1))
        # If a summary line is found but no pass/fail data matched, mark it as an error
        if not fail_match and not pass_match:
            result["error"] = "Summary found, but no pass/failed counts."
    else:
        # If no summary line matched, search globally in the output for patterns
        fail_match = re.search(r"(\d+)\s+failed", output)
        pass_match = re.search(r"(\d+)\s+passed", output)
        if fail_match or pass_match:
            if fail_match:
                result["failed"] = int(fail_match.group(1))
            if pass_match:
                result["passed"] = int(pass_match.group(1))
        else:
            result["error"] = "Unable to parse pytest output summary."
    return result



def run_pytest_sync(file_path: str, timeout: int = 30) -> dict:
    """
    Synchronously invoke pytest on the given file and return structured results.
    """
    try:
        process = subprocess.run(
            ["pytest", file_path, "--tb=short"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False
        )
        stdout_str = process.stdout.decode("utf-8")
        stderr_str = process.stderr.decode("utf-8")
        combined_output = stdout_str + "\n" + stderr_str
        return parse_pytest_output(combined_output)
    except subprocess.TimeoutExpired:
        logger.error("pytest execution timed out")
        return {"error": "Execution timed out"}
    except Exception as e:
        logger.exception("Unexpected error running pytest")
        return {"error": str(e)}


async def run_pytest_async(file_path: str, timeout: int = 30) -> dict:
    """
    Asynchronously invoke pytest on the given file and return structured results.
    """
    try:
        process = await asyncio.create_subprocess_exec(
            "pytest",
            file_path,
            "--tb=short",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        stdout_str = stdout.decode("utf-8")
        stderr_str = stderr.decode("utf-8")
        combined_output = stdout_str + "\n" + stderr_str
        return parse_pytest_output(combined_output)
    except asyncio.TimeoutError:
        logger.error("pytest async execution timed out")
        return {"error": "Execution timed out"}
    except Exception as e:
        logger.exception("Unexpected error running pytest asynchronously")
        return {"error": str(e)}
