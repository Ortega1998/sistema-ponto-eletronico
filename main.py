import cv2
import sqlite3
from banco import conectar, gerar_hash_senha
import datetime
from reportlab.pdfgen import canvas
import os

def verificar_ponto(qrcode_id, senha_digitada):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cargo, senha_hash FROM usuarios WHERE qrcode_id = ?", (qrcode_id,))
    usuario = cursor.fetchone()
    
    if usuario:
        usuario_id, nome, cargo, senha_hash_banco = usuario
        if gerar_hash_senha(senha_digitada) == senha_hash_banco:
            agora = datetime.datetime.now()
            data_hora_str = agora.strftime("%Y-%m-%d %H:%M:%S")
            data_hoje_str = agora.strftime("%Y-%m-%d")
            
            # --- LÓGICA DE DEFINIÇÃO DE ENTRADA / SAÍDA ---
            # Busca todos os registros do usuário na data de hoje (para ignorar dias anteriores)
            cursor.execute("""
                SELECT tipo FROM registros 
                WHERE usuario_id = ? AND DATE(data_hora) = ?
            """, (usuario_id, data_hoje_str))
            
            registros_hoje = cursor.fetchall()
            quantidade_registros = len(registros_hoje)
            
            # Se já bateu um número par de vezes hoje, o próximo é ENTRADA. Se ímpar, SAÍDA.
            if quantidade_registros % 2 == 0:
                tipo_registro = 'ENTRADA'
            else:
                tipo_registro = 'SAIDA'
            # ---------------------------------------------
            
            # Registra no banco com o tipo correto
            cursor.execute("INSERT INTO registros (usuario_id, data_hora, tipo) VALUES (?, ?, ?)", 
                           (usuario_id, data_hora_str, tipo_registro))
            conn.commit()
            
            # Geração do PDF atualizado com o tipo correto
            if not os.path.exists("comprovantes"):
                os.makedirs("comprovantes")
                
            nome_pdf = f"comprovantes/ponto_{usuario_id}_{agora.strftime('%Y%m%d_%H%M%S')}.pdf"
            c = canvas.Canvas(nome_pdf)
            c.drawString(100, 750, f"--- COMPROVANTE DE {tipo_registro} ---")
            c.drawString(100, 730, f"Funcionário: {nome}")
            c.drawString(100, 715, f"Cargo: {cargo}")
            c.drawString(100, 700, f"Tipo de Registro: {tipo_registro}")
            c.drawString(100, 685, f"Data/Hora: {data_hora_str}")
            c.drawString(100, 665, "Assinatura: ___________________________")
            c.save()
            
            print(f"\n[SUCESSO] {tipo_registro} registrada para {nome} às {agora.strftime('%H:%M:%S')}!")
            print(f"Comprovante gerado em: {nome_pdf}")
        else:
            print("\n[ERRO] Senha incorreta!")
    else:
        print("\n[ERRO] QR Code não cadastrado no sistema!")
    conn.close()

def iniciar_leitura():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = cv2.QRCodeDetector()
    
    print("Sistema de Ponto iniciado. Aponte o QR Code para a câmera...")
    print("(A janela da câmera fechará automaticamente assim que o código for lido)")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        val, points, _ = detector.detectAndDecode(frame)
        
        if val:
            print(f"\n[DETECTADO] QR Code Lido: {val}")
            
            # Libera a câmera imediatamente antes de pedir a senha
            cap.release()
            cv2.destroyAllWindows()
            break
            
        cv2.imshow("Ponto Eletronico - Aponte o QR Code", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return

    senha = input("Digite sua senha para confirmar o ponto: ")
    verificar_ponto(val, senha)

if __name__ == "__main__":
    iniciar_leitura()