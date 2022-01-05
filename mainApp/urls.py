from django.contrib.auth import views as auth_views
from django.urls import path


from . import views

urlpatterns = [
    path('', views.HomeView, name="home-view"),
    #path('accounts/login', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/signup', views.SignUpView.as_view(), name="sign-up-view"),
    path('tasks/', views.TasksView, name="tasks-view"),
    path('tasks/task/<int:task_id>', views.TaskShowView, name="task-show-view"),
    path('tasks/add', views.TaskAddView, name="task-add-view"),
    path('tasks/task/<int:task_id>/edit', views.TaskEditView, name="task-edit-view"),
    path('tasks/task/<int:task_id>/delete', views.TaskRemoveView, name="task-remove-view"),
    path('tasks/category/add', views.CategoryAddView, name="category-add-view"),
    path('tasks/category/<int:category_id>/delete', views.CategoryRemoveView, name="category-remove-view"),
    path('api/', views.apiGetTasksView, name="api-task-show"),
]