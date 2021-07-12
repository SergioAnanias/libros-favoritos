from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('newbook', views.newbook),
    path('<int:id>/like', views.like),
    path('<int:id>/dislike', views.dislike),
    path('<int:id>', views.book),
    path('<int:id>/update', views.update),
    path('<int:id>/delete', views.delete)
]
