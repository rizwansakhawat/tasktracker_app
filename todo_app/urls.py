from django.urls import path
from .views import task_list , add_task , update_task , delete_task

urlpatterns = [
    path('', task_list , name="task_list"),
    path('addtask/', add_task , name="add_task"),
    path('updatetask/<int:pk>/', update_task , name="update_task"),
    path('deletetask/<int:pk>/', delete_task , name="delete_task"),
]