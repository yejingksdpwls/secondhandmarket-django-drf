from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'nickname', 'birthday', 'gender', 'bio']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate(self, data):
        # 이메일 중복 검증
        model = get_user_model()
        if model.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("이미 사용중인 이메일입니다.")
        return data

    def create(self, validated_data):
        model = get_user_model()
        # 비밀번호는 set_password()로 암호화하여 저장
        password = validated_data.pop('password')
        user = model(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # 사용자 인증
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("사용자명 또는 비밀번호가 올바르지 않습니다.")

        # 인증된 사용자 반환
        data['user'] = user
        return data



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'nickname', 'bio']