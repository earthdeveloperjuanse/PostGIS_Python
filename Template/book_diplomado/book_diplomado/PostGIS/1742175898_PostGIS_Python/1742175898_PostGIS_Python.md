# Bases de datos espaciales: PostGIS y su integración con Python

```{admonition} Guía para el docente
:class: danger
 - El título  debe corresponder al nombre de la unidad sin incluir numeración. 

```
✅ **Ejemplo correcto:** Introducción a las principales librerías: NumPy, Pandas, rasterio, GDAL y geopandas  
❌ **Ejemplo incorrecto:** 1.2.1. Introducción a las principales librerías: NumPy, Pandas, rasterio, GDAL y geopandas


```{image} Imagenes/unidades.JPG
:width: 500px
:align: center
:alt: unidad
```

<p style="text-align: center; font-size: 12px;"> 
<strong>Fig.1. Unidades temáticas – Creación propia.</strong>
 </p>

## Caso de Uso o Contexto : Exploración de la Cobertura del Suelo para 6 Municipios de Cundinamarca 


```{admonition} Guía para el docente
:class: danger
 - En esta sección, se presentará un **caso de uso o un contexto** con el fin de ilustrar los conceptos a desarrollar en la guía. Esto permitirá una mejor comprensión y aplicación de los temas abordados. 

```


Ejemplo, El departamento de Cundinamarca requiere conocer la distribución de su cobertura del suelo para mejorar la gestión territorial y ambiental. Se busca analizar la cobertura del suelo en seis municipios mediante datos raster y vectoriales, identificando áreas urbanas, agrícolas, bosques y cuerpos de agua.


### Recursos


```{admonition} Recursos
:class: nota
- Jupyter Notebook: [<span>&#x1F4E5;</span> Introducción_librerías.ipynb](ruta/al/archivo.ipynb)  
- Capa vectorial: [<span>&#x1F4E5;</span> cobertura.zip](ruta/al/archivo/cobertura.txt)

**En este recuadro, se deben listar los recursos requeridos para desarrollar la guía, como bases vectoriales, imágenes satelitales y etc** 
```

### Análisis del Problema


```{admonition} Guía para el docente
:class: danger
 - En está sección se describirá el objetivo de la unidad en relación con el caso de uso, así como los conceptos clave que se deben considerar para abordar el análisis del caso de uso.

```

**Objetivo:** Analizar la distribución de la cobertura del suelo en seis municipios de Cundinamarca.

**Conceptos:** 
  * Análisis estadístico: Cálculo de proporciones y tendencias para interpretar la distribución de la cobertura del suelo.
  

```{admonition} Guía para el docente
:class: danger
 - Las siguientes secciones se adaptarán según el desarrollo que desee realizar, culminando con un análisis de resultados o conclusiones.

```


Ejemplo 

### NumPy 

NumPy (Numerical Python) es una biblioteca de Python que proporciona estructuras de datos eficientes y funciones matemáticas  para la manipulación de arreglos multidimensionales (arrays).


```{image} Imagenes/NumPy.png
:width: 300px
:align: center
:alt: numpy
```

<p style="text-align: center; font-size: 12px;">
    <strong> Fig.2. Imagen tomada de 
    <a href="https://numpy.org/" target="_blank">NumPy Website</a></strong>
</p>



**¿Para qué sirve NumPy?**

* Manejo de arreglos y matrices: Facilita la creación, manipulación y almacenamiento de datos en estructuras eficientes.
* Operaciones matemáticas y estadísticas: Permite realizar cálculos rápidos como sumas, promedios, medianas, desviaciones estándar, etc.
* Álgebra lineal: Incluye funciones para resolver ecuaciones, descomposiciones matriciales y transformaciones lineales.
* Manejo eficiente de datos grandes: Optimiza la memoria y el procesamiento en comparación con las listas nativas de Python.
* Interoperabilidad con otras bibliotecas: Se integra con `pandas` , `SciPy`, `scikit-learn` y `TensorFlow` , entre otras.

