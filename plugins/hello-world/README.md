# Hello World Plugin

Example plugin demonstrating the basic structure of a Claude Code plugin.

## Installation

```bash
/plugin install hello-world@g-shudy-plugins
```

## Commands

### `/hello`

Displays a friendly greeting and information about the g-shudy plugin marketplace.

**Usage:**
```
/hello
```

## Purpose

This plugin serves as:
- A template for creating new plugins
- A test to verify marketplace installation works correctly
- An example of the basic plugin structure

## Plugin Structure

```
hello-world/
├── .claude-plugin/
│   └── plugin.json       # Plugin metadata
├── commands/
│   └── hello.md          # Command definition
└── README.md             # This file
```

## Creating Your Own Plugin

Use this as a template:

1. Copy this directory structure
2. Update `plugin.json` with your plugin details
3. Add your commands/agents/skills
4. Update the README
5. Add to `marketplace.json`

## License

MIT
