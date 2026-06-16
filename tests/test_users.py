import requests
import uuid
from jsonschema import validate
from schemas import schema_usuario

# URL base
BASE_URL = "https://compassuol.serverest.dev/usuarios"

# Função auxiliar que serve para gerar um email que nunca vai se repetir         
# Ela pega a palavra 'qa_', adiciona um código aleatório ao lado e termina com '@teste.com'
# Isso evita erros do tipo "email já existente" nos testes de cadastro
def gerar_email_dinamico():
    codigo_aleatorio = uuid.uuid4().hex[:8] # Gera 8 caracteres aleatórios
    return f"qa_{codigo_aleatorio}@teste.com"

def test_listar_usuarios_com_sucesso():
    # 1. FAZ A REQUISIÇÃO (GET)
    resposta = requests.get(BASE_URL)
    
    # 2. GUARDA O CORPO DA RESPOSTA (JSON)
    dados = resposta.json()
    
    # 3. ASSERTS (Validações)
    # Verifica se a API respondeu com 200 (OK)
    assert resposta.status_code == 200
    
    # Verifica a estrutura: se as chaves 'quantidade' e 'usuarios' existem na resposta
    assert "quantidade" in dados
    assert "usuarios" in dados
    
    # Verifica se a lista de usuários é realmente uma lista
    assert isinstance(dados["usuarios"], list)

def test_cadastrar_usuario_valido_com_sucesso():
    # 1. PREPARA OS DADOS (Payload)
    payload = {
        "nome": "Eduardo Testador",
        "email": gerar_email_dinamico(), # Chama a função para não dar erro de e-mail duplicado
        "password": "senha_segura",
        "administrador": "true"
    }
    
    # 2. FAZ A REQUISIÇÃO (POST)
    resposta = requests.post(BASE_URL, json=payload)
    dados = resposta.json()

    # 3. ASSERTS 
    # Verifica se a API respondeu com 201 (Created - Criado com sucesso)
    assert resposta.status_code == 201
    
    # Verifica a mensagem exata retornada pela API
    assert dados["message"] == "Cadastro realizado com sucesso"
    
    # Verifica se a API devolveu um ID para o usuário recém criado
    assert "_id" in dados

def test_tentar_cadastrar_usuario_com_email_ja_existente():
    # 1. CRIA UM USUÁRIO VÁLIDO PRIMEIRO
    email_repetido = gerar_email_dinamico()
    payload = {
        "nome": "Paulo Duplicado",
        "email": email_repetido, 
        "password": "senha",
        "administrador": "true"
    }
    # Faz o primeiro POST 
    requests.post(BASE_URL, json=payload)
    
    # 2. TENTA CADASTRAR DE NOVO COM O MESMO PAYLOAD (Mesmo email)
    resposta_falha = requests.post(BASE_URL, json=payload)
    dados_falha = resposta_falha.json()
    
    # 3. ASSERTS
    # Deve retornar 400 
    assert resposta_falha.status_code == 400
    assert dados_falha["message"] == "Este email já está sendo usado"        

def test_tentar_cadastrar_usuario_sem_email():
    # 1. PREPARA DADOS FALTANDO O EMAIL
    payload = {
        "nome": "Usuário Sem Email",
        "password": "senha",
        "administrador": "true"
    }
    
    # 2. FAZ A REQUISIÇÃO
    resposta = requests.post(BASE_URL, json=payload)
    
    dados = resposta.json()
    
    # 3. ASSERTS
    assert resposta.status_code == 400
    assert "email" in dados 
    assert dados["email"] == "email é obrigatório"

def test_tentar_cadastrar_usuario_sem_senha():
    # 1. PREPARA DADOS FALTANDO A SENHA
    payload = {
        "nome": "Usuário Sem Senha",
        "email": gerar_email_dinamico(),
        "administrador": "true"
    }
    
    # 2. FAZ A REQUISIÇÃO
    resposta = requests.post(BASE_URL, json=payload)
    dados = resposta.json()
    
    # 3. ASSERTS
    assert resposta.status_code == 400
    assert "password" in dados
    assert dados["password"] == "password é obrigatório"

