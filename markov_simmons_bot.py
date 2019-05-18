import json
import nltk
import numpy as np
import private
import random
import string
import sys
import tweepy

def open_twitter_api():
    auth = tweepy.OAuthHandler(private.CONSUMER_KEY, private.CONSUMER_SECRET)
    auth.set_access_token(private.ACCESS_KEY, private.ACCESS_SECRET)
    api = tweepy.API(auth)

    return api

def get_corpus():
    with open('data/simmons.json') as f:
        data = json.load(f)

    return data

def corpus_to_words(corpus):
    remove_punctuation = dict((ord(punct), None) for punct in string.punctuation)
    text = '\n'.join([d['blog_text'] for d in corpus])
    cleaned_text = text.lower().translate(remove_punctuation)
    words = nltk.word_tokenize(cleaned_text)

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

def clean_up_sentence(sentence):
    '''
    Capitalize the first letter of the sentence, end the sentence with a period,
    restrict the sentence length to 280 characters.
    '''
    return sentence.replace("\n","").capitalize()[0:279] + '.'

def generate_sentence(seed_word, sentence_length):
    sentence = []
    word1 = seed_word
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

def get_seed_word(data):
    '''
    Select a random text from the corpus, identify all proper nouns in that text,
    return a random proper noun from that list.
    '''
    stop_words = nltk.corpus.stopwords.words('english')

    random_post_index = int(len(data['data']) * random.random())
    random_post = data['data'][random_post_index]['blog_text']

    remove_punctuation = dict((ord(punct), None) for punct in string.punctuation)
    cleaned_text = random_post.translate(remove_punctuation)
    word_tokens = nltk.word_tokenize(cleaned_text)

    no_stopwords = [word for word in word_tokens if not word in stop_words]
    words_with_part_of_speech = nltk.tag.pos_tag(no_stopwords)
    proper_nouns = [word for word, pos in words_with_part_of_speech if pos == 'NNP']
    seed_word = random.choice(proper_nouns).lower()

    return seed_word

if __name__ == '__main__':
    api = open_twitter_api()

    data = get_corpus()
    words = corpus_to_words(data['data'])
    bigram_cfd = get_bigram_cfd(words)
    trigram_cfd = get_trigram_cfd(words)
    fourgram_cfd = get_fourgram_cfd(words)

    seed_word = get_seed_word(data)
    sentence_length = 45

    sentence = generate_sentence(seed_word, sentence_length)

    api.update_status(sentence)
