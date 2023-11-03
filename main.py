from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd


app = FastAPI()
# Cargar los datos en cada solicitud en lugar de utilizar variables globales

df_gfec = pd.read_parquet("Generos_fecha.parquet")
df_ustiempo = pd.read_parquet("Usuarios_tiempo.parquet")
df_ur = pd.read_parquet("func_3.parquet")
df_games=pd.read_parquet("Game_recom.parquet")

# Combina las cuatro columnas en una columna de texto
df_games['combined_text'] = df_games['tag_1'] + ' ' + df_games['tag_2'] + ' ' + df_games['tag_3'] 

# Crea una instancia del vectorizador TF-IDF
tfidf_vectorizer = TfidfVectorizer()

    # Aplica el vectorizador a la columna de texto combinada
tfidf_matrix = tfidf_vectorizer.fit_transform(df_games['combined_text'])

    # Calcula la similitud del coseno en función de las características TF-IDF
similarity_matrix = cosine_similarity(tfidf_matrix)


# Endpoint para obtener el año con más horas jugadas para un género específico
@app.get('/PlayTimeGenre/{genero}/')
def PlayTimeGenre( genero : str ): 
    #Debe devolver año con mas horas jugadas para dicho género.
    #Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
    
    generos=df_gfec[df_gfec["genres"]==genero ]
    if generos.empty:
        return {'Ese genero no existe'}
     
    # Agrupar por "release_date" y sumar la columna "time_forever"
    resultados_agrupados = generos.groupby('anio')['playtime_forever'].sum()
    # Agrupar por "release_date" y sumar la columna "time_forever"
    
    # Encontrar la fecha con el valor máximo
    max_release_date = resultados_agrupados.idxmax()
    # Mostrar el resultado
    respuesta =f"Año de lanzamiento con más horas jugadas para {genero}: {max_release_date}"
    return {respuesta}

   

def UserForGenre(genero: str):
    #Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación
    # de horas jugadas por año.
    #Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
    # "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
    # Comprobar si el género es una cadena
    
    # Filtrar el DataFrame por el género dado
    generos = df_ustiempo[df_ustiempo["genres"] == genero]
   
    # Comprobar si el género existe en el DataFrame
    if generos.empty:
        return {'No hay horas jugadas para ese género '}

    # Agrupar por "user_id" y sumar la columna "playtime_forever"
    resultados_agrupados = generos.groupby('user_id')['playtime_forever'].sum()

    # Encontrar el usuario con más horas jugadas
    max_por_id = resultados_agrupados.idxmax()

    # Filtrar el DataFrame para contener solo las filas con 'user_id' igual al máximo
    df_max = generos[generos['user_id'] == max_por_id]

    # Crear una lista de acumulación de horas jugadas por año
    acumulacion_horas_anio = df_max.groupby(df_max['anio'])['playtime_forever'].sum()

    # Crear una lista de diccionarios con el año y las horas jugadas
    lista_acumulacion = [{"Año": anio, "Horas": int(horas/60)} for anio, horas in acumulacion_horas_anio.items()]

    respuesta = {
        "Usuario con más horas jugadas para {}".format(genero): max_por_id,
        "Horas jugadas": lista_acumulacion
    }

    return JSONResponse(content=respuesta)
@app.get('/UserForGenre/{genero}/')
async def get_usersForgenre(genero: str):
    return UserForGenre(genero)

def UsersRecommend(anio: int):
    positivos = df_ur[(df_ur['anio'] == anio) & (df_ur['recommend'] == True) & (df_ur['sentiment_analysis'] >= 0)]

    if positivos.empty:
        return {"No hay Recomendados para ese año"}

    recomendaciones = positivos['item_id'].value_counts().reset_index()
    recomendaciones.columns = ['item_id', 'count']
    
    recomendaciones = pd.merge(recomendaciones, df_ur[['item_id', 'item_name']], on='item_id', how='left')
    recomendaciones = recomendaciones.drop_duplicates()
    
    top_3_games = recomendaciones.sort_values(by='count', ascending=False).head(3)
    top_3_games = top_3_games.reset_index(drop=True)
    
    respuesta = [{"Puesto " + str(i + 1): game['item_name']} for i, game in top_3_games.iterrows()]

    return JSONResponse(content=respuesta)

