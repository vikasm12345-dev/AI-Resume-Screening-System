"""
📄 Resume Parser Module
Extracts text from PDF and DOCX files
"""

import PyPDF2
import docx
import io


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text content from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        uploaded_file.seek(0)  # Reset file pointer
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_text_from_docx(uploaded_file) -> str:
    """Extract text content from a DOCX file."""
    try:
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        uploaded_file.seek(0)  # Reset file pointer
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"


def extract_text_from_txt(uploaded_file) -> str:
    """Extract text content from a TXT file."""
    try:
        text = uploaded_file.read().decode("utf-8")
        uploaded_file.seek(0)
        return text.strip()
    except Exception as e:
        return f"Error reading TXT: {str(e)}"


def parse_resume(uploaded_file) -> str:
    """
    Parse resume based on file type and return extracted text.
    Supports PDF, DOCX, and TXT formats.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    elif filename.endswith('.txt'):
        return extract_text_from_txt(uploaded_file)
    else:
        return "Unsupported file format. Please upload PDF, DOCX, or TXT."