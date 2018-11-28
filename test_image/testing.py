from PIL import Image

testImage = r"F:\python\noIcon.jpg"

im = Image.open(testImage)
width, height = im.size

left = int(width * 0.5) - 120
top = int(height * 0.5) - 120

right = left + 240
bottom = top + 240

cropped_im = im.crop((left,top,right,bottom)) 
cropped_im.save(r"F:\python\noIcon.png")


