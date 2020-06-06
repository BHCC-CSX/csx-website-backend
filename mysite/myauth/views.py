from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
from django.db import transaction
from mysite.views import CustomAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        print('we here')

        user = User.objects.get(username=request.data.get('username'))
        if not user.is_valid:
            print('user not valid')
            return Response(data={"error": 'Please activate your account before attempting to log in.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserList(CustomAPIView):
    """
    API Endpoint to list users.
    METHODS: GET
    """
    permission_classes = {"get": [permissions.IsAuthenticated, ],
                          "post": [permissions.AllowAny, ],}
    name_schema = openapi.Schema(type="integer")
    request_schema = openapi.Schema(type="array", items=name_schema)

    @swagger_auto_schema(responses={200: UserSerializer(many=True), 500: "Internal Server Error"})
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: UserNamesSerializer(many=True),
                                    400: "Bad Request",
                                    404: "Resource Not Found",
                                    500: "Internal Server Error"}, request_body=request_schema,
                         operation_id="users_bulk_ids_to_names")
    def post(self, request, format=None):
        ids = set(request.data)  # Remove duplicates
        names = User.objects.filter(pk__in=ids)
        data = {name.id: UserNamesSerializer(name).data for name in names}  # Build the response dict
        if len(names) == len(ids):
            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    """
    API Endpoint to register users.
    METHODS: POST
    """
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses={200: "Success", 500: "Internal Server Error",
                                    400: "Bad Request", 403: "Bad Request", 201: "Created"})
    def post(self, request, format=None):
        if request.auth is None:
            data = request.data
            data['is_active'] = False
            serializer = UserRegisterSerializer(data=data)
            print(serializer)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()
                        print(user)
                        
                        current_site = get_current_site(request)
                        mail_subject = "Activate your CSX account."
                        message = render_to_string('acc_active_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user)
                        })
                        to_email = user.email
                        email = EmailMessage(mail_subject, message, to=[to_email])
                        email.send()

                        serialized_user = UserSerializer(user)
                        refresh = RefreshToken.for_user(user)
                        data = {'user':serialized_user.data,'refresh':str(refresh), 'access':str(refresh.access_token)}
                        return Response(data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

class UserActivate(APIView):
    """
    API Endpoint to activate a user's account.
    METHODS: POST
    """

    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(responses={200: "Success", 500: "Internal Server Error",
                                    400: "Bad Request", 403: "Bad Request", 201: "Created"})
    def post(self, request, format=None):
        try:
            uid = force_text(urlsafe_base64_decode(request.data['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user and account_activation_token.check_token(user, request.data['token']):
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserDetail(APIView):
    """
    API Endpoint to get the details for a user.
    METHODS: GET
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    @swagger_auto_schema(responses={200: UserSerializer(), 404: "User Not Found", 400: "Bad Request",
                                    500: "Internal Server Error"})
    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Groups(APIView):
    """
    API Endpoint to get groups.
    METHODS: GET
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    @swagger_auto_schema(responses={200: GroupSerializer(many=True), 500: "Internal Server Error",
                                    400: "Bad Request"})
    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

