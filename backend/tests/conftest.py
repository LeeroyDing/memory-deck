import sys
from unittest.mock import MagicMock, create_autospec

def pytest_configure(config):
    """
    Mock the scanmem module before any tests run.
    This allows testing on non-Linux systems where the C module cannot be compiled.
    """
    # Create mock Scanmem class
    mock_scanmem_class = MagicMock()
    mock_scanmem_instance = MagicMock()
    mock_scanmem_instance.init = MagicMock(return_value=True)
    mock_scanmem_instance.set_backend = MagicMock()
    mock_scanmem_instance.reset = MagicMock()
    mock_scanmem_instance.exec_command = MagicMock(return_value=True)
    mock_scanmem_instance.get_num_matches = MagicMock(return_value=0)
    mock_scanmem_instance.get_matches = MagicMock(return_value=[])
    mock_scanmem_class.return_value = mock_scanmem_instance
    
    # Create mock module
    mock_scanmem_module = MagicMock()
    mock_scanmem_module.Scanmem = mock_scanmem_class
    mock_scanmem_module.parse_uservalue = MagicMock(return_value=MagicMock())
    mock_scanmem_module.UserValue = MagicMock
    mock_scanmem_module.MatchFlag = MagicMock()
    mock_scanmem_module.ScanMatchType = MagicMock()
    mock_scanmem_module.ScanDataType = MagicMock()
    
    # Legacy mocks for old tests
    mock_scanmem_module.scan = MagicMock(return_value=10)
    mock_scanmem_module.read = MagicMock(return_value="0xDEADBEEF")
    mock_scanmem_module.write = MagicMock(return_value=True)
    
    # Inject into sys.modules
    sys.modules['scanmem'] = mock_scanmem_module

