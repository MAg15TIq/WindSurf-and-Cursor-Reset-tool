# 🚀 Quick Usage Guide - Free Cursor & Windsurf Data Cleaner

## 🎯 What This Tool Does

This tool helps you **reset your Cursor and Windsurf applications** to allow unlimited logins with different accounts by:

1. **Resetting machine/device IDs** - Makes apps think they're on a new computer
2. **Clearing account data** - Removes cached login information and session data  
3. **Cleaning workspace cache** - Removes project-specific cached data
4. **Creating safe backups** - All original data is backed up before modification

## ⚡ Quick Start (3 Steps)

### Step 1: Close Applications
**IMPORTANT:** Close Cursor and Windsurf completely before running the tool.

### Step 2: Run the Tool

**Windows:**
```cmd
# Double-click this file or run in command prompt:
run_cleaner.bat
```

**Mac/Linux:**
```bash
# Run in terminal:
./run_cleaner.sh
```

**Direct Python (any OS):**
```bash
# Basic version:
python cursor_windsurf_cleaner.py

# Advanced version with more options:
python advanced_cleaner.py
```

### Step 3: Follow the Prompts
- The tool will detect your applications automatically
- Choose which app to clean (Cursor, Windsurf, or both)
- Confirm the operation when prompted
- Wait for completion

## 🔍 What to Expect

### During Cleaning:
```
🧹 Starting cleanup for Cursor...
✅ Created backup: /home/user/CursorWindsurf_Backups/cursor_telemetry_20240614_120000
🔄 Updated machineId in state.vscdb
🗑️ Cleared 15 records from cache table
📁 Cleaned storage directory: IndexedDB (2.3 MB freed)
✅ Successfully cleaned Cursor data
```

### After Cleaning:
- Your applications will start fresh (like first install)
- You can log in with any account
- All your backups are saved in your home directory
- A restore script is created for easy recovery

## 🛠️ Advanced Options

### Discovery Mode (See What's Found):
```bash
python advanced_cleaner.py --discover
```

### Clean Specific App:
```bash
python advanced_cleaner.py --clean cursor
python advanced_cleaner.py --clean windsurf
```

### Clean All Without Prompts:
```bash
python advanced_cleaner.py --clean-all --no-confirm
```

## 📁 File Locations

### Where Apps Store Data:

**Windows:**
- Cursor: `%APPDATA%\Cursor`
- Windsurf: `%APPDATA%\Windsurf` or `%APPDATA%\Codeium\Windsurf`

**Mac:**
- Cursor: `~/Library/Application Support/Cursor`
- Windsurf: `~/Library/Application Support/Windsurf`

**Linux:**
- Cursor: `~/.config/Cursor`
- Windsurf: `~/.config/Windsurf`

### Where Backups Are Saved:
- Windows: `C:\Users\YourName\CursorWindsurf_*_Backups\`
- Mac/Linux: `~/CursorWindsurf_*_Backups/`

## 🔧 Troubleshooting

### "Application not found"
- Make sure Cursor/Windsurf is installed
- Try running discovery mode: `python advanced_cleaner.py --discover`

### "Permission denied"
- Run as administrator (Windows) or with sudo (Mac/Linux)
- Make sure the applications are completely closed

### "Application is running"
- Close Cursor and Windsurf completely
- Check Task Manager (Windows) or Activity Monitor (Mac) for background processes
- Wait 10 seconds and try again

### "Python not found"
- Install Python 3.7+ from python.org
- Make sure Python is added to your system PATH

## 🔄 How to Restore (If Needed)

### Option 1: Use Generated Restore Script
```bash
# Look for files like this in your backup directory:
python restore_cursor_20240614_120000.py
```

### Option 2: Manual Restore
1. Go to your backup directory (shown after cleaning)
2. Copy the backed-up files to their original locations
3. Restart the applications

## ⚠️ Important Notes

- **Always backup your work** before using this tool
- **Close applications** before running the cleaner
- **Test with non-critical accounts** first
- **Use responsibly** and in accordance with application terms of service

## 🆘 Need Help?

1. **Check the log files** for detailed error information:
   - `cursor_windsurf_cleaner.log`
   - `advanced_cleaner.log`

2. **Run the test script** to verify everything works:
   ```bash
   python test_cleaner.py
   ```

3. **Try discovery mode** to see what's detected:
   ```bash
   python advanced_cleaner.py --discover
   ```

## 🎉 Success Indicators

You'll know it worked when:
- ✅ The tool reports "Successfully cleaned [app] data"
- ✅ Backups are created in your home directory
- ✅ The application starts like a fresh installation
- ✅ You can log in with any account without restrictions

---

**Remember: This tool only modifies local data on your computer. It doesn't affect any online accounts or services.**
