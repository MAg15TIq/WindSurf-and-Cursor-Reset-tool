# 🧹 Free Cursor & Windsurf Data Cleaner

*Because apparently, some AI coding assistants think you should only get to use them once per lifetime. How adorable.* 🙄

A comprehensive tool to clean user data from Cursor and Windsurf applications, allowing unlimited logins with different accounts by resetting telemetry IDs, clearing cached data, and removing account-specific information. You know, like how a normal application should work in the first place.

## ⚠️ Important Disclaimer (The Boring Legal Stuff)

**Use this tool responsibly and in accordance with application terms of service.** This tool is provided for educational purposes and to help users manage their local application data. Always backup your important work before running this tool.

*Translation: We're not responsible if you break something. But honestly, if you can't follow simple instructions, maybe coding isn't for you.* 😏

## 🚀 Features (What This Magical Tool Actually Does)

- **Cross-platform support** (Windows, macOS, Linux) - *Because we're not savages who only code on one OS*
- **Automatic application detection** - *It finds your apps faster than you can say "account limit exceeded"*
- **Safe backup system** - *Unlike some people, we actually care about your data*
- **Telemetry ID reset** - *Makes your computer look like a shiny new machine to nosy applications*
- **Database cleaning** - *Removes all traces of your previous "unauthorized" usage*
- **Cache clearing** - *Clears more cache than your browser after visiting... questionable websites*
- **Configurable cleaning options** - *Because we're fancy like that*
- **Comprehensive logging** - *So you can see exactly how we're saving your coding career*
- **Restore script generation** - *In case you want to go back to being locked out (but why would you?)*

## 📋 Requirements (The Bare Minimum You Need)

- **Python 3.7 or higher** - *If you don't have Python in 2025, we can't help you*
- **Administrative/user permissions** - *You need to actually own your computer, shocking concept*
- **Cursor and/or Windsurf applications closed** - *Yes, you have to close them. No, alt-tabbing doesn't count*
- **Basic reading comprehension** - *This one's apparently optional for most users*

## 🛠️ Installation (For Those Who Can Follow Instructions)

### Step 1: Clone This Repository (Revolutionary Concept)
```bash
git clone https://github.com/MAg15TIq/WindSurf-and-Cursor-Reset-tool.git
cd WindSurf-and-Cursor-Reset-tool
```

*Or if you're one of those people who downloads ZIP files like it's 2005:*
1. Click the green "Code" button above
2. Select "Download ZIP"
3. Extract it somewhere you'll remember (good luck with that)

### Step 2: Make Scripts Executable (Unix/Linux/macOS Only)
```bash
chmod +x run_cleaner.sh
```

*Windows users can skip this step because Windows handles permissions like a toddler handles scissors.*

## 🎯 Quick Start (The "I Just Want It to Work" Guide)

### Option 1: For Windows Users (The Easy Button)
```cmd
# Double-click run_cleaner.bat like you're opening Solitaire
run_cleaner.bat
```
*Yes, it's that simple. Even your grandmother could do it.*

### Option 2: For macOS/Linux Users (Slightly More Sophisticated)
```bash
# Run the shell script like the terminal warrior you pretend to be:
./run_cleaner.sh
```
*If this doesn't work, you probably forgot Step 2 of installation. Go back and read.*

### Option 3: For Python Purists (Show-offs Welcome)

**Basic Cleaner (For Minimalists):**
```bash
python cursor_windsurf_cleaner.py
```
*Simple, effective, gets the job done. Like a good cup of coffee.*

**Advanced Cleaner (For Control Freaks):**
```bash
# Interactive mode - holds your hand through the process
python advanced_cleaner.py

# Discovery mode - see what we found (spoiler: your apps)
python advanced_cleaner.py --discover

# Clean specific application - because you have favorites
python advanced_cleaner.py --clean cursor
python advanced_cleaner.py --clean windsurf

# Nuclear option - clean everything without asking questions
python advanced_cleaner.py --clean-all --no-confirm

# Show progress bars for large operations (default)
python advanced_cleaner.py --clean cursor

# Disable progress bars (for scripting or minimal output)
python advanced_cleaner.py --clean cursor --no-progress
```
*The last command is for people who live dangerously and don't read warnings.*

