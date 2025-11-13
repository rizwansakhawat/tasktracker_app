from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib.auth.views import LogoutView


# Create your views here.


@login_required
def task_list(request):
    if request.user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user=request.user)
    
    return render(request, 'todo_app/tasks_list.html',{'tasks':tasks})



@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
        return render(request , 'todo_app/add_task.html' , {'form':form})
    

@login_required
def update_task(request , pk):
    task = get_object_or_404(Task , pk=pk)
    if request.user != task.user and not request.user.is_staff:
        return redirect('task_list')
    form = TaskForm(request.POST or None , instance=task)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    
    return render(request , 'todo_app/update_task.html' , {'form':form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user == task.user or request.user.is_staff:
        task.delete()

    return redirect('task_list')
    
    

