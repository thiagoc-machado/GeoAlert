.PHONY: test coverage coverage-html up down build

# 🧪 Rodar testes com Pytest
test:
	pytest -v

# 📊 Gerar coverage.xml e relatório terminal
coverage:
	pytest --cov=alerts --cov=users --cov-report=term-missing --cov-report=xml

# 🌐 Gerar relatório HTML de cobertura (em htmlcov/)
coverage-html:
	pytest --cov=alerts --cov=users --cov-report=html

# 🐳 Subir docker-compose
up:
	docker-compose up --build

# ⬇️ Derrubar containers
down:
	docker-compose down

# 🔁 Rebuild completo do backend
build:
	docker-compose build backend
