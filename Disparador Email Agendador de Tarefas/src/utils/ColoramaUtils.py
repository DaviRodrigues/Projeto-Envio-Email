from colorama import Fore, Style, init
import random

def rand_color():
    init(autoreset=True)
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    return random.choice(colors)