#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os
import nltk
#from nltk.tokenize import word_tokenize
import string #punctuation
from TurkishStemmer import TurkishStemmer
import time
import operator #for sorting dict

def read_file(filename):
	f = open(filename, "r") 
	file_text = f.read()
	f.close()
	return file_text

def write_file(filename, output):
	full_filename = './' + filename + '.txt'
	file = open(full_filename, 'a')
	file.write(str(output))
	file.close()

def add_to_freq_dict(dictionary, word):
	if word not in dictionary:
		freq = 1
		dictionary[word] = freq
	else:
		dictionary[word] += 1

stemmer = TurkishStemmer()
stopwords = read_file("stopwords_new.txt").split("\n")
#exclude = [".", ",", ":", ";", "?", "!", "\"", "#", "$", "%", "&", "\'", "\(", "\)", "\*", "+", "-", "\\", "/", "<", ">", "=", "@", "[", "]", "\^", "_", "`", "{", "}", "|", "~"]

def delete_characters(text, char_list):
	for char in char_list:
		text = re.sub(char, '', text)
	return text

def delete_characters_space(text, char_list):
	for char in char_list:
		text = re.sub(char, ' ', text)
	return text

def remove_words(word_list, delete_list):
	return [word for word in word_list if word not in delete_list]

def remove_with_regex(word_list):
	new_word_list = []
	for word in word_list:
		check = re.findall(r'(?:pic.twitter|^@|\d+|^rt$)', word)
		if not check:
			new_word_list.append(word)
	return new_word_list

def replace_emoticon(word):
	check_pos = re.findall(r'(?::\)|:-\)|=\)|:D|:d|<3|\(:|:\'\)|\^\^|;\))', word)
	check_neg = re.findall(r'(:-\(|:\(|;\(|;-\(|=\(|:/|:\\|-_-)', word)
	if check_pos:
		word = ":)"
	elif check_neg:
		word = ":("
	return word

def remove_punct(word):
    exclude = set(string.punctuation)
    word = replace_emoticon(word)
    if word != ":)" and word != ":(":
    	word = ''.join(ch for ch in word if ch not in exclude)
    return word

def replace_turkish_char(word):
	#corr = {'ş':'s', 'ç':'c', 'ğ':'g', 'ü':'u', 'ö':'o', 'ı':'i'}
	word = word.replace('ş','s')
	word = word.replace('ç','c')
	word = word.replace('ğ','g')
	word = word.replace('ü','u')
	word = word.replace('ö','o')
	word = word.replace('ı','i')
	return word

def remove_repeating_char(word):
    new_word = ""
    prev_char = ''
    for char in word:
    	if prev_char == char:
    		continue
    	new_word = new_word + char
    	prev_char = char
    return new_word

def process_tweet(tweet):
	word_list = tweet.split()
	sentence = ""
	for word in word_list:
		if word in stopwords:
			continue
		check = re.findall(r'(?:pic.twitter|^@|\d+)', word)
		if check:
			continue
		word = remove_repeating_char(remove_punct_neg(remove_punct_pos(word)))
		if len(word) <= 1:
			continue
		st_word = stemmer.stem(word)
		sentence = sentence + " " + st_word
	return sentence

def create_train(text_raw, tag):
	text_lines = text_raw.split("\n")

	for line in text_lines:
		line = line.lower()
		tweet = line.split("\t")[3]
		delete_list = [","]
		
		tweet = delete_characters_space(tweet, delete_list)
		
		#word_list = remove_words(tweet.split(), stopwords)
		word_list = tweet.split()
		
		word_list = remove_with_regex(word_list)

		word_list = [ stemmer.stem(replace_turkish_char(remove_punct(remove_repeating_char(word))))for word in word_list ]

		word_list = [word for word in word_list if len(word) > 1]

		word_list = remove_words(word_list, stopwords)
		
		sentence = ""
		for word in word_list:
			#st_word = stemmer.stem(word)
			sentence = sentence + " " + word
			add_to_freq_dict(dictionary, word)

		#sentence = process_tweet(tweet)

		tup = (sentence, tag)
		train.append(tup)


start = time.time()

direct = "./Train/"

print("Reading files...")
positive_raw = read_file(os.path.join(direct, "positive-train"))
negative_raw = read_file(os.path.join(direct, "negative-train"))
notr_raw = read_file(os.path.join(direct, "notr-train"))

print("Preprocessing...")
train = []
dictionary = {}
create_train(positive_raw, "1")
create_train(negative_raw, "-1")
create_train(notr_raw, "0")


#sorted_d = sorted(dictionary.items(), key=operator.itemgetter(1),reverse=True)
#write_file("dictionary", sorted_d)

print("This thing...")


#training_set = nltk.classify.apply_features(extract_features, train)
#classifier = nltk.NaiveBayesClassifier.train(training_set)

#all_words = set(word for passage in train for word in word_tokenize(passage[0]))

test_sentence = ["SKANDAL !! Boğaziçi ?nde PKK sloganları ve PKK'nın ne işi var? pic.twitter.com/aNE1FKR5BB", "Boğaziçi üni kapatılsın. Bence gereksiz Pkk yuvası", "Hayaller tamda istanbul bogaziçi universitesi", "Boğaziçi Üniversitesi - Tarih Bölümü kalpben <3", "Bugün Bogaziçi Üniversitesi Mithat Alam Film Merkezi'nde Hayko Cepkin'le söylesecegiz: pic.twitter.com/emNtHqGMQD 18.00 itibariyle baslariz.", "Boğaziçi Üniversitesi yds 2014 - Bildirimiz sunuluyor pic.twitter.com/W1i4wQrW3K"]

for test in test_sentence:
	print(test)
	test = test.lower()
	delete_list = [","]
	tweet = delete_characters_space(test, delete_list)
	word_list = tweet.split()
	word_list = remove_with_regex(word_list)
	word_list = [ stemmer.stem(replace_turkish_char(remove_punct(remove_repeating_char(word))))for word in word_list ]
	word_list = [word for word in word_list if len(word) > 1]
	word_list = remove_words(word_list, stopwords)
		
	sentence = ""
	for word in word_list:
		sentence = sentence + " " + word
	print(sentence)
	#print(classifier.classify(extract_features(test.split())))
	print("\n")

end = time.time()
print(end - start)




