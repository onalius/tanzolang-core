"""
Common test fixtures for the Tanzo Schema test suite.
"""

import os
import sys
from pathlib import Path

# Add project root to path to allow imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
