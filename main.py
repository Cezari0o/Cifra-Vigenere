from vigenere import cipher
from attacker import attacker
# from math import ceil
from menu import menu

read_from_file = True
max_key_list = 5
fr_file = "frequency_en.txt"

def read_text():
    """ Lets a user input a text directly, or the text file path, according to the variable read_from_file. Returns the text """
    text = ""
    
    if read_from_file:
        text = open(input("Digite o caminho do arquivo: ")).read()

    else:
        text = input("Digite o texto: ")

    return text


def cipher_msg():
    """ Let the user cipher a message """
    
    key = input("Digite a chave: ")
    key = ''.join(key.split())
    
    text = read_text()
    encipher = cipher(key)
    cipher_text = encipher.encrypt(text)
    print("\n--> Texto cifrado: ")
    print(cipher_text)

    
def decipher_msg():
    """ Let the user decipher a message """
    key = input("Digite a chave: ")
    key = ''.join(key.split())

    text = read_text()
    decipher = cipher(key)
    print("\n--> Texto decifrado: ") 
    print(decipher.decrypt(text))
    

def find_key():
    """ This function tries to break and find the key of a cipher text. Shows to the user the keys guessed by the program and the texts deciphered with every key """
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
    """ This function tries to break and find the key of a cipher text, iteratively. Shows to the user the keys guessed by the program and the texts deciphered with every key """

    cracker = attacker(fr_file, max_key_listing=max_key_list)
    
    text = read_text()

    while True:
        key_len = int(input("Digite o tamanho maximo de chave que voce espera: "))
        keys = cracker.guess_key(crypted_text = text, max_key_len = key_len)

        print("\nTamanho da chave:", key_len)
        print("\nChave / Texto Decifrado\n")
        for k in keys:
            decipher = cipher(k)

            print(k, decipher.decrypt(text), sep=' / ', end="\n\n -------------------------------------------------------------------------------------------------------- \n\n")
            
        continue_exec = (input("Continuar o programa? [Digite 'S' para continuar, sem aspas] ")).upper()

        if continue_exec != 'S':
            break

def config():
    """ Let the user configurate the ambient variables """
    
    def change_max_key_list():

        while True:
            try:
                global max_key_list 
                max_key_list = int(input("Qual o novo tamanho? "))
                if max_key_list < 1:
                    raise
            except:
                print("Digite um tamanho valido!")
            else:
                break

    def change_read_from_file():
        global read_from_file
        read_from_file = not read_from_file

    def change_fr_file():
        global fr_file
        if fr_file == "frequency_en.txt":
            fr_file = "frequency_ptbr.txt"
        else:
            fr_file = "frequency_en.txt"
    
    config_msg = (
        """ \n--- Nome / Valor / Descricao ---\n
read_from_file / {} / Determina se a mensagem de entrada é lida de um arquivo. Se for falso, le da entrada padrao.
        
max_key_list / {} / Listagem maxima de chaves/textos decifrados quando um ataque for executado.

fr_file / {} / O arquivo de frequencia do alfabeto (determina o alfabeto de trabalho).
          """.format(read_from_file, max_key_list, fr_file))

    config_menu = menu(
        options = [
            ("Mudar read_from_file", change_read_from_file),
            ("Mudar max_key_list", change_max_key_list),
            ("Mudar fr_file (entre portugues ou ingles)", change_fr_file),
            ("Voltar", lambda: 0),
        ], 
        choice_msg = "Escolha uma opcao: ", warn_input_msg="""Input invalido! Tente denovo.""", init_msg=config_msg)

    config_menu.execute()
    # Re-executes the main (can cause error, but for now it works)
    main()

def main():

    # The options to execute, in the program, with (description / function)
    options = [
        ("Cifrar uma mensagem", cipher_msg),
        ("Decifrar uma mensagem", decipher_msg),
        ("Executar um ataque, encontrar a chave de uma mensagem cifrada, com um tamanho dado", find_key),
        ("Executar um ataque, fazendo uma busca iterativa pela chave, dado um tamanho inicial", iterative_key_search),
        ("Configurar as variaveis de ambiente", config),
        ("Sair", lambda: 0)
    ]

    initial_msg = """Este é o cifrador/decifrador de textos da cifra de Vigenére. Alem disso, faz o ataque de uma mensagem, estimando uma provavel chave. Para isso, escolha uma das opcoes abaixo
    """
    
    main_menu = (menu(options, choice_msg = "Escolha uma opcao: ", warn_input_msg="""Input inválido! Tente novamente.""", init_msg=initial_msg))

    main_menu.execute()

main()
