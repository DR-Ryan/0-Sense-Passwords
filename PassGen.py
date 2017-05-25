import requests, bs4, sys, string, re
from random import randint, choice

def getLink(letter, number):
    res = requests.get('https://www.merriam-webster.com/browse/dictionary/' + letter + '/' + number)
    res.raise_for_status()
    return bs4.BeautifulSoup(res.text, "html.parser")


def pickWord(soup, wordLine):
    counter = 0
    for url in soup.find_all('div', class_='entries'):
        for word in url.find_all('a'):
            if counter == wordLine:
                if randint(0,1) == 1:
                    return word.text.capitalize()
                else:
                    return word.text
            counter += 1

# Remove special characters that may be in the word natively
def characterReplace(password, allowed):
    if allowed == 'N' or allowed == 'n':
        password = re.sub(r'\W+', '', password)
    elif allowed == 'Y' or allowed == 'y':
        password = password.replace(" ", "")
    else:
        print("So you can't follow directions huh?")
    return password

def main():
    password = ''
    try:
        length = int(input("How many words long should password be? "))
        allowed = input("Are special characters allowed? (y or n) ")
    except ValueError:
        print("So you think you're Mr.FunnyGuy huh?")
        print("I suggest ctrl-c now unless you want to wait for 500+ lookups")
        length = 500
        allowed = 'n'

    for i in range(length):
        letter = choice(string.ascii_lowercase)
        number = '1'
        soup = getLink(letter, number)

        # Webster page list displayed as "page 1 of n"
        pageCount = soup.find(class_='counters').text.split(' ')[3]
        pageCount = int(pageCount)

        # The reasoning for doing a link pull twice is because every letter
        # does not have the same amount of pages
        number = randint(1, pageCount+1)
        wordLine = randint(0, 300)
        if number != 1:
            soup = getLink(letter, str(number))

        # If it ends up on the last page their's a chance wordLine won't exist
        # and returns a nonetype
        while True:
            try:
                password += pickWord(soup, wordLine)
            except TypeError:
                continue
            break

    print("Password:", characterReplace(password, allowed))
if __name__ == '__main__':
    main()
