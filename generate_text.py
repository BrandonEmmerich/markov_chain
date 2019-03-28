import json
import nltk
import numpy as np
import random
import sys

def get_corpus():
    with open('data/simmons.json') as f:
        data = json.load(f)

    return data

def corpus_to_words(corpus):
    big_string = '\n'.join([d['blog_text'] for d in corpus])
    raw_words = big_string.replace(".","").replace(",","").replace("(", "").replace(")","").split(" ")
    words = [word.lower() for word in raw_words]
    return words

def get_bigram_cfd(words):
    bigrams = nltk.bigrams(words)
    cfd = nltk.ConditionalFreqDist(bigrams)
    return cfd

def get_trigram_cfd(words):
    trigrams = nltk.trigrams(words)
    condition_pairs = (((w0, w1), w2) for w0, w1, w2 in trigrams)
    trigram_cfd = nltk.ConditionalFreqDist(condition_pairs)

    return trigram_cfd

def get_fourgram_cfd(words):
    fourgrams = nltk.ngrams(words,4)
    condition_pairs = (((w0, w1, w2), w3) for w0, w1, w2, w3 in fourgrams)
    fourgram_cfd = nltk.ConditionalFreqDist(condition_pairs)

    return fourgram_cfd

def second_word(bigram_cfd, word):
    next_words = bigram_cfd[word].keys()
    next_word_frequencies = bigram_cfd[word].values()
    next_word_probabilities = [float(p) / sum(next_word_frequencies) for p in next_word_frequencies]

    next_word = np.random.choice(next_words, p = next_word_probabilities)

    return next_word

def third_word(trigram_cfd, word1, word2):
    next_words = trigram_cfd[word1, word2].keys()
    next_word_frequencies = trigram_cfd[word1, word2].values()
    next_word_probabilities = [float(p) / sum(next_word_frequencies) for p in next_word_frequencies]

    next_word = np.random.choice(next_words, p = next_word_probabilities)

    return next_word

def next_word(fourgram_cfd, word1, word2, word3):
    next_words = fourgram_cfd[word1, word2, word3].keys()
    next_word_frequencies = fourgram_cfd[word1, word2, word3].values()
    next_word_probabilities = [float(p) / sum(next_word_frequencies) for p in next_word_frequencies]

    next_word = np.random.choice(next_words, p = next_word_probabilities)

    return next_word

def generate_sentence(start_word, sentence_length):
    sentence = []
    word1 = start_word
    i = 0
    sentence.append(word1)
    word2 = second_word(bigram_cfd, word1)
    sentence.append(word2)
    word3 = third_word(trigram_cfd, word1, word2)
    sentence.append(word3)

    while i < sentence_length:
        word4 = next_word(fourgram_cfd, word1, word2, word3)
        sentence.append(word4)
        word1 = word2
        word2 = word3
        word3 = word4
        i +=1

    return ' '.join([word for word in sentence])

if __name__ == '__main__':
    data = get_corpus()
    words = corpus_to_words(data['data'])
    bigram_cfd = get_bigram_cfd(words)
    trigram_cfd = get_trigram_cfd(words)
    fourgram_cfd = get_fourgram_cfd(words)

    start_word = str(sys.argv[1])
    sentence_length = int(sys.argv[2])


    i = 0
    while i < 5:
        sentence = generate_sentence(start_word, sentence_length)
        print(sentence)
        i+=1