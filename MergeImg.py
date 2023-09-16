from PIL import Image
#Read the two images
stt = 0
for i in range(0,10):
    url = "C:\\Users\\admin\\Documents\\GitHub\\Sign-Language-Recognition\\Gesture Image Data\\V\\" + i + ".img"
    url1 = "C:\\Users\\admin\\Documents\\GitHub\\Sign-Language-Recognition\\Gesture Image Data\\L\\" + i + ".img"
    image1 = Image.open(url)
    image2 = Image.open(url1)
    #resize, first image
    image1 = image1.resize((426, 240))
    image1_size = image1.size
    image2_size = image2.size
    new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
    new_image.paste(image1,(0,0))
    new_image.paste(image2,(image1_size[0],0))
    new_image.save("images/merged_image.jpg","JPEG")
    new_image.show()