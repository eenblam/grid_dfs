class BoardColors:
    ZERO = '\033[94m' # Blue
    ONE = '\033[91m' # Red
    X = '\033[96m' # Cyan
    END = '\033[0m'

def colorize(c):
    if c == 'x':
        return BoardColors.X + c + BoardColors.END
    if c == '0':
        return BoardColors.ZERO + c + BoardColors.END
    if c == '1':
        return BoardColors.ONE + c + BoardColors.END
    return c
