"""
Tests for the TanzoLang CLI.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

# Import the CLI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cli.tanzo_cli import cli


def test_validate_command_valid(example_file_path):
    """Test validating a valid file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", str(example_file_path)])
    assert result.exit_code == 0
    assert "Validation passed!" in result.output


def test_validate_command_invalid(invalid_schema_path):
    """Test validating an invalid file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", str(invalid_schema_path)])
    assert result.exit_code == 1
    assert "Validation failed!" in result.output


def test_validate_command_nonexistent():
    """Test validating a nonexistent file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "nonexistent.yaml"])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_simulate_command(example_file_path):
    """Test simulating a valid file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["simulate", str(example_file_path)])
    assert result.exit_code == 0
    assert "Simulation Results" in result.output


def test_simulate_command_with_iterations(example_file_path):
    """Test simulating with a custom number of iterations."""
    runner = CliRunner()
    result = runner.invoke(cli, ["simulate", str(example_file_path), "--iterations", "5"])
    assert result.exit_code == 0
    assert "Simulation Results (5 iterations)" in result.output


def test_simulate_command_invalid(invalid_schema_path):
    """Test simulating an invalid file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["simulate", str(invalid_schema_path)])
    assert result.exit_code == 1
    assert "Validation failed!" in result.output


def test_export_command(example_file_path):
    """Test exporting a valid file to shorthand."""
    runner = CliRunner()
    result = runner.invoke(cli, ["export", str(example_file_path)])
    assert result.exit_code == 0
    assert len(result.output.strip()) > 0


def test_export_command_invalid(invalid_schema_path):
    """Test exporting an invalid file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["export", str(invalid_schema_path)])
    assert result.exit_code == 1
    assert "Validation failed!" in result.output


def test_cli_script_executable():
    """Test that the CLI script is executable directly."""
    cli_path = Path(__file__).parent.parent / "cli" / "tanzo-cli.py"
    
    # Ensure the file exists
    assert cli_path.exists()
    
    # Ensure the file has execute permissions
    cli_path.chmod(0o755)
    
    # Test running the help command
    try:
        result = subprocess.run(
            [str(cli_path), "--help"],
            capture_output=True,
            text=True,
            check=True
        )
        assert "TanzoLang CLI" in result.stdout
        assert "validate" in result.stdout
        assert "simulate" in result.stdout
        assert "export" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        pytest.fail(f"Failed to execute CLI script: {e}")
