from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    FileListCreateView, FileDetailView, DownloadFileView,
    GenerateSpecialLinkView, SpecialLinkView
)

urlpatterns = [
    path('', csrf_exempt(FileListCreateView.as_view()), name='file-list'),
    path('<int:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('<int:pk>/download/', DownloadFileView.as_view(), name='file-download'),
    path('<int:pk>/generate-link/', GenerateSpecialLinkView.as_view(), name='generate-link'),
    path('special/<uuid:uuid>/', SpecialLinkView.as_view(), name='special-link'),
]