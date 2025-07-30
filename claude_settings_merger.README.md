# Claude Settings Merger

A command-line tool for merging multiple Claude settings.json files, combining their permission lists while preserving other configuration options.

## Overview

The Claude Settings Merger intelligently combines `allow` and `deny` permission lists from multiple Claude settings files, automatically deduplicating entries while preserving the order of first appearance. Non-permission settings (like `model`) are preserved from the first input file.

## Installation

Ensure you have Python 3.6 or later installed. The script has no external dependencies beyond the Python standard library.

```bash
chmod +x claude_settings_merger.py
```

## Usage

```bash
./claude_settings_merger.py [OPTIONS] FILE1 FILE2 [FILE3 ...]
```

### Options

- `-o, --output FILE` - Write output to FILE instead of stdout
- `--indent N` - Set JSON indentation to N spaces (default: 2)
- `--compact` - Output compact JSON without indentation
- `-h, --help` - Show help message and exit

### Examples

#### Basic Usage

Merge two settings files and output to stdout:
```bash
./claude_settings_merger.py settings1.json settings2.json
```

#### Output to File

Merge multiple files and save to a new file:
```bash
./claude_settings_merger.py base-settings.json gh-readonly.json -o merged-settings.json
```

#### Using Glob Patterns

Merge all JSON files matching a pattern:
```bash
./claude_settings_merger.py base.json gh-*.json -o complete-settings.json
```

#### Compact Output

Generate minified JSON output:
```bash
./claude_settings_merger.py settings1.json settings2.json --compact -o merged.json
```

## How It Works

1. **File Loading**: The tool loads all specified JSON files, expanding glob patterns if used
2. **Permission Extraction**: Extracts `allow` and `deny` lists from the `permissions` object in each file
3. **Deduplication**: Combines all `allow` lists into one, removing duplicates while preserving the order of first appearance. Same process for `deny` lists
4. **Settings Preservation**: Non-permission settings from the first file are preserved in the output
5. **Output Generation**: Creates a properly formatted JSON file with merged permissions

## Example Scenario

Given two files:

**settings1.json:**
```json
{
  "permissions": {
    "allow": ["Read", "Write", "Bash(git:*)"],
    "deny": ["Bash(rm:*)"]
  },
  "model": "opus"
}
```

**settings2.json:**
```json
{
  "permissions": {
    "allow": ["Write", "Edit", "Bash(gh pr list:*)"],
    "deny": ["Bash(rm:*)", "Bash(sudo:*)"]
  }
}
```

Running:
```bash
./claude_settings_merger.py settings1.json settings2.json -o merged.json
```

Produces **merged.json:**
```json
{
  "permissions": {
    "allow": ["Read", "Write", "Bash(git:*)", "Edit", "Bash(gh pr list:*)"],
    "deny": ["Bash(rm:*)", "Bash(sudo:*)"]
  },
  "model": "opus"
}
```

Note how:
- `"Write"` appears only once despite being in both files
- Order is preserved based on first appearance
- The `"model"` setting from the first file is retained

## Error Handling

The tool provides clear error messages for common issues:
- File not found
- Invalid JSON syntax
- No files matching glob pattern
- Empty file list

## Use Cases

1. **Combining Base and Specific Permissions**: Merge a base settings file with tool-specific permissions
2. **Team Settings Management**: Combine team-wide settings with project-specific permissions
3. **Modular Permission Management**: Build complex permission sets from smaller, focused permission files
4. **Settings Migration**: Merge old and new settings files during configuration updates

## Tips

- Always review the merged output before using it
- Use the `--indent` option for human-readable output
- The first file's non-permission settings take precedence
- Glob patterns are expanded by the tool, not the shell