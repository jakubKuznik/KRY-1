import sys

alphabet = [
            '-','/','1','2','3','4','5','6','7','8',
            '9','0','A','B','C','Č','D','E','Ě','F',
            'G','H','I','J','K','L','M','N','O','P',
            'Q','R','Ř','S','Š','T','U','V','W','X',
            'Y','Z','Ž','.','?','' ,'' ,'' ,'', ''
            ]



def main():

    print(alphabet)
    print(alphabet[0])

    for line in sys.stdin:
        if line.startswith('Datum:'):
            date_str = line.split(':')[1].strip()  # Extract the date string after "Datum:"
            day, month, year = map(int, date_str.split('.'))  # Split the date string and convert to integers
            print(f"Day: {day}, Month: {month}, Year: {year}")  
        elif line.startswith('ZP'):
            sys.stdout.write(line)
        
if __name__ == "__main__":
    main()