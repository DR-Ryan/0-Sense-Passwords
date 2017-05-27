import requests
import bs4

alphabet = "abcdefghijklmnopqrstuvwxyz"


dictionaryFile = open("Webster Dictionary", "w")

for letter in alphabet:
    res = requests.get('https://www.merriam-webster.com/browse/dictionary/' + letter)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    pageCount = soup.find(class_='counters').text.split(' ')[3]
    dictionaryFile.write(letter)
    dictionaryFile.write(":")
    dictionaryFile.write(pageCount)
    dictionaryFile.write("\n")

dictionaryFile.close()
