from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import update_session_auth_hash
from .models import Post, Profile, Follow, Comment, Like
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, PostForm, ProfileEditForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib import messages
from lxml import etree

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
            user.save()

            profile_picture = 'static/images/default-profile.png'
            Profile.objects.create(user=user, profile_picture=profile_picture)

            current_site = get_current_site(request)
            subject = "Activate Your Account"
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            send_mail(subject, message, 'no-reply@yourdomain.com', [email])

            messages.success(request, f"Account created for {username}! Check your email to activate your account.")
            return redirect('home')
        else:
            messages.error(request, "There were errors in your form. Please fix them.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "The activation link is invalid or expired.")
        return redirect('home')


from django.contrib.messages import get_messages

def login_view(request):
    storage = get_messages(request)
    for _ in storage:
        pass

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('home')
            else:
                messages.error(request, "Your account is not activated. Check your email.")
        else:
            messages.error(request, "Invalid username or password.")
        return redirect('login')

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('home')


def home_view(request):
    query = request.GET.get('search', '')

    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower=request.user)
        followed_users = [follow.followed for follow in following_users]


        if not followed_users:
            no_following_message = "You are not following anyone. Search for users to follow."
            no_posts_message = None
            posts = None
        else:
            posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
            if not posts.exists():
                no_posts_message = "The users you follow have no posts."
            else:
                no_posts_message = None
            no_following_message = None

            for post in posts:
                post.is_liked = post.is_liked_by(request.user)
    else:
        posts = None
        no_following_message = None
        no_posts_message = None
        login_message = "You are not logged in. Please <a href='{% url 'login' %}'>log in</a> or <a href='{% url 'register' %}'>register</a> to get started."

    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.none()

    paginator = Paginator(posts, 10) if posts else None
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) if paginator else None

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'query': query,
        'users': users,
        'no_following_message': no_following_message,
        'no_posts_message': no_posts_message,
        'login_message': login_message if not request.user.is_authenticated else None,
    })

def my_profile_view(request):
    profile = request.user.profile
    posts = Post.objects.filter(author=request.user)
    followers = Follow.objects.filter(followed=request.user)
    following = Follow.objects.filter(follower=request.user)

    return render(request, 'profile/profile.html', {
        'profile': profile,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_my_profile': True,
        'messages': messages.get_messages(request)
    })

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    if request.method == "POST" and 'content' in request.POST:
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        if post_id and content:
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, author=request.user.profile, content=content)
            return redirect('profile_view', username=username)

    posts = Post.objects.filter(author=user).order_by('-created_at')
    for post in posts:
        post.is_liked = post.is_liked_by(request.user)
    followers = Follow.objects.filter(followed=user)
    following = Follow.objects.filter(follower=user)

    is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

    return render(request, 'profile/profile.html', {
        'profile': profile,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following,
        'is_my_profile': request.user == user,
    })


@login_required
def edit_profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('my_profile')

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully!")
            return redirect('my_profile')
    else:
        profile_form = ProfileEditForm(instance=profile)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'profile/edit_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def add_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been added successfully!")
            return redirect('my_profile')
    else:
        form = PostForm()

    return render(request, 'posts/add_post.html', {'form': form})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('my_profile')
    return render(request, 'posts/delete_post.html', {'post': post})

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('my_profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_detail.html', {'form': form, 'post': post})


@login_required
def follow_user(request, username):
    followed_user = get_object_or_404(User, username=username)

    if request.user != followed_user:
        Follow.objects.get_or_create(follower=request.user, followed=followed_user)

    return redirect('user_profile', username=username)

@login_required
def unfollow_user(request, username):
    followed_user = get_object_or_404(User, username=username)

    if request.user != followed_user:
        follow_instance = Follow.objects.filter(follower=request.user, followed=followed_user).first()
        if follow_instance:
            follow_instance.delete()

    return redirect('user_profile', username=username)

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    user_profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, author=user_profile, content=content)
            return redirect('post_detail', post_id=post.id)

    comments = post.comments.all()
    return render(request, 'posts/edit_post.html', {'post': post, 'comments': comments})

@login_required
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user.profile:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    comment.delete()
    return redirect('post_detail', post_id=comment.post.id)


@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, author=request.user.profile, content=content)
            return redirect('post_detail', post_id=post.id)

    comments = post.comments.all()
    return render(request, 'posts/edit_post.html', {'post': post, 'comments': comments})


@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True

        return JsonResponse({
            'is_liked': is_liked,
            'likes_count': post.likes_count()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user.profile, content=content)
    return redirect('home')


@login_required
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user.profile:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    post_author_username = comment.post.author.username

    comment.delete()
    return redirect('user_profile', username=post_author_username)

@login_required
def search_users(request):
    query = request.GET.get('search', '')
    if query:
        users = User.objects.filter(username__icontains=query)[:10]
        results = [
            {
                'username': user.username,
                'profile_picture': user.profile.profile_picture.url if user.profile.profile_picture else '/static/images/default-profile.png',
            }
            for user in users
        ]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

@login_required
def download_comments(request):
    user_profile = request.user.profile
    comments = Comment.objects.filter(author=user_profile).order_by('-created_at')

    if not comments.exists():
        return HttpResponse("<h1>No comments found for the user.</h1>", content_type="text/html")

    root = etree.Element("comments")
    for comment in comments:
        comment_element = etree.SubElement(root, "comment", id=str(comment.id))
        etree.SubElement(comment_element, "content").text = comment.content
        etree.SubElement(comment_element, "post_id").text = str(comment.post.id)
        etree.SubElement(comment_element, "created_at").text = str(comment.created_at)

    xslt_path = "static/xsl/my_comments.xsl"
    try:
        with open(xslt_path, "r") as xslt_file:
            xslt_root = etree.XML(xslt_file.read().encode('utf-8'))
    except FileNotFoundError:
        return HttpResponse("<h1>XSL file not found.</h1>", content_type="text/html")

    transform = etree.XSLT(xslt_root)
    result = transform(root)

    return HttpResponse(str(result), content_type="text/html")