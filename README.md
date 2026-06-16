# Desafio ServeRest - Automação de API

Este projeto contém a suíte de testes automatizados para a API [ServeRest](https://serverest.dev/), focada em garantir a qualidade e a estabilidade dos endpoints de Usuários, Login e Produtos.

## 🚀 Como rodar os testes

Para executar a suíte de testes em sua máquina, siga os passos abaixo:

1. **Clone o repositório:**

   ```bash
   git clone [https://github.com/eduardoantonellipersonal-source/serve-rest-tests](https://github.com/eduardoantonellipersonal-source/serve-rest-tests)
   cd serve-rest-tests
   ```

2. **Crie um ambiente virtual (recomendado):**

   ```bash
   python -m venv venv

   # No Windows:

   venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install pytest requests pytest-cov
   ```

4. Execute os testes:

   Para rodar todos os testes e visualizar a cobertura no terminal:

   ```bash
   pytest --cov=.
   ```

## 📊 Relatório de Cobertura de Testes

Método Utilizado: Utilizamos a biblioteca pytest-cov, que monitora a execução do código durante os testes, rastreando quais linhas foram percorridas pela suíte. O cálculo é realizado comparando as linhas de código exercitadas pelos testes contra o total de linhas existentes.

Cobertura Total Atingida: 100%

Cenários fora do escopo:

Testes de carga/performance: Não foram incluídos, pois o objetivo da suíte é validar a integridade funcional (CRUD) e as regras de negócio da API.

Endpoint de carrinhos: Foram excluídos por estarem fora do escopo inicial definido no plano de testes do desafio.

## 🛠️ Tecnologias Utilizadas

Linguagem: Python

Framework de Testes: Pytest

Biblioteca HTTP: Requests

Cobertura: Pytest-cov

_Projeto desenvolvido como parte do Bootcamp | AWS AI FDE DRIVEN QUALITY ENGINEERING da Compass Uol_
