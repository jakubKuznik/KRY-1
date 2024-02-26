import sys
import pandas as pd 
import io
from llist import dllist
import itertools
import unicodedata
import time

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


def remove_diacritics(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))


def LoadCzechDictionary(file):
    with open(file, 'r', encoding='utf-8') as file:
        dictionary = set()  # Create a local set variable
        for line in file:
            word = line.split('/')[0].strip()
            dictionary.add(remove_diacritics(word))
        return dictionary

# Function to check if a word is Czech
def is_czech(word):
    return remove_diacritics(word.lower()) in czech_dictionary

# function that find if the str is prefix of the czech word 
def is_prefix_of_czech_word(prefix):
    normalized_prefix = remove_diacritics(prefix)
    # Check if any word in the Czech dictionary starts with the given prefix
    for word in czech_dictionary:
        if word.startswith(normalized_prefix.lower()):
            return True
    return False

def optimal_check(substring): 

    return True
    if "-" in substring:
        substrings = substring.split("-")
        i = 0
        for sub in substrings:
            i += 1
            if sub == "odboj":
                continue
            elif sub == "priprav":
                continue 
            else:
                return False
        return True

# Check if any word in the Czech dictionary starts with the given prefix
def is_substring_of_czech_word(substring):
    normalized_substring = remove_diacritics(substring)

    for word in czech_dictionary:
        if normalized_substring in word:
            return True
    return False

# Create csv from decrypted text so it can be easily moved to pandas 
def build_csv(decrypted_text):
    csv = ""
    for s in decrypted_text:    
        for i in range(0, len(s)):
            csv += remove_diacritics(s[i]) + ";"
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
                word += str(cell)
        char_count += 1
    word_list.append(word)
    return word_list

def check_double_space(df, fr, to):
    for r in df.iloc:
        prev = "XXX"
        for c in r: 
            if prev == "XXX":
                prev = str(c)
            if prev == "-" and str(c) == "-":
                print("DOUBLE SPACE:" + r)
                return False
            prev = c
    return True

## TODO THIS HAS TO BE CHANNGED BASED ON YOUR USECASE 
def check_manuall_fix(df, fr, to):
    index = 0
    for r in df.iloc:
        word_lists = words_from_to(df, index, fr, to)
        word = word_lists[1]
        # Manuall checks 
        if len(word_lists) > 2: 
            if word_lists[1] == "pri" and word_lists[2] == '':
                print("MANNUALL DECLINE: ", end="")
                print(word_lists)
                return False
            elif word_lists[1] == "prio": 
                print("MANNUALL DECLINE: ", end="")
                print(word_lists)
                return False
            elif word_lists[1] == "pripraven" and word_lists[2] == 'pode': 
                print("MANNUALL DECLINE: ", end="")
                print(word_lists)
                return False
            elif word_lists[1] == "pripraven" and word_lists[2] == 'podo': 
                print("MANNUALL DECLINE: ", end="")
                print(word_lists)
                return False
            elif word_lists[1] == "pripraven" and word_lists[2] == 'podz': 
                print("MANNUALL DECLINE: ", end="")
                print(word_lists)
                return False
            elif word_lists[1] == "pripraven" and word_lists[2] == 'podpe': 
                print("MANNUALL DECLINE: ", end="")
                print(word_lists)
                return False
        if len(word_lists) >3:
            if word_lists[1] == "pripraven" and word_lists[2] == 'p' and word_lists[3] == '':
                print("MANNUALL DECLINE: ", end="")
                print(word_lists)
                return False
        if len(word_lists) > 5:
            if word_lists[1] == "pripraven" and word_lists[4] == 'oper' and word_lists[5] == '':
                print("MANNUALL DECLINE: ", end="")
                print(word_lists)
                return False
        index += 1
    return True

# in DF from a to b check if all word in all rows are prefixes 
def check_if_czech_prefix(df, fr, to):

    index = 0
    for r in df.iloc:
        word_lists = words_from_to(df, index, fr, to)
        print(word_lists)
        for w in word_lists: 
            if is_prefix_of_czech_word(w) == False: 
                print("not a czec prefix: " + " " + w)
                return False
        index += 1
    return True

# in DF from a to b check if all word in all rows are substring  
def check_if_czech_substring(df, fr, to):

    index = 0
    for r in df.iloc:
        word_lists = words_from_to(df, index, fr, to)

        for w in word_lists: 
            if is_substring_of_czech_word(w) == False: 
                return False
        index += 1
    return True

def main():
    
    start_time = time.time()

    global czech_dictionary

    encrypted_text = []
    decrypted_text = []
    ll = []

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
    
    czech_dictionary = LoadCzechDictionary("Czech.dic")
    czech_dictionary.add(str(general))


    ### NOW BRUTE FORCE CHANGE THE COLLUMNS BUT LET EVERYTHING TO BE A CZECH WORD 
    ## first find the general 

    row_general = letters_in_row(df, general)

    for c in range(0, len(general)):
        ll.append(find_letter_column(df, str(general[c]), row_general))

    # Optimalization todo remove 
    print(ll)
    ll[1].remove(2)
    ll[1].remove(7)
    ll[3].remove(0)
    ll[4].remove(13)
    ll[4].remove(15)

    combinations = itertools.product(*ll)
    result = [list(combo) for combo in combinations]

    used_index = []
    res_df = pd.DataFrame()

    ## Find the general word in the text 
    counter = 0 
    for combo in result:  
        # Initialize a temporary DataFrame for the current combination
        temp_df = pd.DataFrame()

        # Iterate over the indices in the current combination
        for i in combo:
            # Append the column to the temporary DataFrame
            temp_df[i] = df.iloc[:, i]
        
        # Check if the combination meets some condition
        if check_if_czech_substring(temp_df, 0, combo[0]):
            used_index = combo
            res_df = pd.concat([res_df, temp_df], axis=1)
            print("heureka")
            break
    
    print(res_df)
    print(used_index)

    kulo = False 
    ## APPEND FROM RIGHT 
    while kulo == False:
        c = 0
        unused_indices = [i for i in range(60) if i not in used_index ]
        combi = set()
        combi = [(i, j) for i in unused_indices for j in unused_indices if i != j]  # Generate combinations for all existing pairs
        values = [res_df.iloc[0, i] for i in range(res_df.shape[1])]
        for combination in combi:
            c = c+1
            temp_df = res_df.copy()

            print("DONE:" + str(c) + "/" + str(len(combi)) ) 
            for i in combination:
                temp_df[i] = df.iloc[:, i] 
            print(temp_df) 
            if  check_if_czech_prefix(temp_df, 0, temp_df.shape[1]) \
                and check_manuall_fix(temp_df, 0 , temp_df.shape[1]) \
                and check_double_space(temp_df, 0, temp_df.shape[1]):
                res_df = temp_df.copy()
                used_index.extend(combination)  # Add all indices in the current combination to used_index
                kulo = False 
                break
            else:
                kulo = True

    print("SOLUTION:")
    print(res_df)
    
    print("")
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time: {:.2f} seconds".format(execution_time))




if __name__ == "__main__":
    main()