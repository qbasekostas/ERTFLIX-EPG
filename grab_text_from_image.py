import pytesseract
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the Tesseract executable (adjust this path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Path to the image
image_path = 'Screenshot 2024-12-25 at 00-05-22 ΕΡΤ Christmas - ERTFLIX.png'

# Open the image using Pillow
image = Image.open(image_path)

# Use Tesseract to do OCR on the image
logging.info(f"Performing OCR on image: {image_path}")
text = pytesseract.image_to_string(image, lang='eng')

# Print the extracted text (for debugging purposes)
logging.info("Extracted text from image:")
print(text)

# Save the extracted text to a file
output_file = 'extracted_text.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(text)

logging.info(f"Extracted text has been saved to {output_file}")
