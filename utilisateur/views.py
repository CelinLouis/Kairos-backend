from rest_framework import viewsets
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from utilisateur.serializers import ProfileSerializers, UtilisateurSerializers , UserSearializer
from utilisateur.models import UtilisateurProfil
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CreateUserAPI(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSearializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })

class LogOutAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try :
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UtilisateurAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(username=request.user)
        user_data = UtilisateurSerializers(user).data
        return Response(user_data)

class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]
  
    def get(self, request):
        try:
            profile = UtilisateurProfil.objects.get(accounts=request.user)
            profile_data = ProfileSerializers(profile).data
        except UtilisateurProfil.DoesNotExist:
            return  Response({"User doesn't have profile"},status=status.HTTP_404_NOT_FOUND)
        return Response(profile_data)
    
# get list off all user
class getUtilisateurAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UtilisateurSerializers
