# P_I_Recomendacion-VideoJuegos# 

Sistema de Recomendación de Videojuegos
Este es un sistema de recomendación de videojuegos que se ha implementado como una API desplegada en Render. El sistema proporciona recomendaciones de videojuegos basadas en Datos proveidos por SoyHenry.
Los archivos parquet se encuentran en este repositorio.
Aquí encontrarás una descripción general del sistema, cómo utilizarlo y una lista de las cinco principales funciones disponibles.

Descripción General
El Sistema de Recomendación de Videojuegos utiliza un conjunto de datos de juegos, revisiones de usuarios y análisis de sentimiento para ofrecer recomendaciones personalizadas. Se ha desplegado como una API en Render para que puedas acceder a sus funciones a través de solicitudes HTTP.

Cómo Usar la API
Puedes interactuar con la API utilizando este URL serviciorecome.onrender.com/docs

Funciones Disponibles
1. Juego con mayor cantidad de Horas
Información sobre en que año fue el lanzamiento del juego con mas horas jugadas para un genero determinado.

2. Ranquing de Videojuegos por Usuario por Genero de Juego

Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación
de horas jugadas por año.
Ejemplo de retorno: "Usuario con más horas jugadas para Género X" : Pedro,
    "Horas jugadas":Año: 2013, Horas: 203, Año: 2012, Horas: 100, Año: 2011, Horas: 23
    

3. Juego Más Recomendado por Usuarios

Esta función te proporciona el juego más recomendado por los usuarios en función de las revisiones positivas y el análisis de sentimiento. Es una excelente manera de descubrir un juego muy valorado por la comunidad de jugadores.

4. Juego Menos Recomendado por Usuarios

Si prefieres saber cuál es el juego menos recomendado por los usuarios, esta función te mostrará esa información. También se basa en revisiones negativas y análisis de sentimiento.

5. Análisis de Sentimiento por Año

Esta función te permite obtener información sobre el análisis de sentimiento de las revisiones de juegos para un año específico. Sabrás cuántas revisiones son negativas, neutrales o positivas para ese año.

Ejemplo de Uso
A continuación, se muestra un ejemplo de cómo utilizar la API para obtener recomendaciones de videojuegos basadas en un género específico utilizando Python y la biblioteca requests:



url = https://serviciorecome.onrender.com/docs

Conclusión
El Sistema de Recomendación de Videojuegos desplegado en Render es una herramienta útil para descubrir nuevos juegos y tomar decisiones informadas sobre tus compras. Puedes explorar diversas funciones para obtener recomendaciones personalizadas y analizar el sentimiento de las revisiones de juegos. ¡Disfruta de tu experiencia de juego!






