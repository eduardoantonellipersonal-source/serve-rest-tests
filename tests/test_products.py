import requests
import random

BASE_URL = "https://serverest.dev/produtos"

# Função auxiliar para pegar o token de admin
def get_admin_token():
    email = f"admin_{random.randint(1000, 9999)}@teste.com"
    requests.post("https://serverest.dev/usuarios", json={
        "nome": "Admin", "email": email, "password": "123", "administrador": "true"
    })
    resp = requests.post("https://serverest.dev/login", json={"email": email, "password": "123"})
    return resp.json()["authorization"]

def test_cadastrar_produto_com_token():
    token = get_admin_token()
    headers = {"authorization": token}
    produto = {
        "nome": f"Produto {random.randint(1, 1000)}",
        "preco": 100,
        "descricao": "Mouse",
        "quantidade": 10
    }
    
    resp = requests.post(BASE_URL, headers=headers, json=produto)
    assert resp.status_code == 201
    assert resp.json()["message"] == "Cadastro realizado com sucesso"

def test_cadastrar_produto_sem_token():
    produto = {"nome": "Produto Errado", "preco": 10, "descricao": "x", "quantidade": 1}
    resp = requests.post(BASE_URL, json=produto) # Sem passar headers para simular ausência de token
    
    assert resp.status_code == 401
    assert resp.json()["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"

def test_listar_produtos():
    resp = requests.get(BASE_URL)
    assert resp.status_code == 200
    assert "produtos" in resp.json()

def test_buscar_produto_por_id():
    token = get_admin_token()
    
    # 1. Nome aleatório para evitar conflitos
    nome_aleatorio = f"Produto Busca {random.randint(1000, 9999)}"
    
    # 2. Cadastro com verificação de sucesso
    resp_cadastro = requests.post(BASE_URL, headers={"authorization": token}, json={
        "nome": nome_aleatorio, "preco": 50, "descricao": "Teste", "quantidade": 5
    })
    
    # Se der erro aqui, a mensagem já nos mostra o porquê
    assert resp_cadastro.status_code == 201, f"Falha ao criar produto: {resp_cadastro.json()}"
    
    # Agora sim, pegamos o ID com segurança
    _id = resp_cadastro.json()["_id"]

    # 3. Busca pelo ID
    resp_busca = requests.get(f"{BASE_URL}/{_id}")
    assert resp_busca.status_code == 200
    assert resp_busca.json()["nome"] == nome_aleatorio
    
def test_atualizar_produto():
    token = get_admin_token()
    
    # 1. Cria o produto com nome ALEATÓRIO para evitar erro de duplicidade
    nome_aleatorio = f"Produto para Atualizar {random.randint(1000, 9999)}"
    
    id_produto = requests.post(BASE_URL, headers={"authorization": token}, json={
        "nome": nome_aleatorio, 
        "preco": 10, 
        "descricao": "x", 
        "quantidade": 1
    }).json()["_id"]

    # 2. Atualiza com nome ALEATÓRIO
    nome_atualizado = f"Produto Atualizado {random.randint(1000, 9999)}"
    
    resp = requests.put(f"{BASE_URL}/{id_produto}", headers={"authorization": token}, json={
        "nome": nome_atualizado, 
        "preco": 20, 
        "descricao": "y", 
        "quantidade": 2
    })
    
    assert resp.status_code == 200, f"Erro na atualização: {resp.json()}"
    assert resp.json()["message"] == "Registro alterado com sucesso"

def test_excluir_produto():
    token = get_admin_token()
    # 1. Cria o produto
    id_produto = requests.post(BASE_URL, headers={"authorization": token}, json={
        "nome": "Para Excluir", "preco": 5, "descricao": "z", "quantidade": 1
    }).json()["_id"]

    # 2. Exclui
    resp = requests.delete(f"{BASE_URL}/{id_produto}", headers={"authorization": token})
    assert resp.status_code == 200
    assert resp.json()["message"] == "Registro excluído com sucesso"    