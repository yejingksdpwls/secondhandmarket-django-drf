from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from rest_framework.generics import ListAPIView
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # 요청 받은 데이터로 serializer 인스턴스 생성
            serializer = ProductSerializer(data=request.data)

            # 유효성 검증
            if serializer.is_valid():
                # 로그인한 사용자를 author 필드에 자동으로 설정
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            # 유효성 검사 실패 시 오류 응답
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        products = Product.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10  # 기본 페이지 크기 설정
        page = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


