import requests
import json

class TextToSpeech:
    def get_audio(self,text):
        url = 'https://texttospeech.googleapis.com/v1/text:synthesize'
        dict_to_send = {
        "input": { "text": text },
        "voice": {
            "languageCode": "en-US",
            "ssmlGender": "FEMALE"
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 0.85
        },}

        # Adding custom headers
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': 'AIzaSyAlv1V9BfOvpUu9uVAbET4LJ9CmILlKirs'
        }
        res = requests.post(url, json=dict_to_send, headers=headers)
        audio = json.loads(res.text)
        return(audio.get('audioContent'))