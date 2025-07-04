from docx import Document
import textract
from fastapi import UploadFile
from app.exception_handlers import InvalidFileTypeException
from io import BytesIO
import json
import fitz
import pytesseract
from PIL import Image
from langchain_core.messages import AIMessage, BaseMessage

def extract_text_from_pdf(uploaded_file: UploadFile) -> str:
    uploaded_file.file.seek(0)
    pdf_bytes = uploaded_file.file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = " ".join([page.get_text() for page in doc]).replace("\n", " ").replace("\r", " ")

    # Text too short, likely non-selectable or image-based, use OCR
    if len(text.strip()) < 50:
        ocr_text = []
        for page in doc:
            # Render page as an image (pixmap)
            pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # High DPI for better OCR accuracy
            img_bytes = pix.tobytes("png")
            img = Image.open(BytesIO(img_bytes))
            page_text = pytesseract.image_to_string(img, lang="eng")  # Perform OCR
            ocr_text.append(page_text.replace("\n", " ").replace("\r", " "))
        text = " ".join(ocr_text)

    doc.close()  # Close the document to free resources
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

def preprocess_llm_output(output: str) -> str:
    output = output.strip()
    if output.startswith("```json"):
        output = output[len("```json"):].strip()
    elif output.startswith("```"):
        output = output[len("```"):].strip()
    if output.endswith("```"):
        output = output[:-3].strip()
    return output

def extract_text_from_llm_output(output: AIMessage | BaseMessage | str) -> str:
    
    # Handle LangChain AIMessage or BaseMessage
    if hasattr(output, 'content') and isinstance(output.content, str):
        return output.content
    if isinstance(output, str):
        return output
        
    return str(output)