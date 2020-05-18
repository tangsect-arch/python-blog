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



class postImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['entries','images']
        #fields = '__all__'



class registrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password','write_only':True})
    class Meta:
        model = User
        fields = ['username','email','password','password2','first_name','last_name']
        extra_kwargs={
                    'password':{'write_only':True}
        }

    def save(self):
        user = User(
                    email= self.validated_data['email'],
                    username= self.validated_data['username'],
            )
        password= self.validated_data['password']
        password2= self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'passwords should be a match'})
        user.set_password(password)
        user.save()
        return user


class entrySerializersData(serializers.ModelSerializer):
    class Meta:
        model = Entries
        fields = ['id','entry_title','entry_text','liked','entry_date','entry_author','entry_images']
        
