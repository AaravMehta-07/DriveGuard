#!/usr/bin/env python3
"""
DriveGuard V3 — Release Verification Script

Executes all core release validation checks and writes machine-readable
verification output to artifacts/release-verification.json.
"""

import sys
import os
import json
import subprocess
import glob
import py_compile
import time

def run_cmd(cmd, cwd=None):
    """Run a shell command and return stdout, stderr, and exit code."""
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return {
            "command": cmd,
            "exit_code": res.returncode,
            "stdout": res.stdout[-2000:],  # Tail stdout
            "stderr": res.stderr[-2000:],
            "passed": res.returncode == 0
        }
    except Exception as e:
        return {
            "command": cmd,
            "exit_code": 1,
            "stdout": "",
            "stderr": str(e),
            "passed": False
        }

def check_python_compilation():
    """Verify all Python files compile cleanly without syntax errors."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    patterns = ['backend/**/*.py', 'packages/**/*.py', 'tests/**/*.py', 'data/**/*.py']
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(project_root, pat), recursive=True))
    
    compiled = 0
    errors = []
    for f in files:
        try:
            py_compile.compile(f, doraise=True)
            compiled += 1
        except Exception as e:
            errors.append({"file": f, "error": str(e)})
            
    return {
        "total_files": len(files),
        "compiled_successfully": compiled,
        "errors": errors,
        "passed": len(errors) == 0
    }

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    artifacts_dir = os.path.join(project_root, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    
    start_time = time.time()
    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python_compilation": check_python_compilation(),
        "pytest_unit_contracts": run_cmd("pytest tests/unit/ tests/provider-contract/ -v", cwd=project_root),
        "pytest_golden_routes": run_cmd("pytest tests/golden-routes/ -v", cwd=project_root),
        "pytest_e2e": run_cmd("pytest tests/e2e/ -v", cwd=project_root),
        "pytest_simulation": run_cmd("pytest tests/simulation/ -v", cwd=project_root),
    }
    
    # Overall summary
    all_passed = (
        results["python_compilation"]["passed"] and
        results["pytest_unit_contracts"]["passed"] and
        results["pytest_golden_routes"]["passed"] and
        results["pytest_e2e"]["passed"] and
        results["pytest_simulation"]["passed"]
    )
    
    results["overall_passed"] = all_passed
    results["elapsed_seconds"] = round(time.time() - start_time, 2)
    
    out_path = os.path.join(artifacts_dir, "release-verification.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Verification output written to {out_path}")
    print(f"Overall Passed: {all_passed}")
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
