from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import PDFStream
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTPage, LTCurve

from tqdm import tqdm

# Ouvrir le fichier PDF
with open("example.pdf", "rb") as pdf_file:
    # Créer un objet de type PDFParser
    parser = PDFParser(pdf_file)

    # Créer un objet de type PDFDocument
    document = PDFDocument(parser)

    # Extraire la première page du PDF
    pages = PDFPage.create_pages(document)
    page = next(pages)

    # Créer un objet de type PDFResourceManager
    resource_manager = PDFResourceManager()

    # Créer un objet de type PDFPageAggregator
    device = PDFPageAggregator(resource_manager, laparams=None)

    # Créer un objet de type PDFPageInterpreter
    interpreter = PDFPageInterpreter(resource_manager, device)

    # Interpréter la page pour extraire les courbes
    interpreter.process_page(page)
    layout = device.get_result()

    # Boucler sur les éléments de la page pour trouver les courbes
    for element in tqdm(layout, desc="Traitement des courbes"):
        if isinstance(element, LTPage):
            for curve in element:
                if isinstance(curve, LTCurve):
                    # Extraire les coordonnées et la bordure de la courbe
                    x, y = curve.bbox[0], curve.bbox[1]
                    width, height = (
                        curve.bbox[2] - curve.bbox[0],
                        curve.bbox[3] - curve.bbox[1],
                    )
                    border_radius = curve.line_width / 2.0

                    # Afficher les résultats
                    print(
                        f"La courbe est située à ({x}, {y}) avec une largeur de {width} et une hauteur de {height}. La bordure a un rayon de {border_radius}."
                    )
