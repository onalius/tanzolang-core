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

from cli.tanzo-cli import cli  # This assumes the CLI uses click for commands


class TestTanzoCLI(unittest.TestCase):
    """Tests for the tanzo-cli.py command-line interface"""
    
    def setUp(self):
        """Setup test files and paths"""
        self.examples_dir = Path(__file__).parent.parent / "examples"
        self.valid_example = self.examples_dir / "Kai_profile.yaml"
        self.digital_example = self.examples_dir / "digital_archetype_only.yaml"
        
        # Ensure example files exist
        self.assertTrue(self.valid_example.exists(), f"Example file not found: {self.valid_example}")
        self.assertTrue(self.digital_example.exists(), f"Example file not found: {self.digital_example}")
    
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
        self.assertIn("Kai's Digital Twin", result.output)
    
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
        self.assertIn("Kai's Digital Twin", result.output)
        
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
        self.assertIn("TanzoProfile: Digital Avatar Only", result.output)
        self.assertIn("DIGITAL:Digital Avatar", result.output)
        
        # Should have formatted attributes
        self.assertIn("digital_id=\"DA-27491\"", result.output)
    
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


if __name__ == "__main__":
    unittest.main()
