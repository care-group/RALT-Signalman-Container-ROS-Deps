from colorama import Fore, Style

class Log(object):
    def __init__(self, id):
        self.id = id

    def startup_msg(self):
        print(Fore.YELLOW + '* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
        print()
        print(Style.BRIGHT + ' RALT Semantic Event Logger' + Style.RESET_ALL + Fore.YELLOW)
        print(' https://github.com/care-group/RALT-Semantic-Event-Logger')
        print()
        print(' Developer: Ronnie Smith')
        print(' Email:     ronnie.smith@ed.ac.uk')
        print(' GitHub:    @ronsm')
        print()
        print('* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')

    def log(self, msg):
        tag = '[' + self.id + ']'
        print(Fore.CYAN + tag, Fore.RESET + msg)

    def log_math(self, msg):
        tag = '[' + self.id + ']'
        print(Fore.CYAN + tag, Fore.YELLOW + msg, Fore.RESET)
    
    def log_warn(self, msg):
        tag = '[' + self.id + ']'
        print(Fore.CYAN + tag, Fore.LIGHTRED_EX + msg, Fore.RESET)

    def log_great(self, msg):
        tag = '[' + self.id + ']'
        print(Fore.CYAN + tag, Fore.GREEN + msg, Fore.RESET)