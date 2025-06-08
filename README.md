# Detector de Gatos (Lupi Cat Detector)

Um script Python que utiliza YOLOv5 e OpenCV para detectar gatos em tempo real usando a webcam. Quando um gato é detectado, um som de alerta é reproduzido.

## Requisitos
- Python 3.8+
- Webcam
- Conexão com a internet (apenas no primeiro uso, para baixar o modelo)

## Instalação

1. Clone este repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
   
   Ou instale manualmente:
   ```
   pip install opencv-python torch torchvision
   pip install pygame
   ```

## Uso

Execute o script:
```
python lupi_cat_detector.py
```

## Controles
- Pressione 'q' para sair do programa

## Como funciona
1. O script utiliza o YOLOv5, um modelo de detecção de objetos em tempo real
2. Captura o vídeo da webcam e processa cada quadro
3. Quando um gato é detectado com confiança superior a 80%, ele:
   - Desenha um retângulo verde ao redor do gato
   - Exibe a confiança da detecção
   - Reproduz um som de alerta (com intervalo mínimo de 5 segundos entre os sons)
4. A detecção roda em tempo real até que 'q' seja pressionado

## Observações
- O modelo YOLOv5 será baixado automaticamente no primeiro uso
- Para melhor detecção, garanta boa iluminação e que o gato esteja visível para a câmera
- O arquivo de som `alerta1_luiz.wav` deve estar no mesmo diretório do script

## Personalização
- Para alterar o som de alerta, substitua o arquivo `alerta1_luiz.wav`
- A sensibilidade da detecção pode ser ajustada modificando a constante `CONFIANCA_MINIMA` no código
- O intervalo entre os sons pode ser alterado modificando `INTERVALO_SOM` (em segundos)
