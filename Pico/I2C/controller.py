
# Standard Library
from machine import Pin, I2C
import time
import _thread

# Local
from i2c_responder import I2CResponder

I2C_FREQUENCY = 100000

CONTROLLER_I2C_DEVICE_ID = 0
GPIO_CONTROLLER_SDA = 0
GPIO_CONTROLLER_SCL = 1

READBUFFER = [0, 0]
RESPONDER_ADDRESS = 0x60
def main():

    # -----------------
    # Initialize Responder and Controller
    # -----------------

    i2c_controller = I2C(
        CONTROLLER_I2C_DEVICE_ID,
        scl=Pin(GPIO_CONTROLLER_SCL),
        sda=Pin(GPIO_CONTROLLER_SDA),
        freq=I2C_FREQUENCY,
    )

    

    # -----------------
    # Demonstrate that the Responder is responding at its assigned I2C address.
    # -----------------
    print('Scanning I2C Bus for Responders...')
    responder_addresses = i2c_controller.scan()
    if len(format_hex(responder_addresses)) < 1:
        print("No devices found")
        exit()
    print('I2C Addresses of Responders found: ' + format_hex(responder_addresses))
    print()

    # -----------------
    # Demonstrate I2C WRITE
    # -----------------
    # buffer_out = bytearray([0x01, 0x02])
    # print('Controller: Issuing I2C WRITE with data: ' + format_hex(buffer_out))
    # i2c_controller.writeto(RESPONDER_ADDRESS, buffer_out)
    # time.sleep(0.25)



    # -----------------
    # Demonstrate I2C READ
    # -----------------
    # NOTE: We want the Controller to initiate an I2C READ, but the Responder implementation
    #   is polled.  As soon as we execute i2c_controller.readfrom() we will block
    #   until the I2C bus supplies the requested data.  But we need to have executional
    #   control so that we can poll i2c_responder.read_is_pending() and then supply the
    #   requested data.  To circumvent the deadlock, we will briefly launch a thread on the
    #   second Pico core, and THAT thread will execute the .readfrom().  That thread will block
    #   while this thread polls, then supplies the requested data.
    # -----------------

    while True:
        for responder in responder_addresses:
            print('Controller: Initiating I2C ON ' + format_hex(responder) + ' READ...')

            try:
                for i in range(2):
                    time.sleep(0.25)
                    data = i2c_controller.readfrom(RESPONDER_ADDRESS, 2)
                    if data:
                        break
                    time.sleep(0.25)
                for i, value in enumerate(data):
                    READBUFFER[i] = value
                print('Controller: Received I2C READ data: ' + format_hex(READBUFFER))
            except:
                continue
        time.sleep(1)
        responder_addresses = i2c_controller.scan()







def format_hex(_object):
    """Format a value or list of values as 2 digit hex."""
    try:
        values_hex = [to_hex(value) for value in _object]
        return '[{}]'.format(', '.join(values_hex))
    except TypeError:
        # The object is a single value
        return to_hex(_object)


def to_hex(value):
    return '0x{:02X}'.format(value)


if __name__ == "__main__":
    main()
    
