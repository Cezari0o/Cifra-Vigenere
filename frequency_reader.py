
class freq_reader(object):
    """ Class used to read a file with the frequencies of an alphabet. 
    Uses a specific format, given in the file frequency_ptbr.txt, for example. """
    
    def __init__(self, file_path):
        """
        file_path: the path to the file with the frequencies
        """
        self.file_path = file_path
        self.histogram = dict()
    
    def __exit__(self, a, b, c):
        self.file.close()
    
    def __enter__(self):
        self.file = open((self.file_path),'r')
        return self

    def read_frequency(self):
        """ Reads the frequency of the alphabet in the file. Returns a dict with the frequencies of every char. """

        lines = self.file.readlines()
        for line in lines:
            line = line.upper()
            find_label = False
            freq = ''
            label = ''
            for char in (line):
                if(char != ' '):
                    if find_label == False:
                        self.histogram[char] = 0
                        find_label = True
                        label = char
                    elif ord(char) >= ord('0') and ord(char) <= ord('9') or char == '.':
                        freq += char

            self.histogram[label] = float(freq) / 100       

        return self.histogram
            
            