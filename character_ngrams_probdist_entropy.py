import re
from collections import Counter, defaultdict
import string
import matplotlib.pyplot as plt
from math import log2


def preprocessing(text):
    '''
    Preprocess the corpus.

    :param text: str, raw corpus
    :return tokens: a list that contains all the preprocessed tokens in the corpus
    '''

    # Convert to lowercase
    text = text.lower()

    # Keep only the the [a-z, ä, ö, ü, ß] characters
    text = re.sub(r'[^a-zäöüß ]+','', text)

    # Apply white-space tokenization
    tokens = text.split()

    return tokens

# N-grams Frequency Analysis

def generate_ngram(token, m):
    '''
    Generate a list of all possible n-grams in the token from n = 1 up to n = m.

    :param token: str, a preprocessed token from the corpus
    :param m: int, defines max size of n-gram
    :return ngram_list: a list containing all possible n-grams of the input token from n = 1 up to n = m
    '''

    # Create an empty list to keep all the possible n-grams of a token
    ngram_list = []
    # Iterate over every character in the word
    for index, character in enumerate(token):
        # Append 1-gram to the n-gram list
        ngram_list.append(character)
        # Define n = 2 for the bigrams
        n = 2
        # Append bigrams to the n-gram list and repeat the process with a larger n (for 3-grams, 4-grams etc)
        # until both conditions are met.
        while (index + n) <= len(token) and n <= m:
            ngram_list.append(token[index:index+n])
            n += 1
    return ngram_list


def make_ngram_corpus(text, m):
    '''
    Convert the corpus into a sequence of character n-grams.

    :param text: a list that contains all the preprocessed tokens in the corpus
    :param m: int, defines max size of n-gram
    :return ngram_corpus: a list that contains all possible n-grams of each token (from n = 1 up to n = m) in the corpus.
    '''
    # Create an empty list to store all the possible n-grams of tokens in the corpus
    ngram_corpus = []
    for token in text:
        # Generate all possible n-grams for one token
        ngram = generate_ngram(token, m)
        # Add generated n-grams to the ngram_corpus list
        ngram_corpus += ngram
    return ngram_corpus


def ngram_count(ngram_corpus):
    '''
    Collect n-gram frequency counts.

    :param ngram_corpus: a list that contains all n-grams of the original corpus.
    :return count: a list that contains n-grams and their frequencies in the descending order.
    '''
    count = dict(Counter(ngram_corpus).most_common())
    return count


def generate_top(ngram_counts, k, ngram_size):
    '''
    Generate top k frequent n-grams.

    :param ngram_counts: dict containing n-grams and their frequencies in the descending order.
    :param k: int, the number of top items to compute
    :param ngram_size: int, the size of the n-gram
    :return top_list: list containing top k frequent n-grams.
    '''
    top_list = []
    for ngram in ngram_counts:
        if len(ngram) == ngram_size:
            top_list.append(ngram)
    return top_list[:k]


# N-gram Probability Distributions

def prob_dist(ngram_counts, alphabet, history):
    '''
    Create a dict with the probability distribution over the alphabet S given a history sequence h.

    :param ngram_counts: dict, contains n-grams and their frequencies in the descending order.
    :param alphabet: list, contains all the characters in the alphabet of a given language
    :param history: str, an ngram that is used to predict the next character in the sequence
    :return probability_dist: dic, keys are possible next characters and values are the probability that
    they will occur after a given history
    '''
    # Initialize a counter to count how many times the ngram formed by history + any other character occurs.
    ngram_sum = 0
    probability_dist = defaultdict()
    # Iterate over every alphabet character
    for character in alphabet:
        # Iterate over every ngram and its frequency
        for ngram, count in ngram_counts.items():
            # If the ngram(history+character) occurs, add a new entry to the probability_dist dict where
            # key is a character and value is (history+character) frequency taken from ngram_counts.
            if ngram == (history + character):
                probability_dist[character] = ngram_counts[(history + character)]
                ngram_sum += count
    # To get the probability of each character occuring after the given history,
    # divide its absolute count by the total ngram count.
    for ngram in probability_dist:
        prob = probability_dist[ngram] / ngram_sum
        probability_dist[ngram] = prob

    # probability_dist dict stores the characters that occur after the given history

    # prob_dist dict stores all the characters with non-zero probability if they occur after the given history
    # and zero-probability if they do not occur
    prob_dic = {}
    for character in alphabet:
        if character in probability_dist:
            prob_dic[character] = probability_dist[character]
        else:
            prob_dic[character] = 0
    return prob_dic


def test_prob_dist(prob_distribution):
    '''
    Validates whether probability mass of the distribution for a
    few arbitrary histories sums to 1 with numerical precision of 1 × 10^−7
    '''

    # Get values of probability distribution and sum them
    prob_values = list(prob_distribution.values())
    sum_prob = sum(prob_values)

    assert abs(1 - sum_prob) <= 1E-7
    

def plotting(probability_dist, language, history):

    plt.bar(probability_dist.keys(), probability_dist.values())
    plt.xlabel('Alphabet')
    plt.ylabel('Probability Value')
    plt.title('Probalility distribution over the' + ' ' + language + ' ' + 'alphabet given the history' + ' ' + history)
    plt.show()


