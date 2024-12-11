"""Test version functionality of CLARA application."""
import pytest
from version import VERSION_INFO

def test_version_endpoint(client):
    """Test version API endpoint."""
    response = client.get('/api/version')
    assert response.status_code == 200
    data = response.get_json()
    assert 'version' in data
    assert 'date' in data
    assert 'stage' in data
    assert data['version'] == VERSION_INFO['version']

def test_version_format():
    """Test version string format."""
    version = VERSION_INFO['version']
    # Should match format: 0.1.0-alpha
    parts = version.split('-')
    assert len(parts) == 2
    version_numbers = parts[0].split('.')
    assert len(version_numbers) == 3
    assert all(n.isdigit() for n in version_numbers)
    assert parts[1] in ['alpha', 'beta']

def test_version_in_about_page(client):
    """Test version information appears in about page."""
    response = client.get('/about')
    assert response.status_code == 200
    assert VERSION_INFO['version'].encode() in response.data
    assert VERSION_INFO['date'].encode() in response.data
