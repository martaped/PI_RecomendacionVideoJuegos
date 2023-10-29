from fastapi import FastAPI

import pandas as pd


app = FastAPI()
df_gfec=pd.read_parquet("Generos_fecha.parquet")

df_ustiempo=pd.read_parquet('Usuarios_tiempo.parquet')

df_ur=pd.read_parquet('func_3.parquet') 

# Endpoint para obtener el año con más horas jugadas para un género específico
@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre( genero ): 
    #Debe devolver año con mas horas jugadas para dicho género.
    #Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}
    
    generos=df_gfec[df_gfec["genres"]==genero ]
    
    # Agrupar por "release_date" y sumar la columna "time_forever"
    resultados_agrupados = generos.groupby('anio')['playtime_forever'].sum()
    # Agrupar por "release_date" y sumar la columna "time_forever"
    
    # Encontrar la fecha con el valor máximo
    max_release_date = resultados_agrupados.idxmax()
    # Mostrar el resultado
    print(f"Año de lanzamiento con más horas jugadas para {genero}: {max_release_date}")

   
    return# Endpoint para obtener el usuario con más horas jugadas y acumulación de horas por año para un género


@app.get('/UserForGenre/{genero}')
def UserForGenre( genero : str ): 
    #Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación
    # de horas jugadas por año.
    #Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
    # "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
    
    generos=df_ustiempo[df_ustiempo["genres"]==genero]
    # Agrupar por "user_id" y sumar la columna "time_forever"
    resultados_agrupados = generos.groupby('user_id')['playtime_forever'].sum()
    # buscar el maximo
    max_por_id = resultados_agrupados.idxmax()


    # Filtrar el DataFrame para contener solo las filas con 'id' igual a maximo
    df_max = generos[generos['user_id'] == max_por_id]
    print(f"Usuario con más horas jugadas para {genero} : {max_por_id}")

    # Agrupar por 'anio' y sumar la columna 'playtime_forever'
    acumulacion_horas_anio = df_max.groupby(df_max['anio'])['playtime_forever'].sum()

    # Crear una lista de acumulación de horas jugadas por año
    lista_acumulacion = acumulacion_horas_anio.to_dict()

    # Iterar a través de la lista e imprimir cada elemento en renglones
    for anio,horas in lista_acumulacion.items():
    
        print(f'Año {anio} : Horas : {horas}')

    return

# Endpoint para obtener los 3 juegos más recomendados por usuarios para un año dado
@app.get('/UsersRecommend/{año}')
def UsersRecommend( año : int ): 
    #Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 
    # (reviews.recommend = True y comentarios positivos/neutrales)
    #Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    # Filtrar las revisiones para el año dado y recomendaciones positivas/neutrales
   
    positivos = df_ur[(df_ur['anio'] == año) & (df_ur['recommend'] == True) & (df_ur['sentiment_analysis'] >0)]

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
    # Crear el formato de salida
    top_3_games = [{"Puesto " + str(i + 1): game} for i, game in enumerate(top_3_games['item_name'])]

    print(top_3_games)
    
    return

# Endpoint para obtener los 3 juegos menos recomendados por usuarios para un año dado
@app.get('/UsersNotRecommend/{año}')
def UsersNotRecommend( año : int ):
    #Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
    # (reviews.recommend = False y comentarios negativos)
    positivos = df_ur[(df_ur['anio'] == año) & (df_ur['recommend'] == False) ]

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

    # Crear el formato de salida
    top_3_games = [{"Puesto " + str(i + 1): game} for i, game in enumerate(top_3_games['item_name'])]
    
    print(top_3_games)
    
    return

# Endpoint para obtener la cantidad de registros de reseñas categorizadas con análisis de sentimiento por año
@app.get('/sentiment_analysis/{año}')

def sentiment_analysis( año : int ):
    #Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios
    # que se encuentren categorizados con un análisis de sentimiento.
    #Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}
    # Agrupar por año y contar las categorías de análisis de sentimiento
    
    sent_por_anio = df_ur.groupby('anio')['sentiment_analysis'].value_counts().unstack(fill_value=0)
   
    # Verificar si el año existe en el índice del DataFrame
    if año in sent_por_anio.index:
        # El año existe, así que puedo filtrar 
        sent_por_anio = sent_por_anio.loc[año].to_dict()
          
        print(f"Negativo : {sent_por_anio[0]} , Neutral : {sent_por_anio[1]} Positivo: {sent_por_anio[2]}")
    return
