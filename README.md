# CLARA (Cybersecurity Learning And Risk Advisor)

![CLARA Logo](static/images/Clara.jpeg)

Your trusted companion for digital security and privacy. A comprehensive toolkit that provides essential security tools and educational resources.

## Features

- **Password Generator**: Create strong, customizable passwords with real-time strength analysis
- **Password Strength Analyzer**: Get detailed security analysis of your passwords with specific recommendations
- **Security Glossary**: Learn about common security terms and concepts with authoritative references
- **Privacy Checklist**: Track and improve your privacy practices with exportable progress reports
- **Password Storage Guide**: Best practices for secure password management
- **Interactive UI**: Clean, responsive interface with intuitive controls

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Visit `http://localhost:5001` in your browser

## Key Components

### Security Glossary
- Comprehensive cybersecurity terminology
- Links to authoritative sources (NIST, IBM, Cisco, Fortinet, Cloudflare)
- Regular updates to maintain current information

### Privacy Checklist
- Interactive checklist with priority levels
- Progress tracking with visual indicators
- PDF export functionality for progress reports
- Detailed explanations for each security measure

### Password Tools
- Client-side password generation
- Customizable password criteria
- Real-time strength analysis
- Specific security recommendations

## Technical Details

Built with:
- **Backend**: Flask (Python web framework)
- **Frontend**: Modern HTML5, CSS3, JavaScript
- **PDF Generation**: jsPDF with autotable plugin
- **Security**: Client-side processing, no data storage
- **Design**: Mobile-responsive, dark theme UI

## Security Features

- No server-side data storage or tracking
- Client-side password generation and analysis
- Secure random number generation
- Educational resources from trusted sources
- Regular updates to security definitions and links

## Best Practices

The application promotes:
- Strong password creation and management
- Two-factor authentication adoption
- Regular security audits
- Privacy-conscious online behavior
- Continuous security education

## Deployment

### Local Development
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt  # For development/testing
   ```
3. Run the application:
   ```bash
   python app.py
   ```

### PythonAnywhere Deployment
1. Create a PythonAnywhere account
2. Upload the code or clone the repository
3. Create a virtual environment and install dependencies
4. Configure the WSGI file to point to app.py
5. Set up the web app configuration

## Testing

Run the test suite:
```bash
python -m pytest -v
```

Generate coverage report:
```bash
python -m pytest --cov=. --html=test-reports/report.html
```

## Version Control

We follow Semantic Versioning (SemVer):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes

Current version information can be found in `VERSION.md` and `version.py`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Write tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
