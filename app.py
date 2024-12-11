import flask
import secrets
import ssl
import socket
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import math

app = flask.Flask(__name__)

def check_domain_security(domain):
    """Check domain security settings"""
    try:
        # Create SSL context with secure configuration
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_3
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Explicitly disable TLS 1.0 and 1.1
        
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # Get SSL/TLS version
                ssl_version = ssock.version()
                
                # Get cipher being used
                cipher = ssock.cipher()
                
                return {
                    'success': True,
                    'ssl_version': ssl_version,
                    'cipher_suite': cipher[0],
                    'certificate': {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'notBefore': cert['notBefore'],
                        'notAfter': cert['notAfter']
                    }
                }
                
    except ssl.SSLError as e:
        return {
            'success': False,
            'error': f'SSL Error: {str(e)}'
        }
    except socket.gaierror:
        return {
            'success': False,
            'error': 'Could not resolve domain'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def analyze_password_strength(password):
    """Analyze password strength with detailed feedback"""
    analysis = {
        'score': 0,
        'length': len(password),
        'has_uppercase': any(c.isupper() for c in password),
        'has_lowercase': any(c.islower() for c in password),
        'has_numbers': any(c.isdigit() for c in password),
        'has_special': any(not c.isalnum() for c in password),
        'criteria_met': {
            'length': len(password) >= 12,
            'uppercase': any(c.isupper() for c in password),
            'lowercase': any(c.islower() for c in password),
            'numbers': any(c.isdigit() for c in password),
            'special': any(not c.isalnum() for c in password),
            'no_common_patterns': True  # Will be updated below
        },
        'patterns_found': [],
        'recommendations': [],
        'entropy': 0
    }
    
    # Length check
    if analysis['length'] < 8:
        analysis['recommendations'].append('Password is too short. Minimum length is 8 characters.')
        analysis['patterns_found'].append('Password is too short')
    elif analysis['length'] >= 12:
        analysis['score'] += 25
        
    # Character type checks
    if analysis['has_uppercase']:
        analysis['score'] += 15
    else:
        analysis['recommendations'].append('Add uppercase letters for stronger password.')
        
    if analysis['has_lowercase']:
        analysis['score'] += 15
    else:
        analysis['recommendations'].append('Add lowercase letters for stronger password.')
        
    if analysis['has_numbers']:
        analysis['score'] += 20
    else:
        analysis['recommendations'].append('Add numbers for stronger password.')
        
    if analysis['has_special']:
        analysis['score'] += 25
    else:
        analysis['recommendations'].append('Add special characters for stronger password.')
    
    # Check for common patterns
    common_patterns = [
        ('123', 'Sequential numbers'),
        ('abc', 'Sequential letters'),
        ('qwerty', 'Keyboard pattern'),
        ('password', 'Common word'),
        ('admin', 'Common word'),
    ]
    
    lower_password = password.lower()
    for pattern, message in common_patterns:
        if pattern in lower_password:
            analysis['patterns_found'].append(f'Contains {message.lower()}')
            analysis['score'] -= 10
            analysis['criteria_met']['no_common_patterns'] = False
    
    # Calculate entropy
    char_set_size = 0
    if analysis['has_lowercase']: char_set_size += 26
    if analysis['has_uppercase']: char_set_size += 26
    if analysis['has_numbers']: char_set_size += 10
    if analysis['has_special']: char_set_size += 32
    
    if char_set_size > 0:
        analysis['entropy'] = len(password) * math.log2(char_set_size)
    
    # Final score adjustments
    analysis['score'] = max(0, min(100, analysis['score']))
    
    # Set strength label
    if analysis['score'] >= 80:
        analysis['strength_label'] = 'Very Strong'
    elif analysis['score'] >= 60:
        analysis['strength_label'] = 'Strong'
    elif analysis['score'] >= 40:
        analysis['strength_label'] = 'Moderate'
    elif analysis['score'] >= 20:
        analysis['strength_label'] = 'Weak'
    else:
        analysis['strength_label'] = 'Very Weak'
    
    return analysis

def get_password_managers():
    """Get comparison data for password managers"""
    return {
        'password_managers': [
            {
                'name': 'Bitwarden',
                'type': 'Cloud-based',
                'price': 'Free / $10 per year',
                'features': [
                    'Cross-platform sync',
                    'Secure password sharing',
                    'Two-factor authentication',
                    'End-to-end encryption',
                    'Password generator'
                ],
                'security_features': [
                    'Zero-knowledge encryption',
                    'Regular third-party security audits',
                    'GDPR compliant',
                    'SOC 2 Type 2 certified',
                    'Bug bounty program'
                ],
                'pros': [
                    'Free tier is feature-rich',
                    'Open source code',
                    'Regular security audits',
                    'Cross-platform support'
                ],
                'cons': [
                    'Web interface could be more intuitive',
                    'Mobile app can be slow sometimes',
                    'Limited customer support on free tier'
                ]
            },
            {
                'name': '1Password',
                'type': 'Cloud-based',
                'price': '$2.99 per month',
                'features': [
                    'Travel mode',
                    'Family sharing',
                    'Secure document storage',
                    'Multiple vaults',
                    'Watch Tower security'
                ],
                'security_features': [
                    'Secret key system',
                    'AES-256 bit encryption',
                    'Biometric authentication',
                    'Secure remote password'
                ],
                'pros': [
                    'Polished user interface',
                    'Travel mode for border crossing',
                    'Excellent customer support',
                    'Strong security model'
                ],
                'cons': [
                    'No free tier',
                    'More expensive than competitors',
                    'No password inheritance feature'
                ]
            },
            {
                'name': 'KeePassXC',
                'type': 'Local',
                'price': 'Free',
                'features': [
                    'Local storage',
                    'Cross-platform',
                    'Password generator',
                    'Auto-type',
                    'Hardware key support'
                ],
                'security_features': [
                    'AES-256 encryption',
                    'ChaCha20 cipher',
                    'Argon2 key derivation',
                    'KDBX 4.0 format',
                    'YubiKey support'
                ],
                'pros': [
                    'Completely free',
                    'Open source',
                    'No cloud dependency',
                    'Very secure'
                ],
                'cons': [
                    'Manual sync required',
                    'Steeper learning curve',
                    'Less convenient than cloud solutions'
                ]
            }
        ],
        'best_practices': [
            {
                'category': 'Use Unique Passwords',
                'tips': [
                    'Never reuse passwords across different accounts',
                    'Use randomly generated passwords when possible',
                    'Longer passwords (12+ characters) are better than complex short ones',
                    'Avoid using personal information in passwords'
                ]
            },
            {
                'category': 'Enable Two-Factor Authentication',
                'tips': [
                    'Use 2FA whenever available, especially for critical accounts',
                    'Prefer authenticator apps over SMS for 2FA',
                    'Keep backup codes in a secure location',
                    'Consider hardware security keys for maximum protection'
                ]
            },
            {
                'category': 'Regular Password Updates',
                'tips': [
                    'Change passwords if a service reports a data breach',
                    'Update critical account passwords every 3-6 months',
                    'Use your password manager\'s security monitoring features',
                    'Check haveibeenpwned.com regularly'
                ]
            },
            {
                'category': 'Secure Master Password',
                'tips': [
                    'Make your master password long and memorable',
                    'Never share your master password with anyone',
                    'Consider using a passphrase instead of a password',
                    'Store master password recovery info securely'
                ]
            }
        ]
    }

def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_numbers=True, use_special=True):
    """Generate a secure random password"""
    if length < 1:
        raise ValueError("Password length must be at least 1")
        
    if not any([use_uppercase, use_lowercase, use_numbers, use_special]):
        raise ValueError("At least one character type must be selected")
        
    chars = ''
    if use_lowercase:
        chars += 'abcdefghijklmnopqrstuvwxyz'
    if use_uppercase:
        chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if use_numbers:
        chars += '0123456789'
    if use_special:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
    return ''.join(secrets.choice(chars) for _ in range(length))

