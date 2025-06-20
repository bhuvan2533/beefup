from docx import Document
import textract
from fastapi import UploadFile
from app.exception_handlers import InvalidFileTypeException
from io import BytesIO
import json
import fitz

def extract_text_from_pdf(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    pdf_bytes = uploaded_file.file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = " ".join([page.get_text() for page in doc]).replace("\n", " ").replace("\r", " ")
    return json.dumps(text)[1:-1]


def extract_text_from_docx(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    content = uploaded_file.file.read()
    document = Document(BytesIO(content))
    return json.dumps(" ".join([para.text for para in document.paragraphs]))[1:-1]


def extract_text_from_doc(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    content = uploaded_file.file.read()
    text = textract.process(BytesIO(content), extension='doc')
    single_line = text.replace("\n", " ").replace("\r", " ")
    return json.dumps(single_line)[1:-1]


def extract_text_from_txt(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    raw_text = uploaded_file.file.read().decode("utf-8-sig")
    single_line = raw_text.replace("\n", " ").replace("\r", " ")
    return json.dumps(single_line)[1:-1]

def extract_text_from_file(uploaded_file: UploadFile) -> str:
    filename = uploaded_file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif filename.endswith(".doc"):
        return extract_text_from_doc(uploaded_file)
    elif filename.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        raise InvalidFileTypeException("Unsupported file format. Supported formats: .pdf, .docx, .doc, .txt")