from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect, get_object_or_404

from django.urls import reverse

from .models import Task, Category
from .forms import AddTaskForm, AddCategoryForm

from django.http import JsonResponse
from rest_framework.decorators import api_view

from django.http import Http404

import json

def HomeView(request):
	context = {}

	return render(request, "mainApp/home.html", context)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def dispatch(self, *args, **kwargs):
	    if self.request.user.is_authenticated:
	        return redirect('home-view')
	    return super().dispatch(*args, **kwargs)

@login_required
def TasksView(request):
	categories = Category.objects.all()

	tasks = Task.objects.order_by('-date').filter(owner_id=request.user)

	context = {'title': 'Liste des tâches', 'tasks': tasks, 'categories': categories}

	return render(request, 'mainApp/tasks.html', context)

@login_required
def TaskShowView(request, task_id):
	task = get_object_or_404(Task, id=task_id)
	if task.owner != request.user:
		raise Http404

	context = {'title': task.title, 'task': task}

	return render(request, 'mainApp/taskShow.html', context)

@login_required
def TaskAddView(request):
	#addForm = AddTaskForm()

	if request.method == 'POST':
		addForm = AddTaskForm(request.POST)

		if addForm.is_valid():
			title = addForm.cleaned_data['titre']
			category = addForm.cleaned_data['category']
			description = addForm.cleaned_data['description']

			newTask = Task(owner=request.user, title=title, category=category, description=description)
			newTask.save()

			return redirect(newTask)
	else:
		addForm = AddTaskForm()

	context = {'title': "Ajouter une Tâche", 'form': addForm}

	return render(request, 'mainApp/taskAdd.html', context)

@login_required
def TaskRemoveView(request, task_id):
	task = get_object_or_404(Task, id=task_id)
	if task.owner != request.user:
		raise Http404

	task.delete()

	return redirect('tasks-view')

@login_required
def TaskEditView(request, task_id):
	task = Task.objects.get(id=task_id)
	if task.owner != request.user:
		raise Http404
	#addForm = AddTaskForm()

	if request.method == 'POST':
		editForm = AddTaskForm(request.POST)

		if editForm.is_valid():
			title = editForm.cleaned_data['titre']
			category = editForm.cleaned_data['category']
			description = editForm.cleaned_data['description']

			task.title = title
			task.category = category
			task.description = description
			task.save()

			return redirect(task)
	else:
		editForm = AddTaskForm(initial={'titre': task.title, 'category': task.category, 'description': task.description })

	context = {'title': "Éditer une Tâche", 'form': editForm}

	return render(request, 'mainApp/taskEdit.html', context)

@login_required
def CategoryAddView(request):
	#addForm = AddTaskForm()

	if request.method == 'POST':
		addForm = AddCategoryForm(request.POST)

		if addForm.is_valid():
			name = addForm.cleaned_data['name']
			
			newCategory = Category(name=name)
			newCategory.save()

			return redirect('tasks-view')
	else:
		addForm = AddCategoryForm()

	context = {'title': "Ajouter une Catégorie", 'form': addForm}

	return render(request, 'mainApp/taskAdd.html', context)

@login_required
def CategoryRemoveView(request, category_id):
	category = get_object_or_404(Category, id=category_id)

	category.delete()

	return redirect('tasks-view')

@api_view(["GET"])
@login_required
def apiGetTasksView(request):
	tasks = Task.objects.order_by('-date').filter(owner_id=request.user)

	content = {}

	for task in tasks:
		addDict = {	"title": str(task.title),
					"category": str(task.category),
					"description": str(task.description)}

		content[str(task.id)] = addDict

	print(content)

	#content = {"tasks": "ss"}
	return JsonResponse(content)