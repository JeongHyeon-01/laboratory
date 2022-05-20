from django.urls import path,include
from questions.views import QuestionsAPI, QuestiondetailAPI,CommentView,LikesView, MostValueableView

urlpatterns = [
    path('posting', QuestionsAPI.as_view()),
    path('detail/<int:question_id>',QuestiondetailAPI.as_view()),
    path('comment/<int:question_id>',CommentView.as_view()),
    path('likes/<int:question_id>',LikesView.as_view()),
    path('most',MostValueableView.as_view())
]
