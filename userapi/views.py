from django.shortcuts import render
#from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from rest_framework.decorators import  api_view, permission_classes
from rest_framework.permissions import  IsAuthenticated
from rest_framework.authtoken.models import  Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from entries.models import Entries, Likes, PostImages
from account.models import Account
from .serializers import  postImagesSerializers, entriesSerializers,entrySerializersData,registrationSerializers


class entryList(APIView):
    def get(self, request):
        model = Entries.objects.all()
        print(model,' model')
        serializer_class = entriesSerializersData(model,many=True)
        #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
        return Response(serializer_class.data)


class entryPost(ListAPIView):
    queryset =  Entries.objects.all().order_by('id')
    serializer_class = entriesSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('entry_title','entry_author__username','entry_tag')


class photoList(APIView):
    def get(self, request):
        images = PostImages.objects.all()
        serializers = postImagesSerializers(images,many=True)
        return Response(serializers.data)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def entry_list_view(request):
    try:
        model = Entries.objects.all()
        
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer_class = entriesSerializers(model,many=True)
    #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
    return Response(serializer_class.data)




@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def entry_list_view_item(request,id):
    try:
        model = Entries.objects.get(id=id)
        
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    serializer_class = entriesSerializers(model)
    #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
    return Response(serializer_class.data)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def entry_list_view_item_detail(request,id):
    try:
        model = Entries.objects.get(id=id)
        tags = model.entry_tag
        relatedPosts = Entries.objects.all().filter(entry_tag=tags).exclude(id=id)
        # author = model.entry_author.username
        postImages = PostImages.objects.all().filter(entries=id)
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = postImagesSerializers(postImages,many=True)
    serializer_class = entriesSerializers(model)
    serializers = entriesSerializers(relatedPosts,many=True)
    # if serializer_class.is_valid():
        #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
        # return Response(serializer_class.data)
    serializerData = serializer_class.data
    serializerData["images"] = serializer.data
    serializerData["relatedPosts"] = serializers.data
    # serializerData["entry_author"]=author
    return Response(serializerData)



@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def entry_list_update_item(request,id):
    print(request.data,' request.data update')
    try:
        model = Entries.objects.get(id=id)
        
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    user = request.user
    print()
    request.data['entry_author']= user.pk
    if model.entry_author != user:
        return Response({'response':"You are not authorised."})
    else:
        serializer_class = entriesSerializers(model,data=request.data)
        data={}
        if serializer_class.is_valid():
            serializer_class.save()
            data["success"]="Updated Successfully."
            return Response(data=data)
        #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
        return Response(serializer_class.errors)



@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
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
@permission_classes((IsAuthenticated,))
def entry_list_create_item(request):
    user = request.user
    request.data['entry_author']=user.pk
    if user.is_superuser:
        model = Entries(entry_author = user)
        serializer_class = entriesSerializers(model,data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        data={}
        data['failure']='You are not authoraised for this operation.'
        return Response(data)


@api_view(['DELETE','POST',])
@permission_classes((IsAuthenticated,))
def like_entry(request,id):
    # userId = request.user
    user = request.user#Author.objects.get(pk=userId)
    postObj = Entries.objects.get(id=id)
    if user in postObj.liked.all():
        postObj.liked.remove(user)
    else:
        postObj.liked.add(user)
    
    like, created = Likes.objects.get_or_create(user=user, entries_id=id)
    if not created:
        if like.value == 'Like':
            like.value = 'Unlike'
        else:
            like.value = 'Like'

    like.save()

    try:
        model = postObj
        author = model.entry_author.username
        postImages = PostImages.objects.all().filter(entries=id)
    except Entries.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = postImagesSerializers(postImages,many=True)

    serializer_class = entriesSerializers(model)
    # if serializer_class.is_valid():
        #pagination_class = LimitOffsetPaginationcd#PageNumberPagination
        # return Response(serializer_class.data)
    serializerData = serializer_class.data
    serializerData["images"] = serializer.data
    # serializerData["entry_author"]=author
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
        token = Token.objects.get(user = user).key
        data['token']= token
    else:
        data = serializer_class.errors
    return Response(data)