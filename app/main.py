#!/usr/bin/env python3
"""
E-commerce Content-Agent Bot (Workshop Edition)
Main CLI orchestrator for generating e-commerce content using LLMs.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add the app directory to Python path to enable imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import ContentAgent

def load_product_data(product_file_path):
    """Load and validate product data from JSON file."""
    try:
        with open(product_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Successfully loaded product data from {product_file_path}")
        return data
    except FileNotFoundError:
        print(f"❌ Error: Product file '{product_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{product_file_path}': {e}")
        sys.exit(1)

def load_prompt_template(template_name):
    """Load prompt template from templates directory."""
    # Construct template file path
    template_path = Path(__file__).parent / "templates" / f"{template_name}.txt"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        print(f"✓ Successfully loaded template '{template_name}'")
        return template_content
    except FileNotFoundError:
        print(f"❌ Error: Template file '{template_path}' not found.")
        print(f"Available templates should be in: {Path(__file__).parent / 'templates'}")
        sys.exit(1)

def save_output(content, output_file_path):
    """Save generated content to file."""
    try:
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Output saved to: {output_file_path}")
    except Exception as e:
        print(f"⚠️  Warning: Could not save to '{output_file_path}': {e}")

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="E-commerce Content-Agent Bot - Generate engaging product content using LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app/main.py --product_file data/sample_product.json --template_name description_prompt
  python app/main.py --product_file data/sample_product.json --template_name seo_snippets --output_file outputs/seo_content.txt
        """
    )
    
    parser.add_argument(
        '--product_file',
        type=str,
        required=True,
        help='Path to the input product JSON file'
    )
    
    parser.add_argument(
        '--template_name', 
        type=str,
        required=True,
        help='Name of the prompt template file (without .txt extension)'
    )
    
    parser.add_argument(
        '--output_file',
        type=str,
        help='Optional: Path to save the generated content'
    )
    
    args = parser.parse_args()
    
    print("🚀 E-commerce Content-Agent Bot (Workshop Edition)")
    print("=" * 50)
    
    # Load product data
    print("📦 Loading product data...")
    product_data = load_product_data(args.product_file)
    
    # Handle both single product and list of products
    if isinstance(product_data, list):
        if len(product_data) == 0:
            print("❌ Error: Product file contains an empty list.")
            sys.exit(1)
        print(f"📱 Found {len(product_data)} products. Processing the first one...")
        product = product_data[0]
    else:
        product = product_data
    
    print(f"📱 Processing product: {product.get('name', 'Unknown Product')}")
    
    # Load prompt template
    print("📝 Loading prompt template...")
    prompt_template = load_prompt_template(args.template_name)
    
    # Initialize and use the Content Agent
    print("🤖 Initializing Content Agent...")
    try:
        agent = ContentAgent()
        print("✓ Content Agent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing Content Agent: {e}")
        sys.exit(1)
    
    # Generate content
    print(f"⚡ Generating content using template '{args.template_name}'...")
    try:
        generated_content = agent.generate_content(product, prompt_template)
        print("✓ Content generation completed!")
    except Exception as e:
        print(f"❌ Error during content generation: {e}")
        sys.exit(1)
    
    # Output results
    print("\n" + "=" * 50)
    print("📄 GENERATED CONTENT:")
    print("=" * 50)
    print(generated_content)
    print("=" * 50)
    
    # Save to file if specified
    if args.output_file:
        save_output(generated_content, args.output_file)
    
    print("\n✅ Content generation completed successfully!")

if __name__ == "__main__":
    main() 