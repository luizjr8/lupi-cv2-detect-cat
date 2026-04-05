import cv2
import torch
import time
import warnings
import os
import pygame  # Para reprodução de áudio

# Variáveis globais para controle do som
ultimo_som = 0
INTERVALO_SOM = 5  # segundos de intervalo entre os sons

# Ignorar avisos
warnings.filterwarnings('ignore')
os.environ.setdefault('OPENCV_LOG_LEVEL', 'ERROR')

# Constantes
CONFIANCA_MINIMA = 0.25  # Limiar de confiança para detecção
TAMANHO_IMAGEM = 640     # Tamanho da imagem para o modelo
CLASSE_GATO = 15         # ID da classe 'gato' no COCO dataset

# Configuração do dispositivo (GPU/CPU)
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Usando dispositivo: {DEVICE}")

def carregar_modelo():
    """Carrega o modelo YOLOv5 pré-treinado"""
    print("Carregando modelo YOLOv5...")
    try:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        model = model.to(DEVICE)
        model.conf = CONFIANCA_MINIMA
        model.classes = [CLASSE_GATO]  # Detecta apenas gatos
        print("Modelo carregado com sucesso!")
        return model
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None

def tocar_alerta():
    """Toca o som de alerta, respeitando o intervalo mínimo"""
    global ultimo_som
    agora = time.time()
    
    if agora - ultimo_som > INTERVALO_SOM:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("alerta1_luiz.wav")
            pygame.mixer.music.play()
            ultimo_som = agora
            print(f"Som tocado em {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Erro ao reproduzir som: {e}")

def detectar_gato(model, frame):
    """
    Detecta gatos no frame, desenha retângulos ao redor deles e toca alerta
    Retorna True se um gato for detectado com alta confiança
    """
    # Converte o frame para RGB (o YOLOv5 espera RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Executa a detecção
    resultados = model(frame_rgb, size=TAMANHO_IMAGEM)
    
    # Processa os resultados
    gato_detectado = False
    
    # Desenha as detecções
    for *xyxy, conf, cls in resultados.xyxy[0]:
        if conf >= CONFIANCA_MINIMA:
            # Converte coordenadas para inteiros
            x1, y1, x2, y2 = map(int, xyxy)
            
            # Desenha retângulo e rótulo
            cor = (0, 255, 0)  # Verde para gatos
            rotulo = f"Gato {conf:.2f}"
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
            cv2.putText(frame, rotulo, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)
            
            if conf > 0.8:  # Considera apenas detecções com alta confiança
                gato_detectado = True
                print(f"Gato detectado com {conf*100:.1f}% de confiança")
                tocar_alerta()  # Toca o som quando um gato é detectado
    
    return gato_detectado

def main():
    """Função principal que gerencia a captura de vídeo e detecção"""
    # Inicializa o mixer de áudio suprimindo erros ALSA de baixo nível
    try:
        devnull_fd = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        os.dup2(devnull_fd, 2)
        os.close(devnull_fd)
        try:
            pygame.mixer.init()
        finally:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
    except Exception as e:
        print(f"Aviso: Não foi possível inicializar o sistema de áudio: {e}")
    
    # Inicializa a webcam (suprime logs C++ do OpenCV durante abertura)
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    os.dup2(devnull_fd, 2)
    os.close(devnull_fd)
    try:
        cap = cv2.VideoCapture(0)
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam")
        return
    
    # Configura resolução da webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Carrega o modelo
    modelo = carregar_modelo()
    if modelo is None:
        print("Falha ao carregar o modelo. Encerrando...")
        cap.release()
        return
    
    print("Detecção de gatos iniciada. Pressione 'q' para sair.")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar frame")
                break
            
            # Detecta gatos no frame
            detectar_gato(modelo, frame)
            
            # Mostra o frame resultante
            cv2.imshow('Detector de Gatos', frame)
            
            # Encerra ao pressionar 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nEncerrando detecção...")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        # Libera os recursos
        cap.release()
        cv2.destroyAllWindows()
        print("Detecção encerrada.")
        
        # Limpa a memória da GPU se estiver sendo usada
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

if __name__ == "__main__":
    main()
