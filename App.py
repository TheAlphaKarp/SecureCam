import time
from multiprocessing import Process
from pydub import AudioSegment
from pydub.playback import play

from Camera import Camera
from GPIO import GPIO
from Detected import Detected


class App:
    def __init__(self):
        self.button_state: bool = False

        self.gpio: GPIO = GPIO()
        self.gpio.bind_to(self.update_button_state)
        self.camera: Camera = Camera(video_device=0)

        Process(target=self.gpio.run).start()
        
    def update_button_state(self, button_state):
        self.button_state = button_state

        self.validate()

    def validate(self):
        if self.button_state:
            capture_result = self.camera.detect()

            if capture_result == Detected.VALID:
                self.gpio.green_led_toggle()
                
                song = AudioSegment.from_mp3('./audio/granted.mp3')
                play(song)
                
                self.gpio.green_led_toggle()

            elif capture_result == Detected.INVALID:
                self.gpio.red_led_toggle()
                
                song = AudioSegment.from_mp3('./audio/alarm.mp3')
                play(song)
                
                self.gpio.red_led_toggle()
            else:
                self.gpio.red_led_toggle()
                self.gpio.green_led_toggle()

                song = AudioSegment.from_mp3('./audio/unknown.mp3')
                play(song)

                self.gpio.red_led_toggle()
                self.gpio.green_led_toggle()

