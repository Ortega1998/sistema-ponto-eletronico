import os
import cv2

def verificar_ponto_facial():
    pasta_rostos = "rostos_cadastrados"
    
    if not os.path.exists(pasta_rostos) or not os.listdir(pasta_rostos):
        print("Nenhuma foto cadastrada na pasta 'rostos_cadastrados'.")
        return None

    print("Iniciando a câmera... Pressione 'q' para sair.")
    cap = cv2.VideoCapture(0)
    usuario_reconhecido = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Desenha um texto orientando na tela
        cv2.putText(frame, "Pressione 'ENTER' para registrar o ponto", (30, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Sistema de Ponto - Reconhecimento Facial", frame)

        # Se o usuário apertar a tecla ENTER (13), simulamos a captura e validação facial da câmera
        key = cv2.waitKey(1) & 0xFF
        if key == 13: 
            # Pega o primeiro usuário cadastrado na pasta para validar o ponto
            for arquivo in os.listdir(pasta_rostos):
                if arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
                    usuario_reconhecido = os.path.splitext(arquivo)[0]
                    break
            break

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return usuario_reconhecido

if __name__ == "__main__":
    identificado = verificar_ponto_facial()
    if identificado:
        print(f"Sucesso! Ponto registrado para: {identificado.upper()}")
    else:
        print("Operação cancelada.")