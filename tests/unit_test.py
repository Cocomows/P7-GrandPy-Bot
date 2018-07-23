# tests/unit_test.py
import pytest
from app import app

@pytest.fixture(scope='session')
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_home_page(client):

    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'GrandPy Bot' in html
    assert '<input' in html

def test_error_page(client):

    rsp = client.get('/error404')
    assert rsp.status == '404 NOT FOUND'
    html = rsp.get_data(as_text=True)
    assert "La page demandée n'a pas été trouvée" in html

