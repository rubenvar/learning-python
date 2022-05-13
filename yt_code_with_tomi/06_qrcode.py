# # create:
# import qrcode

# data = "https://calendarioaguasabiertas.com"

# qr = qrcode.QRCode(version=1, box_size=10, border=5)

# qr.add_data(data)

# qr.make(fit=True)
# img = qr.make_image(fill_color='red', back_color='white')

# img.save('files/test.png')

# decode:
from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('files/test2.png')

result = decode(img)

print(result)
