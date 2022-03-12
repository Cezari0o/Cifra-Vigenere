from frequency_reader import freq_reader
from re import sub

class attacker:

    def __init__(self, frequency_file_path, max_key_listing = 5):
        self.frequency_file_path = frequency_file_path
        self.alfabet_idx_coincidence = 0
        self.cossets_table_list = []

        if max_key_listing <= 0:
            max_key_listing = 1
        self.max_key_listing = max_key_listing

        # A dict with the frequency for the letters of an alfabet
        self.alfabet_hist_freq = dict()

    def set_frequency_file_path(self, file_path):
        self.frequency_file_path = file_path
    
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
        ic = 0

        for word in cossets_table:
            word_hist = self.__get_histogram__(word)

            word_size = len(word)
    
            word_ic = 0
            for letter in word_hist:
                if word_size > 1:
                    word_ic += (word_hist[letter] * (word_hist[letter] - 1)) / (word_size * (word_size - 1))

            ic += word_ic

        ic = ic / len(cossets_table)
        return ic

    def __get_key__(self, key_size, cossets_table):
        key = ""

        char_list = []

        for char_idx in range(ord('A'), ord('Z') + 1):
            char_list.append(chr(char_idx))

        alph_size = len(char_list)

        
        for cosset in cossets_table:
            freq_dict = self.__get_freq_histogram__(cosset)

            
            sum_max = 0
            shift_ans = 0
            for shift_count in range(alph_size):

                
                sum_temp = 0
                for i in range(alph_size):

                    if freq_dict.get(char_list[(i + shift_count) % alph_size]) != None:
                        sum_temp += self.alfabet_hist_freq[char_list[i]] * freq_dict[char_list[(i + shift_count) % alph_size]]

                if sum_temp > sum_max:
                    sum_max = sum_temp
                    shift_ans = shift_count

            key += chr(shift_ans + 65)

        return key

    def guess_key(self, crypted_text, max_key_len = 5):
        alfabet_hist = dict()

        crypted_text = crypted_text.upper()

        # Taking the chars in the alphabet
        chars = "[^"
        for i in range(ord('A'), ord('Z') + 1):
            chars += chr(i)

        chars += ']'
        
        # Filtering, keeping only the alfabet in the crypted_text
        crypted_text = sub(chars, '', crypted_text)


        with freq_reader(self.frequency_file_path) as fr:
            alfabet_hist = fr.read_frequency()

        self.alfabet_hist_freq = alfabet_hist
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

