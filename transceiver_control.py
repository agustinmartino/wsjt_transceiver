import datetime
import time
import serial
import struct
import os
import yaml
from consolemenu import *
from consolemenu.items import *

#Import weakmon to use encoders
import sys
sys.path.append(os.path.expandvars('$WEAKMON'))
from ft8 import FT8Send

#Read configuration file
configs_file = open('transceiver_config.yml', 'r')
configs = yaml.load(configs_file)

#Serial port for arduino
serial_port = configs['serial_port']
baudrate    = configs['baudrate']
try:
    puerto = serial.Serial(serial_port, baudrate, timeout=0.5)
except serial.serialutil.SerialException, e:
    print "\nNo se puede abrir puerto: " + serial_port + "\n"
    exit(1)

#Global variables
callsign = configs['callsign']
grid = configs['grid']
current_msg = ''
rx_callsign = ''

#FT8 encoder
encoder = FT8Send()

def encode_ft8(msg):
    try:
        a77 = encoder.pack(msg, 1)
        symbols = encoder.make_symbols(a77)
    except:
        print "FT8 encoder error, check message!"
        symbols = None
        time.sleep(3)
    return symbols

def load_symbols(symbols):
    print "Load symbols into transmitter.."
    puerto.write('m')
    for symbol in symbols:
        puerto.write(struct.pack('>B', symbol))
    puerto.write('\0')
    time.sleep(1)

def change_freq():
    no_freq = True
    while(no_freq):
        new_freq = int(raw_input("Enter new offset frequency (0 - 2000Hz): "))
        if (new_freq > 0 and new_freq < 2000):
            no_freq = False
    puerto.write('o')
    for kk in range(2):
        puerto.write(struct.pack('>B', (new_freq >> 8*kk) & 0xFF))
    time.sleep(1)    

def new_msg(msg):
    global current_msg
    print msg
    if msg != current_msg:
        symbols = encode_ft8(msg)
        if symbols.any():
            load_symbols(symbols)
            current_msg = msg
        else:
            return
    transmit()       

def transmit():
    if not current_msg:
        print "No previous message!"
        time.sleep(1)
    else:
        print "Waiting for slot.."
        while True:
            utc_time = datetime.datetime.utcnow()
            if (utc_time.second % 15 == 14):
                print "TX!"
                puerto.write('t')        
                time.sleep(1)
                break

def call_cq():
    msg = 'CQ ' + callsign + ' ' + grid
    new_msg(msg)
def resp_new():
    global rx_callsign
    rx_callsign = raw_input("Respond to callsign: ")
    resp_submenu.show()
def resp_last():
    if not rx_callsign:
        print "No previous callsign!"
        time.sleep(1)
    else:
        resp_submenu.show()
def respond(response):
    if 'grid' in response:
        msg = rx_callsign + ' ' + callsign + ' ' + grid
    elif 'signal' in response:
        snr = raw_input("Signal strength: ")        
        msg = rx_callsign + ' ' + callsign + ' ' + snr
    elif 'RR73' in response:
        msg = rx_callsign + ' ' + callsign + ' RR73'
    new_msg(msg)
  

#Create the menus
menu = ConsoleMenu("WJSTX Transceiver Control ", "FT8 Mode")
resp_submenu = ConsoleMenu("Respond with: ", "", exit_option_text = "Go back")

#Main menu
cq_item         = FunctionItem("Call CQ", call_cq, [])
retransmit_item = FunctionItem("Retransmit last", transmit, [])
resp_new_item   = FunctionItem("Respond to new callsign", resp_new, [])
submenu_item    = FunctionItem("Respond to last callsign", resp_last, [])
chfreq_item     = FunctionItem("Change TX frequency", change_freq, [])

#Resp submenu
resp_grid_item   = FunctionItem("Respond with grid", respond, ['grid'])
resp_signal_item = FunctionItem("Respond with R + signal strenght", respond, ['signal'])
resp_73_item     = FunctionItem("Respond with RR73", respond, ['RR73'])

resp_submenu.append_item(resp_grid_item)
resp_submenu.append_item(resp_signal_item)
resp_submenu.append_item(resp_73_item)

menu.append_item(cq_item)
menu.append_item(resp_new_item)
menu.append_item(submenu_item)
menu.append_item(retransmit_item)
menu.append_item(chfreq_item)
menu.show()

