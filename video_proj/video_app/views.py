from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm,VideoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Video
from . import models
from django.db.models import Q
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)


def index(request):
    return render(request,'video_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'video_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(('videoslist'))
            else:

                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:

        return render(request, 'video_app/login.html', {})


@login_required
def showvideo(request):

    lastvideo= Video.objects.last()

    videofile= lastvideo
    #print(videofile)


    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()


    context= {'file_url': videofile,
              'form': form
              }
    return render(request, 'video_app/videos.html', context)


class VideoDetailView(DetailView):
    context_object_name = 'video_details'
    model = models.Video
    template_name = 'video_app/video_detail.html'
    #queryset = Video.objects.all()
    #template_name = 'video_app/index.html'


class VideoListView(ListView):
    model = models.Video
    paginate_by = 10  # <app>/<modelname>_list.html
    
    def get_queryset(self, *args, **kwargs):
        qs = Video.objects.all()
        print(self.request.GET)
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query) | Q(videofile__icontains=query))
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(VideoListView, self).get_context_data(*args, **kwargs)

        return context


class VideoUpdateView(UpdateView):
    fields = ("name","description")
    model = models.Video
