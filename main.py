from vigenere import cipher
from attacker import attacker
from math import ceil
from menu import menu

read_from_file = True
max_key_list = 5
fr_file = "frequency_en.txt"

def read_text():
    text = ""
    
    if read_from_file:
        text = open(input("Digite o caminho do arquivo: ")).read()

    else:
        text = input("Digite o texto: ")

    return text


def cipher_msg():

    key = input("Digite a chave: ")
    key = ''.join(key.split())
    
    text = read_text()
    encipher = cipher(key)
    cipher_text = encipher.encrypt(text)
    print("\n--> Texto cifrado: ")
    print(cipher_text)

    
def decipher_msg():
    key = input("Digite a chave: ")
    key = ''.join(key.split())

    text = read_text()
    decipher = cipher(key)
    print("\n--> Texto decifrado: ") 
    print(decipher.decrypt(text))
    

def find_key():
    text = ""
    
    text = read_text()
    
    key_len = int(
        input("Digite o tamanho maximo da chave que voce espera: "))

    cracker = attacker(fr_file, max_key_listing=max_key_list)

    keys = cracker.guess_key(crypted_text=text, max_key_len=key_len)

    print("\nChaves encontradas / Texto decifrado: \n")
    for k in keys:
        decipher = cipher(k)
        print(k, decipher.decrypt(text), sep=' / ', end="\n\n -------------------------------------------------------------------------------------------------------- \n\n")

def iterative_key_search():
    key_len = int(input("Digite o tamanho maximo de chave que voce espera: "))

    cracker = attacker(fr_file, max_key_listing=max_key_list)
    
    text = read_text()

    while True:
        keys = cracker.guess_key(crypted_text = text, max_key_len = key_len)

        print("\nTamanho da chave:", key_len)
        print("\nChave / Texto Decifrado\n")
        for k in keys:
            decipher = cipher(k)

            print(k, decipher.decrypt(text), sep=' / ', end="\n\n -------------------------------------------------------------------------------------------------------- \n\n")
            
        continue_exec = (input("Continuar o programa? [Digite 'S' para continuar, sem aspas] ")).upper()

        if continue_exec == 'S':

            key_size_incr = ceil(key_len / 2)

            key_size = '0'
            while key_size != '1' and key_size != '2':
                key_size = (input("""O tamanho da chave é maior ou menor?
1 - maior ({})
2 - menor ({})
> """.format(key_len + key_size_incr, key_len - key_size_incr)))

            
            if key_size == '1':
                key_len += key_size_incr

            else:
                key_len -= key_size_incr
            
        else:
            break

def main():
    
    options = [
        ("Cifrar uma mensagem", cipher_msg),
        ("Decifrar uma mensagem", decipher_msg),
        ("Executar um ataque, encontrar a chave de uma mensagem cifrada, com um tamanho dado", find_key),
        ("Executar um ataque, fazendo uma busca iterativa pela chave, dado um tamanho inicial", iterative_key_search)
    ]

    initial_msg = """Este é o cifrador/decifrador de textos da cifra de Vigenére. Alem disso, faz o ataque de uma mensagem, estimando uma provavel chave. Para isso, escolha uma das opcoes abaixo
    """
    
    main_menu = (menu(options, choice_msg = "Escolha uma opcao: ", warn_input_msg="""Input inválido! Tente novamente.""", init_msg=initial_msg))

    main_menu.execute()

main()