NumPy es clave en el procesamiento de datos geoespaciales por varias razones:

* Procesamiento de datos raster : Los archivos raster (como imágenes satelitales y modelos de elevación) son esencialmente matrices de valores numéricos. NumPy permite su manipulación rápida, cálculo de estadísticas y aplicación de filtros.
* Bibliotecas como `rasterio`, `GDAL` y xarray usan NumPy internamente para manejar datos raster.

 📌 [Documentación de Numpy](https://numpy.org/)


En la **Tabla 1**, se presenta la **Clasificación de Uso del Suelo - Nivel 1**.

| Nivel 1 | Nombre                          |
|---------|---------------------------------|
| 1       | Territorios Artificializados   |
| 2       | Territorios Agrícolas          |
| 3       | Bosques y Áreas Seminaturales  |
| 4       | Áreas Húmedas                  |
| 5       | Superficies de Agua            |


<p align="left" style="font-size: 12px;"><b>
<strong>Tabla 1. Clasificación de Uso del Suelo - Nivel 1</strong></b>
</p>


La fórmula para el índice de vegetación normalizado (NDVI) es: 


$$\text{NDVI} = \frac{(NIR - RED)}{(NIR + RED)}$$

<p align="center" style="font-size: 12px;">
<b><strong>Ecuación 1. Ejemplo</strong>
</b></p>

**Ejemplo código:**

```codigo
import numpy as np

# Simulación  dos bandas 
nir = np.array([[0.2, 0.4], [0.6, 0.8]])  # Banda infrarroja cercana
red = np.array([[0.1, 0.3], [0.5, 0.7]])  # Banda roja

# Cálculo del NDVI
ndvi = (nir - red) / (nir + red)

print(ndvi)
```

```{admonition} Actividad 
:class: important
 - **Este reacudro está destinado a preguntas y actividades para los estudiantes.**
```



### Análisis de Resultados o Conclusiones

```{admonition} Guía para el docente
:class: danger
 -Para la sección de Análisis de Resultados o Conclusiones de la unidad, se recomienda que el docente, indique los objetivos de aprendizaje alcanzados 

```





```{admonition} Nota
:class: tip
 - **En este recuadro, proporcione definiciones  conceptos clave, aspectos importantes o recomendaciones que los estudiantes deben comprender para asimilar el contenido de la lección.**
```
   


# Instrucciones para organizar la unidad

Para organizar su unidad:

1. **Crear una carpeta con un código único**: Genere un código único utilizando una marca de tiempo Unix. Puede obtener la marca de tiempo actual en [https://www.unixtimestamp.com/](https://www.unixtimestamp.com/). El nombre de la carpeta debe seguir el formato `marcaDeTiempo_nombreAbreviado`, por ejemplo, `17400010441_introduccion_librerias`.


```{image} Imagenes/codigo.JPG
:width: 800px
:align: center
:alt: alt
```
<p align="center" style="font-size: 12px;"><b>
<strong>Fig.3. Creación carpeta – Creación propia.</strong></b>
</p>



1. **Dentro de esta carpeta**:
   - **Archivo principal**: Cree un archivo principal en formato Markdown (`.md`) o Jupyter Notebook (`.ipynb`). El nombre del archivo debe coincidir con el de la carpeta, por ejemplo, `17400010441_introduccion_librerias.md` o `17400010441_introduccion_librerias.ipynb`.
   - **Carpeta de imágenes**: Cree una subcarpeta llamada `imagenes` donde almacenará todas las imágenes que utilizará en su archivo principal.



```{image} Imagenes/carpetas2.JPG.
:width: 300px
:align: center
:alt: alt
```
<p align="center" style="font-size: 12px;"><b>
<strong>Fig.4. Creación carpetas – Creación propia.</strong></b>
</p>



## Referencias

1. [NumPy - Sitio Oficial](https://numpy.org/)
2. [JupyterBook](https://jupyterbook.org/en/stable/content/index.html)