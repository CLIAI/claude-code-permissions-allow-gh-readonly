#!/usr/bin/env python3
"""
Claude Settings Merger - Merge multiple Claude settings.json files.

This tool merges permission lists from multiple Claude settings JSON files,
combining and deduplicating the allow and deny lists while preserving other
settings from the first file.
"""

import json
import argparse
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Any


def load_json_file(filepath: Path) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def merge_permission_lists(lists: List[List[str]]) -> List[str]:
    """Merge multiple permission lists, removing duplicates while preserving order."""
    seen = set()
    result = []
    
    for permission_list in lists:
        for item in permission_list:
            if item not in seen:
                seen.add(item)
                result.append(item)
    
    return result


def merge_settings_files(files: List[Path]) -> Dict[str, Any]:
    """Merge multiple Claude settings files."""
    if not files:
        raise ValueError("No files provided to merge")
    
    # Load all files
    settings_list = [load_json_file(f) for f in files]
    
    # Start with the first file as base
    merged = settings_list[0].copy()
    
    # Extract all allow and deny lists
    allow_lists = []
    deny_lists = []
    
    for settings in settings_list:
        permissions = settings.get('permissions', {})
        if 'allow' in permissions:
            allow_lists.append(permissions['allow'])
        if 'deny' in permissions:
            deny_lists.append(permissions['deny'])
    
    # Merge the permission lists
    if 'permissions' not in merged:
        merged['permissions'] = {}
    
    merged['permissions']['allow'] = merge_permission_lists(allow_lists)
    merged['permissions']['deny'] = merge_permission_lists(deny_lists)
    
    return merged


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Merge multiple Claude settings.json files by combining their permission lists.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s settings1.json settings2.json -o merged.json
  %(prog)s base.json gh-*.json -o complete-settings.json
  %(prog)s *.json --output final-settings.json
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='Claude settings JSON files to merge (at least one required)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output file path (default: print to stdout)'
    )
    
    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help='JSON indentation spaces (default: 2)'
    )
    
    parser.add_argument(
        '--compact',
        action='store_true',
        help='Output compact JSON without indentation'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create *.bak backup when output file exists'
    )

    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Alias for --no-backup'
    )
    
    args = parser.parse_args()
    
    # Expand any glob patterns in file arguments
    expanded_files = []
    for file_pattern in args.files:
        if '*' in str(file_pattern):
            # Handle glob patterns
            matching_files = list(Path('.').glob(str(file_pattern)))
            if not matching_files:
                print(f"Warning: No files match pattern '{file_pattern}'", file=sys.stderr)
            expanded_files.extend(matching_files)
        else:
            expanded_files.append(file_pattern)
    
    if not expanded_files:
        print("Error: No files to merge", file=sys.stderr)
        sys.exit(1)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for f in expanded_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)
    
    # Merge the files
    print(f"Merging {len(unique_files)} files...", file=sys.stderr)
    merged = merge_settings_files(unique_files)
    
    # Prepare output
    if args.compact:
        output = json.dumps(merged, separators=(',', ':'))
    else:
        output = json.dumps(merged, indent=args.indent)
    
    # Write output
    if args.output:
        # Create backup if destination exists and backups are enabled
        if args.output.exists() and not (args.no_backup or args.force):
            backup_path = args.output.with_suffix(args.output.suffix + '.bak')
            if backup_path.exists():
                idx = 1
                while True:
                    candidate = args.output.with_suffix(args.output.suffix + f'.bak.{idx}')
                    if not candidate.exists():
                        backup_path = candidate
                        break
                    idx += 1
            shutil.copy2(args.output, backup_path)
            print(f"Created backup '{backup_path}'", file=sys.stderr)

        with open(args.output, 'w') as f:
            f.write(output)
            f.write('\n')  # Add trailing newline
        print(f"Successfully wrote merged settings to '{args.output}'", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
