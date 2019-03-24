#!/usr/bin/python
#encoding:utf-8

import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY

class EventHandler(ProcessEvent):
	def process_IN_CREATE(self, event):
		print("Created File: %s.\n" %os.path.join(event.path,event.name))

	def process_IN_DELETE(self, event):
		print("Deleted File: %s.\n" %os.path.join(event.path,event.name))

	def process_IN_MODIFY(self, event):
		print("Modified File: %s.\n" %os.path.join(event.path,event.name))

def FsMonitor(path='.'):
	wm = WatchManager()
	mask = IN_DELETE | IN_CREATE | IN_MODIFY
	notifier = Notifier(wm, EventHandler())
	wm.add_watch(path, mask, auto_add= True, rec=True)
	print("Now Start Monitoring %s.\n"%path)

	while True:
		try:
			notifier.process_events()
			notifier.read_events()
		except KeyboardInterrupt:
			print("Keyboard Interrupt.")
			notifier.stop()
			break

if __name__ == "__main__":
	FsMonitor("/root/mon/")
