from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextLineHorizontal

# Ouverture du fichier PDF
with open("example.pdf", "rb") as pdf_file:
    # Parcours de chaque page du PDF
    for page_layout in extract_pages(pdf_file):
        # Parcours de chaque ligne de texte de la page
        for element in page_layout:
            # Vérification si l'élément est une ligne de texte horizontale
            if isinstance(element, LTTextLineHorizontal):
                # Calcul du rayon de bordure de la ligne de texte
                start_x, start_y = element.bbox[0], element.bbox[1]
                end_x, end_y = element.bbox[2], element.bbox[3]
                borderRadius = (end_y - start_y) / 2
                # Affichage du rayon de bordure de la ligne de texte
                print(f"Border radius: {borderRadius:.2f}")
