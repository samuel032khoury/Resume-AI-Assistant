import json
import re
import PyPDF2


def parse_resume_file(file_obj):
    try:
        reader = PyPDF2.PdfReader(file_obj)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error parsing PDF file: {e}")
    

def parse_modified_resume_to_json(modified_resume_text):
    try:
        return json.loads(modified_resume_text)
    except Exception:
        cleaned_text = re.sub(r"^```(?:json)?\s*", "", modified_resume_text.strip())
        cleaned_text = re.sub(r"\s*```$", "", cleaned_text)
        try:
            return json.loads(cleaned_text)
        except Exception as e:
            print("Failed to parse to json:", e)
            return {}
