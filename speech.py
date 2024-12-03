import math
import json
from vosk import Model, KaldiRecognizer
import pyaudio

class FastSpeechRecognition:
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=16000,
                                  input=True,
                                  frames_per_buffer=4000)
        self.stream.start_stream()

    def get_last_command(self):
        if self.recognizer.AcceptWaveform(self.stream.read(4000, exception_on_overflow=False)):
            result = self.recognizer.Result()
            print(f"result: {result}")  
            try:
                result_dict = json.loads(result)
                command = result_dict.get("text", "")
                
                return command
            except json.JSONDecodeError as e:
                print(f"Error {e}")
        else:
            print("No audio detected")
        return None

    def stop_listening(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
        
