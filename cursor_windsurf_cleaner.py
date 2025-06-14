#!/usr/bin/env python3
"""
Free Cursor & Windsurf Data Cleaner
===================================

A comprehensive tool to clean user data from Cursor and Windsurf applications,
allowing unlimited logins with different accounts by resetting telemetry IDs,
clearing cached data, and removing account-specific information.

Author: AI Assistant
Version: 1.0.0
License: MIT

IMPORTANT: Use this tool responsibly and in accordance with application terms of service.
Always backup your data before running this tool.
"""

import os
import sys
import json
import sqlite3
import shutil
import uuid
import platform
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cursor_windsurf_cleaner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DataCleaner:
    """Main class for cleaning Cursor and Windsurf application data."""
    
    def __init__(self):
        self.os_type = platform.system().lower()
        self.backup_base_dir = self._get_backup_directory()
        self.app_data_paths = self._discover_app_data_paths()
        
    def _get_backup_directory(self) -> Path:
        """Create and return the backup directory path."""
        home_dir = Path.home()
        backup_dir = home_dir / "CursorWindsurf_Cleaner_Backups"
        backup_dir.mkdir(exist_ok=True)
        return backup_dir
    
    def _discover_app_data_paths(self) -> Dict[str, Optional[Path]]:
        """Discover data paths for Cursor and Windsurf applications."""
        paths = {"cursor": None, "windsurf": None}
        
        if self.os_type == "windows":
            appdata = Path(os.environ.get('APPDATA', ''))
            localappdata = Path(os.environ.get('LOCALAPPDATA', ''))
            
            # Cursor paths
            cursor_paths = [
                appdata / "Cursor",
                localappdata / "Cursor",
                appdata / "cursor-ai",
                localappdata / "cursor-ai"
            ]
            
            # Windsurf paths (common locations)
            windsurf_paths = [
                appdata / "Windsurf",
                localappdata / "Windsurf",
                appdata / "windsurf-ai",
                localappdata / "windsurf-ai",
                appdata / "Codeium" / "Windsurf",
                localappdata / "Codeium" / "Windsurf"
            ]
            
        elif self.os_type == "darwin":  # macOS
            app_support = Path.home() / "Library" / "Application Support"
            
            cursor_paths = [
                app_support / "Cursor",
                app_support / "cursor-ai"
            ]
            
            windsurf_paths = [
                app_support / "Windsurf",
                app_support / "windsurf-ai",
                app_support / "Codeium" / "Windsurf"
            ]
            
        else:  # Linux
            config_dir = Path.home() / ".config"
            
            cursor_paths = [
                config_dir / "Cursor",
                config_dir / "cursor-ai"
            ]
            
            windsurf_paths = [
                config_dir / "Windsurf",
                config_dir / "windsurf-ai",
                config_dir / "Codeium" / "Windsurf"
            ]
        
        # Find existing paths
        for path in cursor_paths:
            if path.exists():
                paths["cursor"] = path
                break
                
        for path in windsurf_paths:
            if path.exists():
                paths["windsurf"] = path
                break
        
        return paths
    
    def _is_app_running(self, app_name: str) -> bool:
        """Check if the specified application is currently running."""
        try:
            if self.os_type == "windows":
                result = subprocess.run(
                    ["tasklist", "/FI", f"IMAGENAME eq {app_name}.exe"],
                    capture_output=True, text=True
                )
                return app_name.lower() in result.stdout.lower()
            else:
                result = subprocess.run(
                    ["pgrep", "-i", app_name],
                    capture_output=True, text=True
                )
                return bool(result.stdout.strip())
        except Exception as e:
            logger.warning(f"Could not check if {app_name} is running: {e}")
            return False
    
    def _create_backup(self, source_path: Path, backup_name: str) -> Optional[Path]:
        """Create a backup of the specified path."""
        if not source_path.exists():
            logger.warning(f"Source path does not exist: {source_path}")
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_base_dir / f"{backup_name}_{timestamp}"
        
        try:
            if source_path.is_file():
                shutil.copy2(source_path, backup_path)
            else:
                shutil.copytree(source_path, backup_path)
            
            logger.info(f"Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create backup of {source_path}: {e}")
            return None

    def _modify_telemetry_ids(self, app_path: Path, app_name: str) -> bool:
        """Modify telemetry and machine IDs for the specified application."""
        logger.info(f"Modifying telemetry IDs for {app_name}")

        # Common database files that store telemetry data
        db_files = [
            app_path / "User" / "globalStorage" / "state.vscdb",
            app_path / "User" / "state.vscdb",
            app_path / "state.vscdb",
            app_path / "storage.json"
        ]

        success = True

        for db_file in db_files:
            if not db_file.exists():
                continue

            # Create backup
            backup = self._create_backup(db_file, f"{app_name}_telemetry_db")
            if not backup:
                continue

            try:
                if db_file.suffix == '.vscdb':
                    success &= self._modify_sqlite_telemetry(db_file, app_name)
                elif db_file.suffix == '.json':
                    success &= self._modify_json_telemetry(db_file, app_name)
            except Exception as e:
                logger.error(f"Failed to modify {db_file}: {e}")
                success = False

        return success

    def _modify_sqlite_telemetry(self, db_path: Path, app_name: str) -> bool:
        """Modify telemetry IDs in SQLite database."""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Generate new IDs
            new_machine_id = str(uuid.uuid4())
            new_telemetry_id = str(uuid.uuid4())
            new_session_id = str(uuid.uuid4())

            # Common telemetry keys to update
            telemetry_keys = [
                'machineId',
                'telemetry.machineId',
                'telemetryMachineId',
                'deviceId',
                'telemetry.deviceId',
                'lastSessionId',
                'sessionId',
                'installationId',
                'sqmUserId',
                'sqmMachineId'
            ]

            # Try to update in ItemTable (common in VS Code-based apps)
            for key in telemetry_keys:
                try:
                    if 'machineId' in key.lower() or 'deviceId' in key.lower():
                        cursor.execute("UPDATE ItemTable SET value = ? WHERE key = ?", (new_machine_id, key))
                    elif 'sessionId' in key.lower():
                        cursor.execute("UPDATE ItemTable SET value = ? WHERE key = ?", (new_session_id, key))
                    else:
                        cursor.execute("UPDATE ItemTable SET value = ? WHERE key = ?", (new_telemetry_id, key))

                    if cursor.rowcount > 0:
                        logger.info(f"Updated {key} in {app_name} database")
                except sqlite3.Error:
                    pass  # Key might not exist, which is fine

            # Clear session-related data
            session_keys = [
                'lastSessionDate',
                'sessionStartTime',
                'userSession',
                'authToken',
                'accessToken',
                'refreshToken'
            ]

            for key in session_keys:
                try:
                    cursor.execute("DELETE FROM ItemTable WHERE key = ?", (key,))
                    if cursor.rowcount > 0:
                        logger.info(f"Cleared {key} from {app_name} database")
                except sqlite3.Error:
                    pass

            conn.commit()
            conn.execute("VACUUM")  # Reclaim space
            conn.close()

            logger.info(f"Successfully modified telemetry IDs in {db_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to modify SQLite telemetry in {db_path}: {e}")
            return False

    def _modify_json_telemetry(self, json_path: Path, app_name: str) -> bool:
        """Modify telemetry IDs in JSON configuration files."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Generate new IDs
            new_machine_id = str(uuid.uuid4())
            new_telemetry_id = str(uuid.uuid4())

            # Keys that might contain telemetry data
            telemetry_keys = [
                'machineId', 'telemetry.machineId', 'deviceId', 'sessionId',
                'installationId', 'sqmUserId', 'sqmMachineId'
            ]

            modified = False
            for key in telemetry_keys:
                if key in data:
                    if 'machineId' in key.lower() or 'deviceId' in key.lower():
                        data[key] = new_machine_id
                    else:
                        data[key] = new_telemetry_id
                    modified = True
                    logger.info(f"Updated {key} in {json_path}")

            # Remove session data
            session_keys = ['lastSessionDate', 'sessionStartTime', 'authToken', 'accessToken']
            for key in session_keys:
                if key in data:
                    del data[key]
                    modified = True
                    logger.info(f"Removed {key} from {json_path}")

            if modified:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"Successfully modified JSON telemetry in {json_path}")

            return True

        except Exception as e:
            logger.error(f"Failed to modify JSON telemetry in {json_path}: {e}")
            return False

    def _clean_databases(self, app_path: Path, app_name: str, keywords: List[str] = None) -> bool:
        """Clean account-specific data from application databases."""
        logger.info(f"Cleaning databases for {app_name}")

        if keywords is None:
            keywords = ['augment', 'account', 'session', 'user', 'login', 'auth', 'token']

        # Find all database files
        db_patterns = ['*.db', '*.sqlite', '*.sqlite3', '*.vscdb']
        db_files = []

        for pattern in db_patterns:
            db_files.extend(app_path.rglob(pattern))

        success = True

        for db_file in db_files:
            # Skip if it's a backup file
            if 'backup' in str(db_file).lower() or '.bak' in str(db_file):
                continue

            # Create backup
            backup = self._create_backup(db_file, f"{app_name}_database")
            if not backup:
                continue

            try:
                success &= self._clean_sqlite_database(db_file, keywords, app_name)
            except Exception as e:
                logger.error(f"Failed to clean database {db_file}: {e}")
                success = False

        return success

    def _clean_sqlite_database(self, db_path: Path, keywords: List[str], app_name: str) -> bool:
        """Clean specific records from SQLite database based on keywords."""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            cleaned_records = 0

            for table in tables:
                try:
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = [row[1] for row in cursor.fetchall()]

                    # Look for text/varchar columns that might contain keywords
                    text_columns = []
                    for col in columns:
                        cursor.execute(f"SELECT typeof({col}) FROM {table} LIMIT 1")
                        result = cursor.fetchone()
                        if result and ('text' in str(result[0]).lower() or 'varchar' in str(result[0]).lower()):
                            text_columns.append(col)

                    # Clean records containing keywords
                    for keyword in keywords:
                        for col in text_columns:
                            try:
                                cursor.execute(f"DELETE FROM {table} WHERE {col} LIKE ?", (f'%{keyword}%',))
                                deleted = cursor.rowcount
                                if deleted > 0:
                                    cleaned_records += deleted
                                    logger.info(f"Deleted {deleted} records from {table}.{col} containing '{keyword}'")
                            except sqlite3.Error as e:
                                logger.debug(f"Could not clean {table}.{col}: {e}")

                    # Clear common cache/session tables entirely
                    cache_table_patterns = [
                        'cache', 'session', 'temp', 'log', 'history', 'recent'
                    ]

                    for pattern in cache_table_patterns:
                        if pattern in table.lower():
                            try:
                                cursor.execute(f"DELETE FROM {table}")
                                deleted = cursor.rowcount
                                if deleted > 0:
                                    cleaned_records += deleted
                                    logger.info(f"Cleared {deleted} records from cache table {table}")
                            except sqlite3.Error as e:
                                logger.debug(f"Could not clear table {table}: {e}")
                            break

                except sqlite3.Error as e:
                    logger.debug(f"Could not process table {table}: {e}")
                    continue

            if cleaned_records > 0:
                conn.commit()
                conn.execute("VACUUM")  # Reclaim space
                logger.info(f"Cleaned {cleaned_records} records from {db_path}")

            conn.close()
            return True

        except Exception as e:
            logger.error(f"Failed to clean SQLite database {db_path}: {e}")
            return False

    def _clean_workspace_storage(self, app_path: Path, app_name: str) -> bool:
        """Clean workspace storage and cache directories."""
        logger.info(f"Cleaning workspace storage for {app_name}")

        # Common cache and storage directories
        storage_dirs = [
            'IndexedDB',
            'Local Storage',
            'Cache',
            'Code Cache',
            'GPUCache',
            'blob_storage',
            'logs',
            'User/workspaceStorage',
            'User/History',
            'User/logs',
            'CachedData',
            'CachedExtensions'
        ]

        success = True

        for dir_name in storage_dirs:
            dir_path = app_path / dir_name
            if not dir_path.exists():
                continue

            # Create backup
            backup = self._create_backup(dir_path, f"{app_name}_{dir_name.replace('/', '_')}")
            if not backup:
                continue

            try:
                # Clear contents but keep the directory structure
                self._clear_directory_contents(dir_path)
                logger.info(f"Cleaned storage directory: {dir_path}")
            except Exception as e:
                logger.error(f"Failed to clean storage directory {dir_path}: {e}")
                success = False

        return success

    def _clear_directory_contents(self, directory: Path) -> None:
        """Clear all contents of a directory while preserving the directory itself."""
        for item in directory.iterdir():
            try:
                if item.is_file() or item.is_symlink():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except Exception as e:
                logger.warning(f"Could not remove {item}: {e}")

    def clean_application(self, app_name: str, keywords: List[str] = None) -> bool:
        """Clean all data for the specified application."""
        app_path = self.app_data_paths.get(app_name.lower())

        if not app_path:
            logger.error(f"{app_name} data directory not found")
            return False

        logger.info(f"Starting cleanup for {app_name} at {app_path}")

        # Check if application is running
        if self._is_app_running(app_name):
            logger.error(f"{app_name} is currently running. Please close it before running the cleaner.")
            return False

        success = True

        # Phase 1: Modify telemetry IDs
        try:
            success &= self._modify_telemetry_ids(app_path, app_name)
        except Exception as e:
            logger.error(f"Failed to modify telemetry IDs for {app_name}: {e}")
            success = False

        # Phase 2: Clean databases
        try:
            success &= self._clean_databases(app_path, app_name, keywords)
        except Exception as e:
            logger.error(f"Failed to clean databases for {app_name}: {e}")
            success = False

        # Phase 3: Clean workspace storage
        try:
            success &= self._clean_workspace_storage(app_path, app_name)
        except Exception as e:
            logger.error(f"Failed to clean workspace storage for {app_name}: {e}")
            success = False

        if success:
            logger.info(f"Successfully cleaned {app_name} data")
        else:
            logger.warning(f"Cleanup for {app_name} completed with some errors")

        return success

    def discover_and_report(self) -> None:
        """Discover and report application data locations."""
        logger.info("=== Application Data Discovery ===")

        for app_name, app_path in self.app_data_paths.items():
            if app_path:
                logger.info(f"{app_name.capitalize()}: Found at {app_path}")

                # Check if app is running
                if self._is_app_running(app_name):
                    logger.warning(f"  ⚠️  {app_name.capitalize()} is currently running")

                # Report key files/directories
                key_locations = [
                    "User/globalStorage/state.vscdb",
                    "User/workspaceStorage",
                    "IndexedDB",
                    "Local Storage",
                    "Cache"
                ]

                for location in key_locations:
                    path = app_path / location
                    if path.exists():
                        size = self._get_directory_size(path) if path.is_dir() else path.stat().st_size
                        logger.info(f"  📁 {location}: {self._format_size(size)}")
            else:
                logger.info(f"{app_name.capitalize()}: Not found")

        logger.info(f"Backup directory: {self.backup_base_dir}")

    def _get_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory contents."""
        total_size = 0
        try:
            for item in directory.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
        except Exception:
            pass
        return total_size

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


