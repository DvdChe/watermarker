#! /usr/bin/env python3

from PyPDF2 import PdfFileMerger, PdfReader, PdfWriter
from fpdf import FPDF
from pdf2image import convert_from_path
from PIL import Image
import argparse, os, re, glob

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", required=True, help="PDF file to watermark", dest="input"
    )
    parser.add_argument(
        "-t",
        "--text",
        required=True,
        help="Text to watermark the pdf with",
        dest="watermark_text",
    )

    args = parser.parse_args()

    watermark_text = args.watermark_text
    watermark_text += "\n"
    watermark_pdf = FPDF()
    watermark_pdf.add_page()
    watermark_pdf.set_font("Arial", size=50)
    watermark_pdf.rotate(angle=45)
    watermark_pdf.set_xy(-500,180)
    watermark_pdf.multi_cell(200, 15, txt=watermark_text, align="C")
    watermark_pdf.set_xy(-300,50)
    watermark_pdf.multi_cell(200, 15, txt=watermark_text, align="C")
    watermark_pdf.set_xy(-300,170)
    watermark_pdf.multi_cell(200, 15, txt=watermark_text, align="C")

    watermark_pdf.output(".watermark.pdf")

    for file in glob.glob(args.input):
        if not "_marked" in file:
            input_pdf_path = f"{os.getcwd()}/{file}"
            output_pdf_path = re.sub(
                r"^(.*)\/(.*)\.pdf$", r"\1/\2_marked.pdf", input_pdf_path
            )

            with open(input_pdf_path, "rb") as input_file, open(
                f"{os.getcwd()}/.watermark.pdf", "rb"
            ) as watermark_file:
                print(input_pdf_path)
                input_pdf = PdfReader(input_file)
                watermark_pdf = PdfReader(watermark_file)
                watermark_page = watermark_pdf.pages[0]
                output = PdfWriter()

                for i in range(len(input_pdf.pages)):
                    pdf_page = input_pdf.pages[i]
                    pdf_page.merge_page(watermark_page)
                    output.add_page(pdf_page)

                with open(output_pdf_path, "wb") as merged_file:
                    output.write(merged_file)

            images = convert_from_path(output_pdf_path)
            jpg_files = []
            for i in range(len(images)):
                output_jpg = f"{os.getcwd()}/.{i}.jpg"
                jpg_files.append(output_jpg)
                images[i].save(output_jpg)

            imgs = []
            for jpg_file in jpg_files:
                print(jpg_file)
                imgs.append(Image.open(jpg_file))
            pdf_marked_name = re.sub(
                r"^(.*)\/(.*).pdf$", rf"\2-marked.pdf", input_pdf_path
            )
            imgs[0].save(pdf_marked_name, save_all=True, append_images=imgs)

            os.remove(output_pdf_path)
            for i in jpg_files:
                os.remove(i)
    os.remove(f"{os.getcwd()}/.watermark.pdf")
