from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm


def community_page(request):
    posts = Post.objects.all()
    return render(request, 'community/community_page.html', {'posts': posts})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            return redirect('community_page')
    else:
        form = PostForm()
    return render(request, 'community/create_post.html', {'form': form})