def main():
    """Main CLI interface."""
    print("🧹 Free Cursor & Windsurf Data Cleaner v1.0.0")
    print("=" * 50)
    print("⚠️  IMPORTANT: This tool will modify application data.")
    print("   Always backup your important work before proceeding.")
    print("   Use this tool responsibly and in accordance with application ToS.")
    print()

    cleaner = DataCleaner()

    # Discovery phase
    cleaner.discover_and_report()
    print()

    # Get user confirmation
    print("Available applications to clean:")
    available_apps = [name for name, path in cleaner.app_data_paths.items() if path]

    if not available_apps:
        print("❌ No supported applications found.")
        return

    for i, app in enumerate(available_apps, 1):
        print(f"  {i}. {app.capitalize()}")

    print("  0. Exit")
    print()

    try:
        choice = input("Select application to clean (number): ").strip()

        if choice == "0":
            print("Exiting...")
            return

        choice_idx = int(choice) - 1
        if choice_idx < 0 or choice_idx >= len(available_apps):
            print("❌ Invalid choice.")
            return

        selected_app = available_apps[choice_idx]

        # Final confirmation
        print(f"\n⚠️  You are about to clean ALL data for {selected_app.capitalize()}.")
        print("This will:")
        print("  • Reset machine/device IDs")
        print("  • Clear account-specific database records")
        print("  • Remove cached workspace data")
        print("  • Create backups of all modified files")
        print()

        confirm = input("Are you sure you want to proceed? (type 'yes' to confirm): ").strip().lower()

        if confirm != "yes":
            print("Operation cancelled.")
            return

        # Perform cleaning
        print(f"\n🧹 Starting cleanup for {selected_app.capitalize()}...")
        success = cleaner.clean_application(selected_app)

        if success:
            print(f"\n✅ Successfully cleaned {selected_app.capitalize()} data!")
            print(f"📁 Backups saved to: {cleaner.backup_base_dir}")
            print("\nYou can now launch the application and log in with a different account.")
        else:
            print(f"\n⚠️  Cleanup completed with some errors. Check the log file for details.")
            print(f"📁 Backups saved to: {cleaner.backup_base_dir}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
