# macOS Apple Apps - Detailed Capabilities

Complete reference for what's possible with each macOS native app.

**Based on**: Research from ~/Vault/To-Process/AppleScript Capabilities - macOS Apps.md

---

## 📅 Apple Calendar (Highly Scriptable!)

### What You Can Do

✅ **Events**
- Create/read/update/delete events
- All-day events
- Recurring events
- Event properties: title, date/time, description, location, notes
- Add alerts and reminders to events
- Add attendees to events

✅ **Calendars**
- List all calendars
- Filter events by calendar
- Write to user-managed calendars
- Read from system calendars (Birthdays, US Holidays, Siri Suggestions)

✅ **Date Queries**
- Today's events
- Date range queries
- This week/month
- Recurring event patterns

### Limitations

⚠️ **URI Scheme** - Limited "open event" URL support (can't directly link to specific events)
⚠️ **Large Queries** - Reading all events can be slow with large calendars (years of history)
⚠️ **Read-Only Calendars** - Birthdays, US Holidays, Siri Suggestions are read-only

### Available Calendars (Example)

**User-managed** (read/write):
- Me, Family, FolksDr, Timeline and Events
- Gerald's Missions, gerald@shudys.com, jerry@shudys.com
- Scheduled Reminders

**System-managed** (read-only):
- Birthdays (synced from Contacts)
- US Holidays (Apple-provided)
- Siri Suggestions (AI-generated)

### Implementation

- **Method**: AppleScript via `calendar-*` helper scripts
- **Performance**: Good for typical queries (days/weeks), slow for large ranges (years)
- **Reliability**: Very reliable, Calendar.app doesn't need to be open

---

## 👤 Apple Contacts (Highly Scriptable!)

### What You Can Do

✅ **Read Contact Information**
- Name (first, last, middle, prefix, suffix)
- Company and job title
- Phone numbers (all types: iPhone, Home, Work, Mobile, etc.)
- Email addresses (multiple, with labels)
- Physical addresses (Home, Work, etc.)
- Birthdays and anniversaries
- Notes field
- URLs and social media handles
- Related names (spouse, family, etc.)

✅ **Search**
- By name (first, last)
- By email address
- By phone number
- By company name
- Case-insensitive matching

✅ **Manage Contacts**
- Create new contacts
- Update existing contacts
- Delete contacts
- Organize into groups

### Example Contact Data

```
Name: Eileen Shudy
Birthday: January 9, 1968
Phones:
  - iPhone: +1 (763) 496-7773
  - Home: +1 (763) 425-0992
  - Work: +1 (612) 291-4556
Emails:
  - old: eklein19@comcast.net
  - Other: eileenklein19@gmail.com
  - Home: eileen@shudys.com
  - Work: eileen.shudy@bestbuy.com
Company: Best Buy
```

### High-Value Use Cases

1. **Quick Lookup** - "What's Brandon's phone number?" → instant answer
2. **Birthday Extraction** - Pull all birthdays, add to Journal/Calendar
3. **Contact Sheets** - Generate contact lists for groups (family, work)
4. **Bulk Updates** - Update company names, add notes to multiple contacts
5. **Cleanup** - Find duplicates, contacts without phones/emails

### Implementation

- **Method**: AppleScript via `contacts-search` helper script
- **Performance**: ~700 contacts, enumeration can be slow
- **Reliability**: Very reliable
- **Limitation**: Listing ALL contacts is slow - use targeted searches

---

## 📧 Apple Mail (Highly Scriptable!)

### What You Can Do

✅ **Read Messages**
- Read inbox messages
- Search by sender, subject, date
- Get message counts (total, unread)
- Filter by mailbox
- Extract attachments (with limitations)

✅ **Send/Compose**
- Send emails
- Create drafts
- Add attachments to drafts
- Set recipients (to, cc, bcc)

✅ **Organize**
- Move messages to folders
- Mark as read/unread
- Flag messages
- Delete messages

### Limitations

⚠️ **Requires Mail.app Running** - AppleScript queries fail if Mail.app is not open
⚠️ **Large Queries** - Searching years of email is slow
⚠️ **Attachment Handling** - Limited compared to manual operations

### Use Cases

1. **Unread Check** - "Any unread from Marie?" → quick scan
2. **Email Automation** - Send templated emails (job applications, follow-ups)
3. **Inbox Processing** - Extract action items, dates, tracking numbers
4. **Draft Management** - Create email drafts from journal tasks

### Implementation

- **Method**: AppleScript via `mail-unread` helper script
- **Performance**: Good for recent mail (24-48 hours), slower for large timeframes
- **Reliability**: Requires Mail.app to be running (exit code 1 if not)

---

## 💬 Apple Messages (Very Limited - Hybrid Access)

### What You Can Do

✅ **Read Messages** (via SQLite direct access)
- Recent messages by timeframe
- Search by sender
- Search by content/pattern
- Check for specific notation patterns

⚠️ **Send Messages** (via AppleScript - BLOCKED for privacy)
- Send iMessages (with user confirmation each time)
- Send to individuals or groups
- **BUT**: Requires explicit permission for EACH send

❌ **Cannot Do** (security/privacy restrictions)
- Read via AppleScript (blocked)
- Get conversation history via AppleScript
- Check conversation status
- Bulk operations

### Implementation

**Two Methods**:

1. **SQLite Direct Access** (for reading)
   - Database: `~/Library/Messages/chat.db`
   - Fast, works even when Messages.app closed
   - via `imessage-recent` helper script

2. **AppleScript** (for sending - but rarely works)
   - Heavily locked down for privacy
   - Requires user interaction
   - Frequent timeouts

### Limitations

- **Privacy-Focused** - Apple intentionally limits Messages automation
- **Read via SQLite only** - AppleScript reading is blocked
- **Send is unreliable** - Use sparingly, requires confirmation
- **Database locks** - SQLite may be locked when Messages.app is active

### Use Cases

1. **Message Search** - "Messages from last 24 hours about lunch"
2. **Notation Check** - Look for user directives like `(ghsj→cc:`
3. **Communication Context** - Part of morning context checks

**NOT useful for**: Automation, reading conversations, bulk operations, reliable sending

---

## ✅ Apple Reminders (Highly Scriptable!)

### What You Can Do

✅ **Create Reminders**
- Title and notes
- Due dates and times
- Priority (high/medium/low/none)
- Tags
- Subtasks
- Location-based alerts (arriving/leaving)

✅ **Query Reminders**
- By completion status (complete/incomplete)
- By list
- By due date (today, overdue, upcoming)
- By priority
- By tags

✅ **Manage Reminders**
- Mark complete/incomplete
- Update properties
- Move between lists
- Delete reminders

### Available Lists (Example GTD Setup)

- **Tasks/Next Actions** - Primary action list
- **Projects** - Project tracking
- **Repeating Reminders** - Recurring tasks
- **Attic** - Archived/deferred items
- **Stuff for Eileen** - Shared/delegated items

### Use Cases

1. **Overdue Alerts** - Query overdue tasks, create alerts
2. **Time-Sensitive Tasks** - "Remind me Monday 9am to send resume"
3. **Location-Based** - "Remind me to get milk when I arrive at Target"
4. **GTD Workflow** - Sync tasks between systems

### Limitations

⚠️ **Large Queries** - Can lock up with 100+ reminders
⚠️ **Pagination Needed** - Query specific lists rather than all at once
⚠️ **Test First** - Try small queries before large operations

### Implementation

- **Method**: AppleScript via `reminders-list` helper script
- **Performance**: Good for filtered queries, slow for "all reminders"
- **Reliability**: Can timeout (10s limit) - filter by list if needed

---

## 📝 Apple Notes (Moderately Scriptable)

### What You Can Do

✅ **Basic Operations**
- Create notes with text content
- Read note content
- List notes in folders
- Append text to existing notes
- Move notes between folders
- Search by title

⚠️ **Limitations**
- Mostly plain text (limited formatting support)
- Attachments are tricky via AppleScript
- Can't access locked notes via script
- Less capable than Obsidian for automation

### Decision: Limited Use

**Rationale**:
- Obsidian provides better structure, linking, and search
- Notes AppleScript capabilities are limited compared to other apps
- Most content already migrated to Obsidian vault

**Recommendation**: Focus on Calendar and Reminders integration instead. Use Notes only for locked/sensitive content that shouldn't be in Obsidian.

---

## 🍎 Apple Health (Not Scriptable - Export Only)

### Status: ⚠️ Under Development

Apple Health does NOT have a usable AppleScript dictionary. Access requires:

### Export Methods

1. **Manual Export**
   - Health app → Profile → Export All Health Data
   - Generates `export.xml` file
   - Parse XML to query data

2. **healthexport CLI** (Community Tool)
   ```bash
   pip3 install healthexport
   healthexport ~/health-export/
   ```
   - Exports as CSV files
   - Easier to query than XML

3. **HealthKit Framework** (Advanced)
   - Requires Swift/Xcode development
   - Can query live data
   - Complex setup

### Data Types Available

- **Activity**: Steps, flights, distance, calories, exercise minutes
- **Workouts**: Type, duration, distance, calories, heart rate
- **Heart**: Resting rate, walking rate, variability, exercise rate
- **Sleep**: Duration, stages, time asleep vs. in bed
- **Body**: Weight, height, BMI, body fat percentage
- **Vitals**: Blood pressure, glucose, oxygen, respiratory rate

### Privacy & Security

- **READ-ONLY** - No writing to Health app via automation
- **EXPLICIT CONSENT** - Always ask before accessing
- **AGGREGATED DATA** - Summaries and trends only, not raw detailed records
- **NO EXTERNAL SHARING** - Health data stays local

---

## 🏃 Apple Fitness (Limited - Activity Rings Only)

Fitness.app has limited AppleScript support:

✅ **What Works**
- Query Activity Rings (Move, Exercise, Stand) for current day
- Check ring completion status

❌ **What Doesn't Work**
- Historical data (current day only)
- Detailed workout information (use Health export instead)
- Fitness+ data

**Recommendation**: Use Health data export for fitness analysis. Fitness.app automation is too limited.

---

## ⚡ Apple Shortcuts (Highly Capable!)

### What You Can Do

✅ **Run Shortcuts**
- Execute any user-created shortcut by name
- Pass input (text, files, URLs)
- Receive output

✅ **List Shortcuts**
- View all available shortcuts
- Get shortcut details

⚠️ **Cannot Do**
- Create or edit shortcuts (must use Shortcuts.app)
- Access internal structure
- Modify shortcut logic

### The `shortcuts` Command

macOS provides built-in CLI:

```bash
shortcuts list                      # All shortcuts
shortcuts run "Shortcut Name"       # Execute
shortcuts run "Name" --input-path /path/file  # With input
shortcuts view "Shortcut Name"      # Details
shortcuts sign --mode people-who-know-me "Name"  # Sign for automation
```

### Use Cases

1. **Workflows** - Morning routines, backups, exports
2. **App Control** - Control apps without AppleScript support
3. **Complex Automation** - Multi-step processes
4. **Integration** - Bridge between Apple apps and other systems

### Security

- **ALWAYS CONFIRM** - Shortcuts can do anything (files, network, apps)
- **Sign if Needed** - Some shortcuts require signing for automation
- **Permissions** - Shortcuts may need Automation/Files/etc. permissions

---

## 🎵 Apple Music (Highly Scriptable!)

### What You Can Do

✅ **Playback Control**
- Play, pause, skip, volume
- Shuffle, repeat modes

✅ **Track Information**
- Current track (name, artist, album, artwork)
- Track duration and position
- Lyrics (if available)

✅ **Library**
- Search library
- Get playlists
- Rate songs
- Add to library

✅ **Playlists**
- Create/modify playlists
- Add/remove tracks

### Use Cases

- "What song is playing?" → instant answer
- Create themed playlists programmatically
- Library stats (most played, recently added)
- Smart playlist management

---

## 🌐 Safari (Moderately Scriptable)

### What You Can Do

✅ **Basic Control**
- Open URLs in tabs
- Get current page URL and title
- Navigate (back, forward, reload)
- Close tabs

❌ **Cannot Do** (security restrictions)
- Read page content
- Fill forms
- Click buttons
- Execute JavaScript (security restricted)

### Use Cases

- Open multiple research URLs at once
- Capture current tab as reference
- Batch-open bookmarks

---

## 📁 Finder (Highly Scriptable!)

### What You Can Do

✅ **File Operations**
- Create/move/copy/delete files and folders
- Get file properties (size, date, type, permissions)
- Search files
- Open files in specific applications

✅ **Window Management**
- Get current selection
- Reveal files in Finder
- Open new windows at specific locations

✅ **Volumes**
- Eject volumes
- List mounted volumes

### Security Note

**Use with EXTREME CAUTION** per CLAUDE.md safety guidelines:
- NEVER delete files without confirmation
- NEVER modify files in sensitive locations (`~/.ssh`, `~/Documents`, etc.)
- ALWAYS ask before batch operations
- Stay within project directories when possible

**Recommendation**: Use specialized tools (FindMedia, standard CLI) rather than Finder automation for most tasks.

---

## 📟 System Events (Powerful - UI Automation)

### What You Can Do

✅ **UI Automation**
- Keystroke automation
- Click UI elements
- Control any application's menus
- Navigate complex UIs programmatically

✅ **System Info**
- Get running processes
- Query system preferences
- Control accessibility features

### Use Cases

- Automate apps that aren't scriptable
- Fill forms in any application
- Complex UI workflows

### Requirements

- **Accessibility permissions** required
- More complex than direct AppleScript
- Should be last resort (use app-specific scripts first)

---

## 🔔 Notifications (Simple)

### What You Can Do

✅ **Display Notifications**
- Custom titles and messages
- Optional sounds
- System notification center

❌ **Cannot Do**
- Interactive notifications with buttons
- Custom actions

### Use Cases

- Alert when long-running task completes
- Reminder notifications from journal
- Progress updates during batch operations

---

## 🗣️ Speech (Fun!)

### What You Can Do

✅ **Text-to-Speech**
- Speak text aloud
- Choose voice and rate
- Wait for completion or speak in background

### Use Cases

- Audio alerts ("Your timer is done")
- Read text aloud while multitasking
- Accessibility features
- ADHD reminders (spoken)

---

## Third-Party Apps with AppleScript Support

### Developer Tools

- **iTerm2** - Full scripting support
- **BBEdit/TextWrangler** - Excellent support
- **VS Code** - With extension

### Productivity

- **OmniFocus** - Full task management automation
- **Things** - Task and project scripting
- **DEVONthink** - Document database automation
- **Alfred** - Workflow automation
- **Keyboard Maestro** - Macro automation

### Media

- **VLC** - Playback control
- **Spotify** - Playback and playlist management

### Communication

- **Microsoft Outlook** - Email/calendar automation (alternative to Mail/Calendar)

---

## Testing Apps for Scriptability

```bash
# Check if app has a scripting dictionary
osascript -e 'tell application "System Events" to get name of processes whose background only is false'

# Open app's dictionary in Script Editor
# Script Editor → File → Open Dictionary → Choose App
```

**Apps with rich dictionaries = highly scriptable**

---

## Summary: Automation Value

### ⭐⭐⭐ Highly Valuable (Priority)

- **Calendar** - Events, recurring, multi-calendar
- **Contacts** - Rich data, birthdays, lookup
- **Reminders** - GTD workflows, location-based
- **Mail** - Email automation, inbox processing
- **Music** - Playback, library, playlists

### ⭐⭐ Moderately Valuable

- **Messages** - Read via SQLite, send limited
- **Shortcuts** - Run custom workflows
- **Safari** - Basic control only
- **System Events** - Powerful but complex

### ⭐ Limited Value

- **Notes** - Use Obsidian instead
- **Photos** - Use FindMedia instead
- **Fitness** - Limited to current day Activity Rings
- **Notifications** - Simple alerts only

### ⚠️ Under Development

- **Health** - Export-based access only

---

**Last Updated**: 2025-11-12
**Source**: Research from ~/Vault/To-Process/AppleScript Capabilities - macOS Apps.md
