import os
import re
import nltk
import math
import heapq
import numpy
import string
from nltk.tokenize import RegexpTokenizer

#File operations in local directory for learning process.
def knnLearning(directory, op):

	#####################################################
	# Reading txt files
	#####################################################
	legitimate = []
	spam = []
	tests = []

	for txtFile in os.listdir("dataset/training/legitimate"):
		if txtFile.endswith(".txt"):
			legitimate.append(txtFile)

	for txtFile in os.listdir("dataset/training/spam"):
		if txtFile.endswith(".txt"):
			spam.append(txtFile)

	for txtFile in os.listdir(directory):
		if txtFile.endswith(".txt"):
			tests.append(txtFile)

	#####################################################
	# Preparing for Learning Data
	#####################################################
	vocabularyHash = {}
	allWords = []
	counter = 0
	for f in legitimate:
		oneFile = open("dataset/training/legitimate/" + f, "r")
		oneFile = [''.join(c for c in s if c not in string.punctuation) for s in oneFile]
		for words in oneFile:
			words = nltk.word_tokenize(str(words))
			for item in words:
				if item in vocabularyHash:
					vocabularyHash[item].append(counter)
				else:
					vocabularyHash[item] = [counter]

		counter += 1

	for f in spam:
		oneFile = open("dataset/training/spam/" + f, "r")
		oneFile = [''.join(c for c in s if c not in string.punctuation) for s in oneFile]
		for words in oneFile:
			words = nltk.word_tokenize(str(words))
			for item in words:
				if item in vocabularyHash:
					vocabularyHash[item].append(counter)
				else:
					vocabularyHash[item] = [counter]

		counter += 1

	sizeOfLearningData = len(legitimate) + len(spam)
	sizeOfVocabulary = len(vocabularyHash)

	#####################################################
	# Preparing for Test Data
	#####################################################
	testVocabulary = {}
	counter = 0
	for f in tests:
		oneFile = open(directory + "/" + f, "r")
		oneFile = [''.join(c for c in s if c not in string.punctuation) for s in oneFile]
		for words in oneFile:
			words = nltk.word_tokenize(str(words))
			for item in words:
				if item in testVocabulary:
					testVocabulary[item].append(counter)
				else:
					testVocabulary[item] = [counter]
		counter += 1

	sizeOfTestData = len(tests)
	sizeOfTestVoc = len(testVocabulary)

	#####################################################
	# Filling Matrix
	#####################################################
	tfidfMatrix = numpy.zeros((sizeOfLearningData+sizeOfTestData, sizeOfVocabulary))
	for i in range(0, sizeOfLearningData + sizeOfTestData):
		numberOfVocabulary = 0
		for key in vocabularyHash:
			allWords.append(key)
			if i < sizeOfLearningData:
				tf = vocabularyHash[key].count(i)
				df = len(set(vocabularyHash[key]))
				if tf > 0:
					one = 1.0 + math.log(tf, 10.0)
					second = math.log((float(sizeOfLearningData)/df), 10.0)
					tfidf = one * second
					tfidfMatrix[i][numberOfVocabulary] = tfidf
			else:
				if key in testVocabulary:
					tf = testVocabulary[key].count(i-sizeOfLearningData)
					df = len(set(vocabularyHash[key]))
					if tf > 0:
						one = 1.0 + float(math.log(tf, 10.0))
						second = math.log(float(sizeOfLearningData)/float(df), 10.0)
						tfidf = one * second
						tfidfMatrix[i][numberOfVocabulary] = tfidf

			numberOfVocabulary += 1

	#####################################################
	# kNN Algorithm
	#####################################################
	if op == 1:

		index = []
		numberOfLeg = 0
		numberOfSpam = 0
		for i in range(sizeOfLearningData, sizeOfTestData+sizeOfLearningData):
			cosineSim = []
			del index[:]
			for k in range(0, sizeOfLearningData):
				learnVec = tfidfMatrix[k,:]
				testVec = tfidfMatrix[i,:]
				cos = numpy.dot(learnVec, testVec) / ((numpy.linalg.norm(learnVec)) *  (numpy.linalg.norm(testVec)))
				cosineSim.append(cos)
			
			tmp = cosineSim
			index = sorted(range(len(tmp)), key=lambda x: tmp[x])[-3:]
			counter = 0
			for t in index:
				if t < len(legitimate):
					counter += 1
				else:
					counter -= 1
			if counter > 0:
				#numberOfLeg += 1
				print tests[i-sizeOfLearningData] + " legitimate"
			else:
				#numberOfSpam += 1
				print tests[i-sizeOfLearningData] + " spam"
		
		#print "legitimate: " + str(numberOfLeg)
		#print "spam:       " + str(numberOfSpam)

	#####################################################
	# Rocchio Algorithm
	#####################################################
	elif op == 2:
		legitimateVectorMean = []
		spamVectorMean = []
		numberOfLeg = 0
		numberOfSpam = 0

		legitimateVectorMean = numpy.mean(tfidfMatrix[0:len(legitimate)][:], axis=0)
		total = len(legitimate) + len(spam)
		spamVectorMean = numpy.mean(tfidfMatrix[len(legitimate):total][:], axis=0)
		
		for i in range(sizeOfLearningData, sizeOfTestData+sizeOfLearningData):
			testVec = tfidfMatrix[i,:]
			cosineSimLegi = numpy.dot(legitimateVectorMean, testVec) / ((numpy.linalg.norm(legitimateVectorMean)) *  (numpy.linalg.norm(testVec)))
			cosineSimSpam = numpy.dot(spamVectorMean, testVec) / ((numpy.linalg.norm(spamVectorMean)) *  (numpy.linalg.norm(testVec)))

			if cosineSimLegi > cosineSimSpam:
				#numberOfLeg += 1
				print tests[i-sizeOfLearningData] + " legitimate"
			else:
				#numberOfSpam += 1
				print tests[i-sizeOfLearningData] + " spam"

		#print numberOfLeg
		#print numberOfSpam

	#####################################################
	# Calculates top 20 words in legitimate and spam data
	#####################################################
	'''
	wordsTfidfs = []
	allSumTfidfs = []
	# Legitimate e-mail total tfidf
	for i in range(0, len(vocabularyHash)):
		wordsTfidfs = tfidfMatrix[:len(legitimate),i]
		sumTfidfs = numpy.sum(wordsTfidfs)
		allSumTfidfs.append(sumTfidfs)

	index = sorted(range(len(allSumTfidfs)), key=lambda x: allSumTfidfs[x])[-20:]
	print index
	for item in index:
		print allWords[item] + " => " + str(allSumTfidfs[item])
	
	# Spam e-mail total tfidf
	del allSumTfidfs[:]
	
	for i in range(0, len(vocabularyHash)):
		wordsTfidfs = tfidfMatrix[len(legitimate):len(spam)+len(legitimate),i]
		sumTfidfs = numpy.sum(wordsTfidfs)
		allSumTfidfs.append(sumTfidfs)

	index = sorted(range(len(allSumTfidfs)), key=lambda x: allSumTfidfs[x])[-20:]
	print index
	for item in index:
		print allWords[item] + " => " + str(allSumTfidfs[item])

	'''
	#numpy.savetxt('test.txt', tfidfMatrix, fmt='%-7.2f')

print "Learning Action will use 'dataset/training/legitimate' and 'dataset/training/spam' folders at current directory."
print "What do you want to do: "
print "[1] KNN Spam Filter"
print "[2] Rocchio Spam Filter"

op = input(" ~ ")

print "Enter the directory of test dataset: (ex. if you enter /home/utku/folder, it will take /home/utku/folder/dataset as test data)"
directory = raw_input(" ~ ")
knnLearning(directory, op)