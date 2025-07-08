# Mac Calendar Free Slots Finder

🗓️ Python tool for finding free time slots in Mac Calendar with extensive customization options.

## Features

- ✅ Native Mac Calendar integration through EventKit
- 📅 Analyze current and upcoming weeks
- ⏰ Configurable working hours (default: 8:00-19:00)
- 📊 Beautiful output with emojis and color coding
- 🎯 Minimum slot duration filtering
- 📋 Flexible date range selection
- 🖥️ Desktop shortcut creation
- 💾 Minimal output mode by default
- 📋 Automatic clipboard copy (enabled by default)
- 🔧 Extensive command-line configuration
- 🌐 Multi-language support (English/Russian)

## Requirements

- macOS (EventKit is Mac-only)
- Python 3.7+
- Calendar access permission (system will prompt)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/calslots.git
   cd calslots
   ```

2. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   
   Or install manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python calendar_slots.py
```

### Command Line Options

```bash
# Show help
python calendar_slots.py --help

# Custom working hours
python calendar_slots.py --start-hour 9 --end-hour 18

# Analyze 3 weeks instead of default 2
python calendar_slots.py --weeks 3

# Include weekends
python calendar_slots.py --include-weekends

# Custom date range
python calendar_slots.py --start-date 2024-01-15 --end-date 2024-01-30

# Minimum slot duration (default: 30 minutes)
python calendar_slots.py --min-duration 60

# Verbose output with statistics
python calendar_slots.py --verbose

# Disable automatic clipboard copy
python calendar_slots.py --no-copy

# Copy clean text without emojis
python calendar_slots.py --clean-copy
```

### Desktop Shortcut

Create a desktop shortcut for quick access:

```bash
chmod +x move_to_desktop.sh
./move_to_desktop.sh
```

This creates a "📅 Calendar Slots" shortcut on your desktop that runs the tool with default settings.

## Example Output

### Default (Minimal) Output
```
🗓️  Среда (15.01.2025)
   ✅ 09:00 - 10:00 (1ч 0м)
   ✅ 11:30 - 14:00 (2ч 30м)
   ✅ 16:00 - 19:00 (3ч 0м)

🗓️  Четверг (16.01.2025)
   ✅ 09:00 - 13:00 (4ч 0м)
   ✅ 15:30 - 19:00 (3ч 30м)

📋 Свободные слоты скопированы в буфер обмена!

**Clipboard contains (with emojis by default):**
```
🗓️  Среда (15.01.2025)
   ✅ 09:00 - 10:00 (1ч 0м)
   ✅ 11:30 - 14:00 (2ч 30м)

🗓️  Четверг (16.01.2025)
   ✅ 09:00 - 13:00 (4ч 0м)
   ✅ 15:30 - 19:00 (3ч 30м)
```

**With `--clean-copy` flag:**
```
Среда (15.01.2025)
   09:00 - 10:00 (1ч 0м)
   11:30 - 14:00 (2ч 30м)

Четверг (16.01.2025)
   09:00 - 13:00 (4ч 0м)
   15:30 - 19:00 (3ч 30м)
```
```

### Verbose Output
```
🗓️  Mac Calendar Free Slots Finder
==================================================
📅 Анализируем период с 2025-01-15 по 2025-01-28
🔍 Получаем события из календаря...
📊 Найдено 8 событий

📆 ТЕКУЩАЯ НЕДЕЛЯ
   15.01.2025 - 19.01.2025
----------------------------------------

🗓️  Среда (15.01.2025)
   📝 Запланированные события:
      • 10:00 - 11:30: Важная встреча
      • 14:00 - 16:00: Созвон с командой
   ✅ Свободные слоты:
      • 09:00 - 10:00 (1ч 0м)
      • 11:30 - 14:00 (2ч 30м)
      • 16:00 - 19:00 (3ч 0м)

📊 СТАТИСТИКА
   • Всего рабочих дней: 10
   • Дней с событиями: 6
   • Общее время свободных слотов: 47ч 30м
```

## Configuration

### Working Hours
```bash
# 24-hour format
python calendar_slots.py --start-hour 8 --end-hour 20
```

### Working Days
```bash
# Include weekends
python calendar_slots.py --include-weekends

# Only specific days (Monday=0, Sunday=6)
python calendar_slots.py --working-days 0,1,2,3,4
```

### Date Range
```bash
# Specific date range
python calendar_slots.py --start-date 2025-01-15 --end-date 2025-01-30

# Number of weeks from today
python calendar_slots.py --weeks 4
```

### Minimum Slot Duration
```bash
# Only show slots longer than 1 hour
python calendar_slots.py --min-duration 60
```

### Clipboard Integration
```bash
# Automatic clipboard copy with emojis (default behavior)
python calendar_slots.py

# Copy clean text without emojis (for business emails)
python calendar_slots.py --clean-copy

# Disable clipboard copy
python calendar_slots.py --no-copy
```

The tool automatically copies all free slots to your clipboard **with emojis** by default for better readability. Use `--clean-copy` for plain text format suitable for business emails or formal communications.

## Security and Permissions

- The tool requires Calendar access permission on first run
- Only **read access** to your calendar - cannot modify or delete events
- No data is sent to external servers
- All processing happens locally on your Mac

### Setting Up Calendar Access

1. Run the tool for the first time
2. macOS will prompt for Calendar access
3. Click "OK" to grant permission
4. If permission is denied, go to System Preferences → Security & Privacy → Privacy → Calendars and enable access for Terminal/Python

## Troubleshooting

### EventKit Not Found
- Ensure you're running on macOS (EventKit is Mac-only)
- Install dependencies: `pip install -r requirements.txt`

### Calendar Access Issues
- Check System Preferences → Security & Privacy → Privacy → Calendars
- Ensure Terminal/Python has calendar access
- Try running the installation script again

### No Events Found
- Verify you have events in the specified date range
- Check that your calendar is active in the Calendar app
- Ensure events are not marked as "All Day"

### Virtual Environment Issues
- Make sure to activate the virtual environment: `source venv/bin/activate`
- Reinstall dependencies if needed: `pip install -r requirements.txt`

## System Requirements

- macOS 10.15+ (Catalina or later)
- Python 3.7+
- PyObjC framework

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on macOS
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created for efficient Mac calendar management and meeting scheduling. 