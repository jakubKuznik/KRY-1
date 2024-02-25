import sys
import pandas as pd 
import io
from llist import dllist

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

    index = day-1; 
    for i in range(len(alphabet)-1, 0, -1):
        if cipherAlphabet[i] != '':
            cipherAlphabet[index] = cipherAlphabet[i]
            cipherAlphabet[i] = ''
            index = index - 1
            if index == -1:
                break


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
    return str(cipherAlphabet[num])

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

def is_substring_of_czech_word(substring):
    # Check if any word in the Czech dictionary starts with the given prefix
    for word in czech_dictionary:
        if substring in word:
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

def find_letter_column(df, c, row):
    
    r = df.iloc[row].astype(str)
    indices = []
    for index, cell in enumerate(r):
        if str(cell) == str(c):
            indices.append(index)
    return indices

def switch_columns(df, c1, c2):
    # Store values from the 2nd column
    temp_values = df.iloc[:, c1].copy()

    # Assign values from the 4th column to the 2nd column
    df.iloc[:, c1] = df.iloc[:, c2]

    # Assign stored values to the 4th column
    df.iloc[:, c2] = temp_values

def get_n_word_in_row(df, n, row):
    
    word = ""

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

# return list of word from index to index 
# RETURN SUBSTRING IF WORD IS NO FINISHED 
def words_from_to(df, row, fr, to): 
    
    word = ""
    word_list = []
    char_count = 0 

    r = df.iloc[row]

    for cell in r: 
        if char_count < fr:  # Skip characters until 'from' index
            char_count += 1
        elif char_count >= to:  # Stop when 'to' index is reached
            word_list.append(word)
            return word_list
        else:
            if cell == '-':
                word_list.append(word)
                word = ""
            if cell != '-':
                word += cell
        char_count += 1
    word_list.append(word)
    return word_list

# in DF from a to b check if all word in all rows are prefixes 
def check_if_czech_prefix(df, fr, to):
    
    index = 0
    for r in df.iloc:
        word_lists = words_from_to(df, index, fr, to)

        for w in word_lists: 
            if is_prefix_of_czech_word(w) == False: 
                return False
        index += 1
    return True

# in DF from a to b check if all word in all rows are substring  
def check_if_czech_substring(df, fr, to):

    print("check subs " + str(fr) +  " " + str(to)) 
    index = 0
    for r in df.iloc:
        word_lists = words_from_to(df, index, fr, to)

        for w in word_lists: 
            if is_substring_of_czech_word(w) == False: 
                return False
        index += 1
    return True

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
#        if '0' in translate(i):
#            print("")
#        if '4' in translate(i):
#            print("CTYRKA")
#        if 'O' in translate(i):
#            print("Heureka ")

    csv = build_csv(decrypted_text)

    df = pd.read_csv(io.StringIO(csv), header=None, sep=';')
    df = df.astype(str)
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    print(df)

    czech_dictionary = LoadCzechDictionary("Czech.dic")
    czech_dictionary.add(str(general))
    ### NOW BRUTE FORCE CHANGE THE COLLUMNS BUT LET EVERYTHING TO BE A CZECH WORD 

    ## first find the general 

    #general = "xkuznio4"
    print(general)
    row_general = letters_in_row(df, general)

    first_column = 0
    last_column = -1
    bad = True


    new_df = df.iloc[:, [1, 5]]
    print(new_df)

    dll = dllist()

    for c in range(0, len(general)):
        dll.append(find_letter_column(df, str(general[c]), row_general))

    for item in dll:
        print(item)

#    switch_columns(df, 0,1)
#    print(df)    
    
#    print("here")
#    # Example usage:
#    nth_word = get_n_word_in_row(df, 1, 1)  # Get the 3rd word from the first row
#    print(nth_word)

#    print(check_if_czech_prefix(df,0, 0))
#    print(words_from_to(df, 0, 0, 10))

if __name__ == "__main__":
    main()