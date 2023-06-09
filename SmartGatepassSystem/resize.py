from PIL import Image

image = Image.open(r'C:\Users\Entropic_16\Desktop\Files\321654.jpg')
new_image = image.resize((154, 154))
new_image.save(r'C:\Users\Entropic_16\Desktop\321654_154.jpg')

print(new_image.size)
# input_path = r"C:\Users\Entropic_16\Desktop\Files\123456.jpg"
# output_path = r"C:\Users\Entropic_16\Desktop"
# size = (154, 154)

