import datetime

from django.shortcuts import render, redirect
from .models import Accounts, Posts, Chats
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            Accounts.objects.filter(username=username).update(login_status='Online')
            return redirect('post')
        else:
            messages.info(request,'Invalid Username or Password')
            return redirect('/')
    else:    return render(request, 'signin.html')

def dashboard(request):
    if request.session.has_key('user'):
        user = request.session['user']
        posts = Posts.objects.filter(username=user)
        chats = Chats.objects.all()
        new_msg = False
        for chat in chats:
            if chat.receiver_username == user and chat.msg_status == "Unread":
                new_msg = True
        return render(request, 'dashboard.html', {'posts': posts, 'new_msg':new_msg})
    else: return redirect('/')

def new_post(request):
    if request.session.has_key('user'):
        if request.method == 'POST' and request.FILES['img']:
            user = request.session['user']
            title = request.POST['title']
            content = request.POST['content']
            image = request.FILES['img']
            date = datetime.datetime.utcnow()

            fss = FileSystemStorage()
            file = fss.save(image.name, image)
            file_url = fss.url(file)
            posts = Posts.objects.create(username=user, title=title, contents=content, date_posted=date, image=image)
            posts.save()
            return redirect('dashboard')

        else: return render(request, 'new_post.html')
    else: return redirect('/')

def logout(request):
    if request.session.has_key('user'):
        user = request.session['user']
        Accounts.objects.filter(username=user).update(login_status='Offline')
        auth.logout(request)
        return redirect('/')
    else: return redirect('/')

def post(request):
    if request.session.has_key('user'):
        user = request.session['user']
        posts = Posts.objects.all()

        chats = Chats.objects.all()
        new_msg = False
        for chat in chats:
            if chat.receiver_username == user and chat.msg_status == "Unread":
                new_msg = True

        return render(request, 'index.html', {'posts': posts, 'new_msg':new_msg})
    else:
        return redirect('/')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        gender = request.POST['sex']

        if cpassword != password:
            messages.info(request, "The Passwords are not the same")
        else:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'The Username has been used!!')
                return redirect('signup')
            else:
                users = Accounts.objects.create(username=username, gender=gender)
                users.save()
                user = User.objects.create_user(username=username, password=password)
                user.save()
        return redirect('/')
    else:    return render(request, 'signup.html')

def chat(request, friend):
    if request.session.has_key('user'):
        user = request.session['user']
        users = Accounts.objects.all()

        sender = user
        reciever = friend

        Chats.objects.filter(sender_username=reciever, receiver_username=sender).update(msg_status='Read')

        chats = Chats.objects.all().order_by('id')
        msgs = Chats.objects.filter(receiver_username=sender)

        owner = []
        new_msg = False
        for chat in msgs:
            if chat.msg_status == "Unread":
                new_msg = True
                owner.append(chat.sender_username)
            if chat.sender_username==reciever and chat.receiver_username==sender:
                Accounts.objects.filter(username=reciever).update(msg_status='Read')
        print(owner)



        # Chatting codes
        if request.method == 'POST':
            # print(reciever)
            msg = request.POST['message']
            date = datetime.datetime.utcnow()
            chat = Chats.objects.create(sender_username=sender, receiver_username=reciever, messages=msg, msg_date=date)
            chat.save()
            Accounts.objects.filter(username=sender).update(msg_status='Unread')

        else:  return render(request, 'chat.html', {'users': users, 'owner':owner, 'sender': sender, 'new_msg':new_msg, 'reciever': reciever, 'chats':chats})

        return render(request, 'chat.html', {'users': users, 'owner':owner, 'sender': sender, 'new_msg':new_msg, 'reciever': reciever, 'chats':chats})
    else: return redirect('/')

def delete(request, id):
    if request.session.has_key('user'):
        user = request.session['user']
        Posts.objects.filter(id=id).delete()
        return redirect('dashboard')
    else: return redirect('')