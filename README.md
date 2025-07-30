# GitHub CLI Read-Only Command Permissions for Claude Code

> **⚠️ Security Warning**: These permission templates grant Claude Code automated access to read private repository data through the GitHub CLI. Only use permissions you understand and trust. Consider the security implications of exposing your GitHub data to AI models. Double check each permission you enable on your own responsibility.

## 🎯 Purpose & Context

[Claude Code](https://claude.ai/code) is Anthropic's AI coding assistant that uses a permission system to control which commands it can execute. Adding permissions manually for each GitHub CLI command is **extremely time-consuming and tedious**. 

This repository provides **ready-to-use permission templates** for GitHub CLI (`gh`) commands that are safe to run as read-only operations. You can:

* 🚀 **Save hours** by using pre-configured permission sets instead of adding commands one-by-one
* 🔧 **Customize templates** to match your security needs (e.g., restrict to specific repos/orgs)
* 🛡️ **Maintain security** by only allowing read operations, preventing accidental modifications
* 📦 **Mix and match** permission sets for different workflows (issues, PRs, releases, etc.)

## 💡 How Claude Code Permissions Work

Claude Code requires explicit permissions to run commands that could access or modify your system. Permissions are configured in `settings.json` files with rules like:

```json
{
  "permissions": {
    "allow": [
      "Bash(gh pr list:*)",      // Allow listing PRs with any arguments
      "Bash(gh issue view:*)",    // Allow viewing issues
      "Bash(gh repo clone:*)"     // Allow cloning repos
    ],
    "deny": [
      "Bash(gh pr merge:*)"       // Explicitly deny PR merging
    ]
  }
}
```

Without these permissions, Claude Code will ask for approval every time it wants to run a GitHub CLI command, significantly slowing down your workflow.

## 🚦 Quick Start

1. **Choose permission sets** based on what you want Claude Code to access:
   - `gh-pr-readonly.json` - View and list pull requests
   - `gh-issue-readonly.json` - View and list issues
   - `gh-repo-readonly.json` - View repository information
   - `gh-all.json` - All read-only commands (comprehensive access)

2. **Merge with your Claude Code settings**:
   ```bash
   ./claude_settings_merger.py ~/.claude/settings.json gh-pr-readonly.json -o ~/.claude/settings.json
   ```

3. **Or manually add to your settings** by copying the `allow` entries from any JSON file into your `~/.claude/settings.json`

## Overview

This repository catalogs all GitHub CLI commands that are safe to execute without modifying any state - commands that only read, view, list, or download information without creating, updating, or deleting resources.

## Repository Contents

### Markdown Files

Individual command category files:
- `gh-auth-readonly.md` - Authentication status and token viewing commands
- `gh-browse-readonly.md` - Browser opening commands (inherently read-only)
- `gh-cache-readonly.md` - GitHub Actions cache listing commands
- `gh-gist-readonly.md` - Gist viewing and listing commands
- `gh-issue-readonly.md` - Issue viewing, listing, and status commands
- `gh-org-readonly.md` - Organization listing commands
- `gh-pr-readonly.md` - Pull request viewing, listing, and diff commands
- `gh-project-readonly.md` - Project viewing and listing commands
- `gh-release-readonly.md` - Release viewing and download commands
- `gh-repo-readonly.md` - Repository viewing and listing commands
- `gh-run-readonly.md` - Workflow run viewing and download commands
- `gh-workflow-readonly.md` - Workflow viewing and listing commands
- `gh-api-readonly.md` - API GET requests and GraphQL queries
- `gh-search-readonly.md` - Search commands for code, issues, PRs, etc.
- `gh-status-readonly.md` - Status display command
- `gh-other-readonly.md` - Miscellaneous read-only commands (config, extensions, etc.)

Combined files:
- `gh-all.md` - All unique read-only patterns sorted alphabetically
- `gh-readonly-combined.md` - Initial combined list (similar to gh-all.md)

### JSON Files

Permission configuration files generated from the markdown files. Each JSON file contains:
- Only the specific command patterns extracted from the corresponding markdown file
- Empty deny list
- No additional base permissions (keeping files minimal and focused)

### Python Scripts

- `md_to_json_converter.py` - Intelligently converts markdown pattern files to JSON permission configuration files
  - Extracts patterns from bullet points marked with `*` or `-` containing backtick-wrapped content
  - Ignores any lines that don't match the bullet point format
  - Creates minimal JSON files containing only the patterns from each markdown file

- `claude_settings_merger.py` - Merges multiple Claude settings.json files
  - Combines and deduplicates `allow` and `deny` permission lists
  - Preserves non-permission settings from the first input file
  - Supports glob patterns and multiple output formats
  - [Full documentation](claude_settings_merger.README.md)

## Data Generation Process

1. **Manual Page Analysis**: The GitHub CLI manual pages were analyzed using parallel sub-agents to identify read-only commands for each `gh` subcommand.

2. **Pattern Extraction**: Each sub-agent created a markdown file containing glob patterns in the format `Bash(gh command:*)` for commands that:
   - Only read, view, list, or display information
   - Download files locally without modifying remote state
   - Do not create, update, delete, or modify any resources

3. **Format Standardization**: All markdown files were processed to ensure consistent formatting with backticks around each pattern.

4. **JSON Generation**: The Python script converts markdown lists into JSON configuration files suitable for permission systems.

## Usage

### Running the Converter Script

```bash
python3 md_to_json_converter.py
```

This will:
1. Find all `gh-*.md` files in the current directory
2. Extract command patterns from properly formatted bullet points (lines starting with `*` or `-` containing backtick-wrapped content)
3. Create corresponding `.json` files with minimal permission structure
4. Include only the patterns found in each markdown file (no additional base permissions)

### Pattern Format

All patterns follow the glob format: `Bash(gh command subcommand:*)`

The `:*` suffix allows any additional arguments or flags to be passed to the command.

### Example Permission Usage

The generated JSON files can be used in permission systems to allow specific GitHub CLI commands while blocking potentially destructive operations. For example, `gh-pr-readonly.json` allows:
- `gh pr list` - List pull requests
- `gh pr view` - View pull request details
- `gh pr diff` - View changes

But blocks commands like `gh pr create`, `gh pr merge`, or `gh pr close`.

### Merging Settings Files

Use the `claude_settings_merger.py` tool to combine multiple permission files:

```bash
# Merge base settings with gh-specific permissions
./claude_settings_merger.py ~/.claude/settings.json gh-pr-readonly.json -o merged-settings.json

# Combine all gh permission files into one
./claude_settings_merger.py gh-*.json -o all-gh-permissions.json
```

## Total Commands Cataloged

- 102 unique read-only GitHub CLI command patterns identified
- Covering all major gh command categories
- Including API access patterns for GET requests only

## Related Work

- [dwillitzer/claude-settings](https://github.com/dwillitzer/claude-settings) - Comprehensive Claude Code configuration repository with over 900 development tool permissions covering Docker, Git, cloud providers, and more. While their repository provides a broad allow-list for general development tools, our repository specifically focuses on GitHub CLI read-only operations, making it easier for users to construct targeted permission sets for GitHub workflows.

Co-Authored by LLMs (Claude, GPTs).
