import fitz


def extract_text_colors(pdf_path: str, text: str, x0: float, y0: float) -> str:
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
        for line in block["lines"]:
            for span in line["spans"]:
                if (
                    span["text"] == text
                    and span["bbox"][0] == x0
                    and span["bbox"][1] == y0
                ):
                    r, g, b = span["color"]
                    color = "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))
                    return color
    return None
