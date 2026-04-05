# Lupi Cat Detector

Detecta gatos em tempo real via webcam usando YOLOv5 e OpenCV. Quando um gato é detectado com alta confiança, um som de alerta é reproduzido.

## Requisitos

- Python 3.8+
- Webcam
- Conexão com a internet (apenas no primeiro uso, para baixar o modelo YOLOv5)

## Instalação rápida

### Opção 1 — Makefile (recomendado)

```bash
git clone <url-do-repositório>
cd lupi-cv2-detect-cat
make install
make run
```

### Opção 2 — Script de setup

```bash
git clone <url-do-repositório>
cd lupi-cv2-detect-cat
bash setup.sh
source venv/bin/activate
python lupi_cat_detector.py
```

### Opção 3 — Manual

```bash
git clone <url-do-repositório>
cd lupi-cv2-detect-cat

# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar
python lupi_cat_detector.py
```

## Controles

| Tecla | Ação |
|-------|------|
| `q`   | Encerra o programa |

## Como funciona

1. Captura vídeo da webcam em 1280×720
2. Processa cada frame com o modelo YOLOv5s (COCO dataset)
3. Quando um gato é detectado com confiança > 80%:
   - Desenha um retângulo verde ao redor do gato
   - Exibe o percentual de confiança
   - Reproduz o som `alerta1_luiz.wav` (no máximo uma vez a cada 5 segundos)
4. Se disponível, utiliza GPU (CUDA) automaticamente

## Personalização

As constantes no topo de `lupi_cat_detector.py` permitem ajuste rápido:

| Constante       | Padrão | Descrição                                  |
|-----------------|--------|--------------------------------------------|
| `CONFIANCA_MINIMA` | `0.25` | Limiar para exibir o bounding box        |
| `TAMANHO_IMAGEM`   | `640`  | Resolução de entrada do modelo (px)      |
| `INTERVALO_SOM`    | `5`    | Intervalo mínimo entre alertas (segundos)|

Para trocar o som de alerta, substitua o arquivo `alerta1_luiz.wav` por outro arquivo `.wav`.

## Troubleshooting

**Webcam não abre**
Verifique se outra aplicação está usando a câmera. Se tiver mais de uma câmera, altere o índice em `cv2.VideoCapture(0)` para `1`, `2`, etc.

**Erro ao carregar o modelo**
O download do YOLOv5 requer acesso à internet na primeira execução. O modelo fica em cache em `~/.cache/torch/hub/`.

**Sem áudio / erro no pygame**
Certifique-se de que o arquivo `alerta1_luiz.wav` está na mesma pasta que o script. Em servidores sem interface gráfica, o alerta sonoro é ignorado automaticamente.

**GPU não detectada**
Instale a versão do PyTorch compatível com sua versão do CUDA em [pytorch.org](https://pytorch.org/get-started/locally/).
