from xml.dom.minidom import Comment
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view

from django.db.models   import Q

from questions.serializers import QuestionsSerializer,QuestionDetailSerializer,CommentSerializer
from .models import Comments, Questions
from utils.decorator import login_decorator

class QuestionsAPI(APIView):
#키워드로 질문의 제목 또는 본문내용을 검색하는 API 개발
    def bulid(self, qs):
        q = Q()
        title = qs.GET.get('title',None)
        content = qs.GET.get('content',None)

        if title:
            q &= Q(questions__title__icontains = title)

        if content:
            q &= Q(questions__content__icontains = content)

        return q

    def get(self, request):
        
        q = self.bulid(qs=request.GET)

        questions = Questions.objects.filter(q)
        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @login_decorator
    def post(self, request):
        data = request.data
        user = request.user
        data = {
            "title" : request.data['title'],
            "content" : request.data['content'],
            "user" : user.id
        }
        serializer = QuestionsSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class QuestiondetailAPI(APIView):
    def get(self,request,question_id):
        question = Questions.objects.filter(id = question_id)
        serializer = QuestionDetailSerializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @login_decorator
    def put(self,request,question_id):
        user = request.user
        question = get_object_or_404(Questions, id=question_id, user = user)
        serializer = QuestionDetailSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @login_decorator
    def delete(self,request,question_id):
        user = request.user
        question = get_object_or_404(Questions, id=question_id, user = user)
        question.delete()
        return Response(status=status.HTTP_200_OK)

#코멘트 달기
class CommentView(APIView):
    @login_decorator
    def post(self, request, question_id):
        data = {
            "user" : request.user.id,
            "content" : request.data['content'],
            "question" : question_id
        }
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @login_decorator
    def put(self, request, question_id):
        comment_id = request.GET.get('comment',None)
        data = {
            "user" : request.user.id,
            "content" : request.data['content'],
            "question" : question_id
        }
        comment = get_object_or_404(Comments, question = question_id ,id=comment_id)
        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @login_decorator
    def delete(self,request,question_id):
        user = request.user
        comment_id = request.GET.get('comment',None)
        comment = get_object_or_404(Comments, user=user , question = question_id ,id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_200_OK)

#질문 작성일 기준 각 월별 전체 질문 중에서 가장 좋아요가 많은 질문을 출력하는 API 개발
