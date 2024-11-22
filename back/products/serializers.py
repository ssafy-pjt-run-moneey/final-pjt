# products/serializers.py
from rest_framework import serializers
from .models import Product, Option, ProductMark, ProductComment

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_is_marked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ProductMark.objects.filter(user=request.user, product=obj).exists()
        return False

class ProductCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ProductComment
        fields = ['id', 'content', 'created_date', 'updated_date', 'username']
        read_only_fields = ['user']