def entropy(prob_dist):

    '''
    Calculates the entropy of the probability distribution that measures the uncertainty or the ‘disorder’ within the distribution.

    :param: prob_dict, a dictionary with the probability distribution over the alphabet S given a history sequence h'
    :param: alphabet, a list that contains all the characters in the alphabet of a given language
    return entropy: int, entropy in bits
    '''

    entropy = 0
    for character in prob_dist:
        # Add characters whose P is > 0
        if prob_dist[character] > 0:
            entropy -= (prob_dist[character] * log2(prob_dist[character]))
    return entropy
    


if __name__ == '__main__':

    # Read the file
    with open("corpora/corpus.en", encoding="utf-8") as file:
        en_text = file.read()
    with open("corpora/corpus.de", encoding="utf-8") as file:
        de_text = file.read()

    # Preprocess the file
    en_prep = preprocessing(en_text)
    de_prep = preprocessing(de_text)

    # Convert the preprocessed text into a linear sequence of n-grams.
    en_ngram_corpus = make_ngram_corpus(en_prep, 4)
    de_ngram_corpus = make_ngram_corpus(de_prep, 4)

    # Collect n-gram frequency counts
    en_counts = ngram_count(en_ngram_corpus)
    de_counts = ngram_count(de_ngram_corpus)

    # Generates lists of 15 the most frequent character unigrams, bigrams, 3-grams, and 4-grams for each text corpus.
    en_top_unigrams = generate_top(en_counts, 15, 1)
    print(en_top_unigrams)
    en_top_bigrams = generate_top(en_counts, 15, 2)
    print(en_top_bigrams)
    en_top_trigrams = generate_top(en_counts, 15, 3)
    print(en_top_trigrams)
    en_top_fourgrams = generate_top(en_counts, 15, 4)
    print(en_top_fourgrams)

    de_top_unigrams = generate_top(de_counts, 15, 1)
    print(de_top_unigrams)
    de_top_bigrams = generate_top(de_counts, 15, 2)
    print(de_top_bigrams)
    de_top_trigrams = generate_top(de_counts, 15, 3)
    print(de_top_trigrams)
    de_top_fourgrams = generate_top(de_counts, 15, 4)
    print(de_top_fourgrams)

    # Define the alphabet for English and German
    
    alphabet_en = list(string.ascii_lowercase)
    alphabet_de = list(string.ascii_lowercase) + ['ä', 'ö', 'ü', 'ß']

    # Calculate the probability for every character occurring
    # after the history '', 'n', 'un' and 'gun' for English.
    en_zero_history = prob_dist(en_counts, alphabet_en, '')
    en_n_history = prob_dist(en_counts, alphabet_en, 'n')
    en_un_history = prob_dist(en_counts, alphabet_en, 'un')
    en_gun_history = prob_dist(en_counts, alphabet_en, 'gun')

    # Calculate the probability for every character occurring
    # after the history '', 'n', 'un' and 'gun' for German.
    de_zero_history = prob_dist(de_counts, alphabet_de, '')
    de_n_history = prob_dist(de_counts, alphabet_de, 'n')
    de_un_history = prob_dist(de_counts, alphabet_de, 'un')
    de_gun_history = prob_dist(de_counts, alphabet_de, 'gun')

    # Plot each distribution of the German language as a bar chart
    de_zero_plot = plotting(de_zero_history, 'German', '""')
    de_n_plot = plotting(de_n_history, 'German', '"n"')
    de_un_plot = plotting(de_un_history, 'German', '"un"')
    de_gun_plot = plotting(de_gun_history, 'German', '"gun"')

    # Validate that the probability mass of each distribution sum to 1
    # with a numerical precision of 1 x 10^-7.
    test_prob_dist(de_zero_history)
    test_prob_dist(de_n_history)
    test_prob_dist(de_un_history)
    test_prob_dist(de_gun_history)

    # Calculate the entropy for each distribution of the German language
    de_zero_history_entropy = entropy(de_zero_history)
    de_n_history_entropy = entropy(de_n_history)
    de_un_history_entropy = entropy(de_un_history)
    de_gun_history_entropy = entropy(de_gun_history)
    print(de_zero_history_entropy)
    print(de_n_history_entropy)
    print(de_un_history_entropy)
    print(de_gun_history_entropy)


    # Estimate and plot the bigram distributions P(C|h = ‘a’), P(C|h = ‘d’),
    # P(C|h = ‘z’), and P(C|h = ‘c’). Compute the entropy of each distribution.
    # Calculate the probability for every character occurring
    # after the history '', 'n', 'un' and 'gun' for German.
    de_a_history = prob_dist(de_counts, alphabet_de, 'a')
    de_d_history = prob_dist(de_counts, alphabet_de, 'd')
    de_z_history = prob_dist(de_counts, alphabet_de, 'z')
    de_c_history = prob_dist(de_counts, alphabet_de, 'c')

    # Plot each distribution of the German language as a bar chart
    de_a_plot = plotting(de_a_history, 'German', '"a"')
    de_d_plot = plotting(de_d_history, 'German', '"d"')
    de_z_plot = plotting(de_z_history, 'German', '"z"')
    de_c_plot = plotting(de_c_history, 'German', '"c"')

    # Calculate the entropy
    de_a_history_entropy = entropy(de_a_history)
    de_d_history_entropy = entropy(de_d_history)
    de_z_history_entropy = entropy(de_z_history)
    de_c_history_entropy = entropy(de_c_history)

    print(de_a_history_entropy)
    print(de_d_history_entropy)
    print(de_z_history_entropy)
    print(de_c_history_entropy)