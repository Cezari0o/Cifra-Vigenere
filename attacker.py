from frequency_reader import freq_reader

class attacker:

    def __init__(self, frequency_file_path):
        self.frequency_file_path = frequency_file_path
        self.alfabet_idx_coincidence = 0


    def __get_cossets__(self, text, cossets_count):
        # A table with the cossets
        table = cossets_count * [""]

        for i in range(len(text)):
            table[i % cossets_count] += text[i]

        return table

    def __get_histogram__(self, word):
        hist = dict()

        for c in word:
            if(hist.get(c) == None):
                hist[c] = 1
            else:
                hist[c] += 1

        return hist
        
    def __get_idx_coincidence__(self, cossets_table):
        ic = 0

        for word in cossets_table:
            word_hist = self.__get_histogram__(word)

            word_size = len(word)
    
            word_ic = 0
            for letter in word_hist:
                word_ic += (word_hist[letter] * (word_hist[letter] - 1)) / (word_size * (word_size - 1))

            ic += word_ic

        ic = ic / len(cossets_table)
        return ic

    def guess_key(self, crypted_text, max_key_len = 5):
        alfabet_hist = dict()

        crypted_text = ''.join(crypted_text.split()).upper()
        
        with freq_reader(self.frequency_file_path) as fr:
            alfabet_hist = fr.read_frequency()

        idx_coincidence_alfabet = 0
        text_size = len(crypted_text)

        # Calculating the alfabet's idx_of_coincidence
        for idx in alfabet_hist:
            idx_coincidence_alfabet += alfabet_hist[idx] * (alfabet_hist[idx] * text_size - 1) / (text_size - 1)


        self.alfabet_idx_coincidence = idx_coincidence_alfabet
        # Calculating the idx_of_coincidence for some key sizes
        
        # A list of tuples
        key_size_list = []
        for i in range(1, max_key_len + 1):
            tb = self.__get_cossets__(text = crypted_text, cossets_count = i)

            idx_coincidence_n = self.__get_idx_coincidence__(cossets_table = tb)

            key_size_list.append((i, idx_coincidence_n))
        
        key_size_list.sort(
            key = lambda key_pair: key_pair[1], reverse=True
        )

        return key_size_list
            
        
    # https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC.html
    """" 
    * Primeiro, descobrir o tamanho da chave
    - Necessario calcular o Indice de coincidencia do alfabeto no qual se ta trabalhando
    - Dividir o texto cifrado em palavras de tamanho variado (1, 2, 3, ...), chamados cosets
    - Pra cada uma, calcular o indice de coincidencia de cada palavra
    - Com o indice de cada palavra, somar tudo pra fazer a media
    - A media obtida sera para palavras de tamanho n (n = 1, 2, 3, ...)
    - Para cada indice médio obtido, comparar com o indice do alfabeto em questão
    - a comparacao é a diferença absoluta entre ind_alfabeto - ind_pal_n (priorizar aqueles indices que sao maiores)
    - A que tiver a menor diferença é o tamanho da palavra
    """


    """
    * Com um tamanho estimado, obter a chave a partir do texto cifrado
    - Com os cossets obtidos no passo anterior, obtenha a frequencia de cada letra no cosset
    - Com as frequencias de letras em cada cosset, pegue as frequencias das letras do alfabeto que aparecem na palavra. Bote elas em ordem crescente
    - Faça o mesmo com as frequencias do cosset.
    - Multiplique na ordem e some tudo (tipo, se as frequencias são A_0 : 0.2, B_0: 0.7, C_0:0.14 no alfabeto, e a frequencia do cosset é A_1: 0.9, B_1:0.5, C_1:0.8, faça soma_0 = A_0 * A_1 + B_0 * B_1 + C_0 * C_1 )
    - Faça um shift das frequencias do cosset pra esquerda
    - Novamente, multiplique as frequencias do cosset pelas do alfabeto e some tudo (do exemplo acima, temos agora soma_1 = A_0 * B_1 + B_0 * C_1 + C_0 * A_1)
    - Faz o shift pra esquerda denovo
    - Repita o processo ate num dar mais pra fazer shift
    - Se a maior soma é soma_i, então o numero da chave que a gente quer saber na primeira posicao é i 
    - Repita o processo para os outros cossets, até advinhar todos os numeros da chave (a ordem das letras no alfabeto)

    https://www.youtube.com/watch?v=LaWp_Kq0cKs
    """
