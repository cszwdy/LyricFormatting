# -*- coding: utf-8 -*-  
import os
import re
import shutil
import chardet
import codecs

#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

rootPath = os.getcwd()
dirs = ['origin', 'qualified', 'formatted']
pattern = "(\[(a[rl]):.*]|\[ti:.*]|\[by:.*]|\[offset:-?\d*]|\[\d{2}:\d{2}(.\d{2})?]).*"

originPath = os.path.join(rootPath, dirs[0])
qualifiedPath = os.path.join(rootPath, dirs[1])
formattedPath = os.path.join(rootPath, dirs[2])

def checkTheNecessaryDirsAt(rootPath, dirNames):
	for dirName in dirNames:
		path = os.path.join(rootPath, dirName)
		if os.path.exists(path) == False:
			print(dirName, "is't exist")
			
def makeTheNecessaryDirsIfNeedAt(rootPath, dirNames):
	for dirName in dirNames:
			path = os.path.join(rootPath, dirName)
			if os.path.exists(path) == False:
				os.mkdir(path)
				print(dirName,"maked")
				
def getAllLyricFileAt(path):
	return [os.path.join(path, fileName) for fileName in os.listdir(path) if os.path.splitext(fileName)[1] == '.lrc']
	

def checkFileEncodeAt(path):
	with open(path, 'rb') as f:
		data = f.read()
		encoding = chardet.detect(data)['encoding']
	f.close()
	name = str(os.path.basename(path))
	return (encoding, name)
	
	
def checkLyricQualifiedAt(path, pattern, outputRootPath, qualifiedRootPath):
	fileName = path.split('/')[-1]
	try:
		with open(path, 'rb') as f:
			#https://github.com/llSourcell/tensorflow_chatbot/issues/17
			lines = [line for line in f.readlines()]
			if len(lines) <= 0:
				print("Empty Warning:%s" % fileName)
				f.close()
				return
				
			outputPath = os.path.join(outputRootPath, fileName)
			with open(outputPath, 'w') as o:
				for line in lines:
					if re.match(pattern, line) != None:
						o.write(line)
#						print('write %s' % line)
					else:
						print('not match %s' % line)
			o.close()
		f.close()
		shutil.move(path, os.path.join(qualifiedRootPath, fileName))
	except UnicodeError: 
		#https://stackoverflow.com/questions/37773489/read-line-with-encode-with-utf8
		print("UnicodeError: %s" % fileName)
	except IOError:
		print('IOError:%s' % fileName)
		
def replace_file_to_utf8(fromPath):
	# !!! does not backup the origin file
	content = codecs.open(fromPath, 'r').read()
	source_encoding = chardet.detect(content)['encoding']
	print(source_encoding)
	if source_encoding != 'utf-8' and source_encoding != 'UTF-8-SIG':
		print('will convert\' %s \'to utf-8' % os.path.basename(fromPath))
		content = content.decode(source_encoding, 'ignore') #.encode(source_encoding)
		os.remove(fromPath)
		codecs.open(fromPath, 'w', encoding='utf-8').write(content)
		
			
checkTheNecessaryDirsAt(rootPath, dirs)
makeTheNecessaryDirsIfNeedAt(rootPath, dirs)

#shutil.move(os.path.join(qualifiedPath, movedFileName), os.path.join(originPath, movedFileName))

lyricFiles = getAllLyricFileAt(os.path.join(rootPath, dirs[0]))
for x in lyricFiles:
	(e, n) = checkFileEncodeAt(x)
	if e == 'utf-8':
		checkLyricQualifiedAt(x, pattern, formattedPath, qualifiedPath)
	else:
		replace_file_to_utf8(x)
		checkLyricQualifiedAt(x, pattern, formattedPath, qualifiedPath)
		print('%s   %s' % (e, n))
#[checkLyricQualifiedAt(x, pattern, os.path.join(rootPath, dirs[2]), os.path.join(rootPath, dirs[1])) for x in lyricFiles]