def test_buscar_usuario_por_id_com_sucesso():
    # 1. CRIA O USUÁRIO PRIMEIRO PARA TER UM ID VÁLIDO
    payload = {
        "nome": "Busca ID",
        "email": gerar_email_dinamico(),
        "password": "123",
        "administrador": "true"
    }
    criacao = requests.post(BASE_URL, json=payload).json()
    id_usuario = criacao["_id"] # Guarda o ID gerado
    
    # 2. FAZ A BUSCA POR ESSE ID ESPECÍFICO (GET)
    # A URL fica em: https://compassuol.serverest.dev/usuarios/AQUI_VAI_O_ID
    resposta = requests.get(f"{BASE_URL}/{id_usuario}")
    dados = resposta.json()
    
    # 3. ASSERTS
    assert resposta.status_code == 200
    assert dados["_id"] == id_usuario # Garante que trouxe o usuário certo

def test_buscar_usuario_por_id_inexistente():
    # 1. TENTA BUSCAR UM ID QUE NÃO EXISTE
    id_falso = "0000000000000000" 
    
    resposta = requests.get(f"{BASE_URL}/{id_falso}")
    dados = resposta.json()
    
    # 2. ASSERTS
    assert resposta.status_code == 400
    assert dados["message"] == "Usuário não encontrado"

def test_atualizar_usuario_com_sucesso():
    # 1. CRIA O USUÁRIO INICIAL
    payload_inicial = {
        "nome": "Antes da Atualizacao",
        "email": gerar_email_dinamico(),
        "password": "123",
        "administrador": "true"
    }
    criacao = requests.post(BASE_URL, json=payload_inicial).json()
    id_usuario = criacao["_id"]
    
    # 2. PREPARA OS NOVOS DADOS
    payload_atualizado = {
        "nome": "Depois da Atualizacao", # Nome mudou
        "email": gerar_email_dinamico(), # Novo email dinâmico
        "password": "321",               # Senha mudou
        "administrador": "false"         # Permissão mudou
    }
    
    # 3. FAZ A REQUISIÇÃO DE ATUALIZAÇÃO (PUT)
    resposta = requests.put(f"{BASE_URL}/{id_usuario}", json=payload_atualizado)
    dados = resposta.json()
    
    # 4. ASSERTS
    assert resposta.status_code == 200
    assert dados["message"] == "Registro alterado com sucesso"

def test_excluir_usuario_com_sucesso():
    # 1. CRIA O USUÁRIO PARA DELETAR
    payload = {
        "nome": "Usuario para Deletar",
        "email": gerar_email_dinamico(),
        "password": "123",
        "administrador": "true"
    }
    criacao = requests.post(BASE_URL, json=payload).json()
    id_usuario = criacao["_id"]
    
    # 2. EXCLUI O USUÁRIO (DELETE)
    resposta = requests.delete(f"{BASE_URL}/{id_usuario}")
    dados = resposta.json()
    
    # 3. ASSERTS
    assert resposta.status_code == 200
    assert dados["message"] == "Registro excluído com sucesso"

def test_tentar_excluir_usuario_inexistente():
    # 1. TENTA DELETAR UM ID FALSO
    id_falso = "id_falso_para_deletar"
    resposta = requests.delete(f"{BASE_URL}/{id_falso}")
    dados = resposta.json()
    
    # 2. ASSERTS
    # O ServeRest retorna 200 mesmo quando não deleta nada, mas a mensagem muda
    assert resposta.status_code == 200
    assert dados["message"] == "Nenhum registro excluído"                

def test_validar_schema_usuario():
    # ... código do request ...
    resp = requests.post(...)
    
    # Valida usando o schema que está no arquivo schemas.py
    validate(instance=resp.json(), schema=schema_usuario)
    
    assert resp.status_code == 201 