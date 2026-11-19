import os, pytest
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def app(tmp_path):
    # Set TEST_DATABASE_URL only for a disposable PostgreSQL integration database.
    return create_app(os.getenv('TEST_DATABASE_URL') or str(tmp_path/'test.db'))

@pytest.fixture
def client(app):
    with TestClient(app) as c:
        data=c.get('/api/session').json()
        c.headers['X-CSRF-Token']=data['csrf']
        yield c

@pytest.fixture
def place_data():
    return {'label':'Minha casa de teste','street':'Rua Exemplo A','number':'120','neighborhood':'Jardim Exemplo A','city':'Cidade Exemplo','state':'SP','postal_code':'00000-001','zone':'TESTE-A','chuva':True,'calor':True,'consent':True,'synthetic':True}
