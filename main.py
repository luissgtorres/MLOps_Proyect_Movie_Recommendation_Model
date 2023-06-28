from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

movies_df = pd.read_csv('Datasets/Movies_limpio.csv')

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):  
    '''La función devuelve la cantidad de películas que fueron estrenadas en el mes ingresado por el usuario.'''

    mes = mes.title()
    
    ''' Convertimos la columna release_date a tipo datetime'''

    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'])

    '''Revisamos si el texto ingresado es un mes'''

    lista_mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    if mes not in lista_mes:
        return {'mensaje_error': 'El texto ingresado no es un mes'} # Devuelve este mensaje si no es un mes
    else:
        numero_mes = lista_mes.index(mes) + 1 # Pasamos el mes a número
        cantidad = 0
        for i in range(0, movies_df.shape[0]):
            x = movies_df.loc[i, 'release_date'].month
            if x == numero_mes:
                cantidad += 1
        
        return {'Mes': mes, 'Cantidad': cantidad}           



@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    '''La función devuelve la cantidad de películas que fueron estrenadas en el día de la semana ingresado.'''

    dia = dia.title()

    ''' Convertimos la columna release_date a tipo datetime'''

    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'])

    '''Revisamos si el texto ingresado es un día de la semana'''

    lista_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    if dia not in lista_dias:
        return {'mensaje_error':'El texto ingresado no es un día de la semana'}
    else:
        numero_dia = lista_dias.index(dia) # Pasamos el día a número
        cantidad = 0
        for i in range(0, movies_df.shape[0]):
            x = movies_df.loc[i, 'release_date'].weekday()
            if x == numero_dia:
                cantidad += 1
        
        return {'Dia': dia, 'Cantidad': cantidad}        
    


@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    ''' La función devuelve el año y la popularidad para la película ingresada. En el caso de películas
        con el mismo título, la función ordenará el dataframe en función de la popularidad de las películas 
        de forma descendente. En el caso donde el título se repita tomará cómo el resultado el del 
        primer valor que aparezca.'''
    
    '''Primero revisamos si el texto ingresado es un título presente en el dataframe'''

    titulo = titulo.title()

    j = 0
    for i in range(0, movies_df.shape[0]):
        if titulo in movies_df.loc[i, 'title']:
            j += 1
    if j == 0:
        return {'mensaje_error':'El texto ingresado no se encuentra en el conjunto de datos'}
    else:
        i = 0
        while titulo != movies_df.loc[i, 'title']:
            i += 1
        anio = int(movies_df.loc[i, 'release_year'])
        popularidad = movies_df.loc[i, 'popularity']
        
        return {'titulo': titulo, 'anio': anio, 'popularidad': popularidad}        
    


@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    ''' La función devuelve el voto total y el voto promedio para el título de la película ingresado.
        En el caso de películas con el mismo título, la función ordenara el dataframe en función de 
        la cantidad de votos de forma descendente. En el caso donde el título se repita tomará cómo 
        resultado el del primer valor que aparezca.'''
    
    '''Primero revisamos si el texto ingresado es un título presente en el dataframe'''

    titulo = titulo.title()

    j = 0
    for i in range(0, movies_df.shape[0]):
        if titulo in movies_df.loc[i, 'title']:
            j += 1
    if j == 0:
        return {'mensaje_error': 'El texto ingresado no se encuentra en el conjunto de datos'}
    else:
        movies_df.sort_values(by = ['vote_count'], ascending = False, inplace = True)
        i = 0
        while titulo != movies_df.loc[i, 'title']:
            i += 1
        voto_total = movies_df.loc[i, 'vote_count']
        voto_promedio = movies_df.loc[i, 'vote_average']
        if voto_total < 2000:
            return {'mensaje_error': 'La cantidad de votos de la película es menor a 2000, por lo que no se devuelve ningún valor'}
        else:
            return {'titulo': titulo,'voto_total': voto_total, 'voto_promedio': voto_promedio}



