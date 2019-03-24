#-*- coding: UTF-8 -*-  

import imageio, os, urllib2, re, zipfile, sys

def get_file(id):
	# Fetching the description page
	print('Collecting %s'%id)
	try:
		html = urllib2.urlopen('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s'%id).read()
	except:
		print('Site unreachable or this post has been removed')
		return 0
	url, fps = get_param(html)

	# Get the zip file by fooling the site with fake referer
	request = urllib2.Request(url)
	request.add_header('Accept-Encoding','gzip, deflate')
	request.add_header('Referer','https://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s'%id)
	content = urllib2.urlopen(request).read()
	file = open('.\\%s.zip'%id, 'wb')
	file.write(content)
	file.close()
	print('Done collecting')
	return fps

def get_param(content):
	# Get the exact zip file's address
	url = re.findall(r'(?<=pixiv.context.ugokuIllustData  = {"src":").*?(?=","mime)', content)[0].replace('\\/', '/')
	
	# Get the latency between pictures
	fps = int(re.findall(r'(?<="delay":).*?(?=},{"file)', content)[0])
	return url, fps

def create_gif(id, fps):
	# Unzipping files to current path
	zipFile = zipfile.ZipFile('.\\%s.zip'%id)
	for file in zipFile.namelist():
		zipFile.extract(file, '.\\%s\\'%id)
	zipFile.close()

	# Merging files into a gif file
	print('Making gif %s.gif'%id)
	frames = []
	image_list = os.listdir('.\\%s\\'%id)
	for image_name in image_list:
		frames.append(imageio.imread('.\\%s\\%s'%(id, image_name)))
	imageio.mimsave('.\\%s.gif'%id, frames, 'GIF', duration = fps / 1000)
	
	# Remove temporary files
	os.system('rmdir /Q /S .\\%s'%id)
	os.system('del %s.zip'%id)
	print('Done making gif')

def check_file(id):
	# Check if this id has already been downloaded
	try:
		open('%s.gif'%id).close()
	except:
		return False
	return True

def main():
	id = raw_input('Input id:')
	if check_file(id):
		print('File exists, exiting.')
		return
	fps = get_file(id)
	if fps == 0:
		return
	create_gif(id, fps)

if __name__ == "__main__":
	main()