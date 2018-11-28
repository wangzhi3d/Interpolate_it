from PIL import Image
import argparse
import logging


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


'''
import iconConvert
reload(iconConvert)
startImage = r'F:\python\noIcon.jpg'
resImage = startImage.replace('.jpg','.png')
iconConvert.processScreenCap(startImage,resImage)
'''

parser = argparse.ArgumentParser(description = 'Converts any size png to a 240x240 jpg')
parser.add_argument('-ip','--imagePath',dest='imagePath', 
					help='path to the starting icon.jpg')
parser.add_argument('-irp','--imageResultPath',dest='imageResultPath',
					help='path to where the image will be stored.')
args = parser.parse_args()

def processScreenCap(imagePath = None , imageResultPath = None):
	#testImage = r"F:\python\noIcon.jpg"

	im = Image.open(imagePath)
	width, height = im.size

	left = int(width * 0.5) - 120
	top = int(height * 0.5) - 120

	right = left + 240
	bottom = top + 240

	cropped_im = im.crop((left,top,right,bottom)) 
	cropped_im.save(imageResultPath)
	_logger.info('Done cropping image')



if __name__ == '__main__':
	processScreenCap(imagePath = args.imagePath , imageResultPath = args.imageResultPath)
	_logger.info('DONF! Image processed.')




import subprocess
imageStart = r'F:\python\noIcon.jpg'
imageResult = r'F:\python\noIconResulr.png'


cmd = ['python' , r'F:\python\iconConvert.py',
		'-ip' , imageStart,
		'-irp' , imageResult]

p = subprocess.Popen(cmd , stdout = subprocess.PIPE , stderr = subprocess.PIPE , shell = True)
res,err = p.communicate()
