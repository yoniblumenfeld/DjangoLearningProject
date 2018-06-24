# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import generic
from django.shortcuts import render,redirect,get_object_or_404
from . import models
from django.core.urlresolvers import reverse_lazy,reverse
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.models import User

# Create your views here.

class UserFormView(View):
    from_class = UserForm
    template_name='music/registration_form.html'
    #display a blank form
    def get(self,request):
        form = self.from_class(None)
        return render(request,self.template_name,{'form':form})

    #process form data
    def post(self,request):
        form = self.from_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #take data from form and transfers it to db object - without commiting db!
            #cleaned (normalized) data
            username = form.cleaned_data['username'] #get username from form
            password = form.cleaned_data['password'] #get password from form
            email = form.cleaned_data['email'] #get email from form
            user = User.objects.create(email=email,username=username,password=password)
            user.set_password(password) #set user password right in db - (passwords dont get saved as pure text)
            user.save() #commit db if user doesnt already exists
            user = authenticate(username=str(user.username),password=str(password))
            if not(user is None): #check if user does exists
                if user.is_active: #check if user isnt disabled or banned
                    login(request,user)
                    return redirect('music:index')
            else:
                return redirect('https://www.youtube.com')

        return render(request,self.template_name,{'form':form,'error_message':form.errors})

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = "all_albums"
    def get_queryset(self):
        return models.Album.objects.all()

class DetailView(generic.DetailView):
    model = models.Album
    template_name = 'music/details.html'

class AlbumCreate(CreateView):
    model = models.Album
    fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
    model = models.Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
    model = models.Album
    success_url = reverse_lazy('music:index')


def index(request):
    all_albums = models.Album.objects.all()
    context = {
        'all_albums':all_albums,
    }
    return render(request,'music/index.html',context)

def detail(request,pk):
    """try:
        specific_album = models.Album.objects.get(pk=album_id)
    except models.Album.DoesNotExist:
        raise Http404("Album does not exist!")# equivalent operation on the next line of code"""
    specific_album=get_object_or_404(models.Album,pk=pk)
    specific_album_matrix=get_object_fields_value_matrix(specific_album) # not using dict for keeping list in certain order
    #index 0 represents field, index 1 represents value
    context = {'specific_album':specific_album,'specific_album_matrix':specific_album_matrix}
    return render(request,'music/details.html',context)

def favorite(request,pk):
    specific_album = get_object_or_404(models.Album, pk=pk)
    specific_album_matrix=get_object_fields_value_matrix(specific_album) # not using dict for keeping list in certain order
    try:
        selected_song=specific_album.song_set.get(pk=request.POST['song'])

    except (KeyError,models.Song.DoesNotExist):
        return render(request,'music/details.html',{
            'specific_album':specific_album,
            'error_message':"you did not select a valid song!"
        ,'specific_album_matrix':specific_album_matrix})
    else:
        if not(selected_song.is_favorite == True):
            selected_song.is_favorite=True
            selected_song.save()
            return render(request,'music/details.html',{'specific_album':specific_album,'specific_album_matrix':specific_album_matrix})
        else:
            selected_song.is_favorite=False
            selected_song.save()
            return render(request,'music/details.html',{'specific_album':specific_album,'specific_album_matrix':specific_album_matrix})


###[HELPER FUNCTIONS]####
def get_object_fields_list(obj):
    #recieves specific db object
    #returns a list of its fields
    obj = str(obj.__doc__)
    return obj[obj.find("(")+1:obj.rfind(")")].split(",")

def get_object_fields_value_matrix(obj):
    fields = get_object_fields_list(obj)
    matrix=[]
    for field in fields:
        matrix.append([field,obj.serializable_value(field.strip())])
    return matrix #returns a matrix consisting of 2 elements arrays, in which the first element is a field and the second is its value


######[TEST VIEWS]#######

