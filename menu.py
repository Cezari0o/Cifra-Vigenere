import os

class menu:
    def __init__(self, options : list, choice_msg: str, warn_input_msg = """Invalid input! Type again""", init_msg = None):

        # A dict in the form {key: string, (opt_description: string, action: function)}
        self.opt_menu = dict()
        self.warning_input_msg = warn_input_msg
        self.init_msg = init_msg
        self.choice_msg = choice_msg

        for cont in range(1, len(options) + 1):
            self.opt_menu[str(cont)] = options[cont - 1]

    def print_options(self):

        if self.init_msg != None:
            print("\n" + self.init_msg)
        # A list of strings
        descriptions = []
        
        for key_option in self.opt_menu:
            descr_str = key_option+ ' : ' + self.opt_menu[key_option][0] + ';'

            descriptions.append(descr_str)

        for desc in descriptions:
            
            print(desc, sep = '\n')

    def get_input(self):

        print('\n' + self.choice_msg)
        get_option = input("\n> ")

        while get_option not in self.opt_menu.keys():
            print(self.warning_input_msg)
            get_option = input("\n> ")

        return get_option

    def execute_opt(self):

        opt = self.get_input()

        print('---', self.opt_menu[opt][0], '---')
        # Calling the option in the 
        self.opt_menu[opt][1]()

    def execute(self):
        self.print_options()
        self.execute_opt()
        # os.system("clear || cls")