@app.get("/UsersRecommend/{anio}")
async def get_users_recommend(anio: int):
    return UsersRecommend(anio)



def UsersNotRecommend( anio : int ):
    #Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
    # (reviews.recommend = False y comentarios negativos)
    positivos = df_ur[(df_ur['anio'] == anio) & (df_ur['recommend'] == False) & (df_ur['sentiment_analysis'] == 0)]
    if positivos.empty:
        return {"No hay No recomendados para ese año"}
    # Contar cuántas revisiones tiene cada juego
    recomendaciones = positivos['item_id'].value_counts().reset_index()
    recomendaciones.columns = ['item_id', 'count']

    # Fusionar 'recomendaciones' con 'df_ur' para obtener los nombres
    recomendaciones = pd.merge(recomendaciones, df_ur[['item_id', 'item_name']], on='item_id', how='left')
    # Realizo el merge de ambos DataFrames borro duplicados
    recomendaciones=recomendaciones.drop_duplicates()

    # Ordenar los juegos en función del número de revisiones en orden descendente
    game_recommendations = recomendaciones.sort_values(by='count', ascending=False)

    # Tomar los 3 juegos más recomendados
    top_3_games = game_recommendations.head(3)
    top_3_games = top_3_games.reset_index(drop=True)
    
    respuesta = [{"Puesto " + str(i + 1): game['item_name']} for i, game in top_3_games.iterrows()]

    return JSONResponse(content=respuesta)

@app.get("/UsersNotRecommend/{anio}")
async def get_users_notrecommend(anio: int):
    return UsersNotRecommend(anio)

# Endpoint para obtener la cantidad de registros de reseñas categorizadas con análisis de sentimiento por año
@app.get('/sentiment_analysis/{anio}')
def sentiment_analysis(anio: int):
    # Agrupar por año y contar las categorías de análisis de sentimiento
    sent_por_anio = df_ur.groupby('anio')['sentiment_analysis'].value_counts().unstack(fill_value=0)

    # Verificar si el año existe en el índice del DataFrame
    if anio in sent_por_anio.index:
        # El año existe, así que puedo filtrar
        sent_por_anio = sent_por_anio.loc[anio].to_dict()
        respuesta = {
            "Negativo": sent_por_anio.get(0, 0),
            "Neutral": sent_por_anio.get(1, 0),
            "Positivo": sent_por_anio.get(2, 0)
        }
    else:
        respuesta = {"message": f"No se encontraron datos para el año {anio}."}
    return respuesta

def recomendacion_juego( game_name : str ): 
      
    
    # Verificar si el juego esta
    juego = df_games[df_games['id'] == game_name]
    if juego.empty:
        return {"Juego ingresado NO valido"}    
    # Encuentra el índice del juego en el DataFrame
    game_index = df_games[df_games['id'] == game_name].index[0]
    # Obtén las puntuaciones de similitud para ese juego
    similar_scores = list(enumerate(similarity_matrix[game_index]))
    
    # Ordena las puntuaciones en orden descendente
    similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
    # Recupera los índices de los juegos similares
    similar_game_indices = [i[0] for i in similar_scores]
    
    # Devuelve los nombres de los juegos recomendados (los 5 primeros)
    recommended_games = df_games['app_name'].iloc[similar_game_indices[1:6]]

    # Convierte los nombres de los juegos a una lista
    recommendations_list = recommended_games.tolist()

    # Devuelve la lista de recomendaciones en formato JSON usando JSONResponse
    return JSONResponse(content={"Se recomienda ": recommendations_list})

    
# Define la ruta de la API para obtener recomendaciones
@app.get('/recommendacion/{game_id}')
async def get_recomendacion_juego(game_id: str):
    return recomendacion_juego(game_id)
   

    
