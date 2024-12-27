from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'content', 'image', 'price', 'author']
        read_only_fields = ['author']  # 로그인한 사용자만 author로 자동 저장되도록 설정

    def validate_price(self, value):
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError("가격은 반드시 유효한 숫자여야 합니다.")

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'content', 'price', 'image', 'see_count', 'created_at', 'updated_at']
