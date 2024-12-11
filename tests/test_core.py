"""Test core functionality of CLARA application."""
import pytest
from app import check_domain_security, generate_password

def test_homepage(client):
    """Test homepage loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'CLARA' in response.data
    assert b'Cybersecurity Learning And Risk Advisor' in response.data

def test_about_page(client):
    """Test about page loads correctly."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'How CLARA Helps' in response.data
    assert b'Why Digital Security Matters' in response.data

def test_privacy_checklist(client):
    """Test privacy checklist page loads correctly."""
    response = client.get('/privacy-checklist')
    assert response.status_code == 200
    assert b'Privacy Checklist' in response.data

def test_password_generation():
    """Test password generation functionality."""
    # Test default password generation
    password = generate_password(length=16, use_uppercase=True, 
                               use_lowercase=True, use_numbers=True, 
                               use_special=True)
    assert len(password) == 16
    assert any(c.isupper() for c in password)
    assert any(c.islower() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(not c.isalnum() for c in password)

    # Test password with specific requirements
    password = generate_password(length=12, use_uppercase=True, 
                               use_lowercase=True, use_numbers=False, 
                               use_special=False)
    assert len(password) == 12
    assert any(c.isupper() for c in password)
    assert any(c.islower() for c in password)
    assert not any(c.isdigit() for c in password)
    assert all(c.isalnum() for c in password)

def test_domain_security():
    """Test domain security check functionality."""
    result = check_domain_security("example.com")
    assert isinstance(result, dict)
    assert 'success' in result
    assert 'ssl_version' in result
    assert 'cipher_suite' in result
    assert 'certificate' in result

@pytest.mark.parametrize("test_input,expected", [
    ("example.com", True),
    ("invalid domain", False),
    ("test.example.com", False),
    ("", False),
    ("example.com/path", False),
])
def test_domain_validation(test_input, expected):
    """Test domain validation with various inputs."""
    result = check_domain_security(test_input)
    assert bool(result.get('success', False)) == expected
