from frequency_reader import freq_reader
from re import sub

class attacker:
    """ A class that executes an attack to a crypted message, given by the user, assuming that the message is crypted with the vigenere cypher, and tries to find the key used to cipher the message. Uses the Friedman test in this process. """

    def __init__(self, frequency_file_path, max_key_listing = 5):
        """ Init the instance class
        
        frequency_file_path : the path to the file frequency of the alphabet to work with

        max_key_listing : the max quantity of the keys to return, when the function guess_key is called
        
        """

        # Setting instance variables
        self.frequency_file_path = frequency_file_path
        self.alphabet_idx_coincidence = 0
        self.cossets_table_list = []

        if max_key_listing <= 0:
            max_key_listing = 1
        self.max_key_listing = max_key_listing

        # A dict with the frequency for the letters of an alphabet
        self.alphabet_hist_freq = dict()

    def set_frequency_file_path(self, file_path):
        self.frequency_file_path = file_path
    
    def __get_cossets__(self, text, cossets_count):
        """ 
        Given a text, returns a list of cossets

        text: a string text to be used to generate the cossets_count.

        cossets_count: the max quantity of cossets to generate.
        """
        # A table with the cossets
        table = cossets_count * [""]

        for i in range(len(text)):
            table[i % cossets_count] += text[i]

        return table

    def __get_histogram__(self, word):
        """ Given a word, returns the histogram of the word
        
        word: the word from which the histogram will be generated 
        """
        hist = dict()

        for c in word:
            if(hist.get(c) == None):
                hist[c] = 1
            else:
                hist[c] += 1

        return hist

    def __get_freq_histogram__(self, word):
        """ Returns the histogram frequency of a word """
        hist = self.__get_histogram__(word)
        frequency_dict = dict()

        total_chars_count = sum(hist.values())

        # Getting the frequency of every char in the histogram
        for char in hist:
            frequency_dict[char] = hist[char] / total_chars_count


        return frequency_dict
        
    def __get_idx_coincidence__(self, cossets_table):
        """ Returns the index of coincidence of the N cossets in cossets_table, where N is an arbitrary size.
        
        cossets_table: a list with the cossets generated using the __get_cossets__ 
        
        See also this link: https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-IOC.html (Explain how to calculate the index of coincidence) """
        ic = 0

        for word in cossets_table:
            word_hist = self.__get_histogram__(word)

            word_size = len(word)
    
            word_ic = 0
            for letter in word_hist:
                if word_size > 1:
                    word_ic += (word_hist[letter] * (word_hist[letter] - 1)) / (word_size * (word_size - 1))

            ic += word_ic

        # Obtaining the average value of the index of coincidence
        ic = ic / len(cossets_table)
        return ic

    def __get_key__(self, key_size, cossets_table):
        """ Given a key and a cossets table, tries to guess the key using the table. 
        
        key_size: the key size of the original key_size
        
        cossets_table: a table of cossets, generated with the function __get_cossets__"""
        key = ""

        char_list = []

        for char_idx in range(ord('A'), ord('Z') + 1):
            char_list.append(chr(char_idx))

        alph_size = len(char_list)

        
        for cosset in cossets_table:
            # A histogram of frequencies, the letters frequency in the cosset
            freq_dict = self.__get_freq_histogram__(cosset)

            
            sum_max = 0

            # The shift answer
            shift_ans = 0
            for shift_count in range(alph_size):

                sum_temp = 0
                for i in range(alph_size):

                    # Only doing the calculation if the shifted index returns a frequency != 0
                    if freq_dict.get(char_list[(i + shift_count) % alph_size]) != None:
                        sum_temp += self.alphabet_hist_freq[char_list[i]] * freq_dict[char_list[(i + shift_count) % alph_size]]

                if sum_temp > sum_max:
                    sum_max = sum_temp
                    shift_ans = shift_count

            key += chr(shift_ans + 65)

        return key

    def guess_key(self, crypted_text, max_key_len = 5):
        """ Given a ciphertext, try to guess its generating key. 
        
        crypted_text: the keystream with the ciphered message.

        max_key_len: the maximum size of the key to search for.
        """

        # The alphabet frequency "histogram"
        alphabet_hist = dict()

        crypted_text = crypted_text.upper()

        # Taking the chars in the alphabet, to use in the filtering
        chars = "[^"
        for i in range(ord('A'), ord('Z') + 1):
            chars += chr(i)

        chars += ']'
        
        # Filtering, keeping only the alphabet chars in the crypted_text
        crypted_text = sub(chars, '', crypted_text)

        with freq_reader(self.frequency_file_path) as fr:
            alphabet_hist = fr.read_frequency()

        self.alphabet_hist_freq = alphabet_hist
        idx_coincidence_alphabet = 0
        text_size = len(crypted_text)

        # Calculating the alphabet's idx_of_coincidence
        for idx in alphabet_hist:
            idx_coincidence_alphabet += alphabet_hist[idx] * (alphabet_hist[idx] * text_size - 1) / (text_size - 1)


        self.alphabet_idx_coincidence = idx_coincidence_alphabet
        key_size_list = []    # A list of tuples

        # Calculating the idx_of_coincidence for some key sizes
        for i in range(1, max_key_len + 1):
            tb = self.__get_cossets__(text = crypted_text, cossets_count = i)

            idx_coincidence_n = self.__get_idx_coincidence__(cossets_table = tb)

            # The tuple below is in the form (key size, idx of coincidence, cossets_table)
            key_size_list.append((i, idx_coincidence_n, tb))

        key_size_list.sort(
            key = lambda key_tuple: key_tuple[1], reverse=True
        )

        key_size_list = key_size_list[0:self.max_key_listing]

        possible_keys_list = list(
            map(lambda key_tuple: 
                self.__get_key__(key_size = key_tuple[0], cossets_table = key_tuple[2]),
               key_size_list))

        return possible_keys_list        

