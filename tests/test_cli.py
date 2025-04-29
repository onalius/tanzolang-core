"""
Tests for the TanzoLang CLI
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.tanzo_cli import cli  # This assumes the CLI uses click for commands


class TestTanzoCLI(unittest.TestCase):
    """Tests for the tanzo-cli.py command-line interface"""
    
    def setUp(self):
        """Setup test files and paths"""
        # First try test_data directory (for CI)
        self.test_data_dir = Path(__file__).parent / "test_data"
        if self.test_data_dir.exists():
            self.examples_dir = self.test_data_dir
        else:
            # Fall back to examples directory (for local development)
            self.examples_dir = Path(__file__).parent.parent / "examples"
            
        self.valid_example = self.examples_dir / "Kai_profile.yaml"
        self.digital_example = self.examples_dir / "digital_archetype_only.yaml"
        
        # Print available files for debugging
        print(f"Test files directory: {self.examples_dir}")
        if self.examples_dir.exists():
            print(f"Available files: {list(self.examples_dir.glob('*.yaml'))}")
        
        # Ensure example files exist
        self.assertTrue(self.valid_example.exists() or (self.examples_dir / "Hermit_profile.yaml").exists(), 
                      f"No example files found in: {self.examples_dir}")
        
        # If specific files don't exist but we have alternatives, use them
        if not self.valid_example.exists() and (self.examples_dir / "Hermit_profile.yaml").exists():
            self.valid_example = self.examples_dir / "Hermit_profile.yaml"
            
        if not self.digital_example.exists() and self.valid_example.exists():
            self.digital_example = self.valid_example
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_validate_valid_file(self, mock_stdout):
        """Test validation of a valid file"""
        # Use the click test runner to invoke the CLI
        from click.testing import CliRunner
        runner = CliRunner()
        
        result = runner.invoke(cli, ['validate', str(self.valid_example)])
        
        # Check exit code and output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("valid", result.output)
        # Accept either profile name as valid
        self.assertTrue(
            "Kai's Digital Twin" in result.output or 
            "Hermit" in result.output, 
            f"Expected profile name not found in output: {result.output}"
        )
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_validate_nonexistent_file(self, mock_stdout):
        """Test validation of a nonexistent file"""
        from click.testing import CliRunner
        runner = CliRunner()
        
        result = runner.invoke(cli, ['validate', 'nonexistent.yaml'])
        
        # Should fail with non-zero exit code
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("failed", result.output.lower())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_simulate_command(self, mock_stdout):
        """Test the simulate command"""
        from click.testing import CliRunner
        runner = CliRunner()
        
        # Run with fewer iterations for speed
        result = runner.invoke(cli, ['simulate', str(self.valid_example), '--iterations', '10'])
        
        # Check exit code and output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Simulation completed", result.output)
        
        # Accept either profile name as valid
        self.assertTrue(
            "Kai's Digital Twin" in result.output or 
            "Hermit" in result.output, 
            f"Expected profile name not found in output: {result.output}"
        )
        
        # Should have archetypes section
        self.assertIn("Archetype:", result.output)
        
        # Should have attribute statistics
        self.assertIn("Mean:", result.output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_export_command(self, mock_stdout):
        """Test the export command"""
        from click.testing import CliRunner
        runner = CliRunner()
        
        result = runner.invoke(cli, ['export', str(self.digital_example)])
        
        # Check exit code and output
        self.assertEqual(result.exit_code, 0)
        
        # For flexibility, check that some kind of TanzoProfile is mentioned
        self.assertIn("TanzoProfile:", result.output)
        
        # At least one of these should be present depending on which file was used
        has_expected_content = any([
            "DIGITAL:Digital Avatar" in result.output,
            "ARCHETYPE:Hermit" in result.output,
            "Kai's Digital Twin" in result.output
        ])
        self.assertTrue(has_expected_content, f"None of the expected content was found in: {result.output}")
        
        # Should have some kind of formatted attributes
        has_attributes = any([
            "digital_id=" in result.output,
            "solitude=" in result.output,
            "self_reflection=" in result.output
        ])
        self.assertTrue(has_attributes, f"No attribute formatting found in: {result.output}")
    
    def test_help_command(self):
        """Test the help output"""
        from click.testing import CliRunner
        runner = CliRunner()
        
        result = runner.invoke(cli, ['--help'])
        
        # Check exit code and output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("TanzoLang CLI", result.output)
        
        # Should list all commands
        self.assertIn("validate", result.output)
        self.assertIn("simulate", result.output)
        self.assertIn("export", result.output)
    
    def test_cli_help(self):
        """Test that the CLI help command works"""
        from click.testing import CliRunner
        
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        
        # Check exit code and output
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage:", result.output)


if __name__ == "__main__":
    unittest.main()
