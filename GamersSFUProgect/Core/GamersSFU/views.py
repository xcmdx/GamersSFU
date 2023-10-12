from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.views.generic import View

from django.db.models import Q

from .forms import *
from .models import *

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
                          'GameFileForm' : GameFileForm,
                          'MultiImageForm' : MultiImageForm,
                          'MultiGanreForm' : GameGanreForm,
                          'GameIcoForm' : GameIcoForm,
                       })
    
    def post(self, request):

        # загружаем несколько изображений
        multiimageform = MultiImageForm(request.POST, request.FILES)
        
        # загружаем файл игры в zip
        gamefileform = GameFileForm(request.POST, request.FILES)

        # загружаем информацию об игре
        playergamepostform = PlaerGamePostForm(request.POST)
        
        if playergamepostform.is_valid():

            if gamefileform.is_valid():
                
                gamefile = gamefileform.save(commit=False)
                playergamepost = playergamepostform.save(commit=False)
                playergamepost.GameFile = gamefile

                if multiimageform.is_valid():

                    imgfiles = multiimageform.cleaned_data['gameimages'] # request.FILES.getlist('images')

                    # Проверка количества файлов
                    if len(imgfiles) <= 5:

                        for img in imgfiles:
                            
                            gamefileform.save()
                            playergamepost.save()

                            savefile = GameImage(ImageFile=img)
                            savefile.save()
                            gamepostimage = GamePostImage(Game=playergamepost, GameImage=savefile)
                            gamepostimage.save()
                        return HttpResponseRedirect('')

                    else:
                        return HttpResponse('Количество файлов превышает ограничение')
                else:
                    print('форма не валидна x3')
                    print(multiimageform.errors)
            else:
                print('форма не валидна x2')
                print(gamefileform.errors)
        else:
            
            print('форма не валидна x1')
            print(playergamepostform.errors)

        #return HttpResponseRedirect('')
        return HttpResponse('сомнительно')
    

# получить пост
# прим url /getpost/?post_id=4 для получения поста c id 4 например
class getpost(View):
    def get(self, request):
        try:
            p_id = request.GET['post_id']
            post = Game.objects.get(id=p_id)
            filterimages = GamePostImage.objects.filter(Game = p_id )
            return render(request, 'gamepost.html', {'post' : post, 'img' : filterimages})         

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

            for i in filterimages:
                images['images'].append( { 'id' : str(id), 'img' : str(i.GameImage.ImageFile.url) } )

            return HttpResponse(json.dumps(images, ensure_ascii=False));   
         
        except Exception as ex:
            return HttpResponse(f'ошибка получения {ex.args}')


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


class search(View):

    def get(self, request):
        return render(request, 'search.html', {'searched' : Game.objects.all(), 'search_form' : SearchForm })

    def post(selt, request):
        _searchform = SearchForm(request.POST)

        if _searchform.is_valid():
            query = _searchform.cleaned_data['search_field']
            return render(request, 'search.html', {'searched' : Game.objects.filter(Q(Title__icontains=query)), 'search_form' : SearchForm })
        
        return render(request, 'search.html', {'searched' : Game.objects.all(), 'search_form' : SearchForm })