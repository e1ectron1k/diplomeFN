import os
import uuid
from django.conf import settings
from django.http import FileResponse, Http404
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, permissions, status, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import File
from .serializers import FileSerializer
from apps.users.models import User

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class FileListCreateView(generics.ListCreateAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        print(f"User: {request.user}, authenticated: {request.user.is_authenticated}")

    def get_queryset(self):
        if self.request.user.is_admin:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                return File.objects.filter(owner_id=user_id)
        return File.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        file_obj = self.request.FILES.get('file')
        comment = self.request.data.get('comment', '')
        if not file_obj:
            raise serializers.ValidationError({'file': 'No file uploaded'})
        serializer.save(
            owner=self.request.user,
            original_name=file_obj.name,
            size=file_obj.size,
            file=file_obj,
            comment=comment
        )

class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return File.objects.all()
        return File.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

class DownloadFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            file_obj = File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404
        if file_obj.owner != request.user and not request.user.is_admin:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        file_obj.last_downloaded_at = timezone.now()
        file_obj.save(update_fields=['last_downloaded_at'])
        response = FileResponse(file_obj.file, as_attachment=True, filename=file_obj.original_name)
        return response

class GenerateSpecialLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            file_obj = File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404
        if file_obj.owner != request.user and not request.user.is_admin:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        if not file_obj.special_link_uuid:
            file_obj.special_link_uuid = uuid.uuid4()
            file_obj.save()
        return Response({'special_link': request.build_absolute_uri(f'/api/files/special/{file_obj.special_link_uuid}/')})

class SpecialLinkView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uuid):
        try:
            file_obj = File.objects.get(special_link_uuid=uuid)
        except File.DoesNotExist:
            raise Http404
        file_obj.last_downloaded_at = timezone.now()
        file_obj.save(update_fields=['last_downloaded_at'])
        response = FileResponse(file_obj.file, as_attachment=True, filename=file_obj.original_name)
        return response