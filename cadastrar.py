from banco import conectar, gerar_hash_senha
import qrcode
import os

def cadastrar_usuario():
    print("--- CADASTRO DE NOVO FUNCIONÁRIO ---")
    nome = input("Digite o nome do funcionário: ")
    cargo = input("Digite o cargo/função: ")
    qrcode_id = input("Digite o identificador único do QR Code (ex: MATRICULA123): ")
    senha = input("Digite a senha de acesso: ")
    
    # Converte a senha em hash seguro
    senha_hash = gerar_hash_senha(senha)
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO usuarios (nome, cargo, qrcode_id, senha_hash)
            VALUES (?, ?, ?, ?)
        ''', (nome, cargo, qrcode_id, senha_hash))
        
        conn.commit()
        conn.close()
        
        # Cria a pasta 'crachas' caso não exista
        if not os.path.exists("crachas"):
            os.makedirs("crachas")
            
        # Gera a imagem do QR Code
        nome_arquivo = f"crachas/qrcode_{qrcode_id}.png"
        img = qrcode.make(qrcode_id)
        img.save(nome_arquivo)
        
        print(f"\nSucesso! Usuário '{nome}' cadastrado.")
        print(f"Crachá gerado e salvo em: '{nome_arquivo}'!")
        
        # Abre a imagem automaticamente na tela do computador
        img.show()
        print("A imagem do crachá foi aberta na tela. Peça para sua mãe escanear agora ou tirar uma foto!")
        
    except Exception as e:
        print(f"\nErro ao cadastrar (talvez o ID do QR Code já exista): {e}")

if __name__ == "__main__":
    cadastrar_usuario()
