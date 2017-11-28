import os, pprint
import nltk
from collections import defaultdict

def file_name_input(prompt):
    path = input(prompt)
    if os.path.isfile(path):
        return path
    else:
        return file_name_input('Enter an existing file path: ')

def folder_name_input(prompt):
    path = input(prompt)
    if os.path.isdir(path):
        return path
    else:
        return folder_name_input('Enter an existing folder path: ')

emotions_dict = {}
emotions_location = 'emotions'#folder_name_input("Where are the emotions files located? ")
directory = os.fsencode(emotions_location)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        emotions_dict[filename] = set(open(emotions_location + '\/' + filename).read().splitlines())
        continue
    else:
        continue

with open('intensifiers.txt') as intensifiers_text:
    content = intensifiers_text.readlines()
intensifiers = set([x.strip() for x in content])

with open('negations.txt') as negations_text:
    content = negations_text.readlines()
negations = set([x.strip() for x in content])

file_one = 'texts/Emma.txt'#file_name_input("Please enter the first text name: ")
file_two = 'texts/Great_Expectations.txt'#file_name_input("Please enter the second text name: ")

print("Analysing " + file_one + " and " + file_two)

#
# Tokenize the sentences in each text into tokenized sentences
#

text_one_sentences = set(nltk.sent_tokenize(open(file_one).read().replace('\n', ' ')))
text_two_sentences = set(nltk.sent_tokenize(open(file_two).read().replace('\n', ' ')))

text_one_tokenized_sentences = []
text_two_tokenized_sentences = []

for sentence in text_one_sentences:
    text_one_tokenized_sentences.append(nltk.word_tokenize(sentence))

for sentence in text_two_sentences:
    text_two_tokenized_sentences.append(nltk.word_tokenize(sentence))

#
# Add each sentence with an emotion word into a new list (emotion_sentences)
# AKA it ignores sentences without an emotion word
#

emotion_sentences = defaultdict(list)

for sentence in text_one_tokenized_sentences:
    for word in sentence:
        for emotion in emotions_dict:
            if word in emotions_dict[emotion]:
                emotion_sentences[emotion].append(sentence)

#
# For each emotion sentence, increment the counts of the emotions it belongs in
#

for emotion in emotion_sentences:
    print(len(emotion_sentences[emotion]))