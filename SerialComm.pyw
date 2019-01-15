# -*- coding: utf-8 -*-
# author:smdll

from tkinter import *
import serial
from serial.tools.list_ports import *
import tempfile, zlib, base64

#图标数据
ICONDATA = "eNrtlUtMG1cUhn97xmaCzTCOGYbxAwgQe8z7YQzGpU7G+NGxjR2wcWihTVIrEi1FJBJN3aIqRamaVLCoUKqoUlhUSFSkYkWlLiJRukbqojuWXbAo6qYSElKl0pnxk7Rdt4t8M3Pvufefc+89Z3Q0gEa+mpshtxS+oYB6AIL8yFO4gvy8CokymsIjYzKZQNM0ahkGY6KIEY8HDRyHVDyGtrY25BYW8MWDB7DwPMb8fmw9eYKO9nbcyGTg8/kwm05h+c4dfLW6is3Hj/Hlo0f4YWcHz589w+LtLOZuvInvt7awu7mJ7MwbcDgG0OuZwYi4hP7hm8gkE/j26VM4nT3ocU/D4bqKmbkf8f5nf+Dewz+RvfszXN0xXBb8eP32cySmv8atxZ+Qefs75D4/w8LHv2I0+AFCiVU8/OhDCB0i7q78jgZLC97N/YKu/kncm38Hi/d/Q+qtHbQ6fBgancPaJ/dxc+EA72Vv4dNcDuvr61hZWUE8FsPS0hKy2SzcAwNYXVvD/Pw8Tk9Psb+/j8PDQywvL2NjYwPHx8fY3t7G7Ows0uk0Tk5OsLe3h93dXRwcHODo6Ah93d04OzvDS17yv0OjQlS0lai69u8QhHwXdXq6TISOqEO5oQu6wW/9R/wGIq+zXI1bFN3iuKh2omyIIsuxhoI/O8VTpM7AGCmaZAw6MkIZyYjOUtAJ2d8UTk4xmevhUDLDTCUDwfj1hM7K6omizkupNBNPhcdTcSYdTQSTqWuKf0mvZUITlDSuI0MSNREK0qHQpOxf2p+biEiTFC9FvBJPTUpBWpKCJV32rzdJ0RgTj/Lj0TgTU9aPXlP0Ynz1PBm4QI8FjMHAGB0KhCOvBcKqTqi6mRNJo5E0kjJyZ1QMI18RP2fJU+zzg+L+epbjuHr5eoGK+DkLe9XEV1uVaYu5QTYtsl4+n9XW2tjUaL/UwnFW3t7W1Gyvaqnc39ZxxSkIrvZLFo7v6FRMb1VF/utaO3uFYY/QbWdr6J5eoa9PcNmry/l1D3qEV0Zf9Ti9I/5Bn+Bo9w4LjQ3mwv56s6I3DdmHBe9I9aCvt2toyKHo+sL+5jq6U3A1dRXX7+sfcLrsbMX3t112lM+XN0vnU85vtdkb5aDU+Gyt5+NT88OxhaTIlPNT+r4FVFnJtDoqrq+/aM5TZz5nXCzoGsO/UKwfgq6lShVH5IuQMenz9aW8cKFaXaqiZrXGGp02PyfrpE6r05wraq2+iirrWuKcu/Ljl4ta88Lkf8JfHMDVgw=="

