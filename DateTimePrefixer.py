"""
---------------------------------------------------------------
DateTimePrefixer

Created By Zachary Magnotti
9/1/2017

A script which reads file metadata from a library of images, and
copys them with the Date and Time prefixed to the file name.

Useful for sorting pictures chronologically
----------------------------------------------------------------
"""
from argparse import ArgumentParser
from os import getcwd, mkdir, listdir
from os.path import basename, abspath, join, isdir
from sys import stdout
from PIL import Image, ExifTags
from shutil import copy2
from datetime import datetime 

class Printer:
	"""
	Print things to stdout on one line dynamically
	"""
	def __init__(self,data):
		stdout.write("\r"+str(data))
		stdout.flush()

def makeFolder(folder):	
	"""
	creates new directory if it doesn't already exist
	returns absolute path of new folder
	"""
	try:	
		mkdir(folder)
	except OSError as e:
		if not isdir(folder):
			print('error creating folder')
			print('exiting program...')
			exit()
	return abspath(folder)

def getDateTime(image):
	"""
	Given image return DateTimeOriginal
	if no Exif DateTimeOriginal data exists, return datetime.min
	"""
	try:	return datetime.strptime(image._getexif()[36867], '%Y:%m:%d %H:%M:%S')
	except:	return datetime.min

def PrefixFilenamesWithDateTime(input_folder, output_folder):
	"""
	given a directory of images, prefix filename of each image with Exif Datetime value
	if no Datetime value exists, prefix with "none"
	program will copy images into new folder by default
	"""
	print('Processing files in %s...' % input_folder)
	files = listdir(input_folder)
	count = 0
	# load image data, create new path name, and copy file to new path
	for file in files:

		# load image file and get datetime data
		filePath = abspath(join(input_folder, file))
		try: 
			with Image.open(open(filePath, 'rb')) as image: 
				image_datetime = getDateTime(image)
		except:
			# if invalid image, close file and continue to next iteration
			Printer("Error reading: %s\n" % (filePath,))
			count+=1
			continue

		# create new filename, save to output_folder
		prefix = datetime.strftime(image_datetime, '%Y-%m-%d %H-%M-%S')
		if image_datetime == datetime.min:
			prefix = 'none'
		outPath = abspath(join(output_folder, prefix + ' ' + basename(file)))

		# copy file to new path
		try : 	copy2(filePath, outPath)
		except :Printer("error saving %s\n" % (file))

		# user feedback
		count += 1
		output = "%d of %d completed." % (count, len(files))
		Printer(output)
	stdout.write('\n')

#main function 
def main():
	#parse arguments
	parser = ArgumentParser(description = 'Prefixes the filenames of each image in a library with the Exif Datetime value')

	#add arguments
	parser.add_argument('--input-folder', dest='input_folder', required=True)
	parser.add_argument('--output-folder', dest='output_folder', required=False)

	args = parser.parse_args()

	##### INPUTS #####

	# entering "this-folder" as input_folder returns current working directory
	if args.input_folder != 'this-folder' :
		input_folder = abspath(args.input_folder)
	else:
		input_folder = getcwd()

	# if no output folder, save to current directory
	if args.output_folder : 
		output_folder = makeFolder(args.output_folder)
	else:
		output_folder = getcwd()

	##### END INPUTS #####

	# add prefixes and save to output_folder
	PrefixFilenamesWithDateTime(input_folder, output_folder)

#standard boilerplate
if __name__ == '__main__':
	main()