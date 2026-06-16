# 📝 Plano de Testes - API ServeRest

## 1. Objetivo da Suíte

Garantir a qualidade e estabilidade da API ServeRest, validando regras de negócio, fluxos de autenticação (JWT) e operações CRUD nos endpoints de usuários, login e produtos.

## 2. Estratégia

- **Tipo de Teste:** Testes funcionais de API (Caixa Preta).
- **Camada:** Integração / Serviços (HTTP).
- **Ferramentas:** Python 3, Pytest, Requests.

## 3. Escopo

- **Coberto:**
  - Gestão de Usuários (CRUD completo).
  - Autenticação e geração de token (Login).
- **Não Coberto:**
  - Testes de carga/performance.
  - Endpoint de carrinhos.
  - Testes de interface (UI).

## 4. Cenários a Implementar

### Endpoint `/usuarios`

- [x] Listar usuários (sucesso)
- [x] Cadastrar usuário (sucesso/erro)
- [x] Buscar usuário por ID (sucesso/inexistente)
- [x] Atualizar usuário (sucesso)
- [x] Excluir usuário (sucesso/inexistente)

### Endpoint `/login`

- [x] Login com credenciais corretas (sucesso + token)
- [x] Login com senha errada
- [x] Login com email inexistente
- [x] Login com campos vazios

### Endpoint `/produtos`

- [ ] Listar produtos
- [ ] Cadastrar produto com token de admin
- [ ] Cadastrar produto sem token de admin
- [ ] Buscar produto por ID
- [ ] Atualizar produto
- [ ] Excluir produto

## 5. Critérios de Qualidade

- **Isolamento:** Dados devem ser criados dinamicamente no setup de cada teste.
- **Independência:** O teste não deve depender do sucesso de outro.
- **Validação:** Mínimo de 1 _assert_ para status code e 1 _assert_ para o corpo da resposta (JSON).
- **Limpeza:** Nenhum teste deve deixar lixo no banco (uso de IDs gerados no ato).