class SerialComm:
	root = Tk()
	deviceList = None
	openedDevice = serial.Serial()
	isCRLF = IntVar(root)
	isSendHex = IntVar(root)
	def __init__(self):
		self.root.protocol("WM_DELETE_WINDOW", self.onExit)

		_, ICON_PATH = tempfile.mkstemp() #设置图标
		ICON = zlib.decompress(base64.b64decode(ICONDATA))
		with open(ICON_PATH, 'wb') as icon_file:
			icon_file.write(ICON)
		self.root.iconbitmap(default = ICON_PATH)

		self.root.resizable(width = False, height = False) #禁止改变窗口尺寸
		self.root.title(u"串口监视器")

		self.contentPane = PanedWindow(self.root) #接受内容窗
		self.contentPane.pack(fill = BOTH, expand = True)
		self.incomingComm = Text(self.contentPane, state = DISABLED)
		self.incomingComm.pack()

		self.configPane = PanedWindow(self.root) #配置窗
		self.configPane.pack(fill = BOTH, expand = True)
		Label(self.configPane, text = u"串口: ").grid(row = 0, column = 0)
		self.scanDevice()
		devices = [item.device for item in self.deviceList]
		self.selectedDevice = StringVar(self.configPane)
		if devices == []:
			devices = [u"(无设备)"]
		self.selectedDevice.set(devices[0])
		self.portSelection = OptionMenu(self.configPane, self.selectedDevice, *devices) #串口设备选择
		self.portSelection.grid(row = 0, column = 1)

		Label(self.configPane, text = u"波特率: ").grid(row = 0, column = 2)
		baudrate = [9600, 19200, 115200]
		self.baudRate = StringVar(self.configPane)
		self.baudRate.set(baudrate[0])
		self.baudRateSelection = OptionMenu(self.configPane, self.baudRate, *baudrate) #波特率选择
		self.baudRateSelection.grid(row = 0, column = 3)
		self.openPort = Button(self.configPane, text = u"打开串口", command = self.onPortState, bg = "red", relief = "raised") #打开串口按钮
		self.openPort.grid(row = 0, column = 4)

		Checkbutton(self.configPane, text = u"自动换行", variable = self.isCRLF, onvalue = 1, offvalue = 0).grid(row = 0, column = 5) #自动换行复选框
		self.isCRLF.set(1)
		Checkbutton(self.configPane, text = u"HEX发送", variable = self.isSendHex, onvalue = 1, offvalue = 0).grid(row = 0, column = 6) #HEX发送复选框
		self.isSendHex.set(0)

		Button(self.configPane, text = u"清除窗口", command = self.onClear).grid(row = 0, column = 7) #清除窗口按钮

		self.sendPane = PanedWindow(self.root) #发送窗
		self.sendPane.pack(fill = BOTH, expand = True)
		Label(self.sendPane, text = u"发送: ").pack(side = LEFT)
		self.commToSend = Entry(self.sendPane) #串口指令窗
		self.commToSend.pack(side = LEFT, expand = True, fill = BOTH)
		Button(self.sendPane, text = u"发送", command = self.onSend).pack(side = LEFT) #发送按钮

		self.consolePane = PanedWindow(self.root) #终端窗
		self.consolePane.pack(fill = BOTH, expand = True)
		Label(self.consolePane, text = u"命令: ").pack(side = LEFT)
		self.commandToExecute = Entry(self.consolePane) #终端指令窗
		self.commandToExecute.pack(side = LEFT, expand = True, fill = BOTH)
		Button(self.consolePane, text = u"执行", command = self.onExecute).pack(side = LEFT) #执行按钮

		while True:
			if not self.openedDevice.is_open:
				self.scanDevice()
			elif self.openedDevice.is_open and self.openedDevice.in_waiting > 0: #循环取数据
				content = self.openedDevice.read(self.openedDevice.in_waiting)
				self.onUpdate(content)
			try:
				self.root.update_idletasks()
				self.root.update()
			except:
				return

	def onClear(self):
		self.incomingComm.config(state = NORMAL)
		self.incomingComm.delete(1.0, END)
		self.incomingComm.config(state = DISABLED)

	def onUpdate(self, content):
		self.incomingComm.config(state = NORMAL)
		self.incomingComm.insert(END, content)
		self.incomingComm.config(state = DISABLED)

	def scanDevice(self):
		self.deviceList = serial.tools.list_ports.comports()

	def onPortState(self):
		if self.openedDevice.is_open:
			self.portSelection.config(state = "normal")
			self.baudRateSelection.config(state = "normal")
			self.openedDevice.close()
			self.openPort.config(bg = "red", relief = "raised")
			return
		self.openedDevice.port = self.selectedDevice.get()
		self.openedDevice.baudrate = self.baudRate.get()
		try:
			self.openedDevice.open()
		except serial.SerialException:
			self.onUpdate("!错误@串口无法打开\n")
			self.openedDevice.close()
			return
		self.openPort.config(bg = "green", relief = "sunken")
		self.portSelection.config(state = "disable")
		self.baudRateSelection.config(state = "disable")

	def onSend(self):
		if not self.openedDevice.is_open:
			self.onUpdate("!错误@串口未打开\n")
			return
		if self.isSendHex.get() == 1:
			hexStream = self.commToSend.get().split(' ')
			for byte in hexStream:
				self.openedDevice.write(chr(int(byte, 16)))
		else:
			self.openedDevice.write(self.commToSend.get())
		if self.isCRLF.get() == 1:
			self.openedDevice.write("\n\t")

	def onExecute(self):
		eval(self.commandToExecute.get())

	def onExit(self):
		self.root.destroy()

if __name__ == "__main__":
	SerialComm()