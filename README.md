# laboratory

<h3>ERD</h3>
<img width="980" alt="image" src="https://user-images.githubusercontent.com/89664413/169546124-b5a30884-2d14-4ce4-9d99-6114e2dd6819.png">

<h3>적용 기술</h3>
Python, Django, DRF, sqlite, Jt, Bcrypt

<h3>API 명세서</h3>
참조 : https://app.getpostman.com/join-team?invite_code=b993f9f629b1d238bc79c192c1bd7670&target_code=993a6c331efd3f890a08ef2c24d9ceb6
<h4>회원가입 로그인</h4>
POST :8000/users/signin. :로그인
POST :8000//users/signup  :회원가입
<h4>question</h4>
GET :8000/question/posting : 전체 질문 (쿼리 스트링으로 title 및 content 검색 가능 ex: /question/posting?title=1번&content=안녕하세요)
POST :8000/question/posting : 질문등록
<h4>questionDetail</h4>
GET :8000/question/detail/<int:question_id> : 질문 상세보기
PUT :8000/question/detail/<int:question_id> : 질문 내용 수정
DEL :8000/question/detail/<int:question_id> : 질문 삭제
<h4>Comment</h4>
POST :8000/question/comment/<int:question_id> : 코멘트 등록
PUT :8000/question/comment/<int:question_id> : 코멘트 수정
DEL :8000/question/comment/<int:question_id> : 코멘트 삭제
<h4>Like</h4>
POST :8000/question/likes/<int:question_id> : 좋아요 (한번더 보낸다면 좋아요 취소)
<h4>MostValueAble_Month</h4>
GET :8000/question/most : 쿼리스트링으로 month 정보를 전달 한다면 해당 월에 좋아요 수가 가장많은 질문의 상세정보를 보여준다.

