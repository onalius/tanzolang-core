"""
Tests for the TanzoLang CLI.
"""

import json
import os
import pathlib
import pytest
import yaml
from click.testing import CliRunner

from cli.tanzo_cli import cli


@pytest.fixture
def cli_runner():
    """Return a Click CLI runner."""
    return CliRunner()


@pytest.fixture
def examples_dir():
    """Return the path to the examples directory."""
    return pathlib.Path(__file__).parent.parent / "examples"


@pytest.fixture
def kai_profile(examples_dir):
    """Return the path to the Kai profile example."""
    return examples_dir / "Kai_profile.yaml"


@pytest.fixture
def archetype_only(examples_dir):
    """Return the path to the archetype-only example."""
    return examples_dir / "digital_archetype_only.yaml"


@pytest.fixture
def invalid_profile(tmp_path):
    """Create and return the path to an invalid profile."""
    invalid_data = {
        "version": "0.1.0",
        "profile_type": "invalid_type",
        "archetype": {
            "name": "Invalid Archetype"
            # Missing required fields
        }
    }
    invalid_path = tmp_path / "invalid.yaml"
    with open(invalid_path, "w") as f:
        yaml.dump(invalid_data, f)
    return invalid_path


# Test validate command
def test_validate_command_valid(cli_runner, kai_profile):
    """Test the validate command with a valid profile."""
    result = cli_runner.invoke(cli, ["validate", str(kai_profile)])
    assert result.exit_code == 0
    assert "Validation successful!" in result.output
    assert "Kai" in result.output


def test_validate_command_invalid(cli_runner, invalid_profile):
    """Test the validate command with an invalid profile."""
    result = cli_runner.invoke(cli, ["validate", str(invalid_profile)])
    assert result.exit_code == 1
    assert "Validation failed" in result.output


def test_validate_command_nonexistent(cli_runner):
    """Test the validate command with a nonexistent file."""
    result = cli_runner.invoke(cli, ["validate", "/nonexistent/file.yaml"])
    assert result.exit_code == 1
    assert "File not found" in result.output


# Test simulate command
def test_simulate_command_basic(cli_runner, kai_profile):
    """Test the basic simulate command."""
    result = cli_runner.invoke(cli, ["simulate", str(kai_profile)])
    assert result.exit_code == 0
    assert "Running simulation with 100 iterations" in result.output
    assert "Simulation Results" in result.output
    assert "Core Traits" in result.output
    assert "Skills" in result.output
    assert "Environments" in result.output


def test_simulate_command_custom_iterations(cli_runner, kai_profile):
    """Test the simulate command with custom iterations."""
    result = cli_runner.invoke(cli, ["simulate", str(kai_profile), "--iterations", "50"])
    assert result.exit_code == 0
    assert "Running simulation with 50 iterations" in result.output


def test_simulate_command_specific_environment(cli_runner, kai_profile):
    """Test the simulate command with a specific environment."""
    result = cli_runner.invoke(
        cli, ["simulate", str(kai_profile), "--environment", "Test Environment"]
    )
    assert result.exit_code == 0
    assert "Test Environment" in result.output


def test_simulate_command_output_file(cli_runner, kai_profile, tmp_path):
    """Test the simulate command with output to a file."""
    output_file = tmp_path / "simulation_results.json"
    result = cli_runner.invoke(
        cli, ["simulate", str(kai_profile), "--output", str(output_file)]
    )
    assert result.exit_code == 0
    assert f"Results saved to {output_file}" in result.output
    assert output_file.exists()
    
    # Check that the output file contains valid JSON
    with open(output_file, "r") as f:
        data = json.load(f)
    
    assert "traits" in data
    assert "skills" in data
    assert "environments" in data


def test_simulate_command_invalid(cli_runner, invalid_profile):
    """Test the simulate command with an invalid profile."""
    result = cli_runner.invoke(cli, ["simulate", str(invalid_profile)])
    assert result.exit_code == 1
    assert "Validation failed" in result.output


# Test export command
def test_export_command_full(cli_runner, kai_profile):
    """Test the export command with a full profile."""
    result = cli_runner.invoke(cli, ["export", str(kai_profile)])
    assert result.exit_code == 0
    assert "Kai" in result.output
    assert "[T:" in result.output
    assert "S:" in result.output
    assert result.output.startswith("F:")  # Full profile indicator


def test_export_command_archetype_only(cli_runner, archetype_only):
    """Test the export command with an archetype-only profile."""
    result = cli_runner.invoke(cli, ["export", str(archetype_only)])
    assert result.exit_code == 0
    assert "Nova" in result.output
    assert "[T:" in result.output
    assert "S:" in result.output
    assert result.output.startswith("A:")  # Archetype-only indicator


def test_export_command_invalid(cli_runner, invalid_profile):
    """Test the export command with an invalid profile."""
    result = cli_runner.invoke(cli, ["export", str(invalid_profile)])
    assert result.exit_code == 1
    assert "Validation failed" in result.output


# Test CLI help text
def test_cli_help(cli_runner):
    """Test the CLI help text."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Tanzo CLI" in result.output
    assert "validate" in result.output
    assert "simulate" in result.output
    assert "export" in result.output


def test_validate_command_help(cli_runner):
    """Test the validate command help text."""
    result = cli_runner.invoke(cli, ["validate", "--help"])
    assert result.exit_code == 0
    assert "Validate a Tanzo profile" in result.output


def test_simulate_command_help(cli_runner):
    """Test the simulate command help text."""
    result = cli_runner.invoke(cli, ["simulate", "--help"])
    assert result.exit_code == 0
    assert "Run a Monte Carlo simulation" in result.output
    assert "--iterations" in result.output
    assert "--environment" in result.output
    assert "--output" in result.output


def test_export_command_help(cli_runner):
    """Test the export command help text."""
    result = cli_runner.invoke(cli, ["export", "--help"])
    assert result.exit_code == 0
    assert "Export a Tanzo profile as a shorthand string" in result.output
