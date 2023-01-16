#! /usr/bin/env python3

from PyPDF2 import PdfFileMerger, PdfReader, PdfWriter
from fpdf import FPDF
from pdf2image import convert_from_path
from PIL import Image
import argparse, os, re, glob

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="PDF file to watermark",
        dest="input",
        nargs="+",
    )
    parser.add_argument(
        "-t",
        "--text",
        required=True,
        help="Text to watermark the pdf with",
        dest="watermark_text",
    )

    parser.add_argument(
        "-q",
        "--quality",
        required=False,
        help="Quality conversion",
        dest="quality",
        default=20
    )

    args = parser.parse_args()

    matched_files = []
    for file in args.input:
        if glob.escape(file) != file:
            # -> There are glob pattern chars in the string
            matched_files.extend(glob.glob(file))
        else:
            matched_files.append(file)
    quality_jpg = int(args.quality)
    watermark_text = args.watermark_text
    watermark_text += "\n"
    watermark_pdf = FPDF()
    watermark_pdf.add_page()
    watermark_pdf.set_font("Arial", size=50)
    watermark_pdf.rotate(angle=45)
    watermark_pdf.set_xy(-500, 180)
    watermark_pdf.multi_cell(200, 15, txt=watermark_text, align="C")
    watermark_pdf.set_xy(-300, 50)
    watermark_pdf.multi_cell(200, 15, txt=watermark_text, align="C")
    watermark_pdf.set_xy(-300, 170)
    watermark_pdf.multi_cell(200, 15, txt=watermark_text, align="C")

    watermark_pdf.output(".watermark.pdf")

    for file in matched_files:
        print(f"Processing {file}...")
        if not "marked" in file:
            input_pdf_path = f"{os.getcwd()}/{file}"
            inter_watermarked_pdf_path = re.sub(
                r"^(.*)\/(.*)\.pdf$", r"\1/.\2_marked.pdf", input_pdf_path
            )
            print("     -> Generating watermarked PDF")
            with open(input_pdf_path, "rb") as input_file, open(
                f"{os.getcwd()}/.watermark.pdf", "rb"
            ) as watermark_file:
                input_pdf = PdfReader(input_file)
                watermark_pdf = PdfReader(watermark_file)
                watermark_page = watermark_pdf.pages[0]
                output = PdfWriter()

                print("     -> Applying watermark to PDF")
                for i in range(len(input_pdf.pages)):
                    pdf_page = input_pdf.pages[i]
                    pdf_page.merge_page(watermark_page)
                    output.add_page(pdf_page)

                with open(inter_watermarked_pdf_path, "wb") as merged_file:
                    output.write(merged_file)

            print(" -> Extracting pdf to JPG")
            images = convert_from_path(inter_watermarked_pdf_path)
            jpg_files = []
            for i in range(len(images)):
                output_jpg = f"{os.getcwd()}/.{i}.jpg"
                jpg_files.append(output_jpg)
                images[i].save(output_jpg)
                print(f"    ->{output_jpg}")

            print(" -> Merge jpg to final PDF")
            imgs = []
            for jpg_file in jpg_files:
                imgs.append(Image.open(jpg_file))
            pdf_marked_name = re.sub(
                r"^(.*)\/(.*).pdf$", r"\1/\2-marked.pdf", input_pdf_path
            )
            imgs[0].save(pdf_marked_name, save_all=True, append_images=imgs[1::], quality=quality_jpg)
            print(" -> Removing watermarked PDF files :")
            print(f"    -> {inter_watermarked_pdf_path}")

            os.remove(inter_watermarked_pdf_path)
            print(" -> Removing jpg files")
            for i in jpg_files:
                os.remove(i)

    os.remove(f"{os.getcwd()}/.watermark.pdf")
