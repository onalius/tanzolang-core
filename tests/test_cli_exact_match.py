import sys
from pathlib import Path
from click.testing import CliRunner

# Add parent directory to path for importing CLI
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import tanzo-cli as tanzo_cli - this matches the module name
from cli.tanzo_cli import cli as tanzo_cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(tanzo_cli, ["--help"])
    
    assert result.exit_code == 0
    assert "Usage:" in result.output