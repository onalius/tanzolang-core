"""
Tests for the CLI functionality.
"""

import json
import pytest
import sys
from pathlib import Path
from click.testing import CliRunner

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))
from cli.tanzo-cli import cli, validate_cmd, simulate_cmd, export_cmd


@pytest.fixture
def runner():
    """Click test runner fixture."""
    return CliRunner()


@pytest.fixture
def example_profiles():
    """Return paths to example profiles."""
    examples_dir = Path(__file__).parent.parent / "examples"
    return {
        "kai": examples_dir / "Kai_profile.yaml",
        "minimal": examples_dir / "digital_archetype_only.yaml"
    }


def test_validate_command(runner, example_profiles):
    """Test the validate command."""
    # Test with valid profile
    result = runner.invoke(validate_cmd, [str(example_profiles["kai"])])
    assert result.exit_code == 0
    assert "valid" in result.output
    
    # Test with minimal profile
    result = runner.invoke(validate_cmd, [str(example_profiles["minimal"])])
    assert result.exit_code == 0
    assert "valid" in result.output
    
    # Test with non-existent file
    result = runner.invoke(validate_cmd, ["nonexistent.yaml"])
    assert result.exit_code == 2  # Click's error code for file not found


def test_simulate_command(runner, example_profiles):
    """Test the simulate command."""
    # Test with default iterations
    result = runner.invoke(simulate_cmd, [str(example_profiles["kai"])])
    assert result.exit_code == 0
    assert "Simulation Results" in result.output
    assert "Ran 100 iterations" in result.output
    
    # Test with custom iterations
    result = runner.invoke(simulate_cmd, [str(example_profiles["kai"]), "--iterations", "10"])
    assert result.exit_code == 0
    assert "Ran 10 iterations" in result.output
    
    # Test with minimal profile
    result = runner.invoke(simulate_cmd, [str(example_profiles["minimal"])])
    assert result.exit_code == 0
    assert "Simulation Results" in result.output


def test_export_command(runner, example_profiles):
    """Test the export command."""
    # Test shorthand format (default)
    result = runner.invoke(export_cmd, [str(example_profiles["kai"])])
    assert result.exit_code == 0
    assert "Kai - Technical Advisor" in result.output
    assert "[advisor/expert]" in result.output
    
    # Test JSON format
    result = runner.invoke(export_cmd, [str(example_profiles["kai"]), "--format", "json"])
    assert result.exit_code == 0
    # Verify it's valid JSON
    data = json.loads(result.output)
    assert data["profile"]["name"] == "Kai - Technical Advisor"
    
    # Test YAML format
    result = runner.invoke(export_cmd, [str(example_profiles["kai"]), "--format", "yaml"])
    assert result.exit_code == 0
    assert "name: Kai - Technical Advisor" in result.output
    
    # Test with minimal profile
    result = runner.invoke(export_cmd, [str(example_profiles["minimal"])])
    assert result.exit_code == 0
    assert "Digital Guide" in result.output
