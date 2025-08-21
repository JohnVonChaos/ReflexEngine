#!/usr/bin/env python3
"""
Structural Analysis Validation Script

This script validates the findings documented in STRUCTURAL_ANALYSIS.md
by checking for specific structural issues in the codebase.
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Dict, Any


def analyze_file_structure() -> Dict[str, Any]:
    """Analyze the file structure of the project."""
    project_root = Path(__file__).parent
    py_files = list(project_root.glob("**/*.py"))
    
    return {
        "total_py_files": len(py_files),
        "main_file_size": (project_root / "ReflexEngine_SelfPublished_v1.py").stat().st_size if (project_root / "ReflexEngine_SelfPublished_v1.py").exists() else 0,
        "has_main_module": (project_root / "ReflexEngine_SelfPublished_v1.py").exists(),
        "has_init_files": len(list(project_root.glob("**/__init__.py"))),
        "has_tests_dir": (project_root / "tests").exists(),
        "has_requirements": (project_root / "requirements.txt").exists(),
        "has_setup_docs": (project_root / "SETUP.md").exists(),
    }


def analyze_monolithic_structure() -> Dict[str, Any]:
    """Check for monolithic architecture issues."""
    main_file = Path(__file__).parent / "ReflexEngine_SelfPublished_v1.py"
    
    if not main_file.exists():
        return {"error": "Main file not found"}
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Parse AST to count classes and functions
    try:
        tree = ast.parse(content)
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        return {
            "line_count": len(lines),
            "class_count": len(classes),
            "function_count": len(functions),
            "classes": [cls.name for cls in classes],
            "functions": [func.name for func in functions],
            "is_monolithic": len(lines) > 300 and len(classes) > 3,
        }
    except SyntaxError as e:
        return {"error": f"Syntax error in main file: {e}"}


def analyze_global_state() -> Dict[str, Any]:
    """Check for global state and configuration issues."""
    main_file = Path(__file__).parent / "ReflexEngine_SelfPublished_v1.py"
    
    if not main_file.exists():
        return {"error": "Main file not found"}
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    global_vars = []
    hardcoded_configs = []
    
    # Look for global variable assignments
    for line_num, line in enumerate(content.split('\n'), 1):
        stripped = line.strip()
        if (stripped and not stripped.startswith('#') and not stripped.startswith('def ') 
            and not stripped.startswith('class ') and not stripped.startswith('import ')
            and not stripped.startswith('from ') and '=' in stripped
            and not stripped.startswith(' ')):  # Top-level assignments
            global_vars.append((line_num, stripped))
        
        # Look for hardcoded API endpoints and keys
        if 'api.fireworks.ai' in line or 'FIREWORKS_API_KEY' in line:
            hardcoded_configs.append((line_num, stripped))
    
    return {
        "global_variables": global_vars,
        "hardcoded_configs": hardcoded_configs,
        "has_debug_mode": any('DEBUG_MODE' in var[1] for var in global_vars),
        "has_api_key_exposure": any('print' in line for line in content.split('\n') if 'API_KEY' in line or 'prompt' in line.lower()),
    }


def analyze_error_handling() -> Dict[str, Any]:
    """Check for error handling patterns."""
    main_file = Path(__file__).parent / "ReflexEngine_SelfPublished_v1.py"
    
    if not main_file.exists():
        return {"error": "Main file not found"}
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try_blocks = len(re.findall(r'\btry\s*:', content))
    except_blocks = len(re.findall(r'\bexcept\b', content))
    logging_calls = len(re.findall(r'\blogging\b', content))
    print_statements = len(re.findall(r'\bprint\s*\(', content))
    
    return {
        "try_blocks": try_blocks,
        "except_blocks": except_blocks,
        "has_logging": logging_calls > 0,
        "uses_print_for_logging": print_statements > 0,
        "error_handling_score": "poor" if try_blocks < 3 else "fair" if try_blocks < 5 else "good",
    }


def analyze_threading() -> Dict[str, Any]:
    """Check for threading-related issues."""
    main_file = Path(__file__).parent / "ReflexEngine_SelfPublished_v1.py"
    
    if not main_file.exists():
        return {"error": "Main file not found"}
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    threading_imports = 'import threading' in content
    thread_creations = len(re.findall(r'threading\.Thread', content))
    daemon_threads = len(re.findall(r'daemon\s*=\s*True', content))
    lock_usage = len(re.findall(r'\.lock', content))
    
    return {
        "uses_threading": threading_imports,
        "thread_creations": thread_creations,
        "daemon_threads": daemon_threads,
        "lock_usage": lock_usage,
        "potential_race_conditions": thread_creations > 0 and lock_usage < thread_creations,
    }


def generate_report() -> str:
    """Generate a comprehensive structural analysis report."""
    print("Analyzing ReflexEngine structure...")
    
    file_structure = analyze_file_structure()
    monolithic = analyze_monolithic_structure()
    global_state = analyze_global_state()
    error_handling = analyze_error_handling()
    threading = analyze_threading()
    
    report = []
    report.append("=" * 60)
    report.append("REFLEXENGINE STRUCTURAL ANALYSIS VALIDATION")
    report.append("=" * 60)
    report.append("")
    
    # File Structure Analysis
    report.append("📁 FILE STRUCTURE ANALYSIS")
    report.append("-" * 30)
    report.append(f"Total Python files: {file_structure['total_py_files']}")
    report.append(f"Main file exists: {file_structure['has_main_module']}")
    report.append(f"Has __init__.py files: {file_structure['has_init_files']}")
    report.append(f"Has tests directory: {file_structure['has_tests_dir']}")
    report.append(f"Has requirements.txt: {file_structure['has_requirements']}")
    report.append(f"Has setup documentation: {file_structure['has_setup_docs']}")
    report.append("")
    
    # Monolithic Architecture Analysis
    if 'error' not in monolithic:
        report.append("🏗️ MONOLITHIC ARCHITECTURE ANALYSIS")
        report.append("-" * 40)
        report.append(f"Main file line count: {monolithic['line_count']}")
        report.append(f"Classes in main file: {monolithic['class_count']} ({', '.join(monolithic['classes'])})")
        report.append(f"Functions in main file: {monolithic['function_count']}")
        report.append(f"Is monolithic: {monolithic['is_monolithic']} ⚠️" if monolithic['is_monolithic'] else f"Is monolithic: {monolithic['is_monolithic']} ✓")
        report.append("")
    
    # Global State Analysis
    if 'error' not in global_state:
        report.append("🌐 GLOBAL STATE ANALYSIS")
        report.append("-" * 25)
        report.append(f"Global variables found: {len(global_state['global_variables'])}")
        for line_num, var in global_state['global_variables'][:5]:  # Show first 5
            report.append(f"  Line {line_num}: {var[:50]}{'...' if len(var) > 50 else ''}")
        report.append(f"Has DEBUG_MODE global: {global_state['has_debug_mode']} ⚠️" if global_state['has_debug_mode'] else f"Has DEBUG_MODE global: {global_state['has_debug_mode']} ✓")
        report.append(f"Hardcoded configs: {len(global_state['hardcoded_configs'])}")
        report.append(f"Potential API key exposure: {global_state['has_api_key_exposure']} ⚠️" if global_state['has_api_key_exposure'] else f"Potential API key exposure: {global_state['has_api_key_exposure']} ✓")
        report.append("")
    
    # Error Handling Analysis
    if 'error' not in error_handling:
        report.append("🚨 ERROR HANDLING ANALYSIS")
        report.append("-" * 30)
        report.append(f"Try blocks: {error_handling['try_blocks']}")
        report.append(f"Except blocks: {error_handling['except_blocks']}")
        report.append(f"Has proper logging: {error_handling['has_logging']} ⚠️" if not error_handling['has_logging'] else f"Has proper logging: {error_handling['has_logging']} ✓")
        report.append(f"Uses print for logging: {error_handling['uses_print_for_logging']} ⚠️" if error_handling['uses_print_for_logging'] else f"Uses print for logging: {error_handling['uses_print_for_logging']} ✓")
        report.append(f"Error handling score: {error_handling['error_handling_score']}")
        report.append("")
    
    # Threading Analysis
    if 'error' not in threading:
        report.append("🧵 THREADING ANALYSIS")
        report.append("-" * 20)
        report.append(f"Uses threading: {threading['uses_threading']}")
        report.append(f"Thread creations: {threading['thread_creations']}")
        report.append(f"Daemon threads: {threading['daemon_threads']}")
        report.append(f"Lock usage: {threading['lock_usage']}")
        report.append(f"Potential race conditions: {threading['potential_race_conditions']} ⚠️" if threading['potential_race_conditions'] else f"Potential race conditions: {threading['potential_race_conditions']} ✓")
        report.append("")
    
    # Summary
    report.append("📊 SUMMARY")
    report.append("-" * 10)
    issues_found = []
    if monolithic.get('is_monolithic', False):
        issues_found.append("Monolithic architecture")
    if global_state.get('has_debug_mode', False):
        issues_found.append("Global state issues")
    if not error_handling.get('has_logging', True):
        issues_found.append("Poor error handling")
    if threading.get('potential_race_conditions', False):
        issues_found.append("Threading issues")
    
    if issues_found:
        report.append(f"⚠️ Issues found: {', '.join(issues_found)}")
        report.append("See STRUCTURAL_ANALYSIS.md for detailed recommendations")
    else:
        report.append("✓ No major structural issues detected")
    
    report.append("")
    report.append("Report generated by structural_validation.py")
    report.append("=" * 60)
    
    return "\n".join(report)


if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # Also save to file
    with open("structural_validation_report.txt", "w") as f:
        f.write(report)
    print(f"\nReport saved to: structural_validation_report.txt")