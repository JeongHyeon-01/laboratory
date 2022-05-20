from dataclasses import field
from pyexpat import model
from rest_framework import serializers

from users.models   import Users
from questions.models import Questions,Likes,Comments

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('title','content','user')

class CommentSerializer(serializers.ModelSerializer):
    questions = serializers.ReadOnlyField()
    class Meta:
        model = Comments
        fields = ('questions','question','user','content')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields=['user','like','question']

class QuestionDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes= LikeSerializer(many=True, read_only=True)
    likes
    class Meta:
        model = Questions
        fields =['id','title','content','likes','comments']



