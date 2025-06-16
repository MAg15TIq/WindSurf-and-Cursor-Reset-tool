#!/usr/bin/env python3
"""
Advanced Cursor & Windsurf Data Cleaner
=======================================

Enhanced version with configuration file support, better error handling,
and additional safety features.

Author: AI Assistant
Version: 2.0.0
License: MIT
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
import zipfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import argparse

class AdvancedDataCleaner:
    """Advanced data cleaner with configuration support."""
    
    def __init__(self, config_path: str = "cleaner_config.json"):
        self.config = self._load_config(config_path)
        self.os_type = platform.system().lower()
        self.backup_base_dir = self._get_backup_directory()
        self.app_data_paths = self._discover_app_data_paths()
        self._setup_logging()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Configuration file {config_path} not found. Using defaults.")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing configuration file: {e}")
            sys.exit(1)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "cleaning_options": {
                "telemetry_keys": ["machineId", "deviceId", "sessionId"],
                "session_keys": ["authToken", "accessToken", "userSession"],
                "database_keywords": ["augment", "account", "session", "user"],
                "cache_directories": ["Cache", "IndexedDB", "Local Storage"],
                "database_files": ["state.vscdb", "storage.json"],
                "cache_table_patterns": ["cache", "session", "temp", "log"]
            },
            "backup_options": {
                "enabled": True,
                "compression": False,
                "retention_days": 30
            },
            "safety_options": {
                "require_confirmation": True,
                "check_running_processes": True,
                "create_restore_script": True
            }
        }
    
    def _setup_logging(self) -> None:
        """Setup logging based on configuration."""
        log_config = self.config.get("logging", {})
        log_level = getattr(logging, log_config.get("level", "INFO"))
        log_file = log_config.get("file", "advanced_cleaner.log")
        
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.logger.setLevel(logging.INFO)

        # Ensure handlers are not duplicated if called multiple times
        if not self.logger.handlers:
            # File handler
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.INFO)
            fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(fh_formatter)
            self.logger.addHandler(fh)

            # Console handler
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(logging.INFO)
            # Set encoding for the console handler
            if sys.stdout.encoding != 'UTF-8':
                ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
                ch.stream = open(ch.stream.fileno(), 'w', encoding='utf-8', closefd=False)
            ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            ch.setFormatter(ch_formatter)
            self.logger.addHandler(ch)
    
    def _get_backup_directory(self) -> Path:
        """Create and return the backup directory path."""
        home_dir = Path.home()
        backup_dir = home_dir / "CursorWindsurf_Advanced_Backups"
        backup_dir.mkdir(exist_ok=True)
        return backup_dir
    
    def _discover_app_data_paths(self) -> Dict[str, Optional[Path]]:
        """Discover data paths for applications using configuration."""
        paths = {}
        
        apps_config = self.config.get("applications", {})
        
        for app_name, app_config in apps_config.items():
            paths[app_name] = None
            
            app_paths = app_config.get("data_paths", {}).get(self.os_type, [])
            
            for path_template in app_paths:
                # Expand environment variables and user home
                expanded_path = os.path.expandvars(os.path.expanduser(path_template))
                path = Path(expanded_path)
                
                if path.exists():
                    paths[app_name] = path
                    break
        
        return paths
    
    def _is_app_running(self, app_name: str) -> bool:
        """Check if the specified application is currently running."""
        apps_config = self.config.get("applications", {})
        app_config = apps_config.get(app_name, {})
        process_names = app_config.get("process_names", [app_name])
        
        try:
            if self.os_type == "windows":
                for process_name in process_names:
                    result = subprocess.run(
                        ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
                        capture_output=True, text=True
                    )
                    if process_name.lower() in result.stdout.lower():
                        return True
            else:
                for process_name in process_names:
                    result = subprocess.run(
                        ["pgrep", "-i", process_name],
                        capture_output=True, text=True
                    )
                    if result.stdout.strip():
                        return True
        except Exception as e:
            self.logger.warning(f"Could not check if {app_name} is running: {e}")
        
        return False
    
    def _create_backup(self, source_path: Path, backup_name: str) -> Optional[Path]:
        """Create a backup with optional compression."""
        if not source_path.exists():
            self.logger.warning(f"Source path does not exist: {source_path}")
            return None
        
        backup_options = self.config.get("backup_options", {})
        if not backup_options.get("enabled", True):
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            if backup_options.get("compression", False):
                backup_path = self.backup_base_dir / f"{backup_name}_{timestamp}.zip"
                with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    if source_path.is_file():
                        zipf.write(source_path, source_path.name)
                    else:
                        for file_path in source_path.rglob('*'):
                            if file_path.is_file():
                                arcname = file_path.relative_to(source_path.parent)
                                zipf.write(file_path, arcname)
            else:
                backup_path = self.backup_base_dir / f"{backup_name}_{timestamp}"
                if source_path.is_file():
                    shutil.copy2(source_path, backup_path)
                else:
                    shutil.copytree(source_path, backup_path)
            
            self.logger.info(f"Created backup: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Failed to create backup of {source_path}: {e}")
            return None
    
    def _clean_old_backups(self) -> None:
        """Clean old backups based on retention policy."""
        backup_options = self.config.get("backup_options", {})
        retention_days = backup_options.get("retention_days", 30)
        
        if retention_days <= 0:
            return
        
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        try:
            for backup_file in self.backup_base_dir.iterdir():
                if backup_file.stat().st_mtime < cutoff_date.timestamp():
                    if backup_file.is_file():
                        backup_file.unlink()
                    else:
                        shutil.rmtree(backup_file)
                    self.logger.info(f"Removed old backup: {backup_file}")
        except Exception as e:
            self.logger.warning(f"Error cleaning old backups: {e}")
    
    def _create_restore_script(self, app_name: str, backups: List[Path]) -> None:
        """Create a script to restore from backups."""
        safety_options = self.config.get("safety_options", {})
        if not safety_options.get("create_restore_script", True):
            return
        
        script_name = f"restore_{app_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        script_path = self.backup_base_dir / script_name
        
        script_content = f'''#!/usr/bin/env python3
"""
Restore script for {app_name} data
Generated on {datetime.now().isoformat()}
"""

import shutil
from pathlib import Path

def restore():
    """Restore {app_name} data from backups."""
    print("🔄 Restoring {app_name} data...")
    
    backups = {backups}
    app_path = Path("{self.app_data_paths.get(app_name, '')}")
    
    for backup_path in backups:
        backup = Path(backup_path)
        if backup.exists():
            print(f"Restoring from {{backup}}")
            # Add restore logic here based on backup type
        else:
            print(f"⚠️  Backup not found: {{backup}}")
    
    print("✅ Restore complete!")

if __name__ == "__main__":
    restore()
'''
        
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            script_path.chmod(0o755)  # Make executable
            self.logger.info(f"Created restore script: {script_path}")
        except Exception as e:
            self.logger.warning(f"Could not create restore script: {e}")
    
    def clean_application_advanced(self, app_name: str) -> bool:
        """Advanced cleaning with configuration support."""
        app_path = self.app_data_paths.get(app_name.lower())
        
        if not app_path:
            self.logger.error(f"{app_name} data directory not found")
            return False
        
        self.logger.info(f"Starting advanced cleanup for {app_name} at {app_path}")
        
        # Safety checks
        safety_options = self.config.get("safety_options", {})
        
        if safety_options.get("check_running_processes", True):
            if self._is_app_running(app_name):
                self.logger.error(f"{app_name} is currently running. Please close it first.")
                return False
        
        # Clean old backups first
        self._clean_old_backups()
        
        backups_created = []
        success = True
        
        try:
            # Get cleaning options from config
            cleaning_options = self.config.get("cleaning_options", {})
            
            # Phase 1: Telemetry ID modification
            telemetry_keys = cleaning_options.get("telemetry_keys", [])
            session_keys = cleaning_options.get("session_keys", [])
            
            success &= self._modify_telemetry_advanced(app_path, app_name, telemetry_keys, session_keys, backups_created)
            
            # Phase 2: Database cleaning
            db_keywords = cleaning_options.get("database_keywords", [])
            success &= self._clean_databases_advanced(app_path, app_name, db_keywords, backups_created)
            
            # Phase 3: Cache cleaning
            cache_dirs = cleaning_options.get("cache_directories", [])
            success &= self._clean_cache_advanced(app_path, app_name, cache_dirs, backups_created)
            
            # Create restore script
            if backups_created:
                self._create_restore_script(app_name, backups_created)
            
            if success:
                self.logger.info(f"✅ Successfully cleaned {app_name} data")
            else:
                self.logger.warning(f"⚠️  Cleanup for {app_name} completed with some errors")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Unexpected error during {app_name} cleanup: {e}")
            return False

    def _modify_telemetry_advanced(self, app_path: Path, app_name: str,
                                 telemetry_keys: List[str], session_keys: List[str],
                                 backups_created: List[Path]) -> bool:
        """Advanced telemetry modification with configurable keys."""
        self.logger.info(f"Modifying telemetry IDs for {app_name}")

        cleaning_options = self.config.get("cleaning_options", {})
        db_files = cleaning_options.get("database_files", ["state.vscdb", "storage.json"])

        success = True

        for db_file_name in db_files:
            # Check common locations
            possible_paths = [
                app_path / "User" / "globalStorage" / db_file_name,
                app_path / "User" / db_file_name,
                app_path / db_file_name
            ]

            for db_path in possible_paths:
                if not db_path.exists():
                    continue

                # Create backup
                backup = self._create_backup(db_path, f"{app_name}_telemetry_{db_file_name}")
                if backup:
                    backups_created.append(backup)

                try:
                    if db_path.suffix in ['.vscdb', '.db', '.sqlite', '.sqlite3']:
                        success &= self._modify_sqlite_telemetry_advanced(
                            db_path, telemetry_keys, session_keys
                        )
                    elif db_path.suffix == '.json':
                        success &= self._modify_json_telemetry_advanced(
                            db_path, telemetry_keys, session_keys
                        )
                except Exception as e:
                    self.logger.error(f"Failed to modify {db_path}: {e}")
                    success = False

        return success

    def _modify_sqlite_telemetry_advanced(self, db_path: Path,
                                        telemetry_keys: List[str],
                                        session_keys: List[str]) -> bool:
        """Advanced SQLite telemetry modification."""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Generate new IDs
            new_machine_id = str(uuid.uuid4())
            new_session_id = str(uuid.uuid4())

            # Update telemetry keys
            for key in telemetry_keys:
                try:
                    if 'session' in key.lower():
                        cursor.execute("UPDATE ItemTable SET value = ? WHERE key = ?", (new_session_id, key))
                    else:
                        cursor.execute("UPDATE ItemTable SET value = ? WHERE key = ?", (new_machine_id, key))

                    if cursor.rowcount > 0:
                        self.logger.info(f"Updated {key} in {db_path.name}")
                except sqlite3.Error:
                    pass

            # Clear session keys
            for key in session_keys:
                try:
                    cursor.execute("DELETE FROM ItemTable WHERE key = ?", (key,))
                    if cursor.rowcount > 0:
                        self.logger.info(f"Cleared {key} from {db_path.name}")
                except sqlite3.Error:
                    pass

            conn.commit()
            conn.execute("VACUUM")
            conn.close()

            return True

        except Exception as e:
            self.logger.error(f"Failed to modify SQLite telemetry in {db_path}: {e}")
            return False

    def _modify_json_telemetry_advanced(self, json_path: Path,
                                      telemetry_keys: List[str],
                                      session_keys: List[str]) -> bool:
        """Advanced JSON telemetry modification."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            new_machine_id = str(uuid.uuid4())
            new_session_id = str(uuid.uuid4())

            modified = False

            # Update telemetry keys
            for key in telemetry_keys:
                if key in data:
                    if 'session' in key.lower():
                        data[key] = new_session_id
                    else:
                        data[key] = new_machine_id
                    modified = True
                    self.logger.info(f"Updated {key} in {json_path.name}")

            # Remove session keys
            for key in session_keys:
                if key in data:
                    del data[key]
                    modified = True
                    self.logger.info(f"Removed {key} from {json_path.name}")

            if modified:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)

            return True

        except Exception as e:
            self.logger.error(f"Failed to modify JSON telemetry in {json_path}: {e}")
            return False

    def _clean_databases_advanced(self, app_path: Path, app_name: str,
                                keywords: List[str], backups_created: List[Path]) -> bool:
        """Advanced database cleaning with configurable keywords."""
        self.logger.info(f"Cleaning databases for {app_name}")

        # Find all database files
        db_patterns = ['*.db', '*.sqlite', '*.sqlite3', '*.vscdb']
        db_files = []

        for pattern in db_patterns:
            db_files.extend(app_path.rglob(pattern))

        success = True

        for db_file in db_files:
            if 'backup' in str(db_file).lower() or '.bak' in str(db_file):
                continue

            backup = self._create_backup(db_file, f"{app_name}_database_{db_file.name}")
            if backup:
                backups_created.append(backup)

            try:
                success &= self._clean_sqlite_advanced(db_file, keywords)
            except Exception as e:
                self.logger.error(f"Failed to clean database {db_file}: {e}")
                success = False

        return success

    def _clean_sqlite_advanced(self, db_path: Path, keywords: List[str]) -> bool:
        """Advanced SQLite cleaning with better error handling."""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            cleaned_records = 0
            cleaning_options = self.config.get("cleaning_options", {})
            cache_patterns = cleaning_options.get("cache_table_patterns", [])

            for table in tables:
                try:
                    # Clear cache tables entirely
                    for pattern in cache_patterns:
                        if pattern in table.lower():
                            cursor.execute(f"DELETE FROM {table}")
                            deleted = cursor.rowcount
                            if deleted > 0:
                                cleaned_records += deleted
                                self.logger.info(f"Cleared {deleted} records from cache table {table}")
                            break
                    else:
                        # Clean by keywords for non-cache tables
                        cursor.execute(f"PRAGMA table_info({table})")
                        columns = [row[1] for row in cursor.fetchall()]

                        for keyword in keywords:
                            for col in columns:
                                try:
                                    cursor.execute(f"DELETE FROM {table} WHERE {col} LIKE ?", (f'%{keyword}%',))
                                    deleted = cursor.rowcount
                                    if deleted > 0:
                                        cleaned_records += deleted
                                        self.logger.info(f"Deleted {deleted} records from {table}.{col} containing '{keyword}'")
                                except sqlite3.Error:
                                    pass

                except sqlite3.Error as e:
                    self.logger.debug(f"Could not process table {table}: {e}")
                    continue

            if cleaned_records > 0:
                conn.commit()
                conn.execute("VACUUM")
                self.logger.info(f"Cleaned {cleaned_records} total records from {db_path.name}")

            conn.close()
            return True

        except Exception as e:
            self.logger.error(f"Failed to clean SQLite database {db_path}: {e}")
            return False

    def _clean_cache_advanced(self, app_path: Path, app_name: str,
                            cache_dirs: List[str], backups_created: List[Path]) -> bool:
        """Advanced cache cleaning with configurable directories."""
        self.logger.info(f"Cleaning cache directories for {app_name}")

        success = True

        for dir_name in cache_dirs:
            dir_path = app_path / dir_name
            if not dir_path.exists():
                continue

            # Check size before cleaning
            size_before = self._get_directory_size(dir_path)

            backup = self._create_backup(dir_path, f"{app_name}_cache_{dir_name.replace('/', '_')}")
            if backup:
                backups_created.append(backup)

            try:
                self._clear_directory_contents(dir_path)
                self.logger.info(f"Cleaned cache directory: {dir_path} ({self._format_size(size_before)} freed)")
            except Exception as e:
                self.logger.error(f"Failed to clean cache directory {dir_path}: {e}")
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
                self.logger.warning(f"Could not remove {item}: {e}")

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

    def discover_and_report_advanced(self) -> None:
        """Advanced discovery and reporting with configuration details."""
        self.logger.info("=== Advanced Application Data Discovery ===")

        apps_config = self.config.get("applications", {})

        for app_name, app_path in self.app_data_paths.items():
            app_config = apps_config.get(app_name, {})
            display_name = app_config.get("display_name", app_name.capitalize())

            if app_path:
                self.logger.info(f"{display_name}: Found at {app_path}")

                # Check if app is running
                if self._is_app_running(app_name):
                    self.logger.warning(f"  {display_name} is currently running")
                else:
                    self.logger.info(f"  {display_name} is not running.")
                
                # Report detailed information
                cleaning_options = self.config.get("cleaning_options", {})
                cache_dirs = cleaning_options.get("cache_directories", [])

                total_cache_size = 0
                for cache_dir in cache_dirs:
                    cache_path = app_path / cache_dir
                    if cache_path.exists():
                        size = self._get_directory_size(cache_path)
                        total_cache_size += size
                        self.logger.info(f"  📁 {cache_dir}: {self._format_size(size)}")

                self.logger.info(f"  💾 Total cache size: {self._format_size(total_cache_size)}")

                # Check for database files
                db_files = cleaning_options.get("database_files", [])
                for db_file in db_files:
                    for possible_path in [
                        app_path / "User" / "globalStorage" / db_file,
                        app_path / "User" / db_file,
                        app_path / db_file
                    ]:
                        if possible_path.exists():
                            size = possible_path.stat().st_size
                            self.logger.info(f"  🗄️  {db_file}: {self._format_size(size)}")
                            break
            else:
                self.logger.info(f"{display_name}: Not found")

        self.logger.info(f"📁 Backup directory: {self.backup_base_dir}")

        # Report configuration summary
        backup_options = self.config.get("backup_options", {})
        self.logger.info(f"🔧 Backup enabled: {backup_options.get('enabled', True)}")
        self.logger.info(f"🔧 Compression: {backup_options.get('compression', False)}")
        self.logger.info(f"🔧 Retention: {backup_options.get('retention_days', 30)} days")


