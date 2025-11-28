---
name: apple-photos
description: Query Apple Photos library to find recent photos, get photo metadata, and access photo file paths. Use when user asks about recent photos, wants to find specific photos, or needs to access photo files.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Apple Photos Skill

Access photos from your macOS Photos library through direct database queries.

## Available Helper Scripts

### Photos

**`photos-query`** - Query Photos library for recent photos
```bash
photos-query                    # Last 10 photos (default)
photos-query --last             # Most recent photo only
photos-query -l 1               # Same as --last
photos-query -l 20              # Last 20 photos
photos-query -d 7               # Photos from last 7 days
photos-query -l 5 -j            # Last 5 photos as JSON
```

**Output includes**:
- Photo UUID
- Filename
- Date created
- Date added to library
- Full file path (if available)

**Note**: Works by querying Photos.sqlite database directly - does NOT require Photos.app to be running

## Common Patterns

### Find Recent Photos

```bash
# Most recent photo
photos-query --last

# Last 5 photos
photos-query -l 5

# Photos from last week
photos-query -d 7
```

### Get Photo File Path

```bash
# Get path to most recent photo for reading
photos-query --last -j | jq -r '.photos[0].filePath'
```

### Working with Photo Files

Once you have the file path, you can:
- Read the image with the Read tool
- Copy it to /tmp for processing
- Use `sips` to convert formats (HEIC → JPEG)

```bash
# Convert HEIC to JPEG for easier reading
sips -s format jpeg -s formatOptions 70 input.heic --out output.jpg
```

## Security & Privacy

### READ-ONLY (Safe - No Confirmation Needed)

- ✅ Querying photo metadata
- ✅ Getting photo file paths
- ✅ Reading photo files

### IMPORTANT PRIVACY NOTES

- Photos may contain **sensitive personal content**
- Photos may have **GPS coordinates** in EXIF data
- Always handle photo data with appropriate privacy
- **NEVER** upload or share photos without explicit user permission

**Rule**: Photos are personal data. Treat with maximum privacy and discretion.

## Technical Details

### Database Access

- Database: `~/Pictures/Photos Library.photoslibrary/database/Photos.sqlite`
- Main table: `ZASSET`
- Read-only access via SQLite
- Timestamps use Apple Core Data format (seconds since 2001-01-01)

### File Locations

Photos are stored in:
- Modern: `~/Pictures/Photos Library.photoslibrary/originals/{directory}/{filename}`
- Legacy: `~/Pictures/Photos Library.photoslibrary/Masters/{directory}/{filename}`

### Limitations

- **Read-only**: Cannot modify Photos library
- **No cloud photos**: Only locally available photos are accessible
- **No deleted photos**: Trashed photos are excluded
- **Large files**: High-resolution photos may need format conversion for reading
- **HEIC format**: macOS default format, may need conversion to JPEG for processing

## Examples

### User: "Show me my most recent photo"

```bash
photos-query --last -j
```

Parse JSON output and display photo metadata. If user wants to see the image, get the file path and read it.

### User: "What photos did I take today?"

```bash
photos-query -d 1
```

Show list of photos from last 24 hours.

### User: "Find my last 10 photos"

```bash
photos-query -l 10
```

List 10 most recent photos with dates and file paths.

### User: "I need to see the last photo in my library"

1. Get photo path:
```bash
photos-query --last -j
```

2. If HEIC format and too large, convert:
```bash
sips -s format jpeg -s formatOptions 70 /path/to/photo.heic --out /tmp/photo.jpg
```

3. Read the photo:
```bash
# Use Read tool on the JPEG
```

## Error Handling

### Photos Library Not Found

```bash
$ photos-query --last
Error: Could not find Photos library
# Exit code: 2
```

**Response**: Photos library might be in non-standard location or not set up.

### Database Access Error

```bash
$ photos-query
Error querying Photos library: unable to open database file
# Exit code: 2
```

**Response**: Database might be locked or corrupted. Try closing Photos.app if it's running.

### No Photos Found

```bash
$ photos-query -d 30
No photos found
```

**Response**: No photos match the query criteria.

## Tips

1. **Use JSON output** (`-j`) for programmatic access
2. **Convert large HEIC files** to JPEG before reading
3. **Check file paths** exist before trying to read
4. **Respect privacy** - photos are highly personal content
5. **Batch queries** - Get multiple photos at once rather than one-by-one

## Related Skills

- `apple-productivity` - Calendar, Contacts, Mail, Messages, Reminders
- `apple-health-fitness` - Health and Fitness data

---

**Remember**: This skill gives you READ access to personal photos. Handle all photo data with maximum privacy and discretion.
