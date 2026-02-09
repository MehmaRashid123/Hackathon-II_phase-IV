"""
Test runner script for MCP Server tests.

This script provides a convenient way to run different test suites.
"""
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print results."""
    print(f"\n{'=' * 60}")
    print(f"{description}")
    print(f"{'=' * 60}\n")
    
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def main():
    """Main test runner."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [all|unit|integration|coverage]")
        print("\nOptions:")
        print("  all          - Run all tests")
        print("  unit         - Run only unit tests")
        print("  integration  - Run only integration tests")
        print("  coverage     - Run tests with coverage report")
        print("  quick        - Run fast tests only")
        sys.exit(1)
    
    test_type = sys.argv[1].lower()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    
    if test_type == "all":
        return run_command(
            "pytest tests/",
            "Running all tests"
        )
    
    elif test_type == "unit":
        return run_command(
            "pytest tests/unit/ -v",
            "Running unit tests"
        )
    
    elif test_type == "integration":
        return run_command(
            "pytest tests/integration/ -v",
            "Running integration tests"
        )
    
    elif test_type == "coverage":
        return run_command(
            "pytest tests/ --cov=src --cov-report=html --cov-report=term",
            "Running tests with coverage"
        )
    
    elif test_type == "quick":
        return run_command(
            "pytest tests/ -m 'not slow' -v",
            "Running quick tests"
        )
    
    else:
        print(f"Unknown test type: {test_type}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
