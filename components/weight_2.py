# -*- coding: utf-8 -*-
try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError(
        "You probably have to install RPi.GPIO"
    )
import time
import logging

logger = logging.getLogger(__name__)

__author__ = """Marco Roose"""
__email__ = 'marco.roose@gmx.de'
__version__ = '1.1.2'


class GenericHX711Exception(Exception):
    pass


class ParameterValidationError(Exception):
    pass


class HX711(object):
    _channel = "A"
    _channel_a_gain = 64
    _valid_channels = ['A', 'B']
    _valid_gains_for_channel_A = [64, 128]
    min_measures = 2
    max_measures = 100

    def __init__(self, dout_pin, pd_sck_pin, gain=128, channel='A'):
        if (isinstance(dout_pin, int) and
            isinstance(pd_sck_pin, int)): 
            self._pd_sck = pd_sck_pin  
            self._dout = dout_pin  
        else:
            raise TypeError('dout_pin and pd_sck_pin have to be pin numbers.\nI have got dout_pin: ' \
                            + str(dout_pin) + \
                            ' and pd_sck_pin: ' + str(pd_sck_pin) + '\n')

        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self._pd_sck, GPIO.OUT) 
        GPIO.setup(self._dout, GPIO.IN)  
        self.channel = channel
        self.channel_a_gain = gain

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
        self._apply_setting()

    @property
    def channel_a_gain(self):
        return self._channel_a_gain

    @channel_a_gain.setter
    def channel_a_gain(self, channel_a_gain):
        if self.channel == "A":
            self._channel_a_gain = channel_a_gain
            self._apply_setting()

    def power_down(self):
        GPIO.output(self._pd_sck, False)
        GPIO.output(self._pd_sck, True)
        time.sleep(0.01)
        return True

    def power_up(self):
        GPIO.output(self._pd_sck, False)
        time.sleep(0.01)
        return True

    def reset(self):
        self.power_down()
        self.power_up()
        for i in range(6):
            result = self.get_raw_data()
##        if result is False:
##            raise GenericHX711Exception("failed to reset HX711")
##        else:
##            return True


    def _apply_setting(self):
        self._read()
        time.sleep(0.5)
        return True

    def _ready(self):
        _is_ready = GPIO.input(self._dout) == 0
        return _is_ready

    def _set_channel_gain(self, num):
        if not 1 <= num <= 3:
            raise AttributeError(
                """"num" has to be in the range of 1 to 3"""
            )

        for _ in range(num):
            logging.debug("_set_channel_gain called")
            start_counter = time.perf_counter()  # start timer now.
            GPIO.output(self._pd_sck, True)  # set high
            GPIO.output(self._pd_sck, False)  # set low
            end_counter = time.perf_counter()  # stop timer
            time_elapsed = float(end_counter - start_counter)

            if time_elapsed >= 0.00006:
                result = self.get_raw_data()  
                if result is False:
                    raise GenericHX711Exception("channel was not set properly")
        return True

    def _read(self, max_tries=40):
        GPIO.output(self._pd_sck, False)
        ready_counter = 0

        while self._ready() is False:
            ready_counter += 1 

            if ready_counter >= max_tries:
                return False

        data_in = 0
        for i in range(24):
            GPIO.output(self._pd_sck, True)
            GPIO.output(self._pd_sck, False)
            data_in = (data_in << 1) | GPIO.input(self._dout)

        if data_in == 0x7fffff or data_in == 0x800000:
            print('out of bounds')
            return False

        signed_data = 0
        if (data_in & 0x800000): 
            signed_data = -((data_in ^ 0xffffff) + 1)  
        else: 
            signed_data = data_in

        return signed_data

    def get_raw_data(self):
        return self._read()


class Weight:
  def __init__(self, W_DOUT_PIN=25, W_CLK_PIN=8, HEAVY=23000):
    # Пины
    self.W_DOUT_PIN = W_DOUT_PIN
    self.W_CLK_PIN = W_CLK_PIN
    self.hx711 = HX711(
            dout_pin = self.W_DOUT_PIN,
            pd_sck_pin = self.W_CLK_PIN,
            channel='A',
            gain=64)
    self.hx711.reset()

    self.HEAVY = HEAVY
    self.start_weight = 0
    self.delta = 0


  def measure(self):
    m = self.hx711.get_raw_data()
    return m



if __name__ == '__main__':
  try:
    w = Weight()
    data = []
    mx = 25
    while True:
        m = w.measure()
        if m not in [False, -1]:
            data.append(m)
            print(len(data), sum(data)/len(data))
        if len(data) >= mx:
            data.pop(0)

  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
