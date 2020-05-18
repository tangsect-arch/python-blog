from rest_framework import  serializers
from entries.models import Entries, Likes, PostImages
from django.contrib.auth.models import User


class entriesSerializers(serializers.ModelSerializer):
    # def get_username_from_entry_author(self,entries):
    #     username = entries.entry_author.username


    # username = serializers.SerializerMethodField(get_username_from_entry_author)
    # print(username, ' username')

    class Meta:
        model = Entries
        fields = ('id','entry_title','entry_text','liked','entry_date','entry_author','entry_images')
        #fields = '__all__'



class likesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        #fields = ('user','entries','value')
        fields = '__all__'

class postImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['entries','images']
        #fields = '__all__'



class registrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['entries','images']
        #fields = '__all__'



class entrySerializersData(serializers.ModelSerializer):
    class Meta:
        model = Entries
        fields = ['id','entry_title','entry_text','liked','entry_date','entry_author','entry_images']
        
