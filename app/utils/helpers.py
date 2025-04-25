from docx import Document
import textract
from pdfminer.high_level import extract_text
from fastapi import UploadFile
from app.exception_handlers import InvalidFileTypeException
from io import BytesIO
import json
import tempfile
import gzip
import base64

def extract_text_from_pdf(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.file.read())
        tmp.flush()
        raw_text = extract_text(tmp.name)
    return json.dumps(raw_text)[1:-1]


def extract_text_from_docx(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    content = uploaded_file.file.read()
    document = Document(BytesIO(content))
    return json.dumps("\n".join([para.text for para in document.paragraphs]))[1:-1]


def extract_text_from_doc(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    content = uploaded_file.file.read()
    text = textract.process(BytesIO(content), extension='doc')
    return text.decode('utf-8')


def extract_text_from_txt(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    return uploaded_file.file.read().decode("utf-8")


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

def compress_string(input_string):
    compressed = gzip.compress(input_string.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')

def decompress_string(encoded_string):
    compressed = base64.b64decode(encoded_string.encode('utf-8'))
    return gzip.decompress(compressed).decode('utf-8')