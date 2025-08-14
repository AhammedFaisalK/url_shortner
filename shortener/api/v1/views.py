from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from shortener.models import URL
from .serializers import URLCreateSerializer, URLListSerializer
import json

class URLCreateView(generics.CreateAPIView):
    """Create a new short URL"""
    queryset = URL.objects.all()
    serializer_class = URLCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if URL already exists
            original_url = serializer.validated_data['original_url']
            existing_url = URL.objects.filter(original_url=original_url, is_active=True).first()
            
            if existing_url:
                # Return existing short URL
                response_serializer = URLCreateSerializer(existing_url, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            
            # Create new short URL
            url_obj = serializer.save()
            response_serializer = URLCreateSerializer(url_obj, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class URLListView(generics.ListAPIView):
    """List all URLs with statistics"""
    queryset = URL.objects.filter(is_active=True)
    serializer_class = URLListSerializer

@api_view(['GET'])
def url_stats(request, short_code):
    """Get statistics for a specific short URL"""
    url_obj = get_object_or_404(URL, short_code=short_code, is_active=True)
    serializer = URLListSerializer(url_obj, context={'request': request})
    return Response(serializer.data)

def redirect_short_url(request, short_code):
    """Redirect short URL to original URL"""
    try:
        url_obj = get_object_or_404(URL, short_code=short_code, is_active=True)
        url_obj.increment_click_count()
        return redirect(url_obj.original_url)
    except URL.DoesNotExist:
        return HttpResponse("Short URL not found", status=404)

def custom_404(request, exception):
    """Custom 404 handler"""
    return JsonResponse({"error": "Not found", "message": "The requested resource was not found"}, status=404)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({"status": "healthy", "service": "URL Shortener"})

# Home page with API documentation
def home(request):
    """Simple API documentation"""
    if request.method == 'GET':
        api_docs = {
            "message": "URL Shortener API",
            "version": "1.0",
            "endpoints": {
                "POST /api/urls/": "Create a short URL",
                "GET /api/urls/": "List all URLs",
                "GET /api/stats/<short_code>/": "Get URL statistics",
                "GET /<short_code>/": "Redirect to original URL",
                "GET /api/health/": "Health check"
            },
            "example_request": {
                "url": "/api/urls/",
                "method": "POST",
                "body": {
                    "original_url": "https://example.com/very/long/url"
                }
            },
            "example_response": {
                "original_url": "https://example.com/very/long/url",
                "short_code": "abc123",
                "short_url": "http://127.0.0.1:8000/abc123",
                "created_at": "2024-01-01T12:00:00Z"
            }
        }
        return JsonResponse(api_docs, json_dumps_params={'indent': 2})