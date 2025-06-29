import os, json, subprocess
from django.conf import settings


THEME_PATHS = {
    'flat': 'jsonresume-theme-flat',
    'kendall': 'jsonresume-theme-kendall',
    'macchiato': 'jsonresume-theme-macchiato',
    'relaxed': 'jsonresume-theme-relaxed',
    'stackoverflow': 'jsonresume-theme-stackoverflow',
}

def generate_html_from_json_resume(json_resume: dict, theme: str = 'flat') -> str:
    temp_json = os.path.join(settings.BASE_DIR, 'temp_resume.json')
    with open(temp_json, 'w', encoding="utf-8") as f:
        json.dump(json_resume, f, ensure_ascii=False, indent=2)
    temp_html = os.path.join(settings.BASE_DIR, 'temp_resume.html')
    theme_path = THEME_PATHS.get(theme, THEME_PATHS['flat'])

    cmd = [
        "resume", "export", temp_html,
        "--resume", temp_json,
        "--theme", theme_path,
        "--format", "html"
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception(f"resume CLI error: {result.stderr.decode()}")
    with open(temp_html, 'r', encoding="utf-8") as f:
        html_content = f.read()
    os.remove(temp_json)
    os.remove(temp_html)
    return html_content

def generate_preview_html(html_content):
    preview_html = f"""
    <html>
    <head>
        <style>
            .blur-overlay {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                backdrop-filter: blur(3px);
                background-color: rgba(255, 255, 255, 0.6);
                z-index: 999;
            }}
        </style>
    </head>
    <body>
        {html_content}
        <div class="blur-overlay"></div>
    </body>
    </html>
    """
    return preview_html