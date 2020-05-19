from rest_framework import  serializers
from entries.models import Entries, Likes, PostImages
# from django.contrib.auth.models import User
from account.models import Account


class entriesSerializers(serializers.ModelSerializer):
    
    author = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Entries
        fields = ('id','entry_title','entry_text','liked','entry_date','entry_author','entry_images','author')
        #fields = '__all__'

    def get_author(self, obj):
        return obj.entry_author.username

    



class postImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['entries','images']
        #fields = '__all__'



class registrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password','write_only':True})
    class Meta:
        model = Account
        fields = ['username','email','password','password2','first_name','last_name']
        extra_kwargs={
                    'password':{'write_only':True}
        }

    def save(self):
        user = Account(
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
        
