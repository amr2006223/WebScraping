from flask import Flask, jsonify
import random

app = Flask(__name__)

class WordGenerator:
    @staticmethod
    def load_words():
        with open("WebScraping/words.txt", 'r') as file:
            words = file.read().splitlines()
        return words

    @staticmethod
    def generate_words(num):
        words = WordGenerator.load_words()
        return random.sample(words, num)

@app.route('/generate_words/<int:num>', methods=['GET'])
def generate_words(num):
    words = WordGenerator.generate_words(num)
    return jsonify({"words": words})

if __name__ == '__main__':
    app.run(debug=True)
