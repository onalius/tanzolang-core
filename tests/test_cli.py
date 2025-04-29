"""
Tests for the TanzoLang CLI commands.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

# Find the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
CLI_PATH = ROOT_DIR / "cli" / "tanzo-cli.py"


def run_cli_command(command, *args, expected_exit_code=0):
    """Run a CLI command and check the exit code."""
    full_command = [sys.executable, str(CLI_PATH), command, *args]
    result = subprocess.run(full_command, capture_output=True, text=True)
    
    if result.returncode != expected_exit_code:
        print(f"Command failed with exit code {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        
    assert result.returncode == expected_exit_code, \
        f"Command {full_command} returned exit code {result.returncode}, expected {expected_exit_code}"
    
    return result


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_validate_command_with_valid_profile(example_file):
    """Test that the validate command succeeds with valid profiles."""
    example_path = EXAMPLES_DIR / example_file
    result = run_cli_command("validate", str(example_path))
    assert "Profile is valid" in result.stdout


def test_validate_command_with_verbose_flag():
    """Test that the validate command works with the verbose flag."""
    example_path = EXAMPLES_DIR / "Kai_profile.yaml"
    result = run_cli_command("validate", str(example_path), "--verbose")
    assert "Profile is valid" in result.stdout


def test_validate_command_with_nonexistent_file():
    """Test that the validate command fails with a nonexistent file."""
    with pytest.raises(AssertionError):
        run_cli_command("validate", "nonexistent.yaml", expected_exit_code=2)


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_simulate_command(example_file, tmp_path):
    """Test that the simulate command works."""
    example_path = EXAMPLES_DIR / example_file
    output_file = tmp_path / "simulation_results.json"
    
    result = run_cli_command(
        "simulate", 
        str(example_path), 
        "--iterations", "10", 
        "--output", str(output_file)
    )
    
    # Check if the command ran successfully
    assert "Running 10 simulation iterations" in result.stdout
    assert "Simulation Summary" in result.stdout
    
    # Check if the output file was created
    assert output_file.exists()
    
    # Check if the output file contains valid JSON
    with open(output_file, "r") as f:
        data = json.load(f)
        assert "summary" in data
        assert "simulations" in data
        assert len(data["simulations"]) == 10


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_export_command_shorthand(example_file):
    """Test that the export command works with shorthand format."""
    example_path = EXAMPLES_DIR / example_file
    result = run_cli_command("export", str(example_path), "--format", "shorthand")
    
    # Check that the output contains the profile name and at least one trait
    profile_data = yaml.safe_load(open(example_path, "r"))
    profile_name = profile_data["metadata"]["name"]
    
    assert profile_name in result.stdout
    assert "O:" in result.stdout  # Openness trait


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_export_command_json(example_file, tmp_path):
    """Test that the export command works with JSON format."""
    example_path = EXAMPLES_DIR / example_file
    output_file = tmp_path / "exported.json"
    
    result = run_cli_command(
        "export", 
        str(example_path), 
        "--format", "json",
        "--output", str(output_file)
    )
    
    # Check if the output file was created
    assert output_file.exists()
    
    # Check if the output file contains valid JSON
    with open(output_file, "r") as f:
        data = json.load(f)
        assert "metadata" in data
        assert "digital_archetype" in data


@pytest.mark.parametrize("example_file", [
    "Kai_profile.yaml",
    "digital_archetype_only.yaml",
])
def test_export_command_yaml(example_file, tmp_path):
    """Test that the export command works with YAML format."""
    example_path = EXAMPLES_DIR / example_file
    output_file = tmp_path / "exported.yaml"
    
    result = run_cli_command(
        "export", 
        str(example_path), 
        "--format", "yaml",
        "--output", str(output_file)
    )
    
    # Check if the output file was created
    assert output_file.exists()
    
    # Check if the output file contains valid YAML
    with open(output_file, "r") as f:
        data = yaml.safe_load(f)
        assert "metadata" in data
        assert "digital_archetype" in data
