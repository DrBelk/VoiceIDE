import speech_recognition as sr
from google.cloud import speech_v1p1beta1 as speech

class Listener:    
    def __init__(self, *args, **kwargs):
        self.r = sr.Recognizer()
        print("listener: noise evaluating...")
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)


    def listen(self):
        phrase = ''
        with sr.Microphone() as source:
            print("listener is active, please say something")
            audio = self.r.listen(source)
        client = speech.SpeechClient()
        audio = speech.types.RecognitionAudio(content=audio.get_wav_data())

        config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            audio_channel_count=1,
            language_code = 'ru-RU',
            alternative_language_codes=['en'])

        print('Waiting for operation to complete...')
        response = client.recognize(config, audio)
        print(u'Transcript: {}'.format(response.results[0].alternatives[0].transcript))
        return response.results[0].alternatives[0].transcript