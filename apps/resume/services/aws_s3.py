import datetime
import os
import uuid
from ..utils.resume_renderer import render_resume_html, apply_preview_blur_overlay
from ..config.aws_config import s3_client, AWS_STORAGE_BUCKET_NAME, S3_BASE_URL


def upload_html_resume(json_resume: str, theme: str) -> str:
    html_content = render_resume_html(json_resume, theme)
    preview_html_content = apply_preview_blur_overlay(html_content)

    current_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y/%m/%d")
    file_uuid = uuid.uuid4().hex
    file_name = f"resumes/{current_date}/{file_uuid}.html"
    preview_file_name = f"resumes/{current_date}/{file_uuid}_preview.html"

    temp_html_path = os.path.join("/tmp", file_name)
    temp_preview_path = os.path.join("/tmp", preview_file_name)

    os.makedirs(os.path.dirname(temp_html_path), exist_ok=True)

    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    with open(temp_preview_path, "w", encoding="utf-8") as f:
        f.write(preview_html_content)

    s3_client.upload_file(
        Filename=temp_html_path,
        Bucket=AWS_STORAGE_BUCKET_NAME,
        Key=file_name,
        ExtraArgs={"ContentType": "text/html", "ACL": "public-read"})
    s3_client.upload_file(
        Filename=temp_preview_path,
        Bucket=AWS_STORAGE_BUCKET_NAME,
        Key=preview_file_name,
        ExtraArgs={"ContentType": "text/html", "ACL": "public-read"})
    os.remove(temp_html_path)
    os.remove(temp_preview_path)
    html_url = f"{S3_BASE_URL}{file_name}"
    preview_html_url = f"{S3_BASE_URL}{preview_file_name}"
    return html_url, preview_html_url