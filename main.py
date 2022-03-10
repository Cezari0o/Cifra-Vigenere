from vigenere import cipher
from attacker import attacker


def main():

    escolha = int(
        input("""Digite 1 para cifrar uma mensagem;
Digite 2 para decifrar uma mensagem;
Digite 3 para advinhar uma chave de um texto cifrado;
Escolha: """))

    ler_arquivo = True

    if escolha == 1:
        chave = input("Digite a chave: ")
        text = input("Digite o texto a ser cifrado: ")
        cifra = cipher(chave)
        cifrado = cifra.encrypt(text)
        print("Texto cifrado: ", cifrado)
    elif escolha == 2:
        chave = input("Digite a chave: ")
        text = input("Digite o texto a ser decifrado: ")
        cifra = cipher(chave)
        print("Texto decifrado: ", cifra.decrypt(text))
    elif escolha == 3:

        fr_file = "frequency_ptbr.txt"
        text = ""
        if ler_arquivo:
            reader = open(input("Digite o caminho do arquivo: "))
            text = reader.read()

        else:
            text = input("Digite o texto cifrado: ")
        
        key_len = int(
            input("Digite o tamanho maximo da chave que voce espera: "))

        atacante = attacker(fr_file, max_key_listing=5)

        keys = atacante.guess_key(crypted_text=text, max_key_len=key_len)

        

        # print(keys)

        print("Chaves encontradas / Texto decifrado: \n")
        for k in keys:
            cifra = cipher(k)
            print(k, cifra.decrypt(text), sep=' / ', end="\n\n")

    else:
        vargas = open("test/text_vargas.txt")
        texto = vargas.read()

        atacante = attacker("frequency_en.txt", max_key_listing=3)
        c = cipher("CHAVESUPERSECRETA")

        keys = atacante.guess_key(crypted_text=c.encrypt(plain_text=texto),
                                  max_key_len=100)

        for k in keys:
            print(k)

            # c = cipher(k)
            # print(c.decrypt(c.encrypt(texto)))


main()
