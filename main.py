import fitz
import json
import os

PDF_FILENAME = 'test.pdf'
JSON_FILENAME = 'result.json'

if not os.path.exists(PDF_FILENAME):
    print(f'Error: PDF file "{PDF_FILENAME}" does not exist.')
    exit()

pdf_file = fitz.open(PDF_FILENAME)
num_pages = len(pdf_file)

images = []
lines = []

for page_num, page in enumerate(pdf_file):
    # Extract images and their coordinates
    for img in page.get_images():
        xref = img[0]
        pix = fitz.Pixmap(pdf_file, xref)
        images.append({
            'xref': xref,
            'pix_width': pix.width,
            'pix_height': pix.height,
            'width': img[1],
            'height': img[2],
            'colorspace': pix.colorspace,
            'image_type': pix.colorspace,
            'dpi': pix.h_dpi,
            'page': page.number
        })
        pix = None

        for inst in page.get_text("dict")["blocks"]:
            for line in inst["lines"]:
                bbox = line["bbox"]
                x0, y0, x1, y1 = bbox
                text_box = fitz.Rect(x0, y0, x1, y1)
                text_box = text_box.intersect(page.bound())
                if text_box.width <= 0 or text_box.height <= 0:
                    continue
                text = page.get_text("text", clip=text_box)
                textbox = page.get_textbox(text_box)
                if not textbox or not isinstance(textbox, fitz.Textbox):
                    continue
                font = textbox.font
                font_id = textbox.font
                font_size = textbox.size
                font_family = page.get_fonts()[font_id].get("familyname")
                lines.append({
                    'text': text,
                    'x0': bbox[0],
                    'y0': bbox[1],
                    'x1': bbox[2],
                    'y1': bbox[3],
                    'page': page.number,
                    'font_size': font_size,
                    'font_family': font_family
                })

    # Update progress
    progress = (page_num + 1) / num_pages * 100
    print(f'Processed page {page_num+1}/{num_pages} ({progress:.2f}%)')

# Create a dictionary to store the PDF data
pdf_data = {
    'images': images,
    'lines': lines
}

# Convert the dictionary to JSON format
json_data = json.dumps(pdf_data, indent=4, ensure_ascii=False)

# Write the JSON data to a file
with open(JSON_FILENAME, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print('Process finished!')
