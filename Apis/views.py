from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import mixins, permissions, generics
from rest_framework.response import Response
from rest_framework.reverse import reverse


from django.contrib.auth.models import User
from .models import Post
from .serializers import PostSerializer, UserSerializer


# Create your views here.


# ------------function based view-------------------

# @csrf_exempt
# @api_view(['GET', 'POST'])
# def post_list_create(request, format=None):

#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serialzer = PostSerializer(posts, many=True)
#         if serialzer is not None :
#             return JsonResponse(serialzer.data, safe=False, status=200)
#         else:
#             return JsonResponse({'message' : 'No posts Yet'}, status=404)
#     elif request.method == 'POST':
#         data = request.data
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         else:
#             return JsonResponse(serializer.errors, status=400)
        

# @api_view(['GET', 'PUT', 'DELETE'])
# def single_post(request, pk, format=None):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return JsonResponse({"message" : "Database error"}, status=500)

#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         if serializer is not None:
#             return JsonResponse(serializer.data, safe=False)
#         else:
#             return JsonResponse({"message" : "the post you looked for doesnt exist"}, status=404)
    
#     elif request.method == 'PUT':
#         data = request.data
#         post = PostSerializer(post, data=data)
#         if post.is_valid():
#             post.save()
#             return JsonResponse(post.validated_data, status=200)    
#         else:
#             return JsonResponse(serializer.errors , status=500)
        
#     elif request.method == 'DELETE':
#         confirm = input("are you sure? (y/n)")
#         if confirm == 'y':
#             post.delete()
#             return JsonResponse({"message" : "post was deleted"})
#         else:
#             return JsonResponse({"message" : "post was not deleted"})




# ------------class based view-------------------
        
# class DetailPost(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serialzer = PostSerializer(posts, many=True)
#         if serialzer is not None :
#             return JsonResponse(serialzer.data, safe=False, status=200)
#         else:
#             return JsonResponse({'message' : 'No posts Yet'}, status=404)

#     def post(self, request, format=None):
#         data = request.data
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         else:
#             return JsonResponse(serializer.errors, status=400)

# class SinglePost(APIView):

#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             return JsonResponse({"message" : "Database error"}, status=500)

#     def get(self, request, pk, format=None):
#             post = self.get_object(pk)
#             serializer = PostSerializer(post)
#             if serializer is not None:
#                 return JsonResponse(serializer.data, safe=False)
#             else:
#                 return JsonResponse({"message" : "the post you looked for doesnt exist"}, status=404)

#     def put(self, request, pk, format=None):
#         post = self.get_object(pk)
#         data = request.data
#         serializer = PostSerializer(post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         else:
#             return JsonResponse(serializer.errors, status=400)

#     def delete(self, request, pk, format=None):
#         post = self.get_object(pk)
#         confirm = input("are you sure? (y/n)")
#         if confirm == 'y':
#             post.delete()
#             return JsonResponse({"message" : "post was deleted"})
#         else:
#             return JsonResponse({"message" : "post was not deleted"})
        

# ------------Generic view-------------------

# class DetailPost(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class SinglePost(mixins.RetrieveModelMixin,
#                  mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#                  generics.GenericAPIView):
    
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    

# ------------Django magic view-------------------

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users' : reverse('user-list', request=request, format=format),
        'posts' : reverse('post-list', request=request, format=format)
    })

class IsOwnerOrReadOnly(permissions.BasePermission):

    #read permissions allowed to anyone
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #write permissions for only the users
        return obj.owner == request.user

class DetailPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SinglePost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetriveUserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer