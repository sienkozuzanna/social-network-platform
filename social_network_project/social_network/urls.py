from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/download_comments/', views.download_comments, name='download_comments'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/', views.my_profile_view, name='my_profile'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('search-users/', views.search_users, name='search_users'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('add_post/', views.add_post_view, name='add_post'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('post/<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'),name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),
]
