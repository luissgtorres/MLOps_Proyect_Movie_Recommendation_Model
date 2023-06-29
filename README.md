<h1 align="center"> Proyecto MLOps: Modelo de Recomendación de Películas </h1>

## Descripción del proyecto

Modelo de recomendación de películas desplegado en Render utilizando FastAPI. Se realizó ETL, EDA y modelado del Dataset utilizando Python como lenguaje de programación.

El modelo devuelve 5 películas recomendadas a partir del título de una película. La API también cuenta con funciones para conocer la cantidad de películas estrenadas, la popularidad de las películas y el éxito de los actores y directores.

## Tecnologías utilizadas

- Para realizar el proyecto se utilizó Python como lenguaje de programación.
- Para el ETL se utilizaron pandas y numpy.
- Para el EDA se utilizaron matplotlib y seaborn.
- Para el modelado se utilizó scikit-learn junto con nltk para el procesamiento de lenguaje natural.
- Se utilizó FastAPI para crear la API.
- Se utilizó Render para el despliegue de la API.

## Acceso a la API

Mediante el siguiente [**link**](https://primer-proyecto-individual-mlops.onrender.com/docs) se puede acceder a la API desplegada en Render.

## Funcionalidades del proyect

![Estrucutra_API_PI_1](https://github.com/luissgtorres/MLOps_Proyect_Movie_Recommendation_Model/assets/113273616/c12938a7-9236-4935-97c2-6e39482b80a9)

La API cuenta con 7 funciones:
  - **/cantidad_filmaciones_mes/{mes}**: Devuelve la cantidad de total películas estrenadas en el mes que se indique. El mes debe estar en español.
  - **/cantidad_filmaciones_dia/{dia}**: Devuelve la cantidad total de películas estrenadas en el día que se indique. El día de la semana debe estar en español.
  - **/score_titulo/{titulo}**: Devuelve el año y la popularidad de la película ingresada.
  - **/votos_titulo/{titulo}**: Devuelve el voto total y el voto promedio para la película ingresada.
  - **/get_actor/{nombre_actor}**: Devuelve la cantidad de filmaciones, el retorno total y el retorno promedio del actor ingresado.
  - **/get_director/{nombre_director}**: Devuelve el éxito del director ingresado medido a través del retorno. Además, devulve las películas que haya dirigido, la fecha de lanzamiento, retorno, costo y ganancia de cada película.
  - **/recomendacion/{titulo}**: Devuelve una lista de 5 películas recomendadas a partir del título de película ingresado.

Se puede observar la API en funcionamiento a través del siguiente [**video**]().

## Estructura del repositorio

El repositorio cuenta con las siguientes carpetas y archivos:

- Datasets: donde se encuentran los datasets obtenidos luego de realizar el ETL y el dataset utilizado para el modelado.
- Gráficos: donde se encuentran los gráficos más resaltantes del EDA.
- Notebooks: donde se encuentran los notebooks del ETL, EDA y modelado.
- main.py: el archivo de python utilizado por render para desplegar la API, es donde se encuentran todo el código de las funciones.


## Desarrollo del proyecto

### ETL

El ETL fue realizado utilizando Python como lenguaje de programación y los módulos Pandas y Numpy.
Se contaba con un dataset de películas y otro de creditos, ambos datasets estaban sucios, llenos de valores nulos, datos erroneos, datos duplicados, columnas con datos anidados. Fue necesario realizar la limpieza pertinente para poder utilizar el dataset en las funciones de la API, el EDA y modelado. El proceso de limpieza fue el siguiente:

- Dependiendo de las columnas, los valores nulos fueron reemplazados por 0, cadenas vacías o fueron eliminados. Se eliminaron los datos duplicados y los valores anidados fueron desanidados dejando los datos más relevantes en la columna de origen.
- Se realizó un join de los 2 datasets para poder trabajar todos los datos en un solo dataset para el modelado.
- Se crearon 2 datasets adicionales: uno con los datos de los actores y otro con los datos de los directores de las películas.
- Se eliminaron las columnas que no eran necesarias y se crearon otras que si eran necesarias para las funciones de la API, el EDA y modelado.
- Finalmente, fueron creados los archivos .csv con los datasets limpios.

### EDA

El EDA fue realizado utilizando Python como lenguaje de programación y los módulos matplotlib y seaborn para realizar las gráficas

Entre las gráficas más importantes realizadas se encuentran:

- Un heatmap para observar el valor numérico de la correlación de las columnas.
- Un pairplot que ayudó a dilusidar la correlación a través de los gráficos de dispersión.
- Un gráfico de barras horizontales con la cantidad de películas por género.
- Se realizarón 2 nubes de palabras para observar las palabras más comunes en los títulos y los nombres de actores más comunes, es decir, los que hayan actuado en más películas.
- Por último, se realizó un gráfico de líneas para ver la cantidad de películas estrenadas de forma anual.

Al final de cada gráfico se presenta una conclusión con las observaciones realizadas. Todas las gráficas mencionadas se encuentran en la carpeta Gráficos.

### Modelado

El modelo fue realizado utilizando Python como lenguaje de programación junto con los módulos scikit-learn y nltk.

- Antes de aplicar los módulos para realizar el modelo, se realizó una limpieza adicional de los datos. Esto con la finalidad de reducirlos lo más posible y poder desplegar el modelo en Render. Esta limpieza consistió en eliminar los datos que se consideran menos importantes para el modelo. 
- Luego de la limpieza, se comenzó a realizar el procesamiento de lenguaje natural. Para ello se utilizó el PorterStemmer y el word_tokenize del módulo nltk. Este procesamiento se aplicó en una columna que era la unión del título, resumen, actores, directores, genero y compañía de producción.
- Se creó un nuevo dataset solo con las columnas necesarias para el modelo, el cuál sería utilizado en la función de recomendación de la API.
- Por último se realizó el modelamiento de los datos utilizando el TfidfVectorizer para crear los vectores con los datos y se usó cosine_similarity para determinar la distancia entre los vectores. Ambas funciones de la librería scikit-learn.
  
## Autor

Luis Torres luisgtorres16@gmail.com
