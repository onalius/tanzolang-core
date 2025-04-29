from click.testing import CliRunner
from cli.tanzo_cli import cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    
    assert result.exit_code == 0
    assert "Usage:" in result.output