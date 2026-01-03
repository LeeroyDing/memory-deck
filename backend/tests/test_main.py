import pytest
import sys
import os

# Add project root to sys.path so we can import main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

def test_mock_scanmem_injection():
    """Verify that scanmem is mocked correctly"""
    import scanmem
    assert isinstance(scanmem, object)
    assert scanmem.scan(100, "==") == 10

def test_main_import():
    """Verify that main.py can be imported without crashing due to missing dependencies"""
    try:
        from main import Plugin
        assert Plugin is not None
    except ImportError as e:
        pytest.fail(f"Could not import Plugin from main: {e}")
    except Exception as e:
        pytest.fail(f"Importing main crashed: {e}")