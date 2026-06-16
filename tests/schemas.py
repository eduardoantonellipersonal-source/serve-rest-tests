from jsonschema import validate

# Esquema para o Login
schema_login = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "authorization": {"type": "string"}
    },
    "required": ["message", "authorization"]
}

# Esquema para Usuários
schema_usuario = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"}
    },
    "required": ["message", "_id"]
}

# Esquema para Produtos
schema_produtos = {
    "type": "object",
    "properties": {
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "preco": {"type": "number"},
                    "descricao": {"type": "string"},
                    "quantidade": {"type": "number"},
                    "_id": {"type": "string"}
                }
            }
        }
    }
}