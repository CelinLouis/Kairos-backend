from rest_framework import serializers
from django.contrib.auth.models import User
from utilisateur.models import UtilisateurProfil
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSearializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ('id','username','password','email',)


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UtilisateurProfil
        fields = ('id','accounts','type', 'telephone', 'image')

class UtilisateurSerializers(serializers.ModelSerializer):

    profile =ProfileSerializers(source="utilisateurprofil", read_only=True)
    class Meta: 
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email','password', 'profile')
        extra_kwargs = {"password":{'write_only': True}}

        def create(self,validated_data):
            user = User.objects.create(validated_data['username'],validated_data['first_name'],validated_data['last_name'],validated_data['email'],None,validated_data['password'])
            user.set_unusable_password()
            return user