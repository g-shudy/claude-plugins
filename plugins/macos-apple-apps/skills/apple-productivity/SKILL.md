---
name: apple-productivity
description: Access macOS Apple productivity apps (Calendar, Contacts, Mail, Messages, Reminders) to read events, contacts, messages, and tasks. Use this when user needs to check calendar, look up contacts, read messages/emails, or query reminders.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# Apple Productivity Apps Skill

You have access to macOS native productivity apps through helper scripts installed in ~/bin/.

## Available Helper Scripts

### Calendar

**`calendar-list`** - List all available calendars
```bash
calendar-list
calendar-list -j  # JSON output
```

**`calendar-events`** - Query events
```bash
calendar-events                           # Today's events (default)
calendar-events -d 2025-11-15             # Specific date
calendar-events -w                        # This week
calendar-events -r 2025-11-15 2025-11-20  # Date range
calendar-events -c "Work"                 # Filter by calendar
calendar-events -j                        # JSON output
```

**`calendar-add`** - Add new event (REQUIRES USER CONFIRMATION)
```bash
calendar-add -t "Meeting" -s 2025-11-15T14:00:00 -e 2025-11-15T15:00:00
calendar-add -t "Lunch" -s 2025-11-15T12:00:00 -e 2025-11-15T13:00:00 -l "Cafe" -c "Personal"
```

**Important**: ISO-8601 format required: `YYYY-MM-DDTHH:MM:SS` (24-hour time)

### Contacts

**`contacts-search`** - Search contacts
```bash
contacts-search "Marie"          # Search by name
contacts-search -v "Brandon"     # Verbose (all details)
contacts-search -a               # List all contacts
contacts-search -l 5 "Smith"     # Limit to 5 results
contacts-search -j               # JSON output
```

Searches: First name, last name, email, phone, company (case-insensitive)

### Mail

**`mail-unread`** - Get unread mail (REQUIRES Mail.app RUNNING)
```bash
mail-unread              # Last 24 hours (default)
mail-unread 6            # Last 6 hours
mail-unread -d 3         # Last 3 days
mail-unread -l 5         # Limit to 5 messages
mail-unread -j           # JSON output
```

**Exit code 1** = Mail.app not running (tell user to open Mail.app)

### Messages

**`imessage-recent`** - Get recent iMessages (SQLite direct access)
```bash
imessage-recent              # Last 24 hours (default)
imessage-recent 6            # Last 6 hours
imessage-recent -d 3         # Last 3 days
imessage-recent -l 10        # Limit to 10 messages
imessage-recent -p "lunch"   # Filter by keyword
imessage-recent -n           # Check for notation patterns
imessage-recent -j           # JSON output
```

**Note**: Works even when Messages.app is NOT running (direct SQLite access)

**Notation patterns checked** (`-n` flag):
- `(ghsj→cc:`, `(ghsj:`, `(cc→ghsj:`, `(cc-suggest:`, `(cc-warn:`
- `>>move:`, `>>archive`, `>>defer:`
- `[MUST]`, `[SHOULD]`

### Reminders

**`reminders-list`** - Query reminders
```bash
reminders-list                        # Incomplete reminders (default)
reminders-list -a                     # All reminders
reminders-list -c                     # Only completed
reminders-list -d                     # Due today
reminders-list -o                     # Overdue
reminders-list -l "Work"              # Filter by list name
reminders-list -l "Work" -d           # Work reminders due today
reminders-list --limit 20             # Limit results
reminders-list -j                     # JSON output
```

**Warning**: Large queries can timeout (10s limit). Use `-l` to filter by specific list if needed.

## Common Patterns

### Morning Context Check

```bash
# Today's schedule
calendar-events --today

# Pending tasks
reminders-list -o  # Overdue
reminders-list -d  # Due today

# Unread communications
mail-unread
imessage-recent -n  # Check for notation patterns
```

### Contact Lookup

```bash
# Quick lookup
contacts-search "Marie"

# Full details
contacts-search -v "Brandon"

# Find someone by company
contacts-search "Best Buy"
```

### Message Search

```bash
# Recent messages about specific topic
imessage-recent -p "resume"

# Check for user directives
imessage-recent -n
```

## Security & Privacy

### READ-ONLY (Safe - No Confirmation Needed)

- ✅ Viewing calendar events
- ✅ Looking up contacts
- ✅ Checking unread mail counts/subjects
- ✅ Reading recent iMessages
- ✅ Querying reminder status

### WRITE OPERATIONS (ALWAYS Ask User First)

- ❌ Creating/modifying calendar events (`calendar-add`)
- ❌ Creating/modifying contacts
- ❌ Sending emails
- ❌ Sending iMessages
- ❌ Creating/modifying reminders

**Rule**: ALWAYS use `AskUserQuestion` tool before ANY write operation.

## Error Handling

### Mail Not Running

```bash
$ mail-unread
Error: Mail.app not running
Please open Mail.app before running this command
# Exit code: 1
```

**Response**: Tell user to open Mail.app, then retry.

### Calendar Timeout

```bash
$ calendar-events -r 2020-01-01 2025-12-31
Error: Query timed out after 10s
Try a smaller date range or check if Calendar.app is responsive
# Exit code: 3
```

**Response**: Use smaller date range (days/weeks, not years).

### No Results

All scripts handle "no results" gracefully:
```bash
$ calendar-events
No events found for 2025-11-15
```

## Examples

### User: "What's on my calendar today?"

```bash
calendar-events --today
```

Parse output and summarize for user.

### User: "What's Brandon's phone number?"

```bash
contacts-search "Brandon"
```

Extract phone number from output.

### User: "Any unread emails from Marie?"

First check if Mail.app is running:
```bash
mail-unread -l 20
```

Then filter output for "Marie" in sender field.

### User: "Show my overdue reminders"

```bash
reminders-list -o
```

Present list to user with due dates.

### User: "When is Eileen's birthday?"

```bash
contacts-search -v "Eileen"
```

Look for "Birthday:" in verbose output.

### User: "Create a calendar event for lunch tomorrow at noon"

1. Calculate tomorrow's date
2. Format as ISO-8601: `2025-11-16T12:00:00`
3. **ASK USER FOR CONFIRMATION** using `AskUserQuestion`
4. If confirmed:
```bash
calendar-add -t "Lunch" -s 2025-11-16T12:00:00 -e 2025-11-16T13:00:00
```

## Limitations

- **Mail**: Requires Mail.app to be running
- **Calendar**: Large date ranges (years) may timeout - use smaller ranges
- **Reminders**: Large lists may timeout - filter by specific list
- **Messages**: Read-only via AppleScript (send requires user interaction)
- **Contacts**: ~700 contacts can be slow to enumerate - use specific searches

## Tips

1. **Always check exit codes** - Non-zero = error
2. **Use JSON output** (`-j`) for complex parsing
3. **Limit results** when possible to avoid timeouts
4. **Filter early** - Use script options rather than parsing large outputs
5. **Batch operations** - Run multiple independent queries in parallel with multiple Bash tool calls

## Related Skills

- `apple-health-fitness` - Health and Fitness data
- `apple-shortcuts` - Run macOS Shortcuts

---

**Remember**: This skill gives you READ access to personal productivity data. ALWAYS ask before WRITING any data.
