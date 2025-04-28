"""
Pytest configuration for tanzo-lang-core tests.
"""

import os
import sys
import pytest
from pathlib import Path

# Add parent directory to sys.path to import tanzo_schema
sys.path.insert(0, str(Path(__file__).parent.parent))
