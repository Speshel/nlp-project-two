'''
#=============================================#
#    Assignment: Project 2                    #
#    Student   : Devyn Caterer | Logan Fuller #
#    Student # : T00527623 | T00527200        #
#=============================================#

#=============================================#
#                 How To Run                  #
#=============================================#

python main.py --help
	parameter information
	
python main.py -t1 Emma.txt -t2 Great_Expectations.txt -e emotionFolder
	-t1	Text one to compare. Receives either a full path or filename ending in .txt
	-t2	Text two to compare. Receives either a full path or filename ending in .txt
	-e	folder containing the emotion .txt files. Accepts a string name of the folder (default = 'emotions')
	
#=============================================#
#               Handling Ngrams               #
#=============================================#

Unigrams
	Unigrams are single emotion words and simply add to the count

Bigrams
	Bigrams are preceded by a Valency Shifter
	Valency Shifter:
		- If on parsing find a Valency Shifter check if word after is emotion
		- Add to negative emotion type
		
Trigrams
	Trigrams are as follows:
		- [Emotion --> Intensifier --> Valency Shifter]

'''


import os, re, nltk, pprint
import argparse
from platform import system
from collections import defaultdict
from operator import itemgetter

'''
#=============================================#
#                    Main                     #
#=============================================#
'''

def main():
	# Argument Parsing
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-t1', '--textOne', help='Text #1 Filename to load')
	parser.add_argument('-t2', '--textTwo', help='Text #2 Filename to load')
	parser.add_argument('-e', '--emotions', help='Directory for emotions', type=str, default='emotions')
	args = parser.parse_args()
	
	# No Text One
	if not args.textOne:
		args.textOne = file_input('> Enter text one name [.txt]: ')
	# No Text Two
	if not args.textTwo:
		args.textTwo = file_input('> Enter text two name [.txt]: ')

	emotion_words_dict = defaultdict(list)
	emotions_list = []
	directory = os.fsencode(args.emotions)
	
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".txt"):
			emotion = filename[:-4]
			fullFilename = args.emotions + '\/' + filename
			emotions_list.append(emotion)
			with open(fullFilename, 'r') as x:
				data = x.read().splitlines()
				for item in data:
					emotion_words_dict[item].append(emotion)

					
	# Set of intensifiers
	with open('intensifiers.txt') as intensifiers_text:
		content = intensifiers_text.readlines()
	intensifiers = set([x.strip() for x in content])

	# Set of negations
	with open('negations.txt') as negations_text:
		content = negations_text.readlines()
	negations = set([x.strip() for x in content])

	print("> Analysing " + args.textOne + " and " + args.textTwo)

	#
	# Tokenize the sentences in each text into tokenized sentences
	#

	print("> Tokenizing...")

	text_one_tokenized_sentences = tokenize(args.textOne)
	text_two_tokenized_sentences = tokenize(args.textTwo)

	# Print total number of sentences for each text
	print("> Sentence Count (" + args.textOne + "): " + str(len(text_one_tokenized_sentences)))
	print("> Sentence Count (" + args.textTwo + "): " + str(len(text_two_tokenized_sentences)))
	
	#
	# Add each sentence with an emotion word into a new list (emotion_sentences)
	# AKA it ignores sentences without an emotion word
	#

	# Begin adding sentences from the first text
	emotion_sentences = {}

	print("> Filtering " + args.textOne + " emotion sentences")
	emotion_sentences[args.textOne] = filter_text(text_one_tokenized_sentences, emotion_words_dict)

	print("> Filtering " + args.textTwo + " emotion sentences")
	emotion_sentences[args.textTwo] = filter_text(text_two_tokenized_sentences, emotion_words_dict)
	
	preparsed_sentences = preparse(emotion_sentences, emotion_words_dict)
	
	# print(preparsed_sentences)
	text_metrics = doparse(preparsed_sentences, negations, intensifiers, emotion_words_dict)
	
	tabulize(text_metrics, emotions_list)
	compare(args.textOne, args.textTwo, text_metrics, emotions_list)

'''
#=============================================#
#                  Functions                  #
#=============================================#
'''

def tabulize(metrics, emotions):
	for text in metrics:
		print()
		print('> #======== ' + text + ' ========#')
		print('> Unigrams: ' + str(metrics[text]['unigrams']))
		print('> Bigrams: ' + str(metrics[text]['bigrams']))
		print('> Trigrams: ' + str(metrics[text]['trigrams']))
		print('> #======== Emotions ========#')
		for e in emotions:
			notemotion = 'not ' + e
			print('> ' + e + ': ' + str(metrics[text][e]) + ' | ' + notemotion + ': ' + str(metrics[text][notemotion]))

	print()

