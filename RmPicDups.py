# This script is used to remove duplicated pictures from a folder and it's sub folders, based on image average hashing
from PIL import Image
import imagehash, sqlite3, os, time

def getListOfFiles(dirName):
	listOfFile = os.listdir(dirName)
	allFiles = list()
	for entry in listOfFile:
		fullPath = os.path.join(dirName, entry)
		if os.path.isdir(fullPath):
			allFiles = allFiles + getListOfFiles(fullPath)
		else:
			allFiles.append(fullPath)
	return allFiles

conn = sqlite3.connect("dump.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS pic(name text, hash text)")

fileList = getListOfFiles("tumblr_new")
print("rebuilt file list")
last = time.time()

for file in fileList:
	if time.time() - last > 5:
		print("Processed ", str(fileList.index(file) / len(fileList) * 100), '%')
		last = time.time()
	try:
		hash = str(imagehash.average_hash(Image.open(file), 16))
	except:
		continue
	cur.execute("SELECT name FROM pic WHERE hash=?", (hash, ))
	resultName = cur.fetchone()
	if not resultName:
		cur.execute("INSERT INTO pic(name,hash) VALUES(?,?)", (file, hash, ))
	else:
		if file == resultName[0]:
			continue
		sizeNew = os.path.getsize(file)
		sizeOld = os.path.getsize(resultName[0])
		if sizeNew > sizeOld:
			cur.execute("UPDATE pic SET name=? WHERE hash=?", (file, hash, ))
			os.remove(resultName[0])
			print("deleted ", resultName[0])
		elif sizeNew <= sizeOld:
			os.remove(file)
			print("deleted ", file)
conn.commit()