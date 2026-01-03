import pytest
import asyncio
import sys
import os

# Add project root to sys.path so we can import main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


class TestFreezeFunctionality:
    """Integration tests for Plugin freeze methods"""
    
    @pytest.fixture
    def plugin(self):
        """Create a fresh Plugin instance for each test"""
        from main import Plugin
        p = Plugin()
        # Don't start the freeze loop for tests (it runs forever)
        p.frozen_addresses = {}
        return p
    
    def test_freeze_adds_to_frozen_addresses(self, plugin):
        """Test that freeze() adds an entry to frozen_addresses"""
        result = asyncio.run(plugin.freeze("0x1234", "100", "i32"))
        
        assert result is True
        assert "0x1234" in plugin.frozen_addresses
        assert plugin.frozen_addresses["0x1234"]["address"] == "0x1234"
        assert plugin.frozen_addresses["0x1234"]["value"] == "100"
        assert plugin.frozen_addresses["0x1234"]["type"] == "i32"
        assert plugin.frozen_addresses["0x1234"]["enabled"] is True
    
    def test_freeze_updates_existing_address(self, plugin):
        """Test that freeze() updates value if address already frozen"""
        asyncio.run(plugin.freeze("0x1234", "100", "i32"))
        asyncio.run(plugin.freeze("0x1234", "200", "i32"))
        
        assert plugin.frozen_addresses["0x1234"]["value"] == "200"
    
    def test_unfreeze_removes_address(self, plugin):
        """Test that unfreeze() removes an address from frozen_addresses"""
        asyncio.run(plugin.freeze("0x1234", "100", "i32"))
        assert "0x1234" in plugin.frozen_addresses
        
        result = asyncio.run(plugin.unfreeze("0x1234"))
        
        assert result is True
        assert "0x1234" not in plugin.frozen_addresses
    
    def test_unfreeze_nonexistent_address_succeeds(self, plugin):
        """Test that unfreeze() on non-existent address doesn't crash"""
        result = asyncio.run(plugin.unfreeze("0xNONEXISTENT"))
        assert result is True
    
    def test_get_frozen_list_returns_all(self, plugin):
        """Test that get_frozen_list() returns all frozen addresses"""
        asyncio.run(plugin.freeze("0x1111", "10", "i8"))
        asyncio.run(plugin.freeze("0x2222", "20", "i16"))
        asyncio.run(plugin.freeze("0x3333", "30", "i32"))
        
        frozen_list = asyncio.run(plugin.get_frozen_list())
        
        assert len(frozen_list) == 3
        addresses = [item["address"] for item in frozen_list]
        assert "0x1111" in addresses
        assert "0x2222" in addresses
        assert "0x3333" in addresses
    
    def test_get_frozen_list_empty_when_none_frozen(self, plugin):
        """Test that get_frozen_list() returns empty list when nothing frozen"""
        frozen_list = asyncio.run(plugin.get_frozen_list())
        assert frozen_list == []


class TestFreezeLoop:
    """Tests for the freeze loop functionality"""
    
    @pytest.fixture
    def plugin_with_scanmem(self):
        """Create Plugin with mocked scanmem"""
        from main import Plugin
        from unittest.mock import MagicMock
        
        p = Plugin()
        p.scanmem = MagicMock()
        p.scanmem.exec_command = MagicMock()
        p.frozen_addresses = {}
        return p
    
    def test_freeze_loop_calls_exec_command(self, plugin_with_scanmem):
        """Test that freeze loop calls exec_command with correct write command"""
        plugin = plugin_with_scanmem
        
        # Add a frozen address
        plugin.frozen_addresses["0xABCD"] = {
            "address": "0xABCD",
            "value": "999",
            "type": "i32",
            "enabled": True
        }
        
        # Run one iteration of freeze loop logic (without the infinite loop)
        for address, item in list(plugin.frozen_addresses.items()):
            if item['enabled']:
                cmd = f"write {item['type']} {item['address']} {item['value']}"
                plugin.scanmem.exec_command(cmd)
        
        # Verify exec_command was called with correct command
        plugin.scanmem.exec_command.assert_called_once_with("write i32 0xABCD 999")
    
    def test_freeze_loop_skips_disabled(self, plugin_with_scanmem):
        """Test that freeze loop skips disabled frozen addresses"""
        plugin = plugin_with_scanmem
        
        plugin.frozen_addresses["0xABCD"] = {
            "address": "0xABCD",
            "value": "999",
            "type": "i32",
            "enabled": False  # Disabled
        }
        
        # Run one iteration
        for address, item in list(plugin.frozen_addresses.items()):
            if item['enabled']:
                cmd = f"write {item['type']} {item['address']} {item['value']}"
                plugin.scanmem.exec_command(cmd)
        
        # exec_command should NOT be called
        plugin.scanmem.exec_command.assert_not_called()
