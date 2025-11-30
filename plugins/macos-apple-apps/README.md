# macOS Apple Apps Plugin

Claude Code integration with macOS native productivity apps for workflow automation and personal productivity.

## Features

This plugin gives Claude Code read and (with confirmation) write access to:

- **📅 Calendar** - Events, recurring events, alerts, multi-calendar support
- **👤 Contacts** - Names, phones, emails, birthdays, addresses, company info
- **📧 Mail** - Unread messages, search, send (with confirmation)
- **💬 Messages** - Recent iMessages via SQLite (send with confirmation)
- **✅ Reminders** - Tasks, due dates, priorities, location-based alerts
- **🎙️ Voice Memos** - Transcription with speaker diarization via AssemblyAI
- **🍎 Health** - Health data queries (read-only)
- **🏃 Fitness** - Activity and workout data (read-only)
- **⚡ Shortcuts** - Run user-defined macOS Shortcuts

## Installation

### Prerequisites

- macOS (tested on macOS Sonoma/Sequoia)
- Claude Code
- Helper scripts installed in `~/bin/` (provided in this plugin)

### Install Plugin

```bash
/plugin install macos-apple-apps@g-shudy-plugins
```

### Install Helper Scripts

The plugin includes helper scripts for accessing Apple apps. Install them to `~/bin/`:

```bash
# From the plugin directory
cp scripts/* ~/bin/
chmod +x ~/bin/{mail-unread,imessage-recent,calendar-*,contacts-search,reminders-list,voice-memos}
```

Or use the provided install script:

```bash
./install-scripts.sh
```

## Skills

### `apple-productivity`

**Description**: Access macOS Apple productivity apps (Calendar, Contacts, Mail, Messages, Reminders) to read events, contacts, messages, and tasks.

**When Claude should use it**: When user needs to check calendar events, look up contact information, read recent messages or emails, or query reminders/tasks.

**Allowed tools**: `Bash`, `Read`, `Write` (for output only), `AskUserQuestion`

**Examples**:
- "What's on my calendar today?"
- "What's Brandon's phone number?"
- "Any unread emails from Marie?"
- "Show my overdue reminders"
- "When is Eileen's birthday?"

### `apple-health-fitness`

**Description**: Query Health and Fitness data from Apple Health app including activity, workouts, heart rate, sleep, and other health metrics.

**When Claude should use it**: When user asks about health stats, fitness activity, workouts, sleep data, heart rate, steps, or other health metrics.

**Allowed tools**: `Bash`, `Read`, `Write` (for output only)

**Examples**:
- "How many steps did I take this week?"
- "Show my recent workouts"
- "What was my average heart rate yesterday?"
- "Sleep data for last 7 days"

### `apple-shortcuts`

**Description**: Run user-defined macOS Shortcuts for custom automation workflows.

**When Claude should use it**: When user wants to trigger a Shortcut by name or needs to execute a custom automation workflow.

**Allowed tools**: `Bash`, `AskUserQuestion`

**Examples**:
- "Run my morning routine shortcut"
- "Execute the 'Export Photos' shortcut"
- "Trigger backup shortcut"

## Helper Scripts Reference

The plugin relies on helper scripts that encapsulate AppleScript/SQLite access:

### Calendar

- **`calendar-list`** - List all available calendars
- **`calendar-events [options]`** - Query events by date/range/calendar
- **`calendar-add -t "Title" -s START -e END`** - Add new event (ISO-8601 format)

### Contacts

- **`contacts-search <query>`** - Search contacts by name/email/phone/company
- **`contacts-search -a`** - List all contacts
- **`contacts-search -v <query>`** - Verbose output with all details

### Mail

- **`mail-unread [hours]`** - Get unread mail from last N hours (default: 24)
- **`mail-unread -d <days>`** - Get unread mail from last N days
- **`mail-unread -l <N>`** - Limit to N messages

### Messages

- **`imessage-recent [hours]`** - Get recent iMessages (default: 24 hours)
- **`imessage-recent -d <days>`** - Messages from last N days
- **`imessage-recent -n`** - Check for notation patterns
- **`imessage-recent -p "keyword"`** - Filter by pattern

### Reminders

- **`reminders-list`** - List incomplete reminders (default)
- **`reminders-list -a`** - All reminders
- **`reminders-list -c`** - Only completed
- **`reminders-list -d`** - Due today
- **`reminders-list -o`** - Overdue
- **`reminders-list -l "List Name"`** - Filter by list

