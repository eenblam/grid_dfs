from PIL import Image
l = [(0,0,0), (0,0,0), (128,128,128), (256,256,256), (256,256,256)] * 2000
im = Image.new("RGB", (100,100), "white")
im.putdata(l)
im.show()
