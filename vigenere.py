class cipher:

    def __init__(self, key = "a"):
        self.change_key(key)

        self.SPECIAL_CHAR = -1

    def change_key(self, key):
        key = key.upper()
        
        # Converting the string into a integers list
        self.key = list(map(lambda char: ord(char) - 65, key))
        self.key_idx = 0

    def __get_key_idx__(self):
        """ Returns the actual index of the string. This increments the value of the internal index.
        """
        key_idx = self.key_idx
        self.key_idx = (self.key_idx + 1) % len(self.key)

        return key_idx

    def __treat_special_chars__(self, text, converted_list):
        filtered_list = []

        i = 0
        for c in text:
            if ord(c) < ord('A') or ord(c) > ord('Z'):
               converted_list[i] = self.SPECIAL_CHAR 
            i += 1

        filtered_list = converted_list

        return filtered_list

    def encrypt(self, plain_text):

        self.key_idx = 0
        plain_text = plain_text.upper()
        
        # Converts the string into a list of integers, the indexes of every char in the alfabet
        converted_list = list(map(lambda char: ord(char) - 65, plain_text))

        converted_list = self.__treat_special_chars__(text = plain_text, converted_list = converted_list)
        
        encrypted_list = []

        i = 0
        # Encrypting
        for val in converted_list:
            if val != self.SPECIAL_CHAR:
                val = (val + self.key[self.__get_key_idx__()]) % 26 + 65
            else:
                val = ord(plain_text[i])
                
            i += 1
            encrypted_list.append(val)


        # Transforming the encrypted list into string
        encrypted_string = (map(chr, encrypted_list))
        encrypted_string = ''.join(encrypted_string)

        return encrypted_string.lower()

    def decrypt(self, crypted_text):
        self.key_idx = 0;
        crypted_text = crypted_text.upper()
        
        # Transforming the string into a list of integers, the indexes of chars in the alfabet
        crypted_list = list(map(lambda char: ord(char) - 65, crypted_text))

        crypted_list = self.__treat_special_chars__(text = crypted_text, converted_list = crypted_list)

        i = 0
        # Deciphering
        decrypted_list = []
        for val in crypted_list:
            if val != self.SPECIAL_CHAR:
                val = (val - self.key[self.__get_key_idx__()]) % 26 + 65
            else:
                val = ord(crypted_text[i])

            i += 1
            decrypted_list.append(val)
            
        # Getting the string from the deciphered list
        decrypted_string = map(chr, decrypted_list)
        decrypted_string = ''.join(decrypted_string).lower()

        # Captalizing
        temp_list = decrypted_string.split('.')
        decrypted_string = '. '.join(map(lambda s : s.lstrip().capitalize(), temp_list))
        
        return decrypted_string