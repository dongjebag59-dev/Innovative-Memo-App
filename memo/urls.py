from django.urls import path
from . import views

app_name = "memo"

urlpatterns = [
    path("", views.memo_list, name="list"),
    path("create/", views.memo_create, name="create"),
    path("<int:memo_id>/", views.memo_detail, name="detail"),
    path("<int:memo_id>/edit/", views.memo_update, name="update"),
    path("<int:memo_id>/delete/", views.memo_delete, name="delete"),
]
