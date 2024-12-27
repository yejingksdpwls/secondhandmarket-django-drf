from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            context = {
                "message" : "로그인 성공",
                "refresh" : str(refresh),
                "access" : str(access)
            }

            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                refresh_token = request.data.get("refresh_token")
                if not refresh_token:
                    return Response({"error": "정상적으로 로그인이 되어있지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

                # Refresh 토큰을 무효화 (블랙리스트에 추가)
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({"message": "로그아웃이 완료되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"error": "로그아웃에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    def get(self, request, username):
        if request.user.is_authenticated:
            try:
                User = get_user_model()
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "해당 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
