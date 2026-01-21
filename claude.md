# Claude Project Memory: Adversarial Spec Plugin

**Last Updated:** 2026-01-13
**Purpose:** Configuration and usage guide for the adversarial-spec skill in this repository

---

## 🔧 Critical Project Settings

### Python Environment
- **ALWAYS use `uv` for Python commands in this project**
- Never use `pip` or `python3` directly
- Example: `uv run python script.py` or `uv run --with package python script.py`

### API Keys Location
- **Path:** `/Users/ciaran/GIT/adversarial-spec_plugin/.env` (note: `.env` is in project root, not `skills/`)
- **Available Keys:**
  - `GEMINI_API_KEY` - Google Gemini API
  - `OPENAI_API_KEY` - OpenAI API (check quota before use)
  - Other keys may be commented out (XAI, Mistral, Groq, Deepseek)

### Adversarial Spec Skill Location
- **Base Directory:** `/Users/ciaran/.claude/plugins/cache/adversarial-spec/adversarial-spec/1.0.0/skills/adversarial-spec/`
- **Debate Script:** `scripts/debate.py`
- **Dependencies:** Requires `litellm` package (installed via `uv run --with litellm`)

---

## 📁 Project Structure

```
/Users/ciaran/GIT/adversarial-spec_plugin/
├── .env                              # API keys (READ THIS FOR KEYS!)
├── claude.md                         # This file - project memory
├── README.md                         # Project documentation
├── skills/
│   └── .env                         # OLD location (deprecated, use root .env)
├── site_speed/                      # Project folder (example)
├── gemini/                          # Project folder (example)
├── technical_seo/                   # Project folder (example)
└── ADVERSARIAL-SPEC-SUMMARY.md     # General adversarial spec info
```

---

## 🚀 How to Run Adversarial Debate

### Standard Command Template

```bash
# Load environment variables and run debate
set -a && \
source /Users/ciaran/GIT/adversarial-spec_plugin/.env && \
set +a && \
cd /Users/ciaran/.claude/plugins/cache/adversarial-spec/adversarial-spec/1.0.0/skills/adversarial-spec && \
uv run --with litellm python scripts/debate.py critique \
  --models gpt-4o,gemini/gemini-2.0-flash \
  --doc-type prd \
  --round 1 \
  < /path/to/spec-file.md
```

### Key Parameters Explained

- `--models`: Comma-separated list of models to use for critique
  - Available: `gpt-4o`, `gemini/gemini-2.0-flash`, `deepseek/deepseek-chat`, `xai/grok-3`, `groq/llama-3.3-70b-versatile`
  - Requires corresponding API key in `.env`

- `--doc-type`: Document type being reviewed
  - `prd` - Product Requirements Document
  - `tech` - Technical Specification

- `--round`: Current round number (1, 2, 3, etc.)

### Check Available Providers

```bash
cd /Users/ciaran/.claude/plugins/cache/adversarial-spec/adversarial-spec/1.0.0/skills/adversarial-spec && \
uv run --with litellm python scripts/debate.py providers
```

---

## ⚠️ Known Issues & Blockers

### Current Blockers
1. **OpenAI API Quota Exceeded**
   - Error: "You exceeded your current quota, please check your plan and billing details"
   - Action Required: Add credits at https://platform.openai.com/settings/organization/billing
   - Impact: Cannot run gpt-4o in debate until resolved

### API Key Format Notes
- OpenAI project keys (`sk-proj-...`) work correctly
- Previous key was just `proj-...` which failed
- Current key is correct format

---

## 📝 Common Commands Reference

### Check API Provider Status
```bash
cd /Users/ciaran/.claude/plugins/cache/adversarial-spec/adversarial-spec/1.0.0/skills/adversarial-spec && \
uv run --with litellm python scripts/debate.py providers
```

### Run Next Round (Generic Template)
```bash
set -a && \
source /Users/ciaran/GIT/adversarial-spec_plugin/.env && \
set +a && \
cd /Users/ciaran/.claude/plugins/cache/adversarial-spec/adversarial-spec/1.0.0/skills/adversarial-spec && \
uv run --with litellm python scripts/debate.py critique \
  --models gpt-4o,gemini/gemini-2.0-flash \
  --doc-type prd \
  --round 1 \
  < /path/to/your/document.md
```

### Check Git Status
```bash
cd /Users/ciaran/GIT/adversarial-spec_plugin && git status
```

---

## 🎓 Lessons Learned

### What Works Well
1. **Two models sufficient:** Gemini + Claude critique provides thorough review
2. **Round structure:** 2-3 rounds typically enough for convergence
3. **Specific definitions:** Defining terms like "typical site" eliminates ambiguity
4. **Multiple implementation options:** Plugin, code, hosting choices serve all user types
5. **Accessibility early:** Adding WCAG requirements upfront prevents retrofitting

### What to Watch For
1. **API quotas:** Check OpenAI billing before starting debates
2. **Model agreement:** Early agreement may indicate models didn't read carefully (use `--press` flag)
3. **Vague acceptance criteria:** Always define subjective terms (e.g., "plain English")
4. **Privacy details:** Anonymized data collection needs explicit HOW/WHERE/RETENTION
5. **Tool specifications:** Don't just say "use static analysis" - specify WHICH tool and WHEN

---

## 📚 Reference Links

### Adversarial Spec Documentation
- **Skill Base:** `/Users/ciaran/.claude/plugins/cache/adversarial-spec/adversarial-spec/1.0.0/skills/adversarial-spec/SKILL.md`
- **Project Summary:** `/Users/ciaran/GIT/adversarial-spec_plugin/ADVERSARIAL-SPEC-SUMMARY.md`

### External Resources
- OpenAI Platform: https://platform.openai.com
- Google AI Studio: https://aistudio.google.com
- LiteLLM Documentation: https://docs.litellm.ai/

---

## 🔄 Next Session Checklist

When resuming adversarial spec work in a new Claude session:

1. ✅ Read this `claude.md` file first
2. ✅ Check API key status: `cat /Users/ciaran/GIT/adversarial-spec_plugin/.env`
3. ✅ Verify OpenAI billing if using gpt models: https://platform.openai.com/settings/organization/billing
4. ✅ Review the specific document being worked on (PRD, tech spec, etc.)
5. ✅ Check which round of debate you're on
6. ✅ Remember to use `uv` for all Python commands
7. ✅ Source environment from project root `.env`, not `skills/.env`

---

## 💡 Quick Tips

- **Always** source `.env` from project root: `/Users/ciaran/GIT/adversarial-spec_plugin/.env`
- **Never** run Python commands without `uv run` in this project
- **Check** provider status before running debates to avoid wasted time
- **Save** debate output when it's large (it auto-saves to temp files)
- **Track** rounds carefully - Gemini sometimes doesn't include proper `[SPEC]` tags in responses
- **Incorporate** feedback incrementally - don't batch multiple rounds without showing user

---

## 📞 Contact & Support

- **OpenAI Issues:** https://platform.openai.com/docs/guides/error-codes
- **Gemini Issues:** https://ai.google.dev/gemini-api/docs
- **LiteLLM Docs:** https://docs.litellm.ai/

---

## 📌 Important Reminders

**Adversarial Debate Role:** Claude (you) is an active participant in the debate, not just an orchestrator. Always provide your own independent critique alongside opponent model feedback.

**Environment:** Always use `uv` for Python commands in this repository. Always source API keys from `/Users/ciaran/GIT/adversarial-spec_plugin/.env` (project root).

**End of Configuration Guide**
