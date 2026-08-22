import cv2
import os

def verificar_e_comparar_ponto(nome_usuario):
    pasta = "rostos_cadastrados"
    if not os.path.exists(os.path.join(pasta, f"{nome_usuario.lower()}.jpg")): return "nao_cadastrado"
    
    cap = cv2.VideoCapture(0)
    confirmado = False
    while True:
        ret, frame = cap.read()
        if not ret: break
        cv2.imshow(f"Validando: {nome_usuario.upper()} - Pressione ENTER", frame)
        if cv2.waitKey(1) == 13: 
            confirmado = True
            break
        if cv2.waitKey(1) == 27: break
    cap.release()
    cv2.destroyAllWindows()
    return confirmado