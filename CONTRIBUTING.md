# Contributing to Pneumonia Diagnosis AI

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior vs actual behavior
- Your environment (OS, Python version, TensorFlow version)
- Screenshots or logs if applicable

### Suggesting Enhancements

We welcome suggestions for:
- New features
- Performance improvements
- Better documentation
- Additional visualizations
- Model architecture improvements

Please create an issue with:
- A clear description of the enhancement
- Why this would be useful
- Examples or mockups if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style guidelines
3. **Add tests** if you're adding functionality
4. **Update documentation** (README, docstrings, comments)
5. **Ensure all tests pass**
6. **Submit a pull request**

### Code Style Guidelines

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and small

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be a concise summary (50 chars or less)
- Add detailed description if needed in the body

Example:
```
Add Grad-CAM visualization for model predictions

- Implement grad_cam function in utils/gradcam.py
- Add overlay functionality for heatmap visualization
- Update README with usage examples
```

### Development Setup

1. Clone your fork:
```bash
git clone https://github.com/yourusername/pneumonia-diagnosis-ai.git
cd pneumonia-diagnosis-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

4. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

### Testing

Before submitting a PR:
- Test your changes thoroughly
- Ensure the notebook runs end-to-end without errors
- Verify that model training completes successfully
- Check that all visualizations generate correctly

### Documentation

When adding new features:
- Update the README.md
- Add docstrings to new functions
- Include usage examples
- Update the requirements.txt if needed

### Medical AI Ethics

This project involves medical AI. Please ensure:
- No patient data is committed to the repository
- All medical claims are properly referenced
- Code changes maintain or improve model explainability
- Safety and validation considerations are documented

## Questions?

Feel free to open an issue with the `question` label if you need help or clarification.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone, regardless of:
- Age, body size, disability, ethnicity, gender identity and expression
- Level of experience, education, socio-economic status
- Nationality, personal appearance, race, religion, or sexual identity and orientation

### Our Standards

Positive behavior includes:
- Being respectful and inclusive
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

Unacceptable behavior includes:
- Harassment, trolling, or discriminatory comments
- Publishing others' private information
- Any conduct that could reasonably be considered inappropriate

### Enforcement

Project maintainers have the right to remove, edit, or reject:
- Comments, commits, code, issues, and other contributions
- That do not align with this Code of Conduct

Thank you for helping make this project better! 🎉
