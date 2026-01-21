# Adversarial Spec Plugin

## Commands
- `uv run --no-project --with litellm --with python-dotenv python check_apis.py`: Test API keys (OpenAI, Gemini)
- `uv run --with litellm python skills/adversarial-spec/scripts/debate.py providers`: List available LLM providers
- `uv add <package>`: Add dependency (when using uv project mode)

## Python Environment
- **Always use `uv`** for Python commands in this project
- Never use `pip` or `python3` directly
- Use `--no-project` flag to avoid pyproject.toml errors

## API Configuration
- API keys stored in `.env` (project root)
- See [Issue #1](https://github.com/ciaranq/adversarial-spec/issues/1) for API setup docs
- Current status: Gemini ✅ working, OpenAI ❌ needs billing credits

## Key Files
- `check_apis.py`: Validates API keys for OpenAI & Gemini
- `.env`: API keys (gitignored, never commit)
- `skills/adversarial-spec/`: Plugin skill directory

## Project Notes
- This repo contains the plugin/agent files, not the Python package
- pyproject.toml has naming issues - use `--no-project` when running scripts
- Client secret files (`*client_secret*.json`) are gitignored for security