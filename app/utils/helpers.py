from docx import Document
import textract
from pdfminer.high_level import extract_text
import re
from nltk.corpus import stopwords

def extract_text_from_doc(file_path: str) -> str:
    text = textract.process(file_path)
    return text.decode('utf-8')

def extract_text_from_pdf(file_path: str) -> str:
    text = extract_text(file_path)
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".doc"):
        return extract_text_from_doc(file_path)
    else:
        raise ValueError("Unsupported file format")


print(extract_text_from_file('app/utils/Praveen.pdf'))

# import os
# print(os.path.exists())  # should return True

