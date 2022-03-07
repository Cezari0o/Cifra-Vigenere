from vigenere import cipher
from attacker import attacker

def main():

    escolha = int(input(
"""Digite 1 para cifrar uma mensagem;
Digite 2 para decifrar uma mensagem;
Digite 3 para advinhar uma chave de um texto cifrado;
Escolha: """))
    if escolha == 1:
        chave = input("Digite a chave: ")
        text = input("Digite o texto a ser cifrado: ")
        cifra = cipher(chave);
        cifrado = cifra.encrypt(text)
        print("Texto cifrado: ", cifrado)
    elif escolha == 2:
        chave = input("Digite a chave: ")
        text = input("Digite o texto a ser decifrado: ")
        cifra = cipher(chave)
        print("Texto decifrado: ", cifra.decrypt(text))
    elif escolha == 3:
        text = input("Digite o texto cifrado: ")
        key_len = int(input("Digite o tamanho maximo da chave que voce espera: "))
        
        atacante = attacker("frequency_en.txt")
        print(atacante.guess_key(crypted_text = text, max_key_len = key_len))

main()