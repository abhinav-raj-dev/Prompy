# Prompy 🚀

**Your Privacy-First AI Prompt Optimizer**  
A Chrome extension that enhances AI prompts in real-time using local LLMs. Works across ChatGPT, Claude, Poe, and more.

![Prompy Demo](demo.gif) *Example: Optimizing a ChatGPT prompt*

## Features ✨
- 🔒 **100% Local** - No data leaves your device
- ⚡ **One-Click Optimization** - Rewrite prompts instantly
- 👔 **Multi-Profile Support** - Work/Personal modes
- 🧠 **Learning System** - Improves using your past prompts
- 🛡️ **Privacy Badge** - Visual data safety indicator

## Hardware Requirements
- Minimum: 4GB GPU (GTX 1650+) + 12GB RAM
- Recommended: 8GB GPU + 16GB RAM

## Tech Stack 🔧
| Component               | Technology                  |
|-------------------------|-----------------------------|
| Local LLM               | Mistral 7B 4-bit (GGUF)     |
| Backend                 | Rust + Actix-Web            |
| Storage                 | IndexedDB + HNSW Index      |
| ML Embeddings           | TinyBERT (TF.js)            |
| UI Framework            | Vanilla JS + CSS            |

## Installation 📦

### 1. Prerequisites
```bash
# Windows (WSL2)
wsl --install -d Ubuntu-22.04
choco install lmstudio
```

### 2. Backend Setup
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
git clone https://github.com/yourusername/prompy-backend
cd prompy-backend && cargo build --release
```

### 3. LLM Configuration
1. Download [Mistral-7B-Instruct-v0.2-Q4_K_M.gguf](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
2. Open in LM Studio → Enable GPU offloading (3.5GB)

### 4. Chrome Extension
```bash
git clone https://github.com/yourusername/prompy-extension
chrome://extensions → "Load unpacked"
```

## Usage 🖱️
1. Visit any AI chat interface (ChatGPT/Claude)
2. Start typing - look for the 🛡️ badge
3. Click to see optimized prompts
4. Choose profile (Work/Personal)

**Example Input → Output**  
`"Help me write a blog intro"` →  
```markdown
Act as technical writer for AI audience. 
Draft 3 intro variants for "Local LLMs in 2024" blog:
- Variant 1: Start with surprising statistic
- Variant 2: Pose rhetorical question
- Variant 3: Share personal anecdote
Keep under 100 words each. Use markdown.
```

## Customization 🎨
Edit `profiles/work.json`:
```json
{
  "tone": "professional",
  "goals": ["technical writing", "code examples"],
  "avoid": ["slang", "emoji"],
  "signature_phrases": ["As the data shows..."]
}
```

## Troubleshooting 🐞
| Issue                  | Solution                    |
|------------------------|-----------------------------|
| LM Studio not loading  | Use `--nvidia-smi` flag     |
| Rust build errors      | `rustup update stable`      |
| Inputs not detected    | Whitelist sites in manifest |

## Roadmap 🗺️
- [ ] Mobile companion app (iOS/Android)
- [ ] Team profile sharing
- [ ] Prompt version history
- [ ] Auto-suggest templates

## Contributing 🤝
PRs welcome! Follow our [contribution guidelines](CONTRIBUTING.md).

---

**Made with ❤️ by Abhinav Raj**  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

Let me know if you need adjustments to any section! For actual use:
1. Replace `yourusername` in git URLs
2. Add real demo.gif
3. Update license file
4. Include contribution guidelines
