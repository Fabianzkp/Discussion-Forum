from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Topic, Comment
from django import forms

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Edit Comment')

class TopicForm(forms.Form):
    title = forms.CharField(max_length=200, label='Topic Title')
    content = forms.CharField(widget=forms.Textarea, label='Content')
    category = forms.CharField(max_length=50, label='Category', initial='General')

def register(request):
    # Handles user registration and auto-login
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('topic_list')
    else:
        form = UserCreationForm()
    return render(request, 'discussion/register.html', {'form': form})

@login_required
def topic_list(request):
    # Displays topics with optional category filter and handles topic creation
    category = request.GET.get('category')
    topics = Topic.objects.filter(category=category) if category else Topic.objects.all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            Topic.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                category=form.cleaned_data['category'],
                creator=request.user
            )
            return redirect('topic_list')
    else:
        form = TopicForm()
    return render(request, 'discussion/topic_list.html', {'topics': topics, 'form': form})

@login_required
def topic_detail(request, pk):
    # Displays topic details and comments, handles comment creation
    topic = get_object_or_404(Topic, pk=pk)
    comments = Comment.objects.filter(topic=topic)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(content=content, author=request.user, topic=topic)
        return redirect('topic_detail', pk=pk)
    return render(request, 'discussion/topic_detail.html', {'topic': topic, 'comments': comments})

@staff_member_required
def delete_topic(request, pk):
    # Deletes a topic (admin only)
    topic = get_object_or_404(Topic, pk=pk)
    topic.delete()
    return redirect('topic_list')

@staff_member_required
def delete_comment(request, pk):
    # Deletes a comment (admin only)
    comment = get_object_or_404(Comment, pk=pk)
    topic_pk = comment.topic.pk
    comment.delete()
    return redirect('topic_detail', pk=topic_pk)

@login_required
def edit_comment(request, pk):
    # Allows the comment author to edit their comment
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect('topic_detail', pk=comment.topic.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.content = form.cleaned_data['content']
            comment.save()
            return redirect('topic_detail', pk=comment.topic.pk)
    else:
        form = CommentForm(initial={'content': comment.content})
    return render(request, 'discussion/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def user_delete_comment(request, pk):
    # Allows the comment author to delete their comment
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return redirect('topic_detail', pk=comment.topic.pk)
    topic_pk = comment.topic.pk
    comment.delete()
    return redirect('topic_detail', pk=topic_pk)

@login_required
def edit_topic(request, pk):
    # Allows the topic creator to edit their topic
    topic = get_object_or_404(Topic, pk=pk)
    if topic.creator != request.user:
        return redirect('topic_list')
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic.title = form.cleaned_data['title']
            topic.content = form.cleaned_data['content']
            topic.category = form.cleaned_data['category']
            topic.save()
            return redirect('topic_detail', pk=pk)
    else:
        form = TopicForm(initial={
            'title': topic.title,
            'content': topic.content,
            'category': topic.category
        })
    return render(request, 'discussion/edit_topic.html', {'form': form, 'topic': topic})

@login_required
def user_delete_topic(request, pk):
    # Allows the topic creator to delete their topic
    topic = get_object_or_404(Topic, pk=pk)
    if topic.creator != request.user:
        return redirect('topic_list')
    topic.delete()
    return redirect('topic_list')