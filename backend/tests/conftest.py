import sys
from unittest.mock import MagicMock

def pytest_configure(config):
    """
    Mock the scanmem C extension module before any tests run.
    This allows testing on non-Linux systems where the C module cannot be compiled.
    """
    mock_scanmem = MagicMock()
    mock_scanmem.scan = MagicMock(return_value=10) # 10 matches by default
    mock_scanmem.read = MagicMock(return_value="0xDEADBEEF")
    mock_scanmem.write = MagicMock(return_value=True)
    
    # Inject into sys.modules
    sys.modules['scanmem'] = mock_scanmem
