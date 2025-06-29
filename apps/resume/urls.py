from django.urls import path
from . import views

from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    path('profile/', ensure_csrf_cookie(views.ProfileView.as_view()), name='profile'),
    path('parse-resume/', views.ParseResumeView.as_view(), name='parse-resume'),
    path('enhance-resume/', views.EnhanceResumeView.as_view(), name='enhance-resume'),
    path('generate-html/', views.GenerateHTMLView.as_view(), name='generate-html'),
]