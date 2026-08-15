import qrcode

def criar_qrcode():
    # Digite EXATAMENTE o mesmo identificador (qrcode_id) que você usou no cadastro dela
    codigo_funcionario = input("Digite o identificador (qrcode_id) do funcionário cadastrado: ")
    
    # Gera o QR Code
    img = qrcode.make(codigo_funcionario)
    
    # Salva como imagem
    nome_arquivo = f"qrcode_{codigo_funcionario}.png"
    img.save(nome_arquivo)
    
    print(f"\nQR Code gerado com sucesso! O arquivo '{nome_arquivo}' foi salvo na sua pasta.")
    print("Abra essa imagem no computador ou mande para o celular da sua mãe para testar na webcam!")

if __name__ == "__main__":
    criar_qrcode()