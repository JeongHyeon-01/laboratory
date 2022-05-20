from rest_framework          import status
from rest_framework.response import Response
from rest_framework.views    import APIView
from rest_framework.generics import get_object_or_404

from django.db.models        import Q, Sum

from questions.serializers   import LikeSerializer, QuestionsSerializer,QuestionDetailSerializer,CommentSerializer
from questions.models        import Comments, Questions, Likes

from utils.decorator import login_decorator

class QuestionsAPI(APIView):
    def bulid(self, qs):
        q = Q()

        title = qs.get('title',None)
        content = qs.get('content',None)

        if title:
            q &= Q(title__icontains = title)
        if content:
            q &= Q(content__icontains = content)

        return q

    def get(self, request):
        
        q = self.bulid(qs=request.GET)

        questions = Questions.objects.filter(q)
        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @login_decorator
    def post(self, request):
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
    def get(self,request, question_id):
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
        comment = get_object_or_404(Comments, question = question_id ,id=comment_id, user = request.user)
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

#좋아요 기능 구현
class LikesView(APIView):
    @login_decorator
    def post(self,request,question_id):
        if not Likes.objects.filter(user = request.user, question_id = question_id):
            data = {
                "user" : request.user.id,
                "like" : True,
                "question" : question_id
            }
            serializer = LikeSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, stauts=status.HTTP_200_OK)
        else:
            instance = get_object_or_404(Likes, question=question_id, user=request.user)
            data = {"user" : request.user.id,"like": False if instance.like == True else True, "question" : question_id}
            serializer = LikeSerializer(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
#질문 작성일 기준 각 월별 전체 질문 중에서 가장 좋아요가 많은 질문을 출력하는 API 개발
class MostValueableView(APIView):
    def get(self,request):
        month = request.GET.get('month', None)
        q = Q(created_at__month=month)

        sum = Questions.objects.annotate(like_count = Sum('likes__like')).filter(q).order_by('-like_count')
        serializer = QuestionDetailSerializer(sum[0])
        return Response(serializer.data, status=status.HTTP_200_OK)        

