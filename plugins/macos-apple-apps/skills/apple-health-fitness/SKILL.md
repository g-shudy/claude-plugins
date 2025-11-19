---
name: apple-health-fitness
description: Query Health and Fitness data from Apple Health app including activity, workouts, heart rate, sleep, and health metrics. Use when user asks about health stats, fitness activity, workouts, sleep data, or health metrics.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Apple Health & Fitness Skill

Access Health and Fitness data from Apple Health app.

## Status

⚠️ **UNDER DEVELOPMENT**

The Apple Health app does not have a robust AppleScript dictionary. Health and Fitness data access requires:

1. **Export from Health app** - Manual or via `healthexport` CLI tool
2. **Parse XML/CSV** - Health data is exported as XML or CSV files
3. **Query exported data** - Use standard tools to analyze exports

## Planned Implementation

### Method 1: healthexport CLI Tool

[healthexport](https://github.com/mgile/healthexport) is a community tool for exporting Apple Health data:

```bash
# Install healthexport
pip3 install healthexport

# Export all health data
healthexport ~/health-export/

# Export specific data types
healthexport --data-type StepCount ~/health-export/
healthexport --data-type HeartRate ~/health-export/
```

**Output**: CSV files with timestamps and values

### Method 2: Health.app Export

Manual export via Health app:
1. Open Health app
2. Profile → Export All Health Data
3. Generates `export.xml` file
4. Parse XML with standard tools

### Method 3: HealthKit Framework (Advanced)

Use Swift CLI tool with HealthKit framework:
- Requires Xcode and Swift development
- More powerful but complex setup
- Can query live data without export

## Planned Helper Scripts

### health-export

Export health data for specific timeframe and metrics:

```bash
health-export --days 7 --type steps,heart-rate ~/health-export/
```

### health-query

Query exported health data:

```bash
health-query ~/health-export/ --metric steps --days 7 --summary
health-query ~/health-export/ --metric heart-rate --date 2025-11-15
```

### fitness-summary

Activity and workout summaries:

```bash
fitness-summary --week         # This week's activity
fitness-summary --month        # This month's summary
fitness-summary --workouts 5   # Last 5 workouts
```

## Data Types Available

### Activity
- Steps
- Flights climbed
- Distance walked/run
- Active energy burned
- Exercise minutes

### Workouts
- Workout type
- Duration
- Distance (for running/walking/cycling)
- Calories burned
- Heart rate during workout

### Heart Rate
- Resting heart rate
- Walking heart rate
- Heart rate variability
- Heart rate during exercise

### Sleep
- Sleep duration
- Time asleep vs. time in bed
- Sleep stages (if available)

### Body Measurements
- Weight
- Height
- Body mass index (BMI)
- Body fat percentage

### Vitals
- Blood pressure
- Blood glucose
- Blood oxygen
- Respiratory rate

## Privacy & Security

Health data is **HIGHLY SENSITIVE**. This skill will be:

- **READ-ONLY** - No writing to Health app
- **EXPLICIT CONSENT** - Always ask before accessing health data
- **AGGREGATED DATA ONLY** - Summaries and trends, not raw detailed records
- **NO SHARING** - Health data never sent to external services

## Roadmap

### Phase 1: Export & Basic Queries (In Progress)

- [ ] Install and test `healthexport` tool
- [ ] Create helper scripts for common queries
- [ ] Document export process
- [ ] Test with actual Health app data

### Phase 2: Common Use Cases

- [ ] Weekly activity summaries
- [ ] Workout tracking and analysis
- [ ] Sleep pattern analysis
- [ ] Heart rate trend monitoring
- [ ] Weight tracking

### Phase 3: Advanced Features

- [ ] Live data queries (HealthKit framework)
- [ ] Trend analysis and insights
- [ ] Goal tracking
- [ ] Health correlations
- [ ] Export automation

## Examples (Planned)

### User: "How many steps did I take this week?"

```bash
health-query ~/health-export/ --metric steps --days 7 --summary
```

Response: "You took 45,234 steps this week, averaging 6,462 steps per day."

### User: "Show my recent workouts"

```bash
fitness-summary --workouts 5
```

Response:
- Nov 11: Running, 3.2 miles, 32 minutes
- Nov 9: Cycling, 10 miles, 45 minutes
- Nov 8: Strength training, 40 minutes
- Nov 6: Running, 5K, 28 minutes
- Nov 5: Walking, 2 miles, 35 minutes

### User: "What was my average heart rate yesterday?"

```bash
health-query ~/health-export/ --metric heart-rate --date 2025-11-14 --average
```

Response: "Your average heart rate yesterday was 72 bpm (resting: 65, max: 145)."

## Development Notes

### Testing Requirements

- Real Health app data with multiple data types
- Multiple export formats (XML, CSV)
- Various date ranges and queries
- Privacy-preserving aggregation

### Dependencies

- Python 3.x (for healthexport)
- SQLite (for local data cache)
- jq (for JSON parsing)

### Alternative: Fitness.app

Fitness.app has better AppleScript support than Health.app for Activity Ring data:

```applescript
tell application "Fitness"
    -- Query activity rings
    -- (Limited to current day only)
end tell
```

May be useful for real-time "close your rings" type queries.

## Status Updates

**2025-11-12**: Initial skill created, implementation in progress.
**Next**: Install and test `healthexport`, create first helper scripts.

## Related Skills

- `apple-productivity` - Calendar, Contacts, Mail, Messages, Reminders
- `apple-shortcuts` - Run macOS Shortcuts (could trigger Health exports)

---

**Current Status**: This skill is a placeholder for future development. Health data access is complex due to privacy restrictions and lack of direct API access. Implementation will proceed carefully with security and privacy as top priorities.
