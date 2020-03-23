from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from mysite.parsers import ImageParser
from .models import Project
from .serializers import ProjectSerializer, ProjectCreationSerializer, ProjectImageSerializer
# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_classes = {'create': ProjectCreationSerializer,
                          'update': ProjectCreationSerializer,
                          'partial_update': ProjectCreationSerializer,
                          'image': ProjectImageSerializer}
    default_serializer_class = ProjectSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_approved=True)

    @swagger_auto_schema(method='post', operation_description="Set the image for a project.")
    @action(detail=True, methods=['post'], parser_classes=(MultiPartParser, ImageParser))
    def image(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except:
            return Response({"error": "Project Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = ProjectImageSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response({"error": "Unsupported Media Type"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProjectListCreate(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectImageView(APIView):
    parser_classes = (ImageParser,)

    @swagger_auto_schema(responses={201: "Image Uploaded", 400: "Bad Request",
                                    404: "Project Not Found", 415: "Unsupported Media Type",
                                    500: "Internal Server Error"},
                         request_body=ProjectImageSerializer)
    def post(self, request, project_id, format=None):
        try:
            project = Project.objects.get(pk=project_id)
        except:
            return Response({"error": "Project Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = ProjectImageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response({"error": "Unsupported Media Type"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

