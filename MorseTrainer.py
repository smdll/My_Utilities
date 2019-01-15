#coding=utf-8

import wx, time

# A dictionary for convert morse sequence to alphabet
morse2Alphabet = {
	'.-': 'A',
	'-...': 'B',
	'-.-.': 'C',
	'-..': 'D',
	'.': 'E',
	'..-.': 'F',
	'--.': 'G',
	'....': 'H',
	'..': 'I',
	'.---': 'J',
	'-.-': 'K',
	'.-..': 'L',
	'--': 'M',
	'-.': 'N',
	'---': 'O',
	'.--.': 'P',
	'--.-': 'Q',
	'.-.': 'R',
	'...': 'S',
	'-': 'T',
	'..-': 'U',
	'...-': 'V',
	'.--': 'W',
	'-..-': 'X',
	'-.--': 'Y',
	'--..': 'Z',
	'.----': '1',
	'..---': '2',
	'...--': '3',
	'....-': '4',
	'.....': '5',
	'-....': '6',
	'--...': '7',
	'---..': '8',
	'----.': '9',
	'-----': '0'
}

class MainFrame(wx.Frame):
	morseSequence = ""
	isNextChar = False
	curTime = 0
	wpm = 15
	timeUnit = 0.08 # Seconds

	def __init__(self, parent):
		super(MainFrame, self).__init__(parent, size = (405, 255), title = "Morse Trainer", style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
		self.InitUI()

	# Build up user interface
	def InitUI(self):
		# Place objects on main frame
		wx.StaticText(self, -1, label = "WPM:", pos = (0, 5))
		self.Wpm = wx.TextCtrl(self, 100, pos = (40, 0), size = (50, 25), value = str(self.wpm))
		wx.Button(self, -1, label = "Clear", pos = (90, 0), size = (70, 25))
		self.Text = wx.TextCtrl(self, -1, pos = (0, 25), size = (400, 200), style = wx.EXPAND|wx.TE_MULTILINE|wx.TE_READONLY)
		self.Show(True)
		self.SetFocus()
		# Bind events
		self.Bind(wx.EVT_TEXT, self.onModWpm)
		self.Bind(wx.EVT_KEY_DOWN, self.onPress)
		self.Bind(wx.EVT_KEY_UP, self.onRelease)
		self.Bind(wx.EVT_BUTTON, self.onClear)

	# Record the time when the space key is pressed
	def onPress(self, event):
		if event.GetKeyCode() == wx.WXK_SPACE:
			if self.curTime < time.time() - self.timeUnit * 5 or len(self.morseSequence) > 5:
				self.morseSequence = ""
				self.isNextChar = True
			else:
				self.isNextChar = False
			self.curTime = time.time()			

	# Determine which element should be added to the sequence when the key is released
	def onRelease(self, event):
		if event.GetKeyCode() == wx.WXK_SPACE:
			elapsedTime = time.time() - self.curTime
			if elapsedTime < self.timeUnit * 2:
				self.morseSequence += "."
			elif elapsedTime > self.timeUnit * 2 and elapsedTime < self.timeUnit * 4:
				self.morseSequence += "-"
			else:
				self.isNextChar = True
			self.displayChar()

	# Change the words per minute
	def onModWpm(self, event):
		if event.GetId() == 100:
			self.wpm = int(self.Wpm.GetValue())
			print self.wpm
			self.timeUnit = 60.0 / self.wpm / 50.0

	def onClear(self, event):
		self.Text.Clear()
		self.morseSequence = ""

	# Dynamically display the character in sequence
	def displayChar(self):
		if not self.isNextChar:
			self.Text.Remove(len(self.Text.GetValue()) - 1, len(self.Text.GetValue()))
		self.Text.AppendText(morse2Alphabet[self.morseSequence])

if __name__ == "__main__":
	root = wx.App()
	MainFrame(None)
	root.MainLoop()