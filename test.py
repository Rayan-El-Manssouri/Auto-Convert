from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfexceptions import PDFTextExtractionNotAllowed


def normalize_coordinates(page_num, bbox, pdf_path):
    with open(pdf_path, "rb") as fp:
        for page_layout in extract_pages(fp):
            if page_layout.pageid == page_num:
                page = interpreter.process_page(doc.get_page(page_num))
                break
        else:
            raise ValueError("Invalid page number")
    page_width, page_height = page.width, page.height
    x0, y0, x1, y1 = bbox
    x0, x1 = x0 * page_width, x1 * page_width
    y0, y1 = (1 - y1) * page_height, (1 - y0) * page_height
    text = page.get_text()
    for text_obj in page:
        if isinstance(text_obj, LTTextContainer):
            for line in text_obj:
                if y0 <= line.y1 <= y1:
                    print(line.get_text())


normalize_coordinates(1, (0, 0, 0.2, 0.2), "example.pdf")
