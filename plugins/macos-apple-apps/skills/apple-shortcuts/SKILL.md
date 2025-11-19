---
name: apple-shortcuts
description: Run user-defined macOS Shortcuts for custom automation workflows. Use when user wants to trigger a Shortcut by name or execute a custom automation.
allowed-tools:
  - Bash
  - AskUserQuestion
---

# Apple Shortcuts Skill

Run user-defined macOS Shortcuts through Claude Code.

## Overview

macOS includes the Shortcuts app for creating custom automation workflows. This skill allows Claude to trigger those Shortcuts via the `shortcuts` command-line tool.

## The `shortcuts` Command

macOS provides a built-in CLI tool for running Shortcuts:

```bash
# List all available shortcuts
shortcuts list

# Run a shortcut by name
shortcuts run "Shortcut Name"

# Run with input
shortcuts run "Shortcut Name" --input-path /path/to/file

# Get shortcut details
shortcuts view "Shortcut Name"

# Sign shortcuts for automation (one-time setup)
shortcuts sign --mode people-who-know-me "Shortcut Name"
```

## Usage Pattern

### 1. List Available Shortcuts

```bash
shortcuts list
```

This shows all Shortcuts the user has created. Present this list to the user if they ask "What shortcuts do I have?"

### 2. Run a Shortcut (REQUIRES USER CONFIRMATION)

**Always ask user before running a shortcut** using `AskUserQuestion` tool.

```bash
shortcuts run "Morning Routine"
```

### 3. View Shortcut Details

```bash
shortcuts view "Backup Photos"
```

Shows what the shortcut does (if the user wants to verify before running).

## Common Use Cases

### User: "What shortcuts do I have?"

```bash
shortcuts list
```

Present the list formatted nicely.

### User: "Run my morning routine shortcut"

1. **First**, list shortcuts to find exact name:
```bash
shortcuts list
```

2. **Then**, ask user for confirmation:
"I found the shortcut 'Morning Routine'. This shortcut will:
- [describe what it does if possible]

Should I run it?"

3. **If confirmed**, run it:
```bash
shortcuts run "Morning Routine"
```

### User: "Create a shortcut to..."

**Response**: "I can't create Shortcuts directly. You'll need to create it in the Shortcuts app, then I can run it for you. Would you like me to explain how to create it?"

## Security & Privacy

### ALWAYS REQUIRE CONFIRMATION

Shortcuts can do **anything** - file operations, network requests, app automation, etc.

**Rule**: NEVER run a shortcut without explicit user confirmation.

### What to Ask Before Running

1. "Which shortcut do you want to run?" (verify exact name)
2. Show what it does (if possible via `shortcuts view`)
3. "Should I run this now?"

### Signing Shortcuts

Some shortcuts may need to be signed for automation:

```bash
shortcuts sign --mode people-who-know-me "Shortcut Name"
```

If a shortcut fails with a signing error, tell the user:
"This shortcut needs to be signed for automation. Run this in Terminal:
`shortcuts sign --mode people-who-know-me \"Shortcut Name\"`"

## Examples

### Example 1: Morning Routine

User has a "Morning Routine" shortcut that:
- Sets Focus mode
- Adjusts display brightness
- Opens specific apps
- Reads calendar

```bash
shortcuts run "Morning Routine"
```

### Example 2: Export Photos

User has "Export Photos" shortcut that exports recent photos to a folder:

```bash
shortcuts run "Export Photos"
```

May require input path:
```bash
shortcuts run "Export Photos" --input-path ~/Desktop/
```

### Example 3: Backup Workflow

User has "Backup to NAS" shortcut:

```bash
shortcuts run "Backup to NAS"
```

## Integration with Other Skills

Shortcuts can complement other Apple app integrations:

### Calendar → Shortcuts
- User creates Calendar event via `apple-productivity` skill
- Then triggers "Sync Calendar" shortcut to sync with external service

### Health → Shortcuts
- Trigger "Export Health Data" shortcut
- Then query exported data with `apple-health-fitness` skill

### Contacts → Shortcuts
- Lookup contact with `apple-productivity` skill
- Trigger "Send Birthday Reminder" shortcut for that contact

## Limitations

### Cannot Create Shortcuts

Claude cannot create or modify Shortcuts - only run existing ones. Shortcuts must be created by the user in the Shortcuts app.

### No Direct Shortcut Editing

Cannot view internal structure of shortcuts (they're binary files). Can only run them.

### Shortcut Permissions

Shortcuts may require permissions (Automation, Files, etc.). User must grant these in System Settings.

### Input/Output

- Simple text input/output works well
- File input via `--input-path`
- Complex data structures may be tricky

## Shortcut Ideas for Users

Suggest these shortcuts users could create:

### Productivity
- Morning/Evening routines
- Focus mode triggers
- Calendar sync workflows
- Email templates

### File Management
- Backup workflows
- Photo organization
- Document conversion
- File compression/archiving

### Health & Fitness
- Export health data
- Log workouts
- Meal tracking
- Sleep analysis

### Communication
- Send templated messages
- Email batches
- Social media posts
- Contact management

### Development
- Git workflows
- Build/deploy automation
- Test runners
- Environment setup

## Troubleshooting

### "Shortcut not found"

```bash
shortcuts list
```

Get exact name (case-sensitive, spaces matter).

### "Signing error"

```bash
shortcuts sign --mode people-who-know-me "Shortcut Name"
```

Or tell user to open Shortcuts app → Settings → Advanced → Allow Running Scripts

### "Permission denied"

Shortcut needs permissions. User must grant in:
System Settings → Privacy & Security → Automation

## Resources

- **Shortcuts User Guide**: https://support.apple.com/guide/shortcuts-mac/
- **Command-line Tool**: Run `man shortcuts` for details
- **Gallery**: Open Shortcuts app → Gallery for inspiration

## Related Skills

- `apple-productivity` - Calendar, Contacts, Mail, Messages, Reminders
- `apple-health-fitness` - Health and Fitness data

---

**Remember**: Shortcuts are powerful and potentially destructive. ALWAYS confirm with user before running any shortcut.
