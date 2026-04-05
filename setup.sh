#!/usr/bin/env bash
# Script de configuração do Lupi Cat Detector
set -e

PYTHON=${PYTHON:-python3}
VENV_DIR="venv"

echo "==> Verificando Python..."
$PYTHON --version

echo "==> Criando ambiente virtual em '$VENV_DIR'..."
$PYTHON -m venv "$VENV_DIR"

echo "==> Ativando ambiente virtual..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "==> Atualizando pip..."
pip install --upgrade pip

echo "==> Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "Instalação concluída!"
echo ""
echo "Para ativar o ambiente virtual:"
echo "  source venv/bin/activate"
echo ""
echo "Para executar o detector:"
echo "  python lupi_cat_detector.py"