def compare(t1, t2, metrics, emotions):
	print('> #======== Comparison ========#')
	for e in emotions:
		if (metrics[t1][e] > metrics[t2][e]):
			print('> ' + t1 + ' is more ' + e)
		else:
			print('> ' + t2 + ' is more ' + e)
	for e in emotions:
		notemotion = 'not ' + e
		if (metrics[t1][notemotion] > metrics[t2][notemotion]):
			print('> ' + t1 + ' is more ' + notemotion)
		else:
			print('> ' + t2 + ' is more ' + notemotion)

def doparse(preparsed, negations, intensifiers, edict):
	text_metrics = defaultdict(lambda: defaultdict(int))
	for text in preparsed:
		for sentence in preparsed[text]:
			# Check if valency shifter or nothing
			# if not unigram
			if len(sentence) > 1:
				wombocombo = ''
				wclen = 0
				indices = {}
				indices[0] = 'E'
				for i in range(1,len(sentence)):
					indices[i] = 'X'
					if sentence[i] in negations:
						indices[i] = 'S'
						# found shifter
					elif sentence[i] in intensifiers:
						indices[i] = 'I'
						# found intensifier this is useless if there is not a shifter after it
					else:
						# add to combination word
						wclen += 1
						wombocombo += sentence[i]
						if wombocombo in negations:
							for j in range(wclen):
								indices[i-(j-1)] = 'S'
							# wombocombo is a shifter
						elif wombocombo in intensifiers:
							for j in range(wclen):
								indices[i-(j-1)] = 'I'
							# wombocombo is an intensifier
						else:
							# add space for next item
							wombocombo += ' '
				sorted(indices)
				indiceunigramtypes = ['E', 'EI', 'EII', 'EIII', 'EIIII', 'EIIIII']
				indicebigramtypes = ['ES', 'ESI', 'ESII', 'ESIII', 'ESIIII']
				indicetrigramtypes = ['EIS', 'EISS', 'EIIS', 'EIISS', 'EIIIS', 'EIIISS', 'EIIIIS']			
				checkable = ''
				for i in range(0,len(indices)):
					if indices[i] != 'X':
						checkable += indices[i]
					else:
						if checkable in indicetrigramtypes:
							# trigram
							emotions = edict[sentence[0]]
							for e in emotions:
								text_metrics[text]['not ' + e] += 1
							text_metrics[text]['trigrams'] += 1
						elif checkable in indicebigramtypes:
							# bigram
							emotions = edict[sentence[0]]
							for e in emotions:
								text_metrics[text]['not ' + e] += 1
							text_metrics[text]['bigrams'] += 1
						elif checkable in indiceunigramtypes:
							# unigram
							emotions = edict[sentence[0]]
							for e in emotions:
								text_metrics[text][e] += 1
							text_metrics[text]['unigrams'] += 1
						break
			else:
				# unigram
				emotions = edict[sentence[0]]
				for e in emotions:
					text_metrics[text][e] += 1
				text_metrics[text]['unigrams'] += 1
	return text_metrics

def preparse(e, d):
	preparsed_sentences = defaultdict(list)
	for text in e:
		for sentence in e[text]:
			reversedSentence = sentence[::-1]
			trimmedSentence = []
			currentindex = 0
			for word in reversedSentence:
				# print(word)
				if word in d:
					sentLen = len(reversedSentence)
					numwordstouse = 5
					if abs(sentLen - currentindex) < 5:
						numwordstouse = abs(sentLen - currentindex)
					sindex = currentindex + numwordstouse
					splitSentence = reversedSentence[currentindex:sindex]
					
					cleanedSplit = []
					cleanedSplit.append(splitSentence[0])
					
					for i in range(1,len(splitSentence)):
						if splitSentence[i] not in d:
							cleanedSplit.append(splitSentence[i])
						else:
							break
					preparsed_sentences[text].append(cleanedSplit)
				currentindex += 1
	return preparsed_sentences

def tokenize(t):
	print("> Token Count (" + t + "): " + str(len(nltk.word_tokenize(open(t).read().replace('\n', ' ').replace('--', ' ')))))
	sentences = nltk.sent_tokenize(open(t).read().replace('\n', ' ').replace('--', ' '))
	tok_sent = []
	for sentence in sentences:
		tok_sent.append(nltk.word_tokenize(sentence))
	return tok_sent
	

def filter_text(s, e):
	emotion_sentences = []
	for sentence in s:
		e_word = False
		for word in sentence:
			if e_word == False:
				if word in e:
					emotion_sentences.append(sentence)
					e_word = True
	return emotion_sentences

def file_input(prompt):
	path = input(prompt)
	if os.path.isfile(path):
		return path
	else:
		return file_input('Enter an existing file path: ')

def folder_input(prompt):
	path = input(prompt)
	if os.path.isdir(path):
		return path
	else:
		return folder_input('Enter an existing folder path: ')
main()