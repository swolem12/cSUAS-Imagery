# Contributing to cSUAS-Imagery

Thank you for your interest in contributing to the cSUAS-Imagery project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

- Check if the issue already exists
- Provide detailed information about the problem
- Include system information (OS, Python version, etc.)
- Provide steps to reproduce the issue

### Suggesting Enhancements

- Clearly describe the enhancement
- Explain why it would be useful
- Consider compatibility with Raspberry Pi 5

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Test your changes thoroughly
5. Update documentation if needed
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cSUAS-Imagery.git
cd cSUAS-Imagery

# Setup environment
./scripts/setup_environment.sh

# Initialize submodules
./scripts/setup_submodules.sh

# Activate virtual environment
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
```

## Code Style

### Python

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

### C++

- Follow modern C++ practices (C++17)
- Use meaningful variable names
- Add comments for complex logic
- Use RAII for resource management

## Testing

- Test on Raspberry Pi 5 when possible
- Test with different model formats
- Test with various input sources (camera, video, images)
- Verify performance doesn't degrade

## Documentation

- Update README.md for new features
- Add comments to complex code
- Update configuration examples
- Include usage examples

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep first line under 50 characters
- Add detailed description if needed

Example:
```
Add YOLOv8 support for drone detection

- Implement YOLOv8DroneDetector class
- Add ultralytics dependency
- Update documentation with usage examples
```

## Model Contributions

If contributing trained models:

- Document training parameters
- Provide performance metrics
- Include dataset information
- Test on Raspberry Pi 5
- Consider model size and speed

## Dataset Contributions

If contributing datasets:

- Ensure proper licensing
- Provide dataset statistics
- Include annotation format
- Document collection methodology

## Questions?

Feel free to open an issue for any questions or concerns.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

Thank you for contributing!
