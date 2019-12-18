from django.urls import path

from . import views

app_name = 'lecture'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.course_search, name='course_search'),
    path('create/', views.course_create, name='course_create'),
    path('<int:course_id>/', views.course_index, name='course_index'),
    path('<int:course_id>/join/', views.course_join, name='course_join'),
    path('<int:course_id>/update/', views.course_update, name='course_update'),

    path('<int:course_id>/notice/', views.notice_index, name='notice_index'),
    path('<int:course_id>/notice/create/', views.notice_create, name='notice_create'),
    path('<int:course_id>/notice/<int:notice_id>/', views.notice_read, name='notice_read'),
    path('<int:course_id>/notice/<int:notice_id>/update/', views.notice_update, name='notice_update'),
    path('<int:course_id>/notice/<int:notice_id>/delete/', views.notice_delete, name='notice_delete'),

    path('<int:course_id>/notice/<int:notice_id>/comment/create', views.notice_comment_create,
         name='notice_comment_create'),
    path('<int:course_id>/notice/<int:notice_id>/comment/<int:comment_id>/update', views.notice_comment_update,
         name='notice_comment_update'),
    path('<int:course_id>/notice/<int:notice_id>/comment/<int:comment_id>/delete', views.notice_comment_delete,
         name='notice_comment_delete'),

]
