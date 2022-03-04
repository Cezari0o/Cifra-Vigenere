class cipher:

    def __init__(self, key):
        self.change_key(key)

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

    def encrypt(self, plain_text):

        self.key_idx = 0
        plain_text = plain_text.upper()
        
        # Converts the string into a list of integers, the indexes of every char in the alfabet
        converted_list = list(map(lambda char: ord(char) - 65, plain_text))

        i = 0
        # Treating spaces
        for c in plain_text:
            if ord(c) < ord('A') or ord(c) > ord('Z'):
               converted_list[i] = -1 
            i += 1
        
        encrypted_list = []

        # Encrypting
        for val in converted_list:
            if val != -1:
                val = (val + self.key[self.__get_key_idx__()]) % 26 + 65
            else:
                val = ord(' ')
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

        # Treating spaces
        i = 0
        for c in crypted_text:
            if ord(c) < ord('A') or ord(c) > ord('Z'):
               crypted_list[i] = -1 
            i += 1


        # Deciphering
        decrypted_list = []
        for val in crypted_list:
            if val != - 1:
                val = (val - self.key[self.__get_key_idx__()]) % 26 + 65
            else:
                val = ord(' ')
            decrypted_list.append(val)
            
        # Getting the string from the deciphered list
        decrypted_string = map(chr, decrypted_list)
        decrypted_string = ''.join(decrypted_string)

        return decrypted_string.lower()