### Voice Memos

- **`voice-memos list`** - Show unprocessed voice memos
- **`voice-memos list --all`** - Show all memos (including processed)
- **`voice-memos process`** - Auto-transcribe (prioritizes recent memos)
- **`voice-memos process --dry-run`** - Preview what would be processed
- **`voice-memos transcribe <file>`** - Transcribe specific memo
- **`voice-memos stats`** - Show usage/cost statistics

## Access Patterns

### AppleScript-based (most apps)

Mail, Calendar, Contacts, Reminders use AppleScript via the helper scripts:

```bash
# Calendar events
calendar-events --today

# Contact lookup
contacts-search "Marie"

# Unread mail
mail-unread 6  # Last 6 hours
```

### SQLite Direct Access (Messages)

iMessages are accessed via direct SQLite queries to `~/Library/Messages/chat.db`:

```bash
# Recent messages
imessage-recent 24  # Last 24 hours

# Search for pattern
imessage-recent -p "lunch"

# Check for notation patterns
imessage-recent -n
```

### SQLite + AssemblyAI (Voice Memos)

Voice Memos are read from Apple's synced database and transcribed via AssemblyAI:

```bash
# List unprocessed memos
voice-memos list

# Auto-transcribe all pending
voice-memos process

# Check cost/usage
voice-memos stats
```

**Databases**:
- Apple source: `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/CloudRecordings.db`
- Tracking: `~/.voice-memos.db` (processed, usage, skipped)

**Output**: Transcripts saved to `~/Vault/Voice-Transcripts/` with speaker diarization

**Requirements**: `ASSEMBLYAI_API_KEY` env var, `pip install assemblyai`

### Health/Fitness (healthexport)

Health and Fitness data require exporting from Health app using `healthexport` command-line tool:

```bash
# Export health data
healthexport ~/health-export/

# Query specific metrics
# (Implementation in progress)
```

### Shortcuts (shortcuts CLI)

Run Shortcuts via macOS `shortcuts` command:

```bash
# List available shortcuts
shortcuts list

# Run a shortcut
shortcuts run "Shortcut Name"
```

## Security & Privacy

### Confirmation Required

The following operations **ALWAYS** require explicit user confirmation:

- ❌ Sending emails
- ❌ Sending iMessages
- ❌ Creating/modifying calendar events
- ❌ Creating/modifying contacts
- ❌ Creating/modifying reminders
- ❌ Running shortcuts
- ❌ Accessing health data
- ❌ Transcribing voice memos (incurs AssemblyAI costs ~$0.0025/min)

### Safe Operations (Read-Only)

- ✅ Reading calendar events
- ✅ Looking up contact info
- ✅ Checking unread mail (counts and subjects only)
- ✅ Reading recent iMessages
- ✅ Querying reminder status
- ✅ Viewing health/fitness stats
- ✅ Listing voice memos (`voice-memos list`)
- ✅ Checking voice-memos stats (`voice-memos stats`)

### Privacy Notes

- Mail/Messages content is only shown when explicitly requested
- Contact information is treated as personal data
- Health data is highly sensitive - read-only access only
- All helper scripts have built-in permission checks
- AppleScript operations respect macOS security prompts

## Known Limitations

### App-Specific Limitations

**Messages**:
- Send-only via AppleScript (reading blocked for privacy)
- Reading works via SQLite direct access
- Requires Messages.app database permissions

**Photos**:
- Limited AppleScript support
- Cannot access face information
- Very slow performance
- **Recommendation**: Use FindMedia plugin instead

**Reminders**:
- Can lock up during large queries
- May need pagination for large lists
- Test with small queries first

**Mail**:
- Mail.app must be running for queries
- Large time windows may be slow
- Attachment access is limited

### Performance Considerations

- Calendar queries: Timeout after 10s for large date ranges
- Contacts: ~700 contacts can be slow to enumerate
- iMessages: Direct SQLite access is fast but may hit database locks
- Health data: Export can take several minutes for large datasets

## Use Cases

### Productivity Workflows

1. **Morning Context** - Check calendar, unread mail, and pending reminders
2. **Contact Lookup** - Quick access to phone/email when composing messages
3. **Birthday Tracking** - Extract birthdays from Contacts to Calendar/Journal
4. **Task Management** - Sync overdue tasks between systems
5. **Message Search** - Find specific conversations or patterns

### GTD Integration

