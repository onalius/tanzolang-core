"""Pytest configuration for tanzo-lang-core."""

import sys
import os
from pathlib import Path

# Add repository root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import main modules to ensure they're available for tests
try:
    from clients.python.tanzo_schema import TanzoProfile
except ImportError:
    pass
