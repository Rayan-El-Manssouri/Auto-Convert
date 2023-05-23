from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTAnno

def extract_text_coordinates(pdf_path):
    text_coordinates = []

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for line in element:
                    for word in line:
                        if isinstance(word, LTAnno):
                            continue
                        text = word.get_text().strip()
                        x0, y0, x1, y1 = word.bbox
                        text_coordinates.append((text, x0, y0, x1, y1))

    return text_coordinates

# Exemple d'utilisation
pdf_path = 'example.pdf'
text_coordinates = extract_text_coordinates(pdf_path)

# Affichage des coordonnées de texte
for text_coord in text_coordinates:
    text, x0, y0, x1, y1 = text_coord
    print(f"Texte : {text}")
    print(f"Coordonnées : x0={x0}, y0={y0}, x1={x1}, y1={y1}")
    print("---")
