import sys
from pathlib import Path

# Add project root directory to sys.path so 'backend', 'packages', 'data' can be imported in tests
root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Add packages/provider-contracts to sys.path if needed
contracts_dir = root_dir / "packages" / "provider-contracts"
if str(contracts_dir) not in sys.path:
    sys.path.insert(0, str(contracts_dir))
