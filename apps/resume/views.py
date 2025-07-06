import uuid, os, requests
from datetime import datetime
from django.http import HttpResponse


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from apps.resume.services.aws_s3 import upload_html_resume

from .utils.parser import clean_and_convert_to_json, parse_pdf_to_text
from .services.resume_enhancer import enhance_resume_content
from .utils.resume_renderer import render_resume_html
from .utils.html_to_pdf import generate_pdf_from_html
from .config.aws_config import s3_client, AWS_STORAGE_BUCKET_NAME, S3_BASE_URL

class ProfileView(APIView):    
    def get(self, request):
        if not request.user or request.user.is_anonymous:
            return Response({
                "error": "User not authenticated", 
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            "username": request.user.username,
            "email": request.user.email,
        })
    
    def put(self, request):
        if not request.user or request.user.is_anonymous:
            return Response({
                "error": "User not authenticated"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            data = request.data
            if not data:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            
            # Extract relevant fields
            old_password = data.get("old_password")
            new_password = data.get("new_password")
            new_username = data.get("username")
            new_email = data.get("email")
            
            # Validate password requirements
            if old_password and not (new_password or new_username):
                return Response({
                    "error": "Old password provided but no new password or username specified"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Handle password-protected updates (new password or username)
            if new_password or new_username:
                if not old_password:
                    return Response({
                        "error": "Old password required to update password or username"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not request.user.check_password(old_password):
                    return Response({
                        "error": "Incorrect old password"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Update password if provided
                if new_password:
                    request.user.set_password(new_password)
                
                # Update username if provided
                if new_username:
                    request.user.username = new_username
            
            # Handle email update (no password required)
            if new_email:
                request.user.email = new_email
            
            request.user.save()
            
            return Response({
                "message": "User information updated successfully"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ParseResumeView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def post(self, request):
        resume_text = request.data.get("resume_text", "")
        if resume_text:
            resume_text = resume_text.strip()
            
        resume_file = request.data.get("resume_file")
        
        if not resume_text and resume_file:
            try:
                resume_text = parse_pdf_to_text(resume_file)
            except Exception as e:
                return Response({
                    "error": f"Failed to parse file: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

        if not resume_text:
            return Response({
                "error": "Please provide resume content or upload a resume file"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "parsed_text": resume_text
        }, status=status.HTTP_200_OK)

class EnhanceResumeView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def post(self, request):
        resume_text = request.data.get("resume_text", "")
        if resume_text:
            resume_text = resume_text.strip()
            
        resume_file = request.data.get("resume_file")
        customized_info = request.data.get("customized_info", "")

        if not resume_text and resume_file:
            try:
                resume_text = parse_pdf_to_text(resume_file)
            except Exception as e:
                return Response({
                    "error": f"Failed to parse file: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)

        if not resume_text:
            return Response({
                "error": "Please provide resume content or upload a resume file"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            modified_resume = enhance_resume_content(resume_text, customized_info)
            cleaned_resume = clean_and_convert_to_json(modified_resume)

            return Response({
                "json_resume": cleaned_resume
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error processing resume: {str(e)}")
            return Response({
                "error": f"Failed to process resume: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateHTMLView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def post(self, request):
        json_resume = request.data.get("json_resume", {})
        theme = request.data.get("theme", "engineering")
        
        if not json_resume:
            return Response({
                "error": "Please provide a valid JSON resume"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            html_url, preview_url = upload_html_resume(json_resume, theme)
            return Response({
                "html_url": html_url,
                "preview_url": preview_url
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
class DownloadPDFView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        html_url = request.data.get("html_url", "").strip()
        if not html_url:
            return Response({
                "error": "Please provide a valid HTML URL"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = requests.get(html_url)
            if response.status_code != 200:
                return Response({
                    "error": "Failed to fetch HTML content from the provided URL"
                }, status=status.HTTP_400_BAD_REQUEST)
            html_content = response.text

            current_date = datetime.now().strftime("%Y/%m/%d")
            pdf_key = f"resumes/{current_date}/{uuid.uuid4().hex}.pdf"
            temp_pdf_path = os.path.join("/tmp", pdf_key)
            generate_pdf_from_html(html_content, temp_pdf_path)

            s3_client.upload_file(
                Filename=temp_pdf_path,
                Bucket=AWS_STORAGE_BUCKET_NAME,
                Key=pdf_key,
                ExtraArgs={"ContentType": "application/pdf", "ACL": "public-read"}
            )
            os.remove(temp_pdf_path)
            pdf_url = f"{S3_BASE_URL}{pdf_key}"
            return Response({
                "pdf_url": pdf_url
            }, status=status.HTTP_200_OK)

            

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                