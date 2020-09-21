from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Like
from .forms import PostForm

def new(request):
    return render(request, 'posts/new.html')

def create(request):
    if request.method == 'POST': # method가 post일때
        form = PostForm(request.POST, request.FILES) # form 에 PostForm 할당
        if form.is_valid(): # form 유효성 검증
            form.save(user= request.user) # 저장
            return redirect('posts:main') # 다시 main으로
    else:
        form = PostForm() # 빈 form 열기
    return render(request, 'posts/new.html',{'form' :form})

#  @login_required
# def create(request):
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save(user = request.user)
#             return redirect('posts:main')
#     else:
#         form = PostForm()
#     return render(request, 'posts/new.html', {'form': form})

def main(request):
    posts=Post.objects.all().order_by('-created_at')
    return render(request, 'posts/main.html', {'posts':posts})

def show(request, id):
    post = Post.objects.get(pk=id)
    post.view_count += 1 
    post.save()
    all_comments=post.comments.all().order_by('-created_at')
    return render(request, 'posts/show.html', {'post':post, 'comments':all_comments})
    
def update(request, id):
    post=get_object_or_404(Post, pk=id)
    if request.method =="POST":
        post.title=request.POST.get('title')
        post.content=request.POST.get('content')
        post.image = request.FILES.get('image')
        post.save()
        return redirect('posts:show', post.id)
    return render(request,'posts/update.html',{'post':post})

def delete(request, id):
    post = get_object_or_404(Post, pk=id) 
    post.delete()
    return redirect('posts:main')

def create_comment(request, post_id):
    if request.method =="POST":
        post=get_object_or_404(Post,pk=post_id)
        current_user=request.user
        comment_content=request.POST.get('content')
        Comment.objects.create(content=comment_content, user=current_user, post=post)
    return redirect('posts:show', post.pk)

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.user in post.like_user_set.all():
        post.like_user_set.remove(request.user)
    else:
        post.like_user_set.add(request.user)

    if request.GET.get('redirect_to') == 'show':
        return redirect('posts:show', post_id)
    else:
        return redirect('posts:main')

@login_required
def like_list(request):
    likes = Like.objects.filter(user=request.user)
    return render(request,'posts/like_list.html',{'likes': likes})