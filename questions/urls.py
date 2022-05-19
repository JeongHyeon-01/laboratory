from django.urls import path,include
from questions.views import QuestionsAPI, QuestiondetailAPI,CommentView

urlpatterns = [
    path('posting', QuestionsAPI.as_view()),
    path('detail/<int:question_id>',QuestiondetailAPI.as_view()),
    path('comment/<int:question_id>',CommentView.as_view())
]
