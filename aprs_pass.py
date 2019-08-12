def aprspass(callsign):
	stophere = callsign.find('-')
	if stophere != -1:
		callsign = callsign[:stophere].upper()
	hash = 0x73e2
	i = 0
	length = len(callsign)
	while i < length - 1:
		hash ^= ord(callsign[i]) << 8
		hash ^= ord(callsign[i + 1])
		i += 2
	return hash & 0x7fff

if __name__ == "__main__":
	callsign = "BG7XXV"
	print("Passcode for %s:"%callsign, aprspass(callsign))