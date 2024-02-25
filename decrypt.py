import sys
import pandas as pd 
import io

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

czech_dictionary = set()

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


def LoadCzechDictionary(file):
    with open(file, 'r', encoding='utf-8') as file:
        dictionary = set()  # Create a local set variable
        for line in file:
            word = line.split('/')[0].strip()
            dictionary.add(word)
        return dictionary

# Function to check if a word is Czech
def is_czech(word):
    return word.lower() in czech_dictionary

# Todo function that find if the str is prefix of the czech word 
def is_prefix_of_czech_word(prefix):
    # Check if any word in the Czech dictionary starts with the given prefix
    for word in czech_dictionary:
        if word.startswith(prefix.lower()):
            return True
    return False

# Create csv from decrypted text so it can be easily moved to pandas 
def build_csv(decrypted_text):
    csv = ""
    for s in decrypted_text:    
        for i in range(0, len(s)):
            csv += s[i] + ";"
        csv += "\n"
    return csv

# find row where there is general keywoard 
def letters_in_row(df, general):

    special_char = []
    for i in range(0,len(general)):
        special_char.append(general[i])

    for i, row in df.iterrows():
        all_found = True 
        for j in special_char: 
            if j not in df.iloc[i].values:
                all_found = False 
                break
            if all_found: 
                return i

def switch_columns(df, c1, c2):
    # Store values from the 2nd column
    temp_values = df.iloc[:, c1].copy()

    # Assign values from the 4th column to the 2nd column
    df.iloc[:, c1] = df.iloc[:, c2]

    # Assign stored values to the 4th column
    df.iloc[:, c2] = temp_values

def get_n_word_in_row(df, n, row):
    
    word = ""

    # Split the row by "-"
    r = df.iloc[row]
    
    word_count = 0; 
    for cell in r:
        # todo ignore rest of the special chars. 
        # '.','?','-','/'
        if cell == '-':
            word_count += 1
            if word_count == n: 
                return word
            word = ""
            continue
        word += cell





def main():
    
    global czech_dictionary

    encrypted_text = []
    decrypted_text = []

    df = pd.DataFrame()

    # csv purpose is for easy pandas dataframe creation
    csv = ""

    general = ""

    day     = ""
    month   = ""
    year    = "" 

    password1 = ""
    password2 = ""

    # Parse the encrypted file 
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

    csv = build_csv(decrypted_text)

    df = pd.read_csv(io.StringIO(csv), header=None, sep=';')
    df = df.astype(str)
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    print(df)

    czech_dictionary = LoadCzechDictionary("Czech.dic")
    czech_dictionary.add(str(general))

    ### NOW BRUTE FORCE CHANGE THE COLLUMNS BUT LET EVERYTHING TO BE A CZECH WORD 

    ## first find the general 

    special_letters = []
    
    row_general = letters_in_row(df, general)
    print(row_general)

    # print(special_letters)
    # # First column 
    # print(df[0])
    # # first row 
    # print(df.iloc[0]) 
    # for cell in df.iloc[0]:
        # print(cell)

    switch_columns(df, 0,1)
    print(df)    
    
    print("here")
    # Example usage:
    nth_word = get_n_word_in_row(df, 1, 1)  # Get the 3rd word from the first row
    print(nth_word)


if __name__ == "__main__":
    main()