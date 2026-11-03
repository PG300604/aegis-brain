# Contributing to AegisBrain 🧠✨

Thank you for your interest in contributing to AegisBrain! We welcome pull requests, bug reports, and architectural improvements.

---

## 🛠️ Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PG300604/aegis-brain.git
   cd aegis-brain
   ```

2. **Run tests:**
   AegisBrain has **zero external dependencies**! You can run tests out-of-the-box using the Python standard library:
   ```bash
   cd package
   python -m unittest tests/test_aegis.py
   ```

---

## 📐 Guidelines

- **Simplicity First**: Adhere to Karpathy simplicity principles — write surgical changes with minimal diffs and zero speculative complexity.
- **Zero External Runtime Dependencies**: Core AegisBrain runtime must run on standard Python 3.10+ without requiring `pip install`.
- **Pass All Tests**: Verify that unit tests pass in $< 2\text{ seconds}$ before submitting a pull request.
- **License Compliance**: All contributions are licensed under the GNU General Public License v3 (GPLv3).

---

## 📬 Submitting Changes

1. Create a feature branch: `git checkout -b your-feature-name`
2. Commit your changes: `git commit -m "Add descriptive feature"`
3. Push to your fork and submit a Pull Request.
