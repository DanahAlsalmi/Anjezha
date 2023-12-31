from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from accounts.models import *
from .models import *

# Create your views here.




def display_task_view(request: HttpRequest, task_id):
    tasks = Task.objects.all()

    if request.method == "POST":
        new_comment = Comment(task=tasks, user=request.user,
                              content=request.POST["content"])
        if 'image' in request.FILES:
            new_comment.image = request.FILES["image"]
        new_comment.save()

    return render(request, "service/display_task.html", {"tasks": tasks})
# is_supervisor = booleanfield(false)



def display_task_view(request: HttpRequest ):
    tasks = Task.objects.filter(supervisor=request.user)

    return render(request, "service/display_task.html", {"tasks": tasks })





def add_comment_view(request: HttpRequest, task_id, parent_comment_id=None):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        content = request.POST["content"]
        parent_comment = None

        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)

        new_comment = Comment.objects.create(
            task=task,
            user=request.user,
            content=content,
            parent_comment=parent_comment
        )

        if 'image' in request.FILES:
            new_comment.image = request.FILES["image"]

        new_comment.save()

    comments = Comment.objects.filter(task=task, parent_comment=None)
    comment_count = comments.count()

    return render(request, "service/comment.html", {"comments": comments, "comment_count": comment_count, "task": task})


def reply_view(request: HttpRequest, task_id, comment_id):

    task = get_object_or_404(Task, id=task_id)
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        content = request.POST["content"]
        image = request.FILES["image"] if 'image' in request.FILES else None

        add_comment_view(task, request.user, content, parent_comment=comment, image=image)

    comments = Comment.objects.filter(task=task, parent_comment=None)

    return render(request, "service/comment.html", {"comments": comments,  "task": task})
   





def add_task_view(request: HttpRequest):
    all_workers = User.objects.all()

    if request.method == 'POST':
        selected_worker_ids = request.POST.getlist('workers')

        task = Task(
            name=request.POST['name'],
            description=request.POST['description'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            address=request.POST['address'],
        )

        supervisor_id = request.user.id
        supervisor = User.objects.get(id=supervisor_id)
        task.supervisor = supervisor

        task.save()

        task.workers.set(selected_worker_ids)

        return redirect("service:display_task_view")

    return render(request, "service/add_task.html", {"all_workers": all_workers})




def delete_task_view(request: HttpRequest, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect("service:display_task_view")


def update_task_view(request: HttpRequest, task_id):
    task = Task.objects.get(id=task_id)
    all_workers = User.objects.all()

    if request.method == "POST":
        selected_worker_ids = request.POST.getlist('workers')

        task.name = request.POST['name']
        task.description = request.POST['description']
        task.start_date = request.POST['start_date']
        task.end_date = request.POST['end_date']
        task.address = request.POST['address']
        
        task.save()

        task.workers.set(selected_worker_ids)

        return redirect("service:display_task_view")
    return render(request, "service/update_task.html", {"task": task , "all_workers" : all_workers})
