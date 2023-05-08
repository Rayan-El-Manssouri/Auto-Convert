import os.path
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTCurve

segments = []
seen = set()
processed_pages = set()  # ensemble pour stocker les numéros de page traités

for page_layout in extract_pages("example.pdf"):
    page_number = page_layout.pageid  # obtenir le numéro de page actuel
    if page_number in processed_pages:
        continue  # passer à la page suivante si la page a déjà été traitée
    processed_pages.add(
        page_number
    )  # ajouter le numéro de la page actuelle à l'ensemble des pages traitées

    for element in page_layout:
        if isinstance(element, LTCurve):
            # Ajouter les coordonnées des points de contrôle et le point final dans un dictionnaire
            segment = {
                "type": "courbe",
                "points": [
                    {"x": element.x0, "y": element.y0},
                    {"x": element.x1, "y": element.y1},
                ],
                "points_de_controle": [
                    {"x": p[0], "y": p[1]} for p in element.pts[:-1]
                ],
                "borderColor": element.stroking_color,
            }

            # Vérifier si la courbe a déjà été ajoutée en comparant les coordonnées des points de contrôle
            coords = frozenset((p["x"], p["y"]) for p in segment["points_de_controle"])
            if coords not in seen:
                # Ajouter le dictionnaire à la liste des segments de courbe et stocker les coordonnées dans l'ensemble
                segments.append(segment)
                seen.add(coords)
# Générer le code pour chaque vue
page_code = ""
for segment in segments:
    view_code = (
        "<div style={{  position: 'absolute', top: %f, left: %f, width: %f, height: %f, borderWidth: %f, color: 'rgb%s', borderRadius: %f, backgroundColor: '%s'  }} />"
        % (
            segment["points"][1]["y"],  # échanger avec segment["points"][0]["y"]
            segment["points"][0]["x"],
            segment["points"][1]["x"] - segment["points"][0]["x"],
            segment["points"][0]["y"]
            - segment["points"][1]["y"],  # échanger avec segment["points"][1]["y"]
            1,  # largeur de la bordure
            segment["borderColor"],  # couleur de la bordure
            10,  # rayon de bordure
            "white",  # couleur de fond
        )
    )

    page_code += "<div> \n %s \n </div>\n" % view_code


# Convertir la liste des segments de courbe en JSON
segments_json = json.dumps(segments)

if not os.path.isfile("pdf_views.js"):
    js_code = """
    import React from "react";
    import {{ PDFViewer, Document, Page, Text }} from '@react-pdf/renderer';

    const PdfComponent = () => {{
        return (
            <PDFViewer style={{ {{ width: '100%', height: '100vh', border: 'none', position: 'fixed' }}  }}>
                <Document>
                  <Page size="A4">\n'
                    {page_code}
                    </Page>
                </Document>
            </PDFViewer>
        );
    }}

    export default PdfComponent;
    """.format(
        page_code=page_code
    )

    with open("pdf_views.js", "w") as f:
        f.write(js_code)
else:
    print("Le fichier pdf_views.js existe déjà.")
