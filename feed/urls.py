from django.urls import path

from feed import views

app_name = 'feed'

urlpatterns = [
    path('', views.feed_index, name='feed'),
    path('posts/', views.posts, name='posts'),
    path('tickets/add/', views.create_ticket, name='create-ticket'),
    path('tickets/<int:ticket_id>/update/', views.update_ticket, name='update-ticket'),
    path('tickets/<int:ticket_id>/answer/', views.create_review_by_answer, name='create-review-by-answer'),
    path('tickets/<int:ticket_id>/delete/', views.delete_ticket, name='delete-ticket'),
    path('reviews/add/', views.create_review, name='create-review'),
    path('reviews/<int:review_id>/update/', views.update_review, name='update-review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete-review'),
    path('followings/', views.follow_user, name='follows'),
    path('followings/<int:user_id>/delete/', views.delete_follow_user, name='delete-follow'),
    path('followings/compute/', views.follow_compute_user, name='follow-compute-user'),
]
