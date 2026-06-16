import requests
import random
from jsonschema import validate
from schemas import schema_login

BASE_URL = "https://serverest.dev/login"

def test_login_com_sucesso():
    # 1. Gera um e-mail único e cadastra o usuário direto
    email = f"qa_{random.randint(1000, 9999)}@teste.com"
    requests.post("https://serverest.dev/usuarios", json={
        "nome": "QA Admin", "email": email, "password": "123", "administrador": "true"
    })
    
    # 2. Faz o login e valida
    resposta = requests.post(BASE_URL, json={"email": email, "password": "123"})
    dados = resposta.json()
    
    assert resposta.status_code == 200
    assert dados["message"] == "Login realizado com sucesso"
    assert "authorization" in dados
    
def test_login_com_senha_errada():
    payload = {
        "email": "fulano@qa.com.br",
        "password": "senha_totalmente_errada_123"
    }
    
    resposta = requests.post(BASE_URL, json=payload)
    dados = resposta.json()
    
    assert resposta.status_code == 401
    assert dados["message"] == "Email e/ou senha inválidos"

def test_login_com_email_inexistente():
    payload = {
        "email": "esse_email_nao_existe_mesmo_2026@qa.com",
        "password": "teste"
    }
    
    resposta = requests.post(BASE_URL, json=payload)
    dados = resposta.json()
    
    assert resposta.status_code == 401
    assert dados["message"] == "Email e/ou senha inválidos"

def test_login_com_campos_vazios():
    payload = {
        "email": "",
        "password": ""
    }
    
    resposta = requests.post(BASE_URL, json=payload)
    dados = resposta.json()
    
    assert resposta.status_code == 400
    assert dados["email"] == "email não pode ficar em branco"
    assert dados["password"] == "password não pode ficar em branco"

def test_validar_schema_login():
    resp = requests.post(f"{BASE_URL}/login", json={"email": "beltrano@qa.com", "password": "teste"})
    validate(instance=resp.json(), schema=schema_login) # Se a estrutura estiver errada, o teste falha aqui!
    assert resp.status_code == 200    