import glob
import os
from pdf2docx import Converter

pdf_dir = '/Users/palcacer/Sites/pedroalcacer-com/static/programs/originals'
pdfs = glob.glob(os.path.join(pdf_dir, '*.pdf'))

for pdf_file in pdfs:
    docx_file = pdf_file.replace('.pdf', '.docx')
    cv = Converter(pdf_file)
    cv.convert(docx_file, start=0, end=None)
    cv.close()
    print(f"Converted {pdf_file} to {docx_file}")
