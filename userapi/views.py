from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from entries.models import Entries, Likes, PostImages
from .serializers import  postImagesSerializers, entriesSerializers,entrySerializersData,registrationSerializers
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from rest_framework.decorators import  api_view

class entryList(APIView):
    def get(self, request):
        model = Entries.objects.all()
        print(model,' model')
        serializer_class = entriesSerializers(model,many=True)
        #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
        return Response(serializer_class.data)


# class entryPost(viewsets.ModelViewSet):
#     print('bbbbbbbbbbbbbbbbbbbb')
#     qs =  Entries.objects.all()
#     serializer_class = entriesSerializers(qs)


class photoList(APIView):
    def get(self, request):
        images = PostImages.objects.all()
        serializers = postImagesSerializers(images,many=True)
        return Response(serializers.data)



@api_view(['GET',])
def entry_list_view(request):
    try:
        model = Entries.objects.all()
        
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer_class = entriesSerializers(model,many=True)
    #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
    return Response(serializer_class.data)




@api_view(['GET',])
def entry_list_view_item(request,id):
    try:
        model = Entries.objects.get(id=id)
        
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer_class = entriesSerializers(model)
    #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
    return Response(serializer_class.data)


@api_view(['GET',])
def entry_list_view_item_detail(request,id):
    try:
        model = Entries.objects.get(id=id)
        author = model.entry_author.username
        postImages = PostImages.objects.all().filter(entries=id)
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = postImagesSerializers(postImages,many=True)
    serializer_class = entrySerializersData(model)
    # if serializer_class.is_valid():
        #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
        # return Response(serializer_class.data)
    serializerData = serializer_class.data
    serializerData["images"] = serializer.data
    serializerData["entry_author"]=author
    return Response(serializerData)



@api_view(['PUT',])
def entry_list_update_item(request,id):
    try:
        model = Entries.objects.get(id=id)
        
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer_class = entriesSerializers(model,data=request.data)
    data={}
    if serializer_class.is_valid():
        serializer_class.save()
        data["success"]="Updated Successfully."
        return Response(data=data)
    #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
    return Response(serializer_class.data)



@api_view(['DELETE',])
def entry_list_delete_item(request,id):
    try:
        model = Entries.objects.get(id=id)
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    operation = model.delete()
    data={}
    if operation:
        data["success"]="Deleted successfully."
    else:
        data["failure"]="Something went wrong."
    return Response(data = data)



@api_view(['POST',])
def entry_list_create_item(request):
    user = User.objects.get(pk=1)
    model = Entries(entry_author = user)
    serializer_class = entriesSerializers(model,data=request.data)
    if serializer_class.is_valid():
        serializer_class.save()
        return Response(serializer_class.data, status=status.HTTP_201_CREATED)
    return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE','POST',])
def like_entry(request):
    userId = request.POST.get('user')
    user = User.objects.get(pk=userId)
    postId = request.POST.get('postId')
    postObj = Entries.objects.get(id=postId)
    if user in postObj.liked.all():
        postObj.liked.remove(user)
    else:
        postObj.liked.add(user)
    
    like, created = Likes.objects.get_or_create(user=user, entries_id=postId)
    if not created:
        if like.value == 'Like':
            like.value = 'Unlike'
        else:
            like.value = 'Like'

    like.save()

    try:
        model = postObj
        author = model.entry_author.username
        postImages = PostImages.objects.all().filter(entries=postId)
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = postImagesSerializers(postImages,many=True)
    serializer_class = entrySerializersData(model)
    # if serializer_class.is_valid():
        #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
        # return Response(serializer_class.data)
    serializerData = serializer_class.data
    serializerData["images"] = serializer.data
    serializerData["entry_author"]=author
    return Response(serializerData)


@api_view(['POST',])
def create_user(request):
    # model = User
    data={}
    serializer_class = registrationSerializers(data=request.data)
    if serializer_class.is_valid():
        user = serializer_class.save()
        data['success']="User registration successful."
        data['username']=user.username
        data['email']=user.email
    else:
        data = serializer_class.errors
    return Response(data)