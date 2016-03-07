import nltk
import operator
import unicodedata
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

# All related files
files = ["reut2-000.sgm", "reut2-001.sgm","reut2-002.sgm","reut2-003.sgm","reut2-004.sgm", "reut2-005.sgm", "reut2-006.sgm", "reut2-007.sgm",
		 "reut2-008.sgm", "reut2-009.sgm", "reut2-010.sgm", "reut2-011.sgm", "reut2-012.sgm", "reut2-013.sgm", "reut2-014.sgm",
		 "reut2-015.sgm", "reut2-016.sgm", "reut2-017.sgm", "reut2-018.sgm", "reut2-019.sgm", "reut2-020.sgm", "reut2-021.sgm"]

# Hashmap, in order to store dictionary
hashMap = {}

# Counter of news from files
counter = 1

# Stemmer buffer
stemmer = PorterStemmer()

# Stop words from nltk library
stopWordsList = stopwords.words('english')


for f in files :
	# Open and read all files
	everyThing = open(f)
	allNews = everyThing.read()
	# Parsing sgm file to read easly
	parsedFile = BeautifulSoup(allNews,"html.parser")
	# Texts which have both title and body
	texts = parsedFile.find_all('text')

	for text in texts:

		tokenList = []
		# All title related data
		title = text.find('title')
		# Tokenize words meanwhile adding to the tokenList
		tokenList = tokenList + nltk.word_tokenize(str(title))
		
		# The next body related data
		if text.find('body'):
			body = text.find('body')
			tokenList = tokenList + nltk.word_tokenize(str(body))

		# To make meaningful dictionary, i have decided to remove these trashes from texts
		trashes = (['<', '>', 'body', 'title', '&', 'lt', ';', ':', '...', ')', '(' "'s", '.', 'gt', "'", '/body', '/title', ',', '``', '--', "''", "\x03"])
		newTokenList =  [ i for i in tokenList if i not in trashes ]

		# To lower case tokenList elements
		oneToken = [oneToken.lower() for oneToken in newTokenList]
		# To remove stopwords from dictionary
		newTokenList =  [ i for i in oneToken if i not in stopWordsList ]
			
		for tok in newTokenList:
			# To decode token to utf-8 to avoid python based errors related to non-alphabetical letters
			tok = tok.decode('utf-8')
			# To encode token
			newTok = ''.join(c for c in unicodedata.normalize('NFKD', tok) if unicodedata.category(c) != 'Mn')
			#print(stemmer.stem(newTok))
			newTok = stemmer.stem(newTok)
			if newTok in hashMap:
				hashMap[newTok].append(counter)
				#hashMap[newTok] += 1
			else:
				hashMap[newTok] = [counter]
				#hashMap[newTok] = 1

		counter = counter + 1

# To sort hashmap in the case of first element which is key or second element which is list of indexes
#inverted_index = sorted(hashMap.items(), key=operator.itemgetter(0))

# To sort hashmap lists
for key in hashMap.keys():
	hashMap[key] = sorted(set(hashMap[key]))

#print(hashMap)

andOrOr = raw_input("What do you want to use? (a)AND or (o)OR:\n ~ ")
nOfWords = input("How many words does your query have?\n ~ ")
# Words from user that will be searched
words = []
newString = ''

# To take words one by one and append to words list
for i in range(1, nOfWords+1):
	word = raw_input("Enter the %sth word: " %i)
	newString = newString + str(word) + ' '
	words.append(word)

newWords = []
newWords = newWords + nltk.word_tokenize(str(newString))
oneToken = [oneToken.lower() for oneToken in newWords]
newTokenList =  [ i for i in oneToken if i not in stopWordsList ]
query = []
# Same operations for query to normalize, tokenize etc.
for tok in newTokenList:
	tok = tok.decode('utf-8')
	new = ''.join(c for c in unicodedata.normalize('NFKD', tok) if unicodedata.category(c) != 'Mn')
	new = stemmer.stem(new)
	query.append(new)

resultList = []
# Intersection of words' indexes
if andOrOr == "AND" or andOrOr == "and" or andOrOr == "a":
	resultList = hashMap[query[0]]
	for i in range(1, len(query)):
		resultList = list(set(hashMap[query[i]]).intersection(resultList))
	resultList = sorted(resultList)

# Mergence of words' indexes
elif andOrOr == "OR" or andOrOr == "or" or andOrOr == "o":
	for i in range(0, len(query)):
		resultList = list(set(resultList + hashMap[query[i]]))
	resultList = sorted(resultList)

print("Result of Your Search, Indexes of Words: ")
print(resultList)