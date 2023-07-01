from pdfminer.high_level import extract_pages
from text.clean import clean_text
from text.font import clean_font_name
from typing import List, Dict, Tuple
from pdfminer.layout import (
    LTTextBoxHorizontal,
    LTChar,
    LTTextLineHorizontal,
)
from message_terminal.message import color_text_terminal
from pdfminer.layout import LTChar, LTTextLineHorizontal
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams


def get_bounding_box(word):
    """
    Récupère les coordonnées de la boîte englobante d'un mot.

    Args:
        word (LTTextLineHorizontal): Le mot dont nous voulons récupérer les coordonnées.

    Returns:
        float: La coordonnée x0 de la boîte englobante.
    """
    if isinstance(word, LTChar):
        return word.bbox[0]
    elif isinstance(word, LTTextLineHorizontal):
        # Créez un analyseur de mises en page avec des paramètres par défaut
        laparams = LAParams()
        resource_manager = PDFResourceManager()
        device = PDFPageAggregator(resource_manager, laparams=laparams)
        interpreter = PDFPageInterpreter(resource_manager, device)

        # Exécutez l'interpréteur PDF sur la première page
        interpreter.process_page(word._objs[0])
        layout = device.get_result()

        # Parcourez chaque caractère dans la ligne de texte
        x0 = None
        for char in layout:
            if isinstance(char, LTChar):
                bbox = char.get_textbox()
                if x0 is None or bbox[0] < x0:
                    x0 = bbox[0]

        return x0
    else:
        raise TypeError("Le type de mot n'est pas pris en charge.")


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
                    count = 0
                    for word in line:
                        if isinstance(word, LTChar):
                            font_size = word.size
                            font_name = clean_font_name(word.fontname)
                            text = word.get_text().strip()
                            # calcule les coordonnées de la boîte englobante
                            if text:
                                text = clean_text(text)
                                count += 1
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
    color_text_terminal("Extraction du texte terminé !", "green", 0.01)
    return {"pages": page_data}