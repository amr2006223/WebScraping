import random

class WordGenerator:
    def load_words():
        with open("words.txt", 'r') as file:
            words = file.read().splitlines()
        return words

    def generate_words(self,num):
        words = WordGenerator.load_words()
        return random.sample(words, num)
