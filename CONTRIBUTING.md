# Contributing to Obscura

Thank you for your interest in contributing to Obscura! This document provides guidelines for contributing.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/Dasoam/Obscura.git
cd Obscura

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

## 📝 How to Contribute

### Reporting Bugs
1. Check if the issue already exists in [Issues](https://github.com/Dasoam/Obscura/issues)
2. If not, create a new issue using the bug report template
3. Include steps to reproduce, expected behavior, and screenshots if applicable

### Suggesting Features
1. Open a new issue using the feature request template
2. Describe the problem and proposed solution
3. Be open to discussion and feedback

### Submitting Code

1. **Fork** the repository
2. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test** your changes thoroughly
5. **Commit** with clear messages:
   ```bash
   git commit -m "Add: description of changes"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** against the `main` branch

## 🎨 Coding Standards

### Python
- Follow PEP 8 style guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

### Commits
- Use clear, descriptive commit messages
- Prefix with: `Add:`, `Fix:`, `Update:`, `Remove:`, `Refactor:`

### Privacy First
- **No telemetry or tracking**
- **No persistent storage** of user data
- **Fail closed** - if privacy can't be guaranteed, don't proceed

## 🏗️ Project Structure

See [STRUCTURE.md](STRUCTURE.md) for detailed project layout.

## 📜 License

By contributing, you agree that your contributions will be licensed under the MPL 2.0 License.

## 💬 Questions?

Open an issue with the `question` label.

---

Thank you for helping make Obscura better! 🔒
