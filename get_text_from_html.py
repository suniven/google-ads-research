from bs4 import BeautifulSoup
import lxml
import re

with open('./webpage.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

bs = BeautifulSoup(html, "lxml")
text = bs.get_text()
text = text.translate(text.maketrans("\n\t\r", "   "))
print(text)