@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):

    '''La función devuelve la cantidad de filmaciones, el retorno total y el retorno promedio para el actor
        ingresado.'''

    nombre_actor = nombre_actor.title()

    ''' Importamos el cast dataset'''

    cast_df = pd.read_csv('Datasets/Cast.csv')

    '''Verificamos que el texto ingresado sea el nombre de algún actor'''

    j = 0
    for i in range(0, cast_df.shape[0]):
        if nombre_actor in cast_df.loc[i, 'name']:
            j += 1
    if j == 0:
        return {'mensaje_error': 'El texto ingresado no se encuentra en el conjunto de datos'}
    else:
        cantidad = int(cast_df[cast_df['name'] == nombre_actor]['movie_id'].count())
        lista_peliculas = list(cast_df[cast_df['name'] == nombre_actor]['movie_id'])
        retorno_total = 0
        for l in lista_peliculas:
            l = float(l)
            x = movies_df[movies_df['id'] == l]['return'].reset_index()
            retorno_total += int(x.loc[0, 'return'])
        retorno_promedio = retorno_total / cantidad  
        return {'actor': nombre_actor, 'cantidad_filmaciones': cantidad, 'retorno_total': retorno_total, 'retorno_promedio': retorno_promedio}
    


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):

    ''' La función devuelve el éxito del director ingresado a través del retorno. Además devolverá las
        películas que haya dirijido, la fecha de lanzamiento, el retorno de cada película, el costo
        y la ganancia de cada película.'''

    nombre_director = nombre_director.title()
    
    ''' Importamos el dataset crew_df del archivo Directores.csv'''

    crew_df = pd.read_csv('Datasets/Directores.csv')

    '''Verificamos que el texto ingresado sea el nombre de algún actor'''
    j = 0
    for i in range(0, crew_df.shape[0]):
        if nombre_director in crew_df.loc[i, 'name']:
            j += 1
    if j == 0:
        return {'mensaje_error': 'El texto ingresado no se encuentra en el conjunto de datos'}
    else:
        lista_peliculas = list(crew_df[(crew_df['name'] == nombre_director)]['movie_id'])
        retorno_total_director = 0
        peliculas = []
        titulo = ''
        anio = 0
        retorno_pelicula = 0
        budget_pelicula = 0
        revenue_pelicula = 0
        movie_dict = {}
        for l in lista_peliculas:
            l = float(l)
            x = movies_df[movies_df['id'] == l]['return'].reset_index()
            retorno_total_director += int(x.loc[0, 'return'])
            titulo = (movies_df[movies_df['id'] == l]['title'].reset_index()).loc[0, 'title']
            anio = int((movies_df[movies_df['id'] == l]['release_year'].reset_index()).loc[0, 'release_year'])
            retorno_pelicula = (movies_df[movies_df['id'] == l]['return'].reset_index()).loc[0, 'return']
            budget_pelicula = (movies_df[movies_df['id'] == l]['budget'].reset_index()).loc[0, 'budget']
            revenue_pelicula = (movies_df[movies_df['id'] == l]['revenue'].reset_index()).loc[0, 'revenue']
            movie_dict = {'titulo': titulo, 'anio': anio, 'retorno_pelicula': retorno_pelicula, 'budget_pelicula': budget_pelicula, 'revenue_pelicula': revenue_pelicula}
            peliculas.append(movie_dict)
        
        return {'director': nombre_director, 'retorno_total_director': retorno_total_director, 'peliculas': peliculas}
    


@app.get('/recomendacion/{titulo}')
def recomendacion(titulo: str):
    
    ''' La función devuelve una lista de 5 películas recomendadas a partir del título de película ingresado'''

    ''' Importamos el dataset'''

    model_df = pd.read_csv('Datasets/Movies_modelo.csv')

    titulo = titulo.title()

    '''Verificamos que el texto ingresado sea un título de película'''

    j = 0
    for i in range(0, model_df.shape[0]):
        if titulo in model_df.loc[i, 'title']:
            j += 1
    if j == 0:
        return {'mensaje_error': 'El texto ingresado no se encuentra en el conjunto de datos'}
    else:

        ''' Vectorizamos la columna union y se remueven las stopwords'''

        cv = TfidfVectorizer(max_features = 2000, stop_words = 'english')
        vector = cv.fit_transform(model_df['union']).toarray()
        
        ''' Se utiliza el módulo cosine_similarity de sklearn, para establecer las distancias entre los diferentes
            valores del vector creado.'''
        
        similarity = cosine_similarity(vector)

        movie_index = model_df[model_df['title'] == titulo].index[0]  # Obtenemos el índice de la película  
        distancia = similarity[movie_index] # Aplicamos la similaridad del coseno
    
        # Creamos una lista con las 5 películas recomendadas

        movies_list = sorted(list(enumerate(distancia)), reverse = True, key = lambda x: x[1])[1:6] 
        result_list = []
        for i in movies_list:
            result_list.append(model_df.iloc[i[0]].title)
    
        return {'lista recomendada': result_list}