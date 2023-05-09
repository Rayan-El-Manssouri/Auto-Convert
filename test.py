import fitz


def extract_text_colors(pdf_file):
    # Extraction de la couleur avec fitz
    doc = fitz.open(pdf_file)
    colors = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    color = span["color"]
                    colors.append(color)
    doc.close()
    return colors


colors = extract_text_colors("example.pdf")
print(colors)
