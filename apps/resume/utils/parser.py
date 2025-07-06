import json
import re
import PyPDF2


def parse_pdf_to_text(file_obj):
    try:
        reader = PyPDF2.PdfReader(file_obj)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error parsing PDF file: {e}")   

def clean_and_convert_to_json(text):
    try:
        return json.loads(text)
    except Exception:
        cleaned_text = re.sub(r"^```(?:json)?\s*", "", text.strip())
        cleaned_text = re.sub(r"\s*```$", "", cleaned_text)
        try:
            return json.loads(cleaned_text)
        except Exception as e:
            print("Failed to parse to json:", e)
            return {}