- Query overdue reminders and create alerts
- Time-box calendar events from task estimates
- Location-based reminders for errands
- Email-to-task workflows

### Health & Fitness

- Weekly activity summaries
- Workout tracking and analysis
- Sleep pattern analysis
- Heart rate trend monitoring

## Architecture

### Helper Scripts (~/bin/)

Small, focused shell scripts that:
- Encapsulate AppleScript/SQLite queries
- Provide consistent CLI interface
- Handle errors gracefully
- Support JSON output for automation
- Follow Unix philosophy (do one thing well)

### Skills (Claude Code)

Skills invoke helper scripts via Bash tool:
- `apple-productivity` - Calendar, Contacts, Mail, Messages, Reminders
- `apple-health-fitness` - Health and Fitness data
- `apple-shortcuts` - Shortcut automation

### Plugin Structure

```
macos-apple-apps/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── skills/
│   ├── apple-productivity/
│   │   └── SKILL.md         # Productivity apps skill
│   ├── apple-health-fitness/
│   │   └── SKILL.md         # Health/Fitness skill
│   └── apple-shortcuts/
│       └── SKILL.md         # Shortcuts skill
├── scripts/
│   ├── mail-unread          # Mail helper
│   ├── imessage-recent      # Messages helper
│   ├── calendar-list        # Calendar helper
│   ├── calendar-events      # Calendar queries
│   ├── calendar-add         # Calendar creation
│   ├── contacts-search      # Contacts helper
│   └── reminders-list       # Reminders helper
├── docs/
│   ├── CAPABILITIES.md      # Detailed app capabilities
│   ├── INTEGRATION.md       # Integration workflows
│   └── SECURITY.md          # Security guidelines
├── install-scripts.sh       # Script installer
└── README.md               # This file
```

## Development

### Adding New Apps

1. Research AppleScript capabilities (see docs/CAPABILITIES.md)
2. Create helper script in `scripts/`
3. Test thoroughly with security in mind
4. Document in README and CAPABILITIES.md
5. Add to appropriate skill or create new skill

### Testing

```bash
# Test individual helper scripts
mail-unread --help
calendar-events --help
contacts-search --help

# Test with Claude Code
/skill apple-productivity
# Then: "What's on my calendar today?"
```

### Security Review Checklist

- [ ] Input validation on all user-provided data
- [ ] No command injection vulnerabilities
- [ ] Proper error handling and exit codes
- [ ] Confirmation required for write operations
- [ ] Sensitive data not exposed in logs
- [ ] Timeout handling for slow operations

## Resources

### Documentation

- [AppleScript Capabilities](docs/CAPABILITIES.md) - Detailed app-by-app reference
- [Integration Workflows](docs/INTEGRATION.md) - Common use cases and patterns
- [Security Guidelines](docs/SECURITY.md) - Privacy and security best practices

### External Resources

- [Mac Automation Scripting Guide](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/)
- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [Claude Code Plugin Documentation](https://docs.claude.com/en/docs/claude-code/plugins)

### Related Projects

- [FindMedia Plugin](../findmedia/) - File intelligence and media management
- [Obsidian Integration](../obsidian/) - Knowledge management workflows

## Roadmap

### Phase 1: Core Productivity (Current)

- [x] Calendar integration (read/write)
- [x] Contacts lookup (read)
- [x] Mail queries (read)
- [x] Messages queries (read via SQLite)
- [x] Reminders queries (read)
- [ ] Send message/email workflows
- [ ] Create/update reminders

### Phase 2: Health & Fitness

- [ ] Health data export and queries
- [ ] Workout tracking
- [ ] Activity summaries
- [ ] Sleep analysis
- [ ] Heart rate trends

### Phase 3: Advanced Features

- [ ] Shortcuts integration
- [ ] Photos queries (limited, may defer to FindMedia)
- [ ] Music/Podcast control
- [ ] Safari tab management
- [ ] Finder automation (with extreme caution)

### Phase 4: Automation Workflows

- [ ] Morning context aggregation
- [ ] GTD task sync
- [ ] Birthday/anniversary notifications
- [ ] Location-based reminders
- [ ] Email-to-task conversion

## Contributing

This is a personal plugin, but feel free to fork and adapt for your own use.

## License

MIT

## Support

- **Issues**: https://github.com/g-shudy/claude-plugins/issues
- **Website**: https://ghsj.me
- **Plugins**: https://plugins.ghsj.me

---

*Part of the g-shudy Claude Code plugin collection*
