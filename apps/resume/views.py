from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .services.parser import parse_modified_resume_to_json, parse_resume_file
from .services.resume_enhancer import enhance_resume_content

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
                resume_text = parse_resume_file(resume_file)
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
                resume_text = parse_resume_file(resume_file)
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
            cleaned_resume = parse_modified_resume_to_json(modified_resume)

            return Response({
                "modified_resume": cleaned_resume
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error processing resume: {str(e)}")
            return Response({
                "error": f"Failed to process resume: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)