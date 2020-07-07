from gpiozero import Button
from gpiozero import LED


class GPIO:
    callback_function = None
    
    def __init__(self):
        self._button_state: bool = False
        self.__button = Button(5)
        self.__green_led = LED(19)
        self.__red_led = LED(17)

    @property
    def button_state(self):
        return self._button_state

    @button_state.setter
    def button_state(self, value):
        print(self.callback_function)
        self._button_state = value
        self.callback_function(self.button_state)

    def bind_to(self, callback):
        self.callback_function = callback
        
    def green_led_toggle(self):
        self.__green_led.toggle()
        
    def red_led_toggle(self):
        self.__red_led.toggle()

    def run(self):
        while True:
            if self.__button.is_pressed:
                self.button_state = True
                break



