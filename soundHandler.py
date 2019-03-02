import speech_recognition as sr
r = sr.Recognizer()

class Listener:	
	def listen(self):
		word_eng = word_ru = ''
		with sr.Microphone() as source:
				print("listener: noise evaluating...")
				r.adjust_for_ambient_noise(source)
				print("listener is active, please say something")
				audio = r.listen(source)
		try:
			word_eng = r.recognize_google(audio, language="en-US")
			word_ru = r.recognize_google(audio, language="ru-RU")
			print(word_eng, word_ru)
			
		except sr.UnknownValueError:
			print("Робот не расслышал фразу")
		except sr.RequestError as e:
			print("Ошибка сервиса; {0}".format(e))
		return (word_eng, word_ru)