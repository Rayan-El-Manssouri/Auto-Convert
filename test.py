import pdfminer
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

def extract_text_and_color_coordinates(pdf_path):
    text_coordinates = []
    color_coordinates = []
    
    parser = PDFParser(open(pdf_path, 'rb'))
    document = pdfminer.pdfdocument.PDFDocument(parser)
    
    resource_manager = PDFResourceManager()
    device = PDFPageAggregator(resource_manager, laparams=LAParams())
    interpreter = PDFPageInterpreter(resource_manager, device)
    
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        
        for element in layout:
            if isinstance(element, (LTTextBox, LTTextLine)):
                for text_object in element:
                    if isinstance(text_object, LTChar):
                        x0, y0, x1, y1 = text_object.bbox
                        text_coordinates.append((text_object.get_text(), x0, y0, x1, y1))
                        textstate = text_object.textstate
                        color = textstate.fillcolor if textstate and hasattr(textstate, 'fillcolor') else None
                        color_coordinates.append(color)
    
    return text_coordinates, color_coordinates

# Exemple d'utilisation
pdf_path = 'example.pdf'
text_coordinates, color_coordinates = extract_text_and_color_coordinates(pdf_path)

# Affichage des coordonnées de texte et de couleur
for text_coord, color_coord in zip(text_coordinates, color_coordinates):
    text, x0, y0, x1, y1 = text_coord
    color = color_coord if color_coord else "Inconnue"
    print(f"Texte : {text}")
    print(f"Coordonnées : x0={x0}, y0={y0}, x1={x1}, y1={y1}")
    print(f"Couleur : {color}")
    print("---")
