from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #formulario para crear un usuario, #2 para autentificarse (iniciar session)
from django.contrib.auth.models import User #Class para crear usuario en la DataBase
from django.contrib.auth import login, logout, authenticate  #crea una cookie,
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
	return render(request, 'home.html')

def signup(request):
	if request.method == 'GET':
		return render(request, 'signup.html', {
				'form': UserCreationForm
			}) 

	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				#register user
				user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
				user.save()
				login(request, user)
				return redirect('tasks')

			except:
				return render(request, 'signup.html', {
			'form': UserCreationForm,
			'error': 'User already exists'
			}) 
		else:
			return render(request, 'signup.html', {
			'form': UserCreationForm,
			'error': 'Password do not match'
			}) 

@login_required #decorador que no permite que los usuarios pasen a menos que esten login
def tasks(request):
	tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
	return render(request, 'tasks.html', {
		'tasks': tasks
		})

@login_required
def tasks_completed(request):
	tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
	return render(request, 'tasks.html', {
		'tasks': tasks
		})

@login_required
def signout(request):
	logout(request)
	return redirect('home')


def signin(request):
	if request.method == 'GET':
		return render(request, 'signin.html', {
			'form': AuthenticationForm
			})

	else:
		user = authenticate(
			request, username=request.POST['username'], password=request.POST['password'])

		if user is None:
			return render(request, 'signin.html', {
			'form': AuthenticationForm,
			'error': 'Username or password is incorrect'
			})

		else:
			login(request, user)

			return redirect('tasks')

		return render(request, 'signin.html', {
			'form': AuthenticationForm
			})

@login_required
def create_task(request):

	if request.method == 'GET':
		return render(request, 'create_task.html', {
			'form': TaskForm
			})

	else:
		try:
			form = TaskForm(request.POST)
			new_task = form.save(commit=False)
			new_task.user = request.user #la cookie del user va en toda request
			new_task.save()

			return redirect('tasks')

		except ValueError:
			return render(request, 'create_task.html', {
				'form': TaskForm,
				'error': 'ValueError'
			})


@login_required
def task_detail(request, task_id):

	if request.method == 'GET':
		task = get_object_or_404(Task, pk=task_id, user=request.user)
		form = TaskForm(instance=task)
		return render(request, 'task_detail.html', {
			'task': task,
			'form': form
		})

	else:
		try:
			task = get_object_or_404(Task, pk=task_id, user=request.user)
			form = TaskForm(request.POST, instance=task)
			form.save()
			return redirect('tasks')

		except ValueError:
			return render(request, 'task_detail.html', {
				'task': task,
				'form': form,
				'error': 'Error updating task'
			}) 
		
@login_required
def complete_task(request, task_id):
	task = get_object_or_404(Task, pk=task_id, user=request.user)
	if request.method == 'POST':
		task.date_completed = timezone.now()
		task.save()
		return redirect('tasks')

@login_required
def delete_task(request, task_id):
	task = get_object_or_404(Task, pk=task_id, user=request.user)
	if request.method == 'POST':
		task.delete()
		return redirect('tasks')
