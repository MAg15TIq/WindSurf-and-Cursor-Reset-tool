#!/usr/bin/env python3
"""
Test Script for Cursor & Windsurf Data Cleaner
==============================================

This script tests the functionality of the data cleaner tools
without actually modifying any real application data.

Author: AI Assistant
Version: 1.0.0
"""

import os
import sys
import json
import sqlite3
import tempfile
import shutil
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from cursor_windsurf_cleaner import DataCleaner
    from advanced_cleaner import AdvancedDataCleaner
except ImportError as e:
    print(f"❌ Could not import cleaner modules: {e}")
    print("Please ensure cursor_windsurf_cleaner.py and advanced_cleaner.py are in the same directory")
    sys.exit(1)

class TestDataCleaner(unittest.TestCase):
    """Test cases for the basic data cleaner."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.cleaner = DataCleaner()
        
    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_backup_directory_creation(self):
        """Test that backup directory is created."""
        self.assertTrue(self.cleaner.backup_base_dir.exists())
        self.assertTrue(self.cleaner.backup_base_dir.is_dir())
    
    def test_os_detection(self):
        """Test OS detection."""
        self.assertIn(self.cleaner.os_type, ['windows', 'darwin', 'linux'])
    
    def test_app_data_discovery(self):
        """Test application data path discovery."""
        paths = self.cleaner.app_data_paths
        self.assertIsInstance(paths, dict)
        self.assertIn('cursor', paths)
        self.assertIn('windsurf', paths)
    
    def test_create_test_database(self):
        """Test creating and modifying a test SQLite database."""
        # Create a test database
        test_db = self.test_dir / "test.vscdb"
        
        conn = sqlite3.connect(str(test_db))
        cursor = conn.cursor()
        
        # Create ItemTable like VS Code
        cursor.execute("""
            CREATE TABLE ItemTable (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        # Insert test data
        cursor.execute("INSERT INTO ItemTable (key, value) VALUES (?, ?)", 
                      ("machineId", "test-machine-id-123"))
        cursor.execute("INSERT INTO ItemTable (key, value) VALUES (?, ?)", 
                      ("sessionId", "test-session-id-456"))
        cursor.execute("INSERT INTO ItemTable (key, value) VALUES (?, ?)", 
                      ("authToken", "test-auth-token-789"))
        
        conn.commit()
        conn.close()
        
        # Test the modification function
        success = self.cleaner._modify_sqlite_telemetry(test_db, "test_app")
        self.assertTrue(success)
        
        # Verify changes
        conn = sqlite3.connect(str(test_db))
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM ItemTable WHERE key = 'machineId'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertNotEqual(result[0], "test-machine-id-123")  # Should be changed
        
        cursor.execute("SELECT value FROM ItemTable WHERE key = 'authToken'")
        result = cursor.fetchone()
        self.assertIsNone(result)  # Should be deleted
        
        conn.close()
    
    def test_json_modification(self):
        """Test JSON file modification."""
        # Create test JSON file
        test_json = self.test_dir / "test.json"
        test_data = {
            "machineId": "test-machine-id",
            "sessionId": "test-session-id",
            "authToken": "test-auth-token",
            "otherData": "should-remain"
        }
        
        with open(test_json, 'w') as f:
            json.dump(test_data, f)
        
        # Test modification
        success = self.cleaner._modify_json_telemetry(test_json, "test_app")
        self.assertTrue(success)
        
        # Verify changes
        with open(test_json, 'r') as f:
            modified_data = json.load(f)
        
        self.assertNotEqual(modified_data.get("machineId"), "test-machine-id")
        self.assertNotIn("authToken", modified_data)
        self.assertEqual(modified_data.get("otherData"), "should-remain")


class TestAdvancedDataCleaner(unittest.TestCase):
    """Test cases for the advanced data cleaner."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Create test config
        self.test_config = {
            "cleaning_options": {
                "telemetry_keys": ["machineId", "deviceId"],
                "session_keys": ["authToken", "sessionId"],
                "database_keywords": ["test", "account"],
                "cache_directories": ["Cache", "TestCache"],
                "database_files": ["test.vscdb"],
                "cache_table_patterns": ["cache", "temp"]
            },
            "backup_options": {
                "enabled": True,
                "compression": False,
                "retention_days": 30
            },
            "safety_options": {
                "require_confirmation": False,
                "check_running_processes": False,
                "create_restore_script": True
            }
        }
        
        # Create test config file
        self.config_file = self.test_dir / "test_config.json"
        with open(self.config_file, 'w') as f:
            json.dump(self.test_config, f)
        
        self.cleaner = AdvancedDataCleaner(str(self.config_file))
        
    def tearDown(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_config_loading(self):
        """Test configuration loading."""
        self.assertEqual(
            self.cleaner.config["cleaning_options"]["telemetry_keys"],
            ["machineId", "deviceId"]
        )
    
    def test_backup_creation(self):
        """Test backup creation."""
        # Create test file
        test_file = self.test_dir / "test.txt"
        test_file.write_text("test content")
        
        # Create backup
        backup_path = self.cleaner._create_backup(test_file, "test_backup")
        
        self.assertIsNotNone(backup_path)
        self.assertTrue(backup_path.exists())
    
    @patch('subprocess.run')
    def test_process_detection(self, mock_subprocess):
        """Test process detection."""
        # Mock subprocess to return no running processes
        mock_subprocess.return_value.stdout = ""
        mock_subprocess.return_value.returncode = 0
        
        result = self.cleaner._is_app_running("cursor")
        self.assertFalse(result)


def run_discovery_test():
    """Run a discovery test to see what applications are found."""
    print("\n🔍 Running Application Discovery Test")
    print("=" * 50)
    
    try:
        cleaner = DataCleaner()
        cleaner.discover_and_report()
        print("✅ Basic discovery test completed successfully")
    except Exception as e:
        print(f"❌ Basic discovery test failed: {e}")
    
    try:
        advanced_cleaner = AdvancedDataCleaner()
        advanced_cleaner.discover_and_report_advanced()
        print("✅ Advanced discovery test completed successfully")
    except Exception as e:
        print(f"❌ Advanced discovery test failed: {e}")


def run_configuration_test():
    """Test configuration file loading."""
    print("\n⚙️ Running Configuration Test")
    print("=" * 40)
    
    config_file = "cleaner_config.json"
    
    if not os.path.exists(config_file):
        print(f"⚠️  Configuration file {config_file} not found")
        return
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print("✅ Configuration file loaded successfully")
        print(f"📋 Found {len(config.get('applications', {}))} application configurations")
        
        for app_name in config.get('applications', {}):
            print(f"  • {app_name}")
        
        # Test advanced cleaner with config
        cleaner = AdvancedDataCleaner(config_file)
        print("✅ Advanced cleaner initialized with configuration")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")


def main():
    """Main test runner."""
    print("🧪 Cursor & Windsurf Data Cleaner Test Suite")
    print("=" * 50)
    
    # Check if we can import the modules
    try:
        import cursor_windsurf_cleaner
        import advanced_cleaner
        print("✅ Successfully imported cleaner modules")
    except ImportError as e:
        print(f"❌ Failed to import modules: {e}")
        return 1
    
    # Run discovery test
    run_discovery_test()
    
    # Run configuration test
    run_configuration_test()
    
    # Run unit tests
    print("\n🧪 Running Unit Tests")
    print("=" * 30)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDataCleaner))
    suite.addTests(loader.loadTestsFromTestCase(TestAdvancedDataCleaner))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n✅ All tests passed! The cleaner tools appear to be working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
