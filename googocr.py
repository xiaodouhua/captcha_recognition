import pytesseract

from PIL import Image

image = Image.open("pic_sep/3_0logo.jpg")
code = pytesseract.image_to_string(image)
print (code)