from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


class AccountAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 요청 데이터
        password = request.data.get("password")

        if not password:
            return Response({"error": "비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 기존 패스워드 검증
        if not request.user.check_password(password):
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.user.delete()
            return Response({'message':"회원탈퇴가 완료되었습니다."}, status=status.HTTP_202_ACCEPTED)

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
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, username):
        if request.user.is_authenticated:
            if request.user.username != username:
                return Response({"error": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
            User = get_user_model()
            user = User.objects.get(username=username)
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordChangeAPIView(APIView):
    def put(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 요청 데이터
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        # 기존 패스워드 검증
        if not request.user.check_password(old_password):
            return Response({"error": "기존 패스워드가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 패스워드와 기존 패스워드 비교
        if old_password == new_password:
            return Response({"error": "기존 패스워드와 동일한 패스워드로 변경할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 패스워드 규칙 검증
        try:
            validate_password(new_password, user=request.user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # 패스워드 업데이트
        request.user.set_password(new_password)
        request.user.save()

        return Response({"message": "패스워드가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
