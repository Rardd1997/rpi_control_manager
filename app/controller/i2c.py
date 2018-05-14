from smbus import SMBus
import pigpio
import time
from flask import flash, current_app
from app.models import User


class I2cController():
    def __init__(self, port, addr):
        self.port = port
        self.addr = addr
        self.bus = SMBus(port)
        self.pigpio = pigpio.pi()

    def clean(self):
        self.bus.write_byte_data(self.addr, 0x00, 0x00)
        self.bus.write_byte_data(self.addr, 0x01, 0x00)
        pass

    def open_door(self, number):
        number = int(number)
        if not self.is_door_open(number):
            door_number = 2 ** (number - 1)
            current_state = self.bus.read_byte_data(self.addr, 0)
            self.bus.write_byte_data(self.addr, 0x00, door_number | current_state)
            self.write_info_log("The door #{} was opened!".format(str(number)))
        else:
            self.write_info_log("The door #{} was already opened!".format(str(number)))

    def close_door(self, number):
        number = int(number)
        if self.is_door_open(number):
            door_number = 2 ** (number - 1)
            current_state = self.bus.read_byte_data(self.addr, 0)
            self.bus.write_byte_data(self.addr, 0x00, door_number ^ current_state)
            self.write_info_log("The door #{} was closed!".format(str(number)))
        else:
            self.write_info_log("The door #{} was already closed!".format(str(number)))

    def open_door_reader(self, card_num, number, time_to_open = 10):
        number = int(number)
        if self.is_auth(card_num):
            self.open_door(number)
            self.write_info_log("The door #{} will be opened within {} seconds!".format(str(number), str(time_to_open)))
            time.sleep(time_to_open)
            self.close_door(number)
        else:
            self.write_info_log("Card number #{} is invalid!".format(str(card_num)))

    def is_door_open(self, number):
        door_number = 2 ** (number - 1)
        current_state = self.bus.read_byte_data(self.addr, 0)
        return current_state & door_number != 0

    def is_auth(self, card_num):
        user = User.query.filter_by(card_num=card_num).first()
        result = False
        if user is not None:
            result = True
        return result

    def write_info_log(self, msg):
        flash(msg)
        current_app.logger.info(msg)

    def callback(self, bits, value):
        print("bits={} value={}".format(bits, value))

    def read_card(self, gpio1, gpio2, callback=callback):
        time_to_sleep = 300
        d = Decoder(self.pigpio, 14, 15, callback)
        time.sleep(time_to_sleep)
        d.cancel()

    def run(self):
        self.clean()


class Decoder:

   """
   A class to read Wiegand codes of an arbitrary length.

   The code length and value are returned.

   EXAMPLE

   #!/usr/bin/env python

   import time

   import pigpio

   import wiegand

   def callback(bits, code):
      print("bits={} code={}".format(bits, code))

   pi = pigpio.pi()

   w = wiegand.decoder(pi, 14, 15, callback)

   time.sleep(300)

   w.cancel()

   pi.stop()
   """

   def __init__(self, pi, gpio_0, gpio_1, callback, bit_timeout=5):

      """
      Instantiate with the pi, gpio for 0 (green wire), the gpio for 1
      (white wire), the callback function, and the bit timeout in
      milliseconds which indicates the end of a code.

      The callback is passed the code length in bits and the value.
      """

      self.pi = pi
      self.gpio_0 = gpio_0
      self.gpio_1 = gpio_1

      self.callback = callback

      self.bit_timeout = bit_timeout

      self.in_code = False

      self.pi.set_mode(gpio_0, pigpio.INPUT)
      self.pi.set_mode(gpio_1, pigpio.INPUT)

      self.pi.set_pull_up_down(gpio_0, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpio_1, pigpio.PUD_UP)

      self.cb_0 = self.pi.callback(gpio_0, pigpio.FALLING_EDGE, self._cb)
      self.cb_1 = self.pi.callback(gpio_1, pigpio.FALLING_EDGE, self._cb)

   def _cb(self, gpio, level, tick):

      ""<-"
      Accumulate bits until both gpios 0 and 1 timeout.
      ""<-"

      if level < pigpio.TIMEOUT:

         if self.in_code == False:
            self.bits = 1
            self.num = 0

            self.in_code = True
            self.code_timeout = 0
            self.pi.set_watchdog(self.gpio_0, self.bit_timeout)
            self.pi.set_watchdog(self.gpio_1, self.bit_timeout)
         else:
            self.bits += 1
            self.num = self.num << 1

         if gpio == self.gpio_0:
            self.code_timeout = self.code_timeout & 2 # clear gpio 0 timeout
         else:
            self.code_timeout = self.code_timeout & 1 # clear gpio 1 timeout
            self.num = self.num | 1

      else:

         if self.in_code:

            if gpio == self.gpio_0:
               self.code_timeout = self.code_timeout | 1 # timeout gpio 0
            else:
               self.code_timeout = self.code_timeout | 2 # timeout gpio 1

            if self.code_timeout == 3: # both gpios timed out
               self.pi.set_watchdog(self.gpio_0, 0)
               self.pi.set_watchdog(self.gpio_1, 0)
               self.in_code = False
               self.callback(self.bits, self.num)

   def cancel(self):

      """
      Cancel the Wiegand decoder.
      """

      self.cb_0.cancel()
      self.cb_1.cancel()
