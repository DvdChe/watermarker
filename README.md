# Watermark documents easily : 

This dirty script will add watermark text on pdf documents. Here is how to use it : 

```
python watermarker -i <input_pdf_file> -t "Watermark text" 
```

Watermark text will be placed at all pages of documents and watermarked file will be placed at the same location of the original one with `_watermarked.pdf` at the end of file.

To avoid layer deletion with random pdf editor, the processing is following theses steps : 
1. Generate watermark pdf file ( pdf that contains watermark pattern ) 
2. Merge watermark pdf file to all pages of original pdf in an ephemeral file ( still pdf )
3. Render watermarked pages from pdf to jpg
4. Merging jpg file to final pdf

By this way, final pdf file contains no layers.

# Limitations :
Some editors are still able to recognize text based on computer vision or machine learning. 