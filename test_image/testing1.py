from PIL import Image

testImage = r"F:\python\noIcon.jpg"

im = Image.open(testImage)

#size = im.size

im.thumbnail((240 , 158) , Image.ANTIALIAS)

cropped_im = im.crop() 
cropped_im.save(r"F:\python\noIcon.png")
