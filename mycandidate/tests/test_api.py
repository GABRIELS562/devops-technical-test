import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_ward_candidates_returns_json(client):
    """Test that endpoint returns JSON with candidates"""
    response = client.get('/api/v1/wards/1/candidates')
    assert response.status_code == 200

    data = response.get_json()
    assert 'ward' in data
    assert 'count' in data
    assert 'candidates' in data
    assert data['ward'] == 'Ward 1'

def test_get_ward_candidates_structure(client):
    """Test that each candidate has required fields"""
    response = client.get('/api/v1/wards/1/candidates')
    data = response.get_json()

    if data['count'] > 0:
        candidate = data['candidates'][0]
        assert 'full_names' in candidate
        assert 'surname' in candidate
        assert 'party' in candidate
        assert 'age' in candidate
        assert 'gender' in candidate
        assert 'orderno' in candidate

def test_invalid_ward_returns_404(client):
    """Test that non-existent ward returns 404"""
    response = client.get('/api/v1/wards/999/candidates')
    assert response.status_code == 404

    data = response.get_json()
    assert 'error' in data
