#! /usr/bin/env python3

from PyPDF2 import PdfFileMerger, PdfReader, PdfWriter
from fpdf import FPDF
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import argparse, os, re, glob, random

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
    
    parser.add_argument(
        "-bw",
        "--black-n-white",
        required=False,
        help="Convert to B&W",
        dest="bw",
        default=False
    )


    args = parser.parse_args()

    matched_files = []
    for file in args.input:
        if glob.escape(file) != file:
            matched_files.extend(glob.glob(file))
        else:
            matched_files.append(file)
    quality_jpg = int(args.quality)
    convert_bw = args.bw
    watermark_text = args.watermark_text



    for file in matched_files:
        print(f"Processing {file}...")
        if not "marked" in file:
            input_pdf_path = f"{os.getcwd()}/{file}"

            print(" -> Extracting pdf to JPG")
            images = convert_from_path(input_pdf_path)
            jpg_files = []
            for i in range(len(images)):
                output_jpg = f"{os.getcwd()}/.{i}.jpg"
                jpg_files.append(output_jpg)
                watermark_jpg = Image.new('RGBA', images[i].size, (255,255,255,0))
                draw = ImageDraw.Draw(watermark_jpg)
                font = ImageFont.truetype(f"{os.path.dirname(os.path.realpath(__file__))}../Arial.ttf", 50)
                width, height = images[i].size 
                y=200
                for j in range(7):
                    x=random.randint(0, width-300)
                    y+=random.randrange(0,int(height/8), 19)+random.randint(0,100)
                    draw.text((x,y), watermark_text, fill=(255,255,255, 0), font=font)

                #Combining both layers and saving new image
                
                watermarked = Image.alpha_composite(images[i].convert("RGBA"), watermark_jpg)
                watermarked_jpg = watermarked.convert("RGB")
                if convert_bw:
                    watermarked.convert("L")
                # imgs.append(watermarked_img)
                watermarked_jpg.save(output_jpg)
                print(f"    ->{output_jpg}")
                exit(0)
            exit(0)

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
