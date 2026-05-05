import pymupdf

def pdf_to_text(path):
    ''' To extract the pdf content to text'''

    doc = pymupdf.open(path)
    out = open(r"data/data.txt", "wb")

    for page in doc: 
        text = page.get_text().encode("utf8") 
        out.write(text) 
        out.write(bytes((12,)))
    out.close()
