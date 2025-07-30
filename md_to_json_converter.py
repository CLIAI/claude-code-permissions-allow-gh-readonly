#!/usr/bin/env python3
"""
Convert markdown files with command patterns to JSON permission files.

This script reads markdown files containing bullet point lists (using * or - markers)
with backtick-wrapped command patterns and converts them to JSON files with a 
permissions structure. The script is intelligent enough to only extract content from
properly formatted bullet points with backticks.
"""

import json
import re
import os
import glob


def parse_markdown_file(filepath):
    """Parse a markdown file and extract command patterns from bullet points."""
    patterns = []
    
    with open(filepath, 'r') as f:
        for line in f:
            # Match lines that start with * or - and contain backtick-wrapped content
            # This regex matches both "* `content`" and "- `content`" formats
            match = re.match(r'^[\*\-]\s+`([^`]+)`', line.strip())
            if match:
                patterns.append(match.group(1))
    
    return patterns


def create_permissions_json(patterns):
    """Create the permissions JSON structure with only the patterns from the markdown file."""
    # Remove duplicates while preserving order
    seen = set()
    unique_permissions = []
    for perm in patterns:
        if perm not in seen:
            seen.add(perm)
            unique_permissions.append(perm)
    
    return {
        "permissions": {
            "allow": unique_permissions,
            "deny": []
        }
    }


def process_file(markdown_filepath):
    """Process a single markdown file and create corresponding JSON file."""
    # Extract patterns from markdown
    patterns = parse_markdown_file(markdown_filepath)
    
    # Create permissions structure
    permissions_data = create_permissions_json(patterns)
    
    # Create output filename by replacing .md with .json
    json_filepath = os.path.splitext(markdown_filepath)[0] + '.json'
    
    # Write JSON file
    with open(json_filepath, 'w') as f:
        json.dump(permissions_data, f, indent=2)
    
    print(f"Created {json_filepath} with {len(patterns)} patterns")
    return json_filepath


def main():
    """Main function to process all markdown files."""
    # Find all gh-*.md files in the current directory
    markdown_files = glob.glob('gh-*.md')
    
    if not markdown_files:
        print("No gh-*.md files found in the current directory")
        return
    
    print(f"Found {len(markdown_files)} markdown files to process")
    print("-" * 50)
    
    # Process each file
    created_files = []
    for md_file in sorted(markdown_files):
        try:
            json_file = process_file(md_file)
            created_files.append(json_file)
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    print("-" * 50)
    print(f"Successfully created {len(created_files)} JSON files")


if __name__ == "__main__":
    main()