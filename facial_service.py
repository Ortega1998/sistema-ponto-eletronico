import cv2
import os

def salvar_foto_cadastro(nome_usuario):
    pasta = "rostos_cadastrados"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        
    cap = cv2.VideoCapture(0)
    sucesso = False
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow("Cadastro Facial - Pressione ESPACO para capturar", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # Tecla ESPAÇO
            caminho_foto = os.path.join(pasta, f"{nome_usuario.lower()}.jpg")
            cv2.imwrite(caminho_foto, frame)
            sucesso = True
            break
        elif key == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return sucesso

import cv2
import os

def verificar_e_comparar_ponto(nome_usuario):
    pasta = "rostos_cadastrados"
    caminho_cadastro = os.path.join(pasta, f"{nome_usuario.lower()}.jpg")
    
    if not os.path.exists(caminho_cadastro):
        return "nao_cadastrado"
        
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False
        
    reconhecido = False
    
    while True:
        ret, frame_atual = cap.read()
        if not ret:
            break
            
        cv2.imshow(f"Validando Ponto: {nome_usuario.upper()} - Pressione ENTER", frame_atual)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 13: # Tecla ENTER
            img_cadastrada = cv2.imread(caminho_cadastro)
            
            if img_cadastrada is not None:
                img1 = cv2.resize(img_cadastrada, (200, 200))
                img2 = cv2.resize(frame_atual, (200, 200))
                
                gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                
                hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
                
                cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
                cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
                
                similaridade = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                
                if similaridade >= 0.6:
                    reconhecido = True
            break
            
        elif key == ord('q') or key == 27: # Tecla Q ou ESC para sair
            break
            
    cap.release()
    cv2.destroyAllWindows()
    # Pequena pausa para garantir que o OpenCV destruiu as janelas antes de voltar pra UI
    cv2.waitKey(1) 
    return reconhecido

def salvar_foto_cadastro(nome_usuario):
    pasta = "rostos_cadastrados"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        
    cap = cv2.VideoCapture(0)
    sucesso = False
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow("Cadastro Facial - Pressione ESPACO para capturar", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # Tecla ESPAÇO
            caminho_foto = os.path.join(pasta, f"{nome_usuario.lower()}.jpg")
            cv2.imwrite(caminho_foto, frame)
            sucesso = True
            break
        elif key == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return sucesso

def verificar_existencia(nome_usuario):
    pasta = "rostos_cadastrados"
    caminho_foto = os.path.join(pasta, f"{nome_usuario.lower()}.jpg")
    return os.path.exists(caminho_foto)

def abrir_camera_ponto():
    """Abre a webcam para verificação visual obrigatória e fecha ao apertar ENTER."""
    cap = cv2.VideoCapture(0)
    confirmado = False
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.imshow("Verificacao de Ponto - Pressione ENTER para confirmar", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 13: # Tecla ENTER confirma a presença
            confirmado = True
            break
        elif key == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return confirmado