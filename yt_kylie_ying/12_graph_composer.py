import random
import re
import string
import os

from graph_composer.graph import Graph


def get_words_from_text(text_path):
    with open(text_path, 'r') as f:
        text = f.read()

        # for the songs implementation:
        # remove [text]
        text = re.sub(r'\[(.+)\]', ' ', text)

        # turn any whitespace (newlines, etc.) into just spaces
        text = ' '.join(text.split())
        text = text.lower()
        # remove all punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split()  # split on space again
    return words


def make_graph(words):
    g = Graph()

    previous_word = None

    # check that each word is in the graph. if not, add it
    # if previous word (most times), add an edge if doesn't exist already, or increment the weight:
    for word in words:
        word_vertex = g.get_vertex(word)

        if previous_word:
            previous_word.increment_edge(word_vertex)

        # set to previous word and iterate
        previous_word = word_vertex

    # generate the probability mappings
    g.generate_probability_mappings()

    return g


def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))  # pick a random word to start
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)  # keep getting words

    return composition


def main(artist):
    # 1. get the words from the text
    # words = get_words_from_text('graph_composer/texts/hp_sorcerer_stone.txt')

    # for the songs implementation:
    words = []
    # 1. get the words from the files
    for song_file in os.listdir(f'graph_composer/songs/{artist}'):
        if song_file == '.DS_Store':
            continue
        song_words = get_words_from_text(
            f'graph_composer/songs/{artist}/{song_file}')
        words.extend(song_words)

    # 2. create a graph with those words
    g = make_graph(words)

    # 3. get the next word for x (input) number of words
    composition = compose(g, words, 100)
    # returns a string where all the wrods are separated by a space

    # 4. show the user
    return ' '.join(composition)


if __name__ == '__main__':
    print(main('taylor_swift'))
