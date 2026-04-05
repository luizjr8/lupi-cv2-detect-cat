PYTHON  ?= python3
VENV    := venv
PIP     := $(VENV)/bin/pip
PYTHON_VENV := $(VENV)/bin/python

.PHONY: help venv install run clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make venv     - Cria o ambiente virtual"
	@echo "  make install  - Instala as dependências (cria venv se necessário)"
	@echo "  make run      - Executa o detector de gatos"
	@echo "  make clean    - Remove o ambiente virtual e cache"

venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "Instalação concluída. Execute 'make run' para iniciar."

run:
	@test -f $(PYTHON_VENV) || (echo "Rode 'make install' primeiro." && exit 1)
	$(PYTHON_VENV) lupi_cat_detector.py

clean:
	rm -rf $(VENV) __pycache__ *.pyc
