from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import custom_login
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('register_student/', views.register_student, name='register_student'),
    path('login/', custom_login, name='login'),
    path('profile/', views.profile, name='profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('view-feedback/', views.user_feedback, name='view_feedback'),
    
    path('update-profile/', views.update_profile, name='update_profile'),
    
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('redirect-url/', views.redirect_url, name='redirect-url'),
    
    
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/unread/', views.unread_notifications, name='get_unread_notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('send-notification/', views.send_notification, name='send_notification'),
    
    path('notifications/unread_count/', views.get_unread_notification_count, name='unread_notification_count'),
    
    path('discussion/', views.discussion_board_list, name='discussion_board_list'),
    path('board/<int:pk>/', views.discussion_board_detail, name='discussion_board_detail'),
    path('board/<int:board_pk>/post/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('board/<int:board_pk>/new_post/', views.new_post, name='new_post'),
    
    path('chat/', views.chat, name='chat'),
    
    
    path('upload_result/', views.upload_result, name='upload_result'),
    path('student_results/<str:student_id>/', views.student_results, name='student_results'),
    path('download_results/<str:student_id>/', views.download_results, name='download_results'),
    
    path('hostel-form/', views.hostel_form, name='hostel_form'),
    path('hostel/', views.hostel, name='hostel'),
    
    path('forms/', views.forms, name='forms'),

    path('search/', views.search, name='search'), 

    path('level/', views.select_level, name='select_level'),
    path('register_courses/100lv/', views.register_courses, {'level': '100lv'}, name='register_courses_100lv'),
    path('register_courses/200lv/', views.register_courses, {'level': '200lv'}, name='register_courses_200lv'),
    path('register_courses/300lv/', views.register_courses, {'level': '300lv'}, name='register_courses_300lv'),
    path('summary/', views.registration_summary, name='registration_summary'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)