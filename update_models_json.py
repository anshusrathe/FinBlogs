#!/usr/bin/env python3
import os
import json
import re
import yaml
import datetime
import pathlib

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def extract_frontmatter(markdown_content):
    """Extract frontmatter from markdown content."""
    # Match content between --- and --- at the beginning of the text
    frontmatter_match = re.match(r'^---\s+(.*?)\s+---', markdown_content, re.DOTALL)
    if frontmatter_match:
        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
            return frontmatter
        except yaml.YAMLError as e:
            print(f"Error parsing frontmatter: {e}")
    return {}

def generate_link(file_name):
    """Generate a link for the markdown file."""
    # Remove the .md extension
    base_name = os.path.splitext(file_name)[0]
    
    # Convert to URL-friendly format (replace spaces with hyphens, lowercase)
    url_friendly = base_name.replace(' ', '-').lower()
    
    # Return the potential webpage URL with the repo name prefix
    return f"/FinBlogs/content/models/{url_friendly}"

def create_models_json():
    """Create or update models.json file based on markdown files in /content/models."""
    models_dir = os.path.join("content", "models")
    json_file_path = os.path.join("content", "models", "models.json")
    
    # Create the models directory if it doesn't exist
    os.makedirs(models_dir, exist_ok=True)
    
    # Initialize the models data
    models_data = []
    
    # Get all markdown files in the models directory
    markdown_files = [f for f in os.listdir(models_dir) if f.endswith('.md')]
    
    # Process each markdown file
    for file_name in markdown_files:
        file_path = os.path.join(models_dir, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Extract frontmatter
                frontmatter = extract_frontmatter(content)
                
                # Generate link
                link = generate_link(file_name)
                
                # Extract only the specified fields
                extracted_data = {
                    "file": file_name,
                    "title": frontmatter.get("title", ""),
                    "date": frontmatter.get("date", ""),
                    "category": frontmatter.get("category", ""),
                    "summary": frontmatter.get("summary", ""),
                    "link": link
                }
                
                models_data.append(extracted_data)
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
    
    # Sort models by date (newest first)
    models_data.sort(key=lambda x: str(x.get("date", "")), reverse=True)
    
    # Write to JSON file
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(models_data, json_file, indent=2, ensure_ascii=False, default=json_serial)
        print(f"Successfully updated {json_file_path}")
    except Exception as e:
        print(f"Error writing to {json_file_path}: {e}")

if __name__ == "__main__":
    create_models_json()