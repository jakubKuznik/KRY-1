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
    result = ""

    for i in range(0, len(str) - 1, 2):
        two_chars = str[i:i+2]
        result += countChar(int(two_chars))
    
    return result

# return char from cipher table  
def countChar(num):
    # cannot be created in the cipher table 
    if num > 49: 
        return ''
    return cipherAlphabet[num]

def main():

    encrypted_text = []
    decrypted_text = []

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

    # Create cipher table 
    createCipherAlphabet(day) 
    
    
    for i in encrypted_text:
        decrypted_text.append(translate(i))

    for i in range(0,61):
        print(f"{i:2}", end=" ")
    print()
    for str in decrypted_text:
        print(" ", end="")
        for i in range(0, len(str)):
            print(str[i], end="  ")
        print()

if __name__ == "__main__":
    main()