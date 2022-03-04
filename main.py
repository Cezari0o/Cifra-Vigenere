from vigenere import cipher

def main():
    chave = input("Digite a chave: ")
    text = input("Digite o texto a ser cifrado: ")

    cifra = cipher(chave);

    cifrado = cifra.encrypt(text)
    print("Texto cifrado: ", cifrado)
    print("Texto decifrado: ", cifra.decrypt(cifrado))

main()