@app.route('/')
def index():
    """Render the main page"""
    return flask.render_template('index.html')

@app.route('/roadmap')
def roadmap():
    """Render the roadmap page"""
    return flask.render_template('roadmap.html')

@app.route('/about')
def about():
    """Render the about page"""
    return flask.render_template('about.html')

@app.route('/api/analyze-password', methods=['POST'])
def analyze_password():
    """Analyze password strength"""
    data = flask.request.get_json()
    if not data or 'password' not in data:
        return flask.jsonify({'error': 'No password provided'}), 400
        
    password = data['password']
    analysis = analyze_password_strength(password)
    return flask.jsonify(analysis)

@app.route('/api/check-domain', methods=['POST'])
def check_domain():
    """Check domain security"""
    data = flask.request.get_json()
    if not data or 'domain' not in data:
        return flask.jsonify({'error': 'No domain provided'}), 400
        
    domain = data['domain']
    results = check_domain_security(domain)
    return flask.jsonify(results)

@app.route('/password-storage-guide')
def password_storage_guide():
    """Render the password storage guide page"""
    return flask.render_template('password-storage-guide.html')

@app.route('/api/password-manager-data')
def password_manager_data():
    """Get password manager comparison data"""
    managers = get_password_managers()
    return flask.jsonify(managers)

@app.route('/privacy-checklist')
def privacy_checklist():
    """Render the privacy checklist page"""
    return flask.render_template('privacy-checklist.html')

@app.route('/security-glossary')
def security_glossary():
    """Render the security glossary page"""
    return flask.render_template('security-glossary.html')

@app.route('/password-generator')
def password_generator_page():
    """Render the password generator page"""
    return flask.render_template('password-generator.html')

@app.route('/api/generate-password', methods=['POST'])
def generate_password_api():
    """Generate a password based on user criteria"""
    data = flask.request.get_json()
    
    # Set defaults if not provided
    length = int(data.get('length', 12))
    use_uppercase = data.get('uppercase', True)
    use_lowercase = data.get('lowercase', True)
    use_numbers = data.get('numbers', True)
    use_special = data.get('special', True)
    
    try:
        password = generate_password(
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_numbers=use_numbers,
            use_special=use_special
        )
        return flask.jsonify({'password': password})
    except ValueError as e:
        return flask.jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
