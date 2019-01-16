from tkinter import *
from tkinter import filedialog

def onSave(content):
	File = filedialog.asksaveasfilename(initialdir = ".", title = u"选择文件", filetypes = [("文本", ("*.txt"))])
	if File == '':
		return
	with open(File, "at") as f:
		f.write(content)

root = Tk()
content = Text(root)
content.pack(expand = True, fill = BOTH)
Button(root, text = u"保存内容", command = lambda: onSave(content.get())).pack()
new = last = ""
while True:
	new = root.clipboard_get()
	if not last == new:
		content.insert(END, last)
		content.insert(END, "\n")
		last = new
	try:
		root.update_idletasks()
		root.update()
	except:
		exit()
