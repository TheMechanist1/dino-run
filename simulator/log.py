# ANSI terminal escape codes
YELLOW = "\x1b[33m"
RESET = "\x1b[0m"

def print_warning(message):
    print(f"{YELLOW}Simulator warning: {message}{RESET}")
