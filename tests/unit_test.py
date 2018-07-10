# tests/unit_test.py
import pytest
from app import app

@pytest.fixture(scope='session')
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_page(client):

    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert 'Hello world' in html
