# E-commerce Content-Agent Bot (Workshop Edition)

An AI-powered content generation bot that transforms structured product data into engaging e-commerce content using Large Language Models (LLMs). Built for the 91mobiles AI-Powered Product Growth Accelerator workshop.

## 🎯 Project Overview

This application demonstrates how to:
- Use LLMs as "agents" for content generation
- Engineer effective prompts for e-commerce content
- Structure AI applications with clean, modular code
- Package AI applications with Docker for easy deployment
- Work with structured product data and persona-driven content

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ecommerce-content-agent
```

### 2. 🔒 Configure API Key (SECURE METHODS)

**Method 1: Environment Variable (RECOMMENDED)**
```bash
# Set for current session
export OPENAI_API_KEY='sk-your-actual-api-key-here'

# Add to your shell profile for persistence
echo 'export OPENAI_API_KEY="sk-your-actual-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Method 2: Docker Environment (RECOMMENDED)**
```bash
# Set environment variable for Docker
export OPENAI_API_KEY='sk-your-actual-api-key-here'
```

**Method 3: Config File (Development Only)**
```bash
# Copy template and edit with your key
cp config.example.py config.py
# Edit config.py with your API key
# ⚠️ WARNING: Never commit config.py to version control!
```

### 3. Build and Run with Docker

**Using Environment Variables (RECOMMENDED):**
```bash
# Build the Docker image
docker-compose build

# Set your API key in environment
export OPENAI_API_KEY='sk-your-actual-api-key-here'

# Generate product description
docker-compose run content_agent python app/main.py \
  --product_file data/sample_product.json \
  --template_name description_prompt

# Generate SEO snippets
docker-compose run content_agent python app/main.py \
  --product_file data/sample_product.json \
  --template_name seo_snippets

# Save output to file
docker-compose run content_agent python app/main.py \
  --product_file data/sample_product.json \
  --template_name description_prompt \
  --output_file outputs/product_description.txt
```

**Alternative: Pass API key directly (for testing):**
```bash
docker-compose run -e OPENAI_API_KEY='your-key' content_agent python app/main.py \
  --product_file data/sample_product.json \
  --template_name description_prompt
```

### 4. Run Locally (Alternative)

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY='sk-your-actual-api-key-here'

# Run the application
python app/main.py --product_file data/sample_product.json --template_name description_prompt
```

## 📁 Project Structure

```
ecommerce-content-agent/
├── app/
│   ├── main.py              # CLI orchestrator
│   ├── agent.py             # ContentAgent class with LLM integration
│   └── templates/           # Prompt templates
│       ├── description_prompt.txt
│       └── seo_snippets.txt
├── data/
│   └── sample_product.json  # Sample product data
├── outputs/                 # Generated content (created automatically)
├── config.example.py       # Configuration template (safe to commit)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Docker orchestration
└── README.md             # This file
```

**Note:** `config.py` is gitignored and should never be committed!

## 🛠 Usage

### Command Line Interface

```bash
python app/main.py [OPTIONS]

Options:
  --product_file PATH     Path to product JSON file (required)
  --template_name NAME    Template name without .txt extension (required)
  --output_file PATH      Optional: Save output to file
  --help                  Show help message