def main():
    """Main CLI interface for advanced cleaner."""
    parser = argparse.ArgumentParser(
        description="Advanced Cursor & Windsurf Data Cleaner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python advanced_cleaner.py --discover
  python advanced_cleaner.py --clean cursor
  python advanced_cleaner.py --clean windsurf --config custom_config.json
  python advanced_cleaner.py --clean-all --no-confirm
        """
    )

    parser.add_argument("--config", "-c", default="cleaner_config.json",
                       help="Configuration file path (default: cleaner_config.json)")
    parser.add_argument("--discover", "-d", action="store_true",
                       help="Discover and report application data locations")
    parser.add_argument("--clean", choices=["cursor", "windsurf"],
                       help="Clean specific application")
    parser.add_argument("--clean-all", action="store_true",
                       help="Clean all found applications")
    parser.add_argument("--no-confirm", action="store_true",
                       help="Skip confirmation prompts (use with caution)")
    parser.add_argument("--version", action="version", version="Advanced Cleaner v2.0.0")

    args = parser.parse_args()

    print("🧹 Advanced Cursor & Windsurf Data Cleaner v2.0.0")
    print("=" * 55)
    print("⚠️  IMPORTANT: This tool will modify application data.")
    print("   Always backup your important work before proceeding.")
    print("   Use this tool responsibly and in accordance with application ToS.")
    print()

    try:
        cleaner = AdvancedDataCleaner(args.config)
    except Exception as e:
        print(f"❌ Failed to initialize cleaner: {e}")
        return 1

    if args.discover:
        cleaner.discover_and_report_advanced()
        return 0

    # Get available applications
    available_apps = [name for name, path in cleaner.app_data_paths.items() if path]

    if not available_apps:
        print("❌ No supported applications found.")
        return 1

    apps_to_clean = []

    if args.clean:
        if args.clean in available_apps:
            apps_to_clean = [args.clean]
        else:
            print(f"❌ {args.clean} not found or not supported.")
            return 1
    elif args.clean_all:
        apps_to_clean = available_apps
    else:
        # Interactive mode
        cleaner.discover_and_report_advanced()
        print("\nAvailable applications to clean:")
        for i, app in enumerate(available_apps, 1):
            apps_config = cleaner.config.get("applications", {})
            display_name = apps_config.get(app, {}).get("display_name", app.capitalize())
            print(f"  {i}. {display_name}")
        print("  0. Exit")

        try:
            choice = input("\nSelect application to clean (number): ").strip()
            if choice == "0":
                return 0

            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_apps):
                apps_to_clean = [available_apps[choice_idx]]
            else:
                print("❌ Invalid choice.")
                return 1
        except (ValueError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return 0

    # Confirmation
    if not args.no_confirm:
        safety_options = cleaner.config.get("safety_options", {})
        if safety_options.get("require_confirmation", True):
            print(f"\n⚠️  You are about to clean data for: {', '.join(apps_to_clean)}")
            print("This will:")
            print("  • Reset machine/device IDs")
            print("  • Clear account-specific database records")
            print("  • Remove cached workspace data")
            print("  • Create backups of all modified files")

            confirm = input("\nAre you sure you want to proceed? (type 'yes' to confirm): ").strip().lower()
            if confirm != "yes":
                print("Operation cancelled.")
                return 0

    # Perform cleaning
    overall_success = True
    for app_name in apps_to_clean:
        print(f"\n🧹 Starting cleanup for {app_name}...")
        success = cleaner.clean_application_advanced(app_name)
        overall_success &= success

    if overall_success:
        print(f"\n✅ Successfully cleaned data for: {', '.join(apps_to_clean)}")
        print(f"📁 Backups saved to: {cleaner.backup_base_dir}")
        print("\nYou can now launch the applications and log in with different accounts.")
    else:
        print(f"\n⚠️  Cleanup completed with some errors. Check the log file for details.")
        print(f"📁 Backups saved to: {cleaner.backup_base_dir}")

    return 0 if overall_success else 1


if __name__ == "__main__":
    sys.exit(main())
