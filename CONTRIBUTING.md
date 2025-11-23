# Contributing to StockSherlok

Thank you for your interest in contributing to StockSherlok! This document provides guidelines for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/StockSherlok-Using-AGI-openAI-Telnyx-and-Lovable.git
```

3. Set up the development environment:
```bash
./setup.sh
```

4. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the issue template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Enhancements

1. Check if the enhancement has been suggested
2. Explain the use case
3. Describe the proposed solution
4. Consider alternatives

### Code Contributions

We welcome contributions in these areas:

#### Backend
- New analysis algorithms
- Additional data sources
- Performance improvements
- Better error handling
- API enhancements

#### Frontend
- UI/UX improvements
- New visualizations
- Mobile responsiveness
- Accessibility features

#### Documentation
- Tutorials
- API documentation
- Deployment guides
- Code comments

#### Testing
- Unit tests
- Integration tests
- End-to-end tests

## Development Workflow

1. **Pick an Issue**: Look for issues labeled `good first issue` or `help wanted`

2. **Discuss**: Comment on the issue to let others know you're working on it

3. **Develop**: 
   - Write clean, readable code
   - Follow existing patterns
   - Add comments for complex logic
   - Update documentation

4. **Test**: Ensure all tests pass and add new tests for your changes

5. **Commit**: Use clear, descriptive commit messages

6. **Push**: Push to your fork

7. **Pull Request**: Open a PR with a clear description

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for functions and classes

Example:
```python
def analyze_company(ticker: str, company_name: Optional[str] = None) -> Dict:
    """
    Perform comprehensive company analysis.
    
    Args:
        ticker: Stock ticker symbol
        company_name: Optional company name
        
    Returns:
        Dictionary containing analysis results
    """
    pass
```

### JavaScript (Frontend)

- Use ES6+ features
- Follow Airbnb JavaScript Style Guide
- Use meaningful variable names
- Add JSDoc comments for complex functions

Example:
```javascript
/**
 * Analyze a company using the API
 * @param {string} ticker - Stock ticker symbol
 * @returns {Promise<Object>} Analysis results
 */
async function analyzeCompany(ticker) {
    // Implementation
}
```

### File Organization

- Keep files focused and single-purpose
- Use meaningful file and folder names
- Group related functionality

## Testing

### Backend Tests

Run Python tests:
```bash
cd backend
python -m pytest
```

### Frontend Tests

Run React tests:
```bash
cd frontend
npm test
```

### Writing Tests

- Test edge cases
- Test error handling
- Use descriptive test names
- Keep tests simple and focused

Example:
```python
def test_analyze_company_with_invalid_ticker():
    """Test that invalid ticker returns appropriate error"""
    result = research_agent.analyze_company("INVALID123")
    assert 'error' in result
```

## Submitting Changes

### Pull Request Process

1. **Update Documentation**: Update README, API docs, etc.

2. **Add Tests**: Ensure new features have tests

3. **Run Linters**: 
```bash
# Python
flake8 backend/

# JavaScript
cd frontend && npm run lint
```

4. **Create PR**: 
   - Use a clear title
   - Describe changes in detail
   - Reference related issues
   - Add screenshots for UI changes

5. **Code Review**: 
   - Address review comments
   - Keep discussion professional
   - Be open to feedback

### Commit Message Guidelines

Format:
```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Example:
```
feat(backend): add support for cryptocurrency analysis

- Add crypto data fetching
- Implement crypto-specific analysis
- Update API documentation

Closes #123
```

## Areas for Contribution

### High Priority
- [ ] Add unit tests for backend
- [ ] Implement caching layer
- [ ] Add more data sources
- [ ] Improve error handling
- [ ] Mobile UI optimization

### Medium Priority
- [ ] Add user authentication
- [ ] Implement portfolio tracking
- [ ] Add historical analysis
- [ ] Create data visualization dashboard
- [ ] Add email alerts

### Low Priority
- [ ] Dark mode support
- [ ] Export reports to PDF
- [ ] Add more chart types
- [ ] Internationalization
- [ ] Social sharing features

## Questions?

- Open an issue for discussion
- Join our community chat (if available)
- Read the documentation
- Check existing issues and PRs

## Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Part of a growing community

Thank you for contributing to StockSherlok! 🔍
