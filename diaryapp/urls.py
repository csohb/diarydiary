from django.urls import path
from diaryapp import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.diary_home),
    path('shop/',views.diary_shop),
    path('detail/',views.diary_detail),
    path('mydiary/',views.myDiary),
    path('record/',views.myDiaryRecord),
    path('record_ok',views.myDiaryRecordOk),
    path('mydiary_detail/',views.myDiaryDetatil),
    path('login/',views.login),
    path('login_ok',views.login_ok),
    path('delete/',views.mydiaryDelete),
    path('delete_ok',views.mydiaryDeleteOK),
    path('update/',views.myDiaryUpdate),
    path('update_ok',views.myDiaryUpdateOK),
    path('heart/',views.myDiaryHeart),
    path('logout',views.logout),
    path('signup/',views.signup),

]