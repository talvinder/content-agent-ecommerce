# 🔒 Security Guidelines

## API Key Management Best Practices

### ⚠️ Critical Security Issues to Avoid

1. **Never commit API keys to version control**
   - Even if you delete them later, they remain in git history
   - Automated tools scan public repositories for exposed keys
   - Compromised keys can lead to unauthorized usage and charges

2. **Don't hardcode keys in source code**
   - Keys should never appear in .py, .js, .yaml, or any source files
   - Use environment variables or secure secret management systems

### ✅ Recommended Approaches (in order of preference)

#### 1. Environment Variables (RECOMMENDED)

**Local Development:**
```bash
# Set for current session
export OPENAI_API_KEY='sk-your-actual-api-key-here'

# Make permanent (choose your shell)
# For bash:
echo 'export OPENAI_API_KEY="sk-your-key"' >> ~/.bashrc
source ~/.bashrc

# For zsh:
echo 'export OPENAI_API_KEY="sk-your-key"' >> ~/.zshrc
source ~/.zshrc
```

**Docker:**
```bash
# Method 1: Use host environment
export OPENAI_API_KEY='sk-your-key'
docker-compose up

# Method 2: Pass directly (testing only)
docker-compose run -e OPENAI_API_KEY='sk-your-key' content_agent

# Method 3: .env file (for docker-compose)
echo "OPENAI_API_KEY=sk-your-key" > .env
# Add .env to .gitignore!
```

#### 2. Secret Management Systems (PRODUCTION)

**Cloud Providers:**
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager
- HashiCorp Vault

**CI/CD Platforms:**
- GitHub Secrets
- GitLab CI Variables
- Jenkins Credentials
- Azure DevOps Variable Groups

#### 3. Config Files (DEVELOPMENT ONLY)

**Safe approach:**
```bash
# 1. Copy template
cp config.example.py config.py

# 2. Edit with your key
vim config.py  # or your preferred editor

# 3. Verify it's gitignored
git status  # config.py should NOT appear
```

**config.py structure:**
```python
# config.py (NEVER COMMIT THIS FILE)
OPENAI_API_KEY = "sk-your-actual-key-here"
```

### 🛡️ Implementation in Code

The application loads API keys in this order:

1. **Environment variable** (highest priority)
2. **config.py file** (fallback for development)
3. **Error with helpful instructions** (if none found)

```python
# From app/agent.py
def _load_api_key(self) -> str:
    # Method 1: Environment variable (RECOMMENDED)
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key
    
    # Method 2: config.py file (fallback)
    try:
        import config
        return config.OPENAI_API_KEY
    except ImportError:
        pass
    
    # No key found - show helpful error
    raise ValueError("API key not found. Use environment variable.")
```

### 🚨 What to Do If You Accidentally Commit an API Key

1. **Immediately revoke the key** at https://platform.openai.com/api-keys
2. **Generate a new API key**
3. **Remove the key from git history:**
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch config.py' \
     --prune-empty --tag-name-filter cat -- --all
   ```
4. **Force push to update remote history** (if working alone)
5. **Notify team members** to pull latest changes

### 🔍 Automated Security Scanning

**GitHub:**
- Enable secret scanning in repository settings
- Use dependabot for dependency vulnerabilities
- Add pre-commit hooks for secret detection

**Pre-commit Hook Example:**
```bash
# Install detect-secrets
pip install detect-secrets

# Initialize
detect-secrets scan --baseline .secrets.baseline

# Add to .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### 📋 Security Checklist

- [ ] API keys stored in environment variables
- [ ] `config.py` added to `.gitignore`
- [ ] No hardcoded secrets in source code
- [ ] Secret scanning enabled (if using GitHub)
- [ ] API key rotation plan in place
- [ ] Team members trained on security practices
- [ ] Production uses proper secret management system

### 🎓 Educational Notes for Workshop

This workshop demonstrates both:
- **What NOT to do** (config.py with real keys)
- **What TO do** (environment variables, proper practices)

The application gracefully handles multiple authentication methods while promoting secure practices through clear messaging and documentation.

### 📞 Getting Help

**If you're unsure about security:**
- Ask your team's security expert
- Consult your organization's security policies
- When in doubt, use environment variables
- Never share API keys in plain text (Slack, email, etc.)

**OpenAI Security Resources:**
- [API Key Safety](https://platform.openai.com/docs/guides/safety-best-practices)
- [Rate Limits and Usage](https://platform.openai.com/docs/guides/rate-limits)

---

**Remember: Security is everyone's responsibility! 🛡️** 