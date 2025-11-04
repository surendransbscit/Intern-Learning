from django.urls import path
from .views import (StudentCreateListView,StudentRetriveUpdateeDestoryView,TeacherCrateListView,TeacherRetriveupdatedestoryView,
                    HobbyCraeteListView,HobbyRetriveUpdateDeleteView,CreatelistView ,Studentupdate, AdmittePatientDetailsView)


urlpatterns = [
    path('api/student/', StudentCreateListView.as_view()),
    path('api/student/<int:pk>/', StudentRetriveUpdateeDestoryView.as_view()),
    path('api/teacher/', TeacherCrateListView.as_view()),
    path('api/teacher/<int:pk>/', TeacherRetriveupdatedestoryView.as_view()),
    path('api/hobby/', HobbyCraeteListView.as_view()),
    path('api/hobby/<int:pk>/', HobbyRetriveUpdateDeleteView.as_view()),
    path('api/studentCL/', CreatelistView.as_view()),
    path('api/studentGUD/<int:pk>/', Studentupdate.as_view()),
    path('api/admittepatient/', AdmittePatientDetailsView.as_view()),
]
