 # Standard Library
from machine import Pin, I2C
import time
import _thread

# Local
from i2c_responder import I2CResponder

I2C_FREQUENCY = 100000   
    
RESPONDER_I2C_DEVICE_ID = 0
RESPONDER_ADDRESS = 0x60
GPIO_RESPONDER_SDA = 0
GPIO_RESPONDER_SCL = 1 
    

READBUFFER = [0, 0]

def main():

    i2c_responder = I2CResponder(
        RESPONDER_I2C_DEVICE_ID, sda_gpio=GPIO_RESPONDER_SDA, scl_gpio=GPIO_RESPONDER_SCL, responder_address=RESPONDER_ADDRESS
    )

    print('Testing I2CResponder v' + i2c_responder.VERSION)

    # print('   Responder: Getting I2C WRITE data...')
    # while True:
    #     if i2c_responder.write_data_is_available():
    #         buffer_out = bytearray([0x01, 0x02])
    #         buffer_in = i2c_responder.get_write_data(max_size=len(buffer_out))
    #         break
    #     #time.sleep(0.5)

    # print('   Responder: Received I2C WRITE data: ' + format_hex(buffer_in))
    # print()

    
    buffer_out = bytearray([0x09, 0x08])
    for value in buffer_out:
        while not i2c_responder.read_is_pending():
            pass
        time.sleep(0.1)
        i2c_responder.put_read_data(value)
        print('   Responder: Transmitted I2C READ data: ' + format_hex(value))
    
    
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

