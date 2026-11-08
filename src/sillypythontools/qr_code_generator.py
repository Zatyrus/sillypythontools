# encoding: utf-8

# === description ====
# This script generates a QR code from a specified string and saves it as an image file.

# === usage ====
# 1. Set the `data` variable to the desired string you want to encode in the QR code.
# 2. Set the `outpath` variable to the desired output file path for the QR code image.
# 3. Run the script. It will generate a QR code and save it as an image file.

# ==== dependencies ====
import qrcode

# === parameters ====
data: str = "This is a test string for generating a QR code."
outpath: str = "path/to/your/file.png"  # the output file path for the QR code image

# === main logic ====
# iamge setup
border_size: int = 2
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=border_size,
)

# add data to the QR code and generate the QR code
qr.add_data(data)
qr.make(fit=True)

# create an image from the QR code
img = qr.make_image(fill_color="black", back_color="white")

# save the image
img.save(outpath)
