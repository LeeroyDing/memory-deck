import pytest
import sys

def test_scan_operation():
    """Test that scanmem.scan is called correctly"""
    import scanmem
    
    # Call the mocked function
    matches = scanmem.scan("100", "==")
    
    # Verify return value
    assert matches == 10
    
    # Verify call arguments
    scanmem.scan.assert_called_with("100", "==")

def test_read_operation():
    """Test reading memory"""
    import scanmem
    val = scanmem.read(0x12345678)
    assert val == "0xDEADBEEF"
    scanmem.read.assert_called_with(0x12345678)

def test_write_operation():
    """Test writing memory"""
    import scanmem
    success = scanmem.write(0x12345678, "100")
    assert success is True
    scanmem.write.assert_called_with(0x12345678, "100")
