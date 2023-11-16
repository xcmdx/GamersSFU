



from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.html import escape
from django.db.models import Q
from .models import *
from os import remove
from .forms import *
import os
import json



def index(request):
    return render(request, "main.html")

# загрузка поста пользователем
class upload(LoginRequiredMixin, View):
    
    login_url = '/login/'

    def get(self, request):

        # проверка на разработчика
        if (not request.user.is_developer):
            return HttpResponse("недостаточно прав")
        
        return render(
                    request, 'upload.html', 
                      { 
                          'PlaerGamePostForm' : PlaerGamePostForm, 
                          'MultiImageForm' : MultiImageForm,
                          'MultiGanreForm' : GameGanreForm,
                       })
    
    def post(self, request):
        
        # проверка на разработчика
        if (not request.user.is_developer):
            return HttpResponse("недостаточно прав")
        
        # теги игры
        gametags = GameGanreForm(request.POST)

        # информацию об игре
        playergamepostform = PlaerGamePostForm(request.POST, request.FILES)

        # несколько изображений
        multiimageform = MultiImageForm(request.POST, request.FILES)
        
        check_form = (playergamepostform.is_valid(), multiimageform.is_valid())
        
        # if playergamepostform.is_valid() and gamefileform.is_valid() and multiimageform.is_valid() and gametags.is_valid() and gameico.is_valid():
        if playergamepostform.is_valid() and multiimageform.is_valid() and gametags.is_valid():

            # gamefile = gamefileform.save(commit=False)
            
            playergamepost = playergamepostform.save(commit=False)
            
            playergamepost_data = playergamepostform.cleaned_data

            gamefile = ZipFile.objects.create(GameFile=playergamepost_data['GameFile'])
            gameico  = GameIco.objects.create(ImageFile=playergamepost_data['GameIco'])
            
            playergamepost.GameFile = gamefile
            playergamepost.GameIco = gameico

            # потом добавлю 
            playergamepost.Developer = request.user
            
            imgfiles = multiimageform.cleaned_data['gameimages'] # request.FILES.getlist('images')

            playergamepost.Title = escape(playergamepost.Title)
            playergamepost.Description = escape(playergamepost.Description)

            playergamepost.save()
            
            for genre in gametags.cleaned_data['Genre']:
                GameGanre.objects.create(Game=playergamepost, Genre=genre)

            for img in imgfiles:
            
                savefile = GameImage(ImageFile=img)
                savefile.save()                
                GamePostImage.objects.create(Game=playergamepost, GameImage=savefile)

            return HttpResponseRedirect('')

        else:
            print(check_form)


        #return HttpResponseRedirect('')
        return HttpResponse(f'ошибка в данных форм {check_form}')
    
# получить пост
# прим url /getpost/?post_id=4 для получения поста c id 4 например
class getpost(View):
    def get(self, request, post_id):
        try:
            p_id = int(post_id) 
            post = Game.objects.get(id=p_id)
            filterimages = GamePostImage.objects.filter(Game = p_id )

            tags = GameGanre.objects.filter(Game = p_id)

            return render( request, 'gamepost.html', {'post' : post, 'img' : filterimages, 'tags' : tags })         

        except Exception as ex:
            return HttpResponse(f'ошибка получения {ex.args}')

# получить изображения поста
# прим url /imgsbyid/?post_id=4 для получения изображений поста c id 4 например
class get_img_from_post_id(View):

    def get(self, request):
        try:
            id = 0
            images = {'images': []}
            p_id = request.GET['post_id']
            filterimages = GamePostImage.objects.filter(Game = p_id )
            tags = GameGanre.objects.filter(Game = p_id)

            for i in filterimages:
                images['images'].append( { 'id' : str(id), 'img' : str(i.GameImage.ImageFile.url) } )

            return HttpResponse(json.dumps(images, ensure_ascii=False));   
         
        except Exception as ex:
            return HttpResponse(f'ошибка получения {ex.args}')

# удаляет пост по id  
# прим /delpost/4/ удалит пост и файлы на диске поста с id = 4
def delete_post_from_post_id(request, post_id):
    
    # проверка на разработчика
    if (not request.user.is_developer):
        return HttpResponse("недостаточно прав")
    
    try:
        id = 0
        images = {'images': []}
        p_id = int(post_id) 
        post = Game.objects.get(id=p_id)

        filterimages = GamePostImage.objects.filter(Game = p_id )
        tags = GameGanre.objects.filter(Game = p_id)

        for img in filterimages:
            
            if os.path.exists(f"./{img.GameImage.ImageFile.url}"):
                remove(f"./{img.GameImage.ImageFile.url}")

            img.delete()
        
        for tg in tags:
            tg.delete()

        gameico = post.GameIco
        postfile = post.GameFile 

        post.delete()
        
        if os.path.exists(f"./{gameico.ImageFile.url}"):
            remove(f"./{gameico.ImageFile.url}")

        if os.path.exists(f"./{postfile.GameFile.url}"):
            remove(f"./{postfile.GameFile.url}")

        postfile.delete()
        gameico.delete()

        return HttpResponse('sucsess')

    except Exception as ex:
        return HttpResponse(f'ошибка {ex}')
    
class search(View):

    def get(self, request):
        return render(request, 'search.html', {'searched' : Game.objects.all(), 'search_form' : SearchForm })

    def post(selt, request):
        _searchform = SearchForm(request.POST)

        if _searchform.is_valid():
            query = _searchform.cleaned_data['search_field']
            return render(request, 'search.html', {'searched' : Game.objects.filter(Q(Title__icontains=query)), 'search_form' : SearchForm })
        
        return render(request, 'search.html', {'searched' : Game.objects.all(), 'search_form' : SearchForm })

class register(View):

    def post(self, request):

        login_f = request.POST.get('username')

        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if (password1 == password and len(password) >= 5 and len(password) >= 5):
            
            print(login_f)
            if ( MyUsers.objects.filter(Login = login_f).count() <= 0):
                user = MyUsers(Login=login_f)
                user.set_password(password)
                user.save()
            else:
                return HttpResponse("пользователь уже есть в базе")
            return redirect("/")
        else:
            return HttpResponse("форма не валидна")

class v_login(View):

     def post(self, request):

        # login_f = LoginFrom(request.POST)
        login_f = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(Login=login_f, password=password)
        print(user)
        if (user is not None):
            login(request, user)
            return redirect("/")        
        else:
            response = redirect('/login') 
            response.set_cookie('error', 'log&pass', max_age=1)  
            return response
        
def get_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

def get_logout(request):

    if request.method == 'GET':
        logout(request)
        return render(request, 'index.html')
   