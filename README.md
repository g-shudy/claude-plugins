# g-shudy Claude Plugins

Personal Claude Code plugin marketplace for workflow automation, file intelligence, and productivity tools.

🌐 **Website**: [plugins.ghsj.me](https://plugins.ghsj.me)
📦 **GitHub**: [g-shudy/claude-plugins](https://github.com/g-shudy/claude-plugins)
👤 **Author**: [ghsj.me](https://ghsj.me)

## Installation

### Add this marketplace to Claude Code

```bash
/plugin marketplace add g-shudy/claude-plugins
```

### Install plugins

```bash
# List available plugins
/plugin list g-shudy-plugins

# Install a specific plugin
/plugin install <plugin-name>@g-shudy-plugins
```

## Available Plugins

*Coming soon! Plugins will be added as they're developed.*

## Plugin Development

This marketplace follows the [Claude Code plugin specification](https://docs.claude.com/en/docs/claude-code/plugins).

### Structure

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace catalog
├── plugins/
│   └── <plugin-name>/        # Individual plugins
│       ├── .claude-plugin/
│       │   └── plugin.json   # Plugin metadata
│       ├── commands/         # Slash commands
│       ├── agents/           # AI agents
│       ├── skills/           # Agent skills
│       └── README.md         # Plugin documentation
├── docs/                     # GitHub Pages site
└── README.md
```

### Adding a New Plugin

1. Create plugin directory structure
2. Add plugin metadata to `marketplace.json`
3. Document in plugin's `README.md`
4. Test locally
5. Submit PR or push directly

## About

Personal plugin collection by [g-shudy](https://github.com/g-shudy) focused on:

- **File Intelligence**: Tools for media file management, deduplication, and provenance tracking
- **Workflow Automation**: Personal productivity and GTD workflows
- **Obsidian Integration**: Knowledge management and note-taking automation
- **Developer Tools**: Custom utilities for software development

## License

Individual plugins may have their own licenses. Check each plugin's directory for details.

## Resources

- **Claude Code Documentation**: https://docs.claude.com/en/docs/claude-code/
- **Plugin Guide**: https://docs.claude.com/en/docs/claude-code/plugins
- **Main Website**: https://ghsj.me

---

*Built with Claude Code • Hosted on GitHub Pages*
