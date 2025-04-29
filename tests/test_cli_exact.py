from click.testing import CliRunner
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.tanzo_cli import cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    
    assert result.exit_code == 0
    assert "Usage:" in result.output