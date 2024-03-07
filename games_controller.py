from flask import Flask, jsonify, request
from flask_cors import CORS
from services.image_scraper import ImageScraper
from services.rhyme_scraper import RhymeScraper
from services.word_generator import WordGenerator
from services.text_to_speech import TextToSpeech
import queue

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
    },
)
with app.app_context():
    rhymeScraper = RhymeScraper()
    imageScraper = ImageScraper()
    textToSpeech = TextToSpeech()
    wordGenerator = WordGenerator()
    
    import threading

def getUserWordImage(queue,word):
    # Check if the person forgot to provide a word; if they did, tell them it's needed
    if not word:
        return jsonify({'error': 'Word parameter is missing'}), 400

    # Use services to find rhymes and images for the provided word and rhyme words
    word_image_links = None
    while not word_image_links:
        word_image_links = imageScraper.get_image_links(word) 
    # 0. get the word and its image and sound
    word_sound = textToSpeech.get_audio(word)
    
    keyWord = {'text': word, 'image': word_image_links[0]['image_link'], 'sound': word_sound}
    
    queue['keyWord'] = keyWord

def getRhymesForWord(queue,word):
    rhymes = rhymeScraper.fetch_rhymes(word)

    # 1. words that rhyme with the word
    for i in range(len(rhymes)):
        image = None
        while not image:
            image = imageScraper.get_image_links(rhymes[i])
        word_sound = textToSpeech.get_audio(rhymes[i])
        rhymes[i] = {'text': rhymes[i], 'image': image[0]['image_link'], 'rhyme': True, 'sound': word_sound}
    queue['rhymes'] = rhymes

def getNotRhymesForWord(queue):
     # Create an instance of WordGenerator
    word_generator = WordGenerator()
    
    # 2. get words that do not rhyme with the word
    not_rhymes = word_generator.generate_words(3)
    
    for i in range(len(not_rhymes)):
        image = None
        while not image:
            image = imageScraper.get_image_links(not_rhymes[i])
        word_sound = textToSpeech.get_audio(not_rhymes[i])
        not_rhymes[i] = {'text': not_rhymes[i], 'image': image[0]['image_link'], 'rhyme': False, 'sound': word_sound}
    queue["not_rhymes"] = not_rhymes

@app.route('/get_rhymes_game_data', methods=['GET'])
def get_rhymes_and_images():
    result = {}
     # Get a word from the person who is asking for rhymes and images
    word = request.args.get('word')
    thread1 = threading.Thread(target = getUserWordImage, args = (result,word))
    thread2 = threading.Thread(target = getRhymesForWord, args = (result,word))
    thread3 = threading.Thread(target = getNotRhymesForWord, args = (result,))
    
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    
    print(result)
    try:
        response =  jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except: 
        return jsonify({'error': 'Failed to retrieve rhymes or images'}), 500
        

@app.route('/get_memory_game_data', methods=['GET'])
def get_memory_game():
    # Get a word from the person who is asking for a memory game
    word = request.args.get('word')

    # Check if the person forgot to provide a word; if they did, tell them it's needed
    if not word:
        return jsonify({'error': 'Word parameter is missing'}), 400

    # Use the ImageService to get a list of images for the memory game
    wrodImage = imageScraper.get_image_links(word)
    # 
    
    
    # sha8al
    # nemberOfWords = 3
    # otherWords = []
    # i = 0
    # while len(otherWords) < nemberOfWords:
    #     word = wordGenerator.generate_words(1)
    #     image = imageScraper.get_image_links(word)
    #     if image:
    #         otherWords.append({'query': word, 'image_link': image[0]['image_link']})
    #         i += 1
    #     else: 
    #         print('No image found for word: ', word)
            
    otherWords = wordGenerator.generate_words(3)
    # get the images for the other words
    for i in range(len(otherWords)):
        image = None
        while not image:
            image = imageScraper.get_image_links(otherWords[i])
            if image:
                otherWords[i] = {'query': otherWords[i], 'image_link': image[0]['image_link']}
                break
            else:
                print('No image found for word: ', otherWords[i])
    
    response = jsonify({'keyword': wrodImage, 'other_words': otherWords})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route('/get_image_word', methods=['GET'])
def get_image_word():
    word = request.args.get('word')
    iamge = imageScraper.get_image_links(word)
    return jsonify({'image': iamge[0]['image_link']})

@app.route('/get_audio_word', methods=['GET'])
def get_audio_word():
    word = request.args.get('word')
    sound = textToSpeech.get_audio(word)
    return jsonify({'sound': sound})

@app.route('/test', methods=['GET'])
def test():
    word = request.args.get('word')
    rhymes = rhymeScraper.fetch_rhymes(word)
    return jsonify({'rhymes': rhymes})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True,port=5001)

#http://127.0.0.1:5000/get_rhymes_game_data?word=cat
#http://127.0.0.1:5000/get_memory_game_data?word=cat
