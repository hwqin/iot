from MCP3008 import MCP3008
import time


#initialize MCP3008 module
adc = MCP3008()

for i in range(10000):
    # read sensor value from channel 0
    value = adc.read( channel = 0 ) # You can of course adapt the channel to be read out

    # print the value out
    print("value read out is ", value)
    #print("Applied voltage: %.2f" % (value / 1023.0 * 3.3) )
    
    time.sleep(0.1)