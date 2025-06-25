def generate_resume_prompt(user_input, customized_info):
    prompt = f"""
    You are a professional resume optimization expert. Transform the provided resume according to these guidelines:

    OPTIMIZATION REQUIREMENTS:
    1. Apply STAR methodology (Situation, Task, Action, Result) to all experience descriptions
    2. Quantify achievements with specific metrics (e.g., "increased performance by 50%", "managed team of 12")
    3. Use strong action verbs (Developed, Optimized, Spearheaded, Implemented, Led, Architected)
    4. Ensure ATS-friendly formatting and keyword optimization
    5. Maintain professional tone and industry-relevant terminology

    OUTPUT FORMAT:
    Return the optimized resume as a valid JSON following the JSON Resume standard:

    {{
    "basics": {{
        "name": "Full Name",
        "email": "email@example.com",
        "phone": "phone number",
        "location": {{"city": "City", "region": "State/Province", "countryCode": "US"}},
        "url": "portfolio/website",
        "summary": "Professional summary with key achievements"
    }},
    "work": [{{
        "name": "Company Name",
        "position": "Job Title",
        "startDate": "YYYY-MM",
        "endDate": "YYYY-MM",
        "summary": "Brief role overview",
        "highlights": [
        "STAR-formatted achievement with quantified results",
        "Another achievement demonstrating impact and value"
        ]
    }}],
    "education": [{{
        "institution": "University/School Name",
        "area": "Field of Study",
        "studyType": "Degree Type",
        "startDate": "YYYY-MM",
        "endDate": "YYYY-MM",
        "gpa": "GPA if relevant"
    }}],
    "skills": [{{
        "name": "Category (e.g., Programming Languages)",
        "keywords": ["skill1", "skill2", "skill3"]
    }}],
    "projects": [{{
        "name": "Project Name",
        "description": "Brief description with technologies used",
        "highlights": ["Key achievement or metric"]
    }}]
    }}

    ORIGINAL RESUME:
    {user_input}

    CUSTOMIZATION REQUIREMENTS:
    {customized_info}

    Please optimize the resume content while preserving accuracy and ensuring all claims are truthful. Focus on impact, results, and professional growth.
    """

    return prompt
