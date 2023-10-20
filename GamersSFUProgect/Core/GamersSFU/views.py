from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.views.generic import View

from django.db.models import Q

from .forms import *
from .models import *
from os import remove
import os
import json

def index(request):
    return render(request, "index.html")


# загрузка поста пользователем
class upload(View):

    def get(self, request):
        return render(
                    request, 'upload.html', 
                      { 
                          'PlaerGamePostForm' : PlaerGamePostForm, 
                          'MultiImageForm' : MultiImageForm,
                          'MultiGanreForm' : GameGanreForm,
                       })
    
    def post(self, request):

        # теги игры
        gametags = GameGanreForm(request.POST)

        # информацию об игре
        playergamepostform = PlaerGamePostForm(request.POST, request.FILES)

        # иконка игры
        # gameico = GameIcoForm(request.POST, request.FILES)

        # несколько изображений
        multiimageform = MultiImageForm(request.POST, request.FILES)
        
        # файл игры в zip
        # gamefileform = GameFileForm(request.POST, request.FILES)

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

            # потом добавлю пофигу
            # playergamepost.Developer =
            

            imgfiles = multiimageform.cleaned_data['gameimages'] # request.FILES.getlist('images')
            
            playergamepost.save()
            
            for genre in gametags.cleaned_data['Genre']:
                GameGanre.objects.create(Game=playergamepost, Genre=genre)

            for img in imgfiles:
                
                savefile = GameImage(ImageFile=img)
                savefile.save()
                
                GamePostImage.objects.create(Game=playergamepost, GameImage=savefile)
                # gamepostimage = GamePostImage(Game=playergamepost, GameImage=savefile)
                # gamepostimage.save()

            return HttpResponseRedirect('')

        else:
            print(check_form)


        #return HttpResponseRedirect('')
        return HttpResponse(f'ошибка в данных форм {check_form}')
    
# получить пост
# прим url /getpost/?post_id=4 для получения поста c id 4 например
class getpost(View):
    def get(self, request):
        try:
            p_id = request.GET['post_id']
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
# прим /delpost/?post_id=4 

def delete_post_from_post_id(request, post_id):


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

    def get(self, request):
        return render(request, 'register.html', {'RegisterForm' : RegisterForm })

    def post(self, request):
        pass

class login(View):

    def get(self, request):
        return render(request, 'login.html', {'LoginForm' : LoginFrom })

    def post(self, request):
        pass
