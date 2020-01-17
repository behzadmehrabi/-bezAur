import os


from termcolor import colored


def get_input(text, func=str):
    print(_cyan('>>> '), end='')
    answer = func(input(text))
    return answer

def yes_no_checker(input):
    if input.lower().startswith('y'):
        return True
    return False

def _cyan(text):
    return  colored(text, "cyan")

def _boldcyan(text):
    return colored(text, 'cyan', attrs=['bold'])

def _yellow(text):
    return colored(text, 'yellow')

def abs_path(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))
