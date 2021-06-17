import pytesseract
from PIL import Image, ImageGrab
import keyboard
import sys,os
import argparse
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

pytesseract.pytesseract.tesseract_cmd='/usr/bin/tesseract'

def parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    screenshot_parser = subparsers.add_parser('ss')
    screenshot_parser.add_argument('-o', nargs=1,choices=['docx','txt'], default=['txt'])
    screenshot_parser.add_argument('-l', nargs=1, default=['rus'])

    img2txt_parser = subparsers.add_parser('img')
    img2txt_parser.add_argument('-p',type=argparse.FileType('rb'))
    img2txt_parser.add_argument('-o', nargs=1, default=['txt'])
    img2txt_parser.add_argument('-l', nargs=1, default=['rus'])

    pdf_parser = subparsers.add_parser('pdf')
    pdf_parser.add_argument('-p')
    pdf_parser.add_argument('-o', nargs=1, default=['txt'])

    return parser

def write_img(ext,lang,path):
    with open(f'ocr_output/output.{ext}','w') as f:
        f.write(pytesseract.image_to_string(Image.open(path),lang=lang))
        f.close()

def write_pdf(ext,path):
    output_string = StringIO()
    with open(path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    with open(f'ocr_output/output.{ext}','w') as f:
        f.write(output_string.getvalue())
        f.close()

def screenshot():
    keyboard.wait('space')
    img = ImageGrab.grab()
    img.save('input.png')
    write_img(namespace.o[0],namespace.l[0],'input.png')
    os.remove('input.png')

create_parser = parser()
namespace = create_parser.parse_args(sys.argv[1:])
    
if namespace.command == 'ss':
    screenshot()
    
elif namespace.command == 'img':
    write_img(namespace.o[0],namespace.l[0],namespace.p)

elif namespace.command == 'pdf':
    write_pdf(namespace.o[0],namespace.p)




# add partial screenshot
