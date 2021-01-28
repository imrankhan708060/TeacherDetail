from django.urls import path
from . import views


urlpatterns=[
    path('upload_teacher/',views.TeacherUploadCsvView.as_view(),name='upload-teacher'),
    path('teacher_list/',views.TeacherListView.as_view(),name='teacher-list'),
    path('teacher_detail/<pk>',views.TeacherDetailView.as_view(),name='teacher-detail'),
]