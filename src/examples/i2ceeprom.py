#!/usr/bin/env python

from mpsse import *

SIZE = 0x8000		# Size of EEPROM chip (32 KB)
WCMD = "\xA0\x00\x00"	# Write start address command
RCMD = "\xA1"		# Read command
FOUT = "eeprom.bin"	# Output file

try:
	eeprom = MPSSE(I2C, FOUR_HUNDRED_KHZ)

	print "%s initialized at %dHz (I2C)" % (eeprom.GetDescription(), eeprom.GetClock())

	eeprom.Start()
	eeprom.Write(WCMD)

	if eeprom.GetAck() == ACK:

		eeprom.Start()
		eeprom.Write(RCMD)
	
		if eeprom.GetAck() == ACK:
			data = eeprom.Read(SIZE)
			eeprom.SendNacks()
			eeprom.Read(1)

	eeprom.Stop()
	
	open(FOUT, "wb").write(data)	
	print "Dumped %d bytes to %s" % (len(data), FOUT)
	
	eeprom.Close()
except Exception, e:
	print "MPSSE failure:", e
	