## 📖 Detailed Usage Guide (Because Apparently We Need to Explain Everything)

### Step 1: Close Applications (Rocket Science, I Know)
Before running the cleaner, ensure that Cursor and Windsurf are **completely closed**.

*This means:*
- ❌ **NOT** minimized to system tray
- ❌ **NOT** "I think I closed it"
- ❌ **NOT** running in the background like your trust issues
- ✅ **ACTUALLY CLOSED** - as in, not appearing in Task Manager

*Pro tip: If you see the application icon anywhere on your screen, it's probably still running.*

### Step 2: Run Discovery (The "What Do You Have?" Phase)
```bash
python advanced_cleaner.py --discover
```

*This command will:*
- 🔍 **Scan your system** for Cursor and Windsurf installations
- 📊 **Show cache sizes** (prepare to be shocked at how much space they waste)
- 📁 **Display data locations** (so you know we're not just making stuff up)
- 🎯 **Confirm what can be cleaned** (spoiler: probably everything)

*Example output you might see:*
```
Cursor AI: Found at C:\Users\YourName\AppData\Roaming\Cursor
  📁 Cache: 83.3 MB (yes, that much)
  🗄️ Database: 107.6 MB (they really like storing stuff)
```

### Step 3: Choose Your Weapon (Cleaning Method)

**Option A: The Lazy Way (Recommended for Most Humans)**
- Double-click `run_cleaner.bat` (Windows) or run `./run_cleaner.sh` (Mac/Linux)
- Follow the prompts like you're ordering pizza
- Confirm when asked (unless you enjoy being locked out)

**Option B: The Command Line Hero Way**
```bash
# For people who like to feel important
python advanced_cleaner.py
```

**Option C: The "I Know What I'm Doing" Way**
```bash
# Skip all the hand-holding
python advanced_cleaner.py --clean cursor --no-confirm
python advanced_cleaner.py --clean windsurf --no-confirm
```

### Step 4: Watch the Magic Happen
The tool will now:
1. 🛡️ **Create backups** (because we're not monsters)
2. 🔄 **Reset telemetry IDs** (new machine, who dis?)
3. 🗑️ **Clean databases** (goodbye, account restrictions)
4. 🧹 **Clear cache** (free up space for more important things)
5. 📝 **Generate restore scripts** (in case you change your mind)

*You'll see output like:*
```
✅ Successfully cleaned cursor data
📁 Backups saved to: C:\Users\YourName\CursorWindsurf_Advanced_Backups
```

### Step 5: Verify Results (Trust But Verify)
- ✅ **Check log files** for any errors (there shouldn't be any, but humans are unpredictable)
- ✅ **Verify backups exist** in your home directory
- ✅ **Launch applications** to test (they should start like fresh installs)
- ✅ **Try logging in** with any account (prepare to be amazed)

## 🔧 Configuration (For the Tweakers and Perfectionists)

The `cleaner_config.json` file allows you to customize the cleaning behavior, because apparently some people can't just use defaults like normal humans:

```json
{
  "applications": {
    "cursor": {
      "display_name": "Cursor AI",
      "process_names": ["cursor", "cursor.exe"],
      "data_paths": {
        "windows": ["%APPDATA%/Cursor"],
        "darwin": ["~/Library/Application Support/Cursor"],
        "linux": ["~/.config/Cursor"]
      }
    }
  },
  "cleaning_options": {
    "telemetry_keys": ["machineId", "deviceId", "sessionId"],
    "session_keys": ["authToken", "accessToken"],
    "database_keywords": ["augment", "account", "session"],
    "cache_directories": ["Cache", "IndexedDB", "Local Storage"]
  },
  "backup_options": {
    "enabled": true,
    "compression": false,
    "retention_days": 30
  }
}
```

*What you can customize:*
- 🎯 **Application paths** - In case your apps live in weird places
- 🔑 **Telemetry keys** - Add more tracking IDs to reset
- 🗑️ **Keywords to clean** - Target specific data patterns
- 📁 **Cache directories** - Specify what to nuke
- 💾 **Backup settings** - Control how paranoid you want to be

## 📁 What Gets Cleaned (The Dirty Details)

### Telemetry IDs (Your Digital Fingerprints)
- 🆔 **Machine IDs** - The unique snowflake identifier for your computer
- 📱 **Device IDs** - Because one ID wasn't enough, apparently
- 🎫 **Session IDs** - Links to your previous "unauthorized" usage
- 🔢 **Installation IDs** - Proof you installed the app (the audacity!)

*Result: Your computer becomes a mysterious stranger to the applications.*

### Database Records (The Incriminating Evidence)
- 👤 **Account-specific data** - Your digital DNA in SQLite databases
- 🎭 **Cached user profiles** - Who you pretended to be
- 🔐 **Authentication tokens** - Your digital keys to the kingdom
- 💳 **Credentials** - The "remember me" checkboxes you definitely clicked

*Result: The apps forget you ever existed (in a good way).*

### Cache Directories (The Digital Hoarding)
- 🗂️ **Workspace storage** - Your project breadcrumbs
- 💾 **IndexedDB and Local Storage** - Web storage that thinks it's important
- 📄 **Temporary files** - The "temporary" files that live forever
- 🎮 **GPU cache** - Because even your graphics card judges your coding
- 📊 **Logs** - Evidence of your coding crimes

*Result: Gigabytes of space freed up for more important things (like memes).*

## 🔒 Safety Features (Because We're Not Savages)

- 💾 **Automatic backups** - We backup everything before touching it (unlike some people)
- 🚫 **Process detection** - Won't run if apps are open (prevents you from breaking things)
- ⚠️ **Confirmation prompts** - Makes you think twice before nuking everything
- 🔄 **Restore script generation** - Easy undo button for when you inevitably panic
- 📝 **Comprehensive logging** - So you can see exactly what we did (transparency is sexy)
- 🧪 **Test mode** - Verify everything works without actually doing anything

*We're basically the responsible adult in this relationship.*

## 📂 File Structure

```
cursor-windsurf-cleaner/
├── cursor_windsurf_cleaner.py    # Basic cleaner script
├── advanced_cleaner.py           # Advanced cleaner with config
├── cleaner_config.json           # Configuration file
├── run_cleaner.bat              # Windows batch script
├── run_cleaner.sh               # Unix shell script
├── README.md                    # This documentation
└── backups/                     # Created automatically
    ├── cursor_telemetry_20240614_120000/
    ├── windsurf_database_20240614_120001/
    └── restore_cursor_20240614_120002.py
```

## 🔍 Troubleshooting (When Things Go Wrong, As They Do)

### Common Issues (And Why They Happen)

**"Application not found" 😤**
- 🤔 **Cause**: You probably installed apps in weird places or they don't exist
- 🔧 **Solution**:
  - Ensure the application is actually installed (revolutionary concept)
  - Check the configuration file for correct paths
  - Run discovery mode: `python advanced_cleaner.py --discover`
  - *If discovery finds nothing, the apps probably aren't installed. Shocking.*

**"Permission denied" 🚫**
- 🤔 **Cause**: Your computer doesn't trust you (smart computer)
- 🔧 **Solution**:
  - Run as administrator (Windows) or with sudo (Unix)
  - Make sure applications are completely closed (see Step 1 above)
  - Check if you actually own the files you're trying to modify
  - *Stop running things as a limited user if you want unlimited power*

**"Database locked" 🔒**
- 🤔 **Cause**: The app is still running somewhere, lurking in the shadows
- 🔧 **Solution**:
  - Close ALL instances of the applications (yes, all of them)
  - Wait 10 seconds (patience is a virtue)
  - Check Task Manager/Activity Monitor for sneaky background processes
  - *If you see the app running, close it. This isn't rocket science.*

**"Python not found" 🐍**
- 🤔 **Cause**: You don't have Python installed or it's not in PATH
- 🔧 **Solution**:
  - Install Python 3.7+ from python.org
  - Add Python to your system PATH
  - *It's 2025, having Python installed should be a given*

### Log Files (Your New Best Friends)
When things break (and they will), check these files:
- 📄 `cursor_windsurf_cleaner.log` (basic cleaner logs)
- 📄 `advanced_cleaner.log` (advanced cleaner logs)

*These files contain more information than you probably want, but hey, at least we're thorough.*

## 🔄 Recovery (The "Oh Crap, I Need My Data Back" Guide)

If you need to restore your data (because you panicked or your boss found out):

### Option 1: The Easy Way (Use Our Magic Scripts)
```bash
# Look for files like this in your backup directory:
python restore_cursor_20250614_120002.py
python restore_windsurf_20250614_120003.py
```
*These scripts are automatically generated and do all the heavy lifting for you.*

### Option 2: The Manual Way (For Control Freaks)
1. 📁 **Navigate to the backup directory** (shown after cleaning)
   - Windows: `C:\Users\YourName\CursorWindsurf_Advanced_Backups`
   - Mac/Linux: `~/CursorWindsurf_Advanced_Backups`
2. 📋 **Copy backed-up files** to their original locations
3. 🔄 **Restart the applications** and pray to the coding gods

*Manual restoration is like performing surgery with a butter knife - possible, but why would you?*

## ⚖️ Legal and Ethical Considerations (The Fine Print)

- 🏠 **This tool modifies local application data only** - We're not hacking anything, just cleaning your own computer
- 🌐 **No network traffic or external services involved** - Your data stays on your machine where it belongs
- 📜 **Users are responsible for compliance with application ToS** - Don't blame us if you get in trouble
- 🎯 **Intended for legitimate use cases** - Like testing, development, and not being locked out of tools you need

*Translation: Use your brain and don't do anything stupid.*

## 🤝 Contributing (Join the Rebellion)

Contributions are welcome! Please:
- 🧪 **Test thoroughly** before submitting (we have standards)
- 🎨 **Follow the existing code style** (consistency is beautiful)
- 📚 **Update documentation** as needed (future you will thank you)
- 🌍 **Consider cross-platform compatibility** (not everyone uses Windows)
- 😏 **Maintain the sarcastic tone** in documentation (it's part of our brand)

*If you can make this tool better, we'll gladly accept your improvements.*

## 📄 License

MIT License - Because we believe in freedom (see LICENSE file for the boring legal stuff)

## 🆘 Support (When You Need Help)

For issues and questions:
1. 📖 **Check the troubleshooting section** (it's there for a reason)
2. 📄 **Review log files** for error details (they're surprisingly helpful)
3. 🔄 **Ensure you're using the latest version** (old versions are like old milk)
4. 🐛 **Create an issue** with detailed information (not just "it doesn't work")

*Please include actual error messages, not just "it's broken." We're good, but we're not mind readers.*

## 🎉 Final Words

This tool exists because some applications think they can limit how you use your own computer. We respectfully disagree.

**Use responsibly, backup your data, and may your coding sessions be unlimited!** 🚀

---

*P.S. - If this tool saved your coding career, consider starring the repo. It's free and makes us feel good about ourselves.* ⭐

## ⚡ Dependencies

This tool now requires the following Python packages:

```bash
pip install -r requirements.txt
```

- `tqdm` (for progress bars and status output)

## 🚀 New Features & Enhancements

- **Performance Optimization:**
  - File and directory operations are now optimized for speed, especially on large directories.
- **Progress Bar/Status Output:**
  - All major cleaning operations now display a progress bar using `tqdm`.
  - Use `--no-progress` to disable progress bars for scripting or quiet mode.
- **Improved CLI:**
  - The CLI now supports a `--no-progress` flag for user control over output.
