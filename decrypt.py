import sys

alphabet = [
            'A','B','C','Č','D','E','Ě','F','G','H',
            'I','J','K','L','M','N','O','P','Q','R',
            'Ř','S','Š','T','U','V','W','X','Y','Z',
            'Ž','.','?','-','/','1','2','3','4','5',
            '6','7','8','9','0','' ,'' ,'' ,'' , '', 
            ]
            
cipherAlphabet = [
            'A','B','C','Č','D','E','Ě','F','G','H',
            'I','J','K','L','M','N','O','P','Q','R',
            'Ř','S','Š','T','U','V','W','X','Y','Z',
            'Ž','.','?','-','/','1','2','3','4','5',
            '6','7','8','9','0','' ,'' ,'' ,'' , '', 
            ]

def createCipherAlphabet(day):

    # Create the cipher alphabet with cyclic shift
    for i in range(len(alphabet)):
        index = (i + day) % len(alphabet)
        cipherAlphabet[index] = alphabet[i]

# Translate the numbers into the string using cipher table 
def translate(str):
    str = str.replace(" ", "")
    print(str)
    for i in range(0, len(str) - 1, 2):
        two_chars = str[i:i+2]
        #print(two_chars)


# return char shiftet in table 
def countChar(day, c):
    index = alphabet.index(c)

    print(alphabet.index(c))


def main():

    encrypted_text = []

    general = ""

    day     = ""
    month   = ""
    year    = "" 

    password1 = ""
    password2 = ""


    for line in sys.stdin:
        if line.startswith('Datum:'):
            date_str = line.split(':')[1].strip()  
            day, month, year = map(int, date_str.split('.'))  
            print(f"Day: {day}, Month: {month}, Year: {year}")  
        elif line.startswith('ZP'):
            next_line = next(sys.stdin, None)
            encrypted_text.append((line.split(':')[1].lstrip().rstrip('\n')) + ' ' + next_line.lstrip().rstrip('\n'))
        elif " x" in line: 
            general = line.split(' ')[1].split()[0]
            print("General:",general)

    for i in encrypted_text:
        print(i)     
    translate(encrypted_text[0])
    createCipherAlphabet(day) 
    print(alphabet)
    print(cipherAlphabet)
            


if __name__ == "__main__":
    main()