import sys
import pandas as pd 
import io
from llist import dllist
import itertools
import unicodedata

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
                return False
            prev = c
    return True

def check_manuall_fix(df, fr, to):
    print("CHECK MANNUALL")
    index = 0
    for r in df.iloc:
        word_lists = words_from_to(df, index, fr, to)
        for w in word_lists: 
            if w == "přio":
                print(word_lists) 
                return False
            elif w == "pří":
                print(word_lists) 
                return False
            elif w == "pri":
                print(word_lists) 
                return False
            elif w == "při":
                print(word_lists) 
                return False
        index += 1
    return True

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

    res_df[20] = df.iloc[:,20]
    used_index.append(20)
    
    res_df[15] = df.iloc[:,15]
    used_index.append(15)
    
    res_df[26] = df.iloc[:,26]
    used_index.append(26)
    
    res_df[39] = df.iloc[:,39]
    used_index.append(39)
    
    res_df[23] = df.iloc[:,23]
    used_index.append(23)

    res_df[1] = df.iloc[:,1]
    used_index.append(23)

    res_df[29] = df.iloc[:,29]
    used_index.append(29)
    
    res_df[42] = df.iloc[:,42]
    used_index.append(42)
    
    res_df[8] = df.iloc[:,8]
    used_index.append(8)
    
    res_df[48] = df.iloc[:,48]
    used_index.append(48)
    
    res_df[32] = df.iloc[:,32]
    used_index.append(32)
    
    res_df[53] = df.iloc[:,53]
    used_index.append(53)
    
    res_df[11] = df.iloc[:,11]
    used_index.append(11)
    
    res_df[51] = df.iloc[:,51]
    used_index.append(51)

    res_df[35] = df.iloc[:,35]
    used_index.append(35)
    
    res_df[4] = df.iloc[:,4]
    used_index.append(4)
    
    res_df[14] = df.iloc[:,14]
    used_index.append(14)
    
    res_df[19] = df.iloc[:,19]
    used_index.append(19)
    
    res_df[38] = df.iloc[:,38]
    used_index.append(38)
    
    res_df[7] = df.iloc[:,7]
    used_index.append(7)
    
    res_df[44] = df.iloc[:,44]
    used_index.append(44)
    
    res_df[56] = df.iloc[:,56]
    used_index.append(56)
    
    res_df[41] = df.iloc[:,41]
    used_index.append(56)
    
    res_df[28] = df.iloc[:,28]
    used_index.append(28)
    
    res_df[47] = df.iloc[:,47]
    used_index.append(47)
    
    res_df[59] = df.iloc[:,59]
    used_index.append(59)

    res_df[0] = df.iloc[:,0]
    used_index.append(0)
    
    res_df[22] = df.iloc[:,22]
    used_index.append(22)
    
    res_df[50] = df.iloc[:,50]
    used_index.append(50)
    
    res_df[10] = df.iloc[:,10]
    used_index.append(10)
    
    res_df[3] = df.iloc[:,3]
    used_index.append(3)
    
    res_df[25] = df.iloc[:,25]
    used_index.append(25)
    
    res_df[52] = df.iloc[:,52]
    used_index.append(52)
    
    res_df[31] = df.iloc[:,31]
    used_index.append(31)
    
    res_df[6] = df.iloc[:,6]
    used_index.append(6)
    
    res_df[37] = df.iloc[:,37]
    used_index.append(37)
    
    res_df[55] = df.iloc[:,55]
    used_index.append(55)

    res_df[34] = df.iloc[:,34]
    used_index.append(34)
    
    res_df[18] = df.iloc[:,18]
    used_index.append(18)
    
    res_df[13] = df.iloc[:,13]
    used_index.append(13)
    
    res_df[58] = df.iloc[:,58]
    used_index.append(58)
    
    res_df[46] = df.iloc[:,46]
    used_index.append(46)
    
    res_df[21] = df.iloc[:,21]
    used_index.append(21)
    
    res_df[16] = df.iloc[:,16]
    used_index.append(16)
    
    res_df[27] = df.iloc[:,27]
    used_index.append(27)
    
    res_df[40] = df.iloc[:,40]
    used_index.append(40)
    
    res_df[24] = df.iloc[:,24]
    used_index.append(24)
    
    res_df[2] = df.iloc[:,2]
    used_index.append(2)
    
    res_df[30] = df.iloc[:,30]
    used_index.append(30)
    
    res_df[43] = df.iloc[:,43]
    used_index.append(43)
    
    res_df[9] = df.iloc[:,9]
    used_index.append(9)
    
    res_df[49] = df.iloc[:,49]
    used_index.append(49)
    
    maybe = []

    kulo = False 
    ## APPEND FROM RIGHT 
    while kulo == False:
        c = 0
        unused_indices = [i for i in range(60) if i not in used_index]
        combi = list(itertools.combinations(unused_indices, 1))
        values = [res_df.iloc[0, i] for i in range(res_df.shape[1])]
        result_string = ''.join(values)
        for combination in combi:
            c = c+1
            temp_df = res_df.copy()
                
#            temp_df2 = ""
#            for i in combination:
#                temp_df2 += df.iloc[0, i]
#            if optimal_check(result_string + temp_df2) == False:
#                continue

            print("DONE:" + str(c) + "/" + str(len(combi)) ) 
            for i in combination:
                temp_df[i] = df.iloc[:, i] 
            print(temp_df) 
            if check_if_czech_substring(temp_df, 0, temp_df.shape[1]) and check_double_space(temp_df, 0, temp_df.shape[1]):
                kulo = False
                #res_df = temp_df.copy()
                used_index.extend(combination)  # Add all indices in the current combination to used_index
            else:
                kulo = True





if __name__ == "__main__":
    main()