```

### Available Templates

1. **description_prompt** - Generates engaging product descriptions
2. **seo_snippets** - Creates SEO-optimized content elements

### Sample Product Data Format

```json
{
  "id": "SKU123",
  "name": "Galaxy Stellaris Pro",
  "brand": "Samsung",
  "price_inr": 69999,
  "display": {
    "type": "Dynamic AMOLED 2X",
    "size_inches": 6.7,
    "resolution": "3088 x 1440"
  },
  "camera": {
    "rear_primary_mp": 108,
    "rear_secondary_mp": [12, 10, 10],
    "front_mp": 40
  },
  "processor": "Snapdragon 8 Gen X",
  "ram_gb": 12,
  "storage_gb": 256,
  "battery_mah": 5000,
  "key_features": [
    "Advanced Nightography Camera",
    "120Hz Adaptive Refresh Rate Display",
    "S-Pen Support (Optional)",
    "5G Connectivity"
  ],
  "brief_description": "Experience the next level of mobile technology..."
}
```

## 🎨 Creating Custom Templates

Templates use placeholder syntax with curly braces. You can access nested data using dot notation:

```
Product Name: {name}
Display Type: {display.type}
Camera: {camera.rear_primary_mp}MP
Features: {key_features}
```

To create a new template:

1. Create a `.txt` file in `app/templates/`
2. Use placeholder syntax for dynamic content
3. Run with `--template_name your_template_name`

## 🔧 Advanced Configuration

### LLM Parameters

The ContentAgent supports various OpenAI parameters:

```python
agent.generate_content(
    product_data,
    prompt_template,
    llm_model="gpt-3.5-turbo",  # or "gpt-4"
    temperature=0.7,            # Creativity (0.0-2.0)
    max_tokens=500             # Response length
)
```

### Error Handling

The application handles common errors gracefully:
- Missing or invalid API keys
- File not found errors
- JSON parsing errors
- API rate limits and authentication issues

## 🔒 Security Best Practices

### ✅ DO:
- **Use environment variables** for API keys
- Set `OPENAI_API_KEY` in your shell environment
- Use Docker environment variables
- Add `config.py` to `.gitignore`
- Use `config.example.py` as a template

### ❌ DON'T:
- **Never commit API keys** to version control
- Don't hardcode keys in source code
- Don't share API keys in chat/email
- Don't commit `config.py` with real keys

### 🛡️ API Key Management Methods (by preference):

1. **Environment Variables (BEST)**
   ```bash
   export OPENAI_API_KEY='sk-your-key'
   ```

2. **CI/CD Secrets (Production)**
   - GitHub Secrets
   - GitLab CI Variables
   - AWS Secrets Manager
   - Azure Key Vault

3. **Local Config File (Development only)**
   ```bash
   cp config.example.py config.py
   # Edit config.py (never commit this file)
   ```

## 📝 Workshop Learning Objectives

This project demonstrates:

1. **Prompt Engineering**: How to structure effective prompts for content generation
2. **LLM Integration**: Programmatic interaction with OpenAI's API
3. **Agent Architecture**: Simple but effective AI agent design
4. **Docker Packaging**: Containerization for consistent environments
5. **Data Structure**: Working with structured product data
6. **Security**: Proper API key management and secure coding practices

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: No OpenAI API key found!
   ```
   **Solutions:**
   - Set environment variable: `export OPENAI_API_KEY='your-key'`
   - Create config.py from config.example.py
   - Pass key via Docker: `docker-compose run -e OPENAI_API_KEY='your-key' ...`

2. **Template Not Found**
   ```
   Error: Template file 'app/templates/template_name.txt' not found
   ```
   **Solution:** Check template name and ensure file exists

3. **Docker Permission Issues**
   ```
   Permission denied
   ```
   **Solution:** Ensure Docker daemon is running and you have proper permissions

4. **Rate Limit Errors**
   ```
   Rate limit exceeded
   ```
   **Solution:** Wait a moment and try again, or upgrade your OpenAI plan

## 🤝 Contributing

This is a workshop project, but contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Security Note:** Never include real API keys in pull requests!

## 📄 License

This project is created for educational purposes as part of the 91mobiles AI workshop.

## 🎓 Next Steps

After completing this workshop, consider exploring:

- Multiple LLM providers (Anthropic, Cohere, etc.)
- Multi-step agent workflows
- Web interfaces with Streamlit or Flask
- Database integration for product catalogs
- Advanced prompt engineering techniques
- Production deployment strategies
- Secrets management systems (HashiCorp Vault, AWS Secrets Manager)

---

**Happy coding! 🚀** 