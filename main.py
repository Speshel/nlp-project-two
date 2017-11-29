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
	Bigrams are either preceded by Intensifiers or a Valency Shifter
	Valency Shifter:
		- If on parsing find a Valency Shifter check if word after is emotion
		- Add to negative emotion type

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
		args.textOne = file_input('Enter text one name [.txt]: ')
	# No Text Two
	if not args.textTwo:
		args.textTwo = file_input('Enter text two name [.txt]: ')

	emotions_dict = {}
	directory = os.fsencode(args.emotions)

	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".txt"):
			fileString = filename[:-4]
			emotions_dict[fileString] = set(open(args.emotions + '\/' + filename).read().splitlines())
			continue
		else:
			continue

	with open('intensifiers.txt') as intensifiers_text:
		content = intensifiers_text.readlines()
	intensifiers = set([x.strip() for x in content])

	with open('negations.txt') as negations_text:
		content = negations_text.readlines()
	negations = set([x.strip() for x in content])

	file_one = args.textOne
	file_two = args.textTwo

	print("Analysing " + file_one + " and " + file_two)

	#
	# Tokenize the sentences in each text into tokenized sentences
	#

	print("Tokenizing...")

	# Replace '--' with ' ' because '--' seems to break sentences.
	text_one_sentences = set(nltk.sent_tokenize(open(file_one).read().replace('\n', ' ').replace('--', ' ')))
	text_one_tokenized_sentences = []

	for sentence in text_one_sentences:
		text_one_tokenized_sentences.append(nltk.word_tokenize(sentence))

	###################

	text_two_sentences = set(nltk.sent_tokenize(open(file_two).read().replace('\n', ' ').replace('--', ' ')))
	text_two_tokenized_sentences = []

	for sentence in text_two_sentences:
		text_two_tokenized_sentences.append(nltk.word_tokenize(sentence))

	# Print total number of sentences for each text
	print("Sentence Count (" + file_one + "): " + str(len(text_one_sentences)))
	print("Sentence Count (" + file_two + "): " + str(len(text_two_sentences)))

	#
	# Add each sentence with an emotion word into a new list (emotion_sentences)
	# AKA it ignores sentences without an emotion word
	#

	# Begin adding sentences from the first text

	print("\nFiltering " + file_one + " emotion sentences")

	emotion_sentences = {}
	emotion_sentences[file_one] = defaultdict(list)

	for sentence in text_one_tokenized_sentences:
		for word in sentence:
			for emotion in emotions_dict:
				if word in emotions_dict[emotion]:
					emotion_sentences[file_one][emotion].append(sentence)

	emotion_sentences[file_two] = defaultdict(list)

	print("\nFiltering " + file_two + " emotion sentences")

	for sentence in text_two_tokenized_sentences:
		for word in sentence:
			for emotion in emotions_dict:
				if word in emotions_dict[emotion]:
					emotion_sentences[file_two][emotion].append(sentence)

	print(emotion_sentences.keys())

	# Example to access values
	# print(emotion_sentences[file_one]['anger'])

	#
	# For each emotion sentence, increment the counts of the emotions it belongs in
	#

	print("\nTypes of Sentences")
	print("====================")

	for text in emotion_sentences:
		print("\n" + text)
		print("-" * len(text))
		for emotion in emotion_sentences[text]:
			print(str(emotion) + ': ' + str(len(emotion_sentences[text][emotion])))

'''
#=============================================#
#                  Functions                  #
#=============================================#
'''
	
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