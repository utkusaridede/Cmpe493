from bs4 import BeautifulSoup
import nltk
import unicodedata
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

files = ["reut2-000.sgm", "reut2-001.sgm","reut2-002.sgm","reut2-003.sgm","reut2-004.sgm", "reut2-005.sgm", "reut2-006.sgm", "reut2-007.sgm",
		 "reut2-008.sgm", "reut2-009.sgm", "reut2-010.sgm", "reut2-011.sgm", "reut2-012.sgm", "reut2-013.sgm", "reut2-014.sgm",
		 "reut2-015.sgm", "reut2-016.sgm", "reut2-017.sgm", "reut2-018.sgm", "reut2-019.sgm", "reut2-020.sgm", "reut2-021.sgm" ]

hashMap = {}
counter = 1

for i in files :

	content = open(i)
	x = content.read()
	soup = BeautifulSoup(x,"html.parser")
	print(soup)
	documents = soup.find_all('body')
	titles = soup.find_all('title')
	
	for document in documents :
		tokens = []
		tokens = tokens + nltk.word_tokenize(str(document))
		dandiqler = (['<', '>', 'body', 'title', '&', 'lt', ';', "'s", '.', 'gt', "'", '-', '/body', '/title', ',', '``', '--', "''", "\x03"])
		newTokens =  [ i for i in tokens if i not in dandiqler ]

		stop = stopwords.words('english')
		token = [token.lower() for token in newTokens]
		doc =  [ i for i in token if i not in stop ]

		ps = PorterStemmer()
			
		for w in doc:
			w = w.decode('utf-8')
			new = ''.join(c for c in unicodedata.normalize('NFKD', w) if unicodedata.category(c) != 'Mn')
			#print(ps.stem(new))

			if new in hashMap:
				hashMap[new].append(counter)
			else:
				hashMap[new] = [counter]

		counter = counter + 1

	print(counter)

print(counter)
print(hashMap['week'])