from tkinter import *
import random, time, math

def onCalEntropy(c):
	result = -1;
	if(len(c)>0):
		result = 0;
	for x in c:
		result += ord(x)*math.log(ord(x), 2)
	return result

def onGenerate():
	pool = ""
	if isUpperCase.get():
		pool += printable["upper"]
	if isLowerCase.get():
		pool += printable["lower"]
	if isDigit.get():
		pool += printable["digit"]
	if isSymbol.get():
		pool += printable["symbol"]
	random.seed(time.time())
	randStr = "".join(random.choices(pool, k = pwLength.get()))
	pwEntry.insert (0, randStr)
	pwEntropy.set(str(onCalEntropy(randStr)))

def onCopy():
	root.clipboard_clear()
	root.clipboard_append(pwEntry.get())
	root.update()

def onCheckRules():
	if not (isUpperCase.get() or isLowerCase.get() or isDigit.get() or isSymbol.get()):
		isLowerCase.set(1)

printable = {"lower":"abcdefghijklmnopqrstuvwxyz", "upper":"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "digit":"0123456789", "symbol":"~!@#$%^&*()_+{}|:\"<>?`-=[]\\;',./"}

root = Tk()
root.resizable(width = False, height = False)
root.title(u"gmssl-python")
isUpperCase = IntVar(root)
isLowerCase = IntVar(root)
isDigit = IntVar(root)
isSymbol = IntVar(root)
pwLength = IntVar(root)
pwEntropy = StringVar(root)

isUpperCase.set(1)
isLowerCase.set(1)
isDigit.set(1)

pane1 = PanedWindow(root)
pane1.pack(expand = True, fill = BOTH)
Label(pane1, text = u"密码: ", ).pack(side = LEFT)
pwEntry = Entry(pane1)
pwEntry.pack(side = LEFT, expand = True, fill = BOTH)

pane2 = PanedWindow(root)
pane2.pack(expand = True, fill = BOTH)
Checkbutton(pane2, text = u"A-Z", variable = isUpperCase, onvalue = 1, offvalue = 0, command = onCheckRules).pack(side = LEFT)
Checkbutton(pane2, text = u"a-z", variable = isLowerCase, onvalue = 1, offvalue = 0, command = onCheckRules).pack(side = LEFT)
Checkbutton(pane2, text = u"0-9", variable = isDigit, onvalue = 1, offvalue = 0, command = onCheckRules).pack(side = LEFT)
Checkbutton(pane2, text = u"/*_...", variable = isSymbol, onvalue = 1, offvalue = 0, command = onCheckRules).pack(side = LEFT)
Label(pane2, text = u"熵：").pack(side = LEFT)
pwEntropyLb = Label(pane2, textvariable = pwEntropy)
pwEntropyLb.pack(side = LEFT)

pane3 = PanedWindow(root)
pane3.pack(expand = True, fill = BOTH)
Label(pane3, text = u"长度").pack(side = LEFT)
pwLengthScale = Scale(pane3, from_ = 3, to = 128, variable = pwLength, orient = HORIZONTAL)
pwLengthScale.pack(side = LEFT, expand = True, fill = BOTH)
Button(pane3, text = u"生成", command = onGenerate).pack(side = LEFT)
Button(pane3, text = u"复制", command = onCopy).pack(side = LEFT)

root.mainloop()