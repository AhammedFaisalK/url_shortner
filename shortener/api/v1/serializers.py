from rest_framework import serializers
from shortener.models import URL
import validators

class URLCreateSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = URL
        fields = ['original_url', 'short_code', 'short_url', 'created_at']
        read_only_fields = ['short_code', 'created_at']
    
    def validate_original_url(self, value):
        """Validate that the URL is properly formatted"""
        if not validators.url(value):
            raise serializers.ValidationError("Please enter a valid URL")
        return value
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/{obj.short_code}')
        return f'http://127.0.0.1:8000/{obj.short_code}'

class URLListSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = URL
        fields = ['id', 'original_url', 'short_code', 'short_url', 'created_at', 'click_count', 'is_active']
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/{obj.short_code}')
        return f'http://127.0.0.1:8000/{obj.short_code}'