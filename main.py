import json
from typing import List, Dict, Tuple
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTChar, LTCurve, LTLine

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
                    {"x": element.pts[i], "y": element.pts[i + 1]}
                    for i in range(0, len(element.pts) - 1, 2)
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
page_height = page_layout.height  # obtenir la hauteur de la page actuelle
for segment in segments:
    view_code = (
        "<div style={{  position: 'absolute', top: %f, left: %f, width: %f, height: %f, color: 'rgb%s', borderRadius: %f, backgroundColor: '%s', zIndex: 1, borderWidth: 1  }} />"
        % (
            page_height - segment["points"][1]["y"],  # inverser la valeur du top
            segment["points"][0]["x"],
            segment["points"][1]["x"] - segment["points"][0]["x"],
            segment["points"][1]["y"] - segment["points"][0]["y"],
            segment["borderColor"],  # couleur de la bordure
            1,  # rayon de bordure
            "transparent",  # couleur de fond
        )
    )

    page_code += "<div> %s </div>\n" % view_code


def extract_text_coords_font_from_pdf(
    pdf_path: str,
    special_chars_offsets: Dict[str, Tuple[float, float]] = None,
    block_offsets: Dict[str, Tuple[float, float]] = None,
) -> Dict[str, List[Dict[str, str]]]:
    page_data = []
    for page_layout in extract_pages(pdf_path):
        height = page_layout.height
        page_objects = []
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for line in element:
                    line_text = ""
                    line_width = (
                        20  # Ajout d'une variable pour stocker la largeur de la ligne
                    )
                    for word in line:
                        if isinstance(word, LTChar):
                            font_size = word.size
                            font_name = clean_font_name(word.fontname)
                            text = word.get_text().strip()
                            if text:
                                text = clean_text(text)
                                if (
                                    special_chars_offsets is not None
                                    and text in special_chars_offsets
                                ):
                                    x_offset, y_offset = special_chars_offsets[text]
                                    x, y = (
                                        word.bbox[0] + x_offset,
                                        height
                                        - word.bbox[3]
                                        - word.height * font_size / 70
                                        + y_offset,
                                    )
                                else:
                                    x, y = (
                                        word.bbox[0],
                                        height
                                        - word.bbox[3]
                                        - word.height * font_size / 70,
                                    )

                                if (
                                    block_offsets is not None
                                    and line_text in block_offsets
                                ):
                                    x_offset, y_offset = block_offsets[line_text]
                                    x += x_offset
                                    y += y_offset

                                # Ajout de la largeur du mot à la largeur de la ligne
                                line_width += word.width * font_size / 70

                                x -= 13
                                page_objects.append(
                                    {
                                        "text": text,
                                        "font_name": font_name,
                                        "font_size": font_size,
                                        "x": x,
                                        "y": y,
                                    }
                                )
                                line_text += text
                    # Ajout de la condition pour ajuster la position des caractères spéciaux
                    if (
                        special_chars_offsets is not None
                        and line_text in special_chars_offsets
                    ):
                        x_offset, y_offset = special_chars_offsets[line_text]
                        for obj in page_objects[-len(line) :]:
                            obj["x"] -= line_width * x_offset
                            obj["y"] += y_offset

        if page_objects:
            page_data.append({"text_objects": page_objects})
    return {"pages": page_data}


def clean_text(text: str) -> str:
    return text.replace("\n", "\\n").replace("'", "’")


def clean_font_name(font_name: str) -> str:
    font_name = font_name.split("+")[-1]
    font_name = font_name.replace(" ", "")
    return font_name


def format_text(text: str) -> str:
    return text.replace("\n", "\\n").replace("'", "\\'")


def generate_react_component(json_data: Dict[str, List[Dict[str, str]]]) -> str:
    font_paths = {
        "Helvetica-Compressed": "./ttf/Helvetica-Compressed-Regular.ttf",
        "TimesNewRomanPS-BoldItalicMT": "./ttf/TimesNewRomanBoldItalic.ttf",
        "Arial-BoldMT": "./ttf/Arial-BoldMT.ttf",
        "Helvetica-Black": "./ttf/Helvetica-Black.ttf",
        "Webdings": "./ttf/Webdings.ttf",
        "Helvetica-Condensed-Bold": "./ttf/Helvetica-Condensed-Bold.ttf",
        "Helvetica-Narrow": "./ttf/Helvetica-Narrow.ttf",
        "SourceSansPro-Semibold": "./ttf/SourceSansPro-SemiBold.ttf",
        "SourceSansPro-Bold": "./ttf/SourceSansPro-Bold.ttf",
        "Wingdings-Regular": "./ttf/Wingdings-Regular.ttf",
        "Helvetica-Narrow-Bold": "./ttf/Helvetica-Narrow-Bold.ttf",
    }

    font_registers = [
        f"Font.register({{ family: '{font}', src: '{path}' }});"
        for font, path in font_paths.items()
    ]

    font_registers_str = "\n".join(font_registers)

    component = f"""
import React from 'react';
import {{ PDFViewer, Document, Page, Text }} from '@react-pdf/renderer';
import {{ Font }} from '@react-pdf/renderer';

{font_registers_str}

const PdfComponent = () => (
    <PDFViewer style={{ {{  width: '100%', height: '100vh', border: 'none', position: 'fixed' }}  }}>
"""
    for page in json_data["pages"]:
        component += f"        <Document>\n"
        component += f'        <Page size="A4">\n'
        for text_obj in page["text_objects"]:
            component += f"            <Text style={{  {{ position: 'absolute', left: {text_obj['x'] + 10}, top: {text_obj['y']}, zIndex: 2, fontSize: {text_obj['font_size']}, fontFamily: '{text_obj['font_name']}' }} }}>"
            component += f"                {format_text(text_obj['text'])}"
            component += f"            </Text>\n"
            component += f"           "
        component += f"        {page_code}\n"
        component += f"        </Page>\n"
        component += f"        </Document>\n"

    component += f"""    </PDFViewer>
);

export default PdfComponent;
"""

    return component


pdf_path = "example.pdf"
json_path = "example.json"
react_component_path = "PdfComponent.js"

# extract text and font information from the PDF file
pdf_data = extract_text_coords_font_from_pdf(pdf_path)

# write extracted data to a JSON file with UTF-8 encoding
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=4)

# generate a React component that renders the PDF
react_component = generate_react_component(pdf_data)

# write the React component to a file with UTF-8 encoding
with open(react_component_path, "w", encoding="utf-8") as f:
    f.write(react_component)
