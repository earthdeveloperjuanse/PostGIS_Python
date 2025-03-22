# Bases de datos espaciales: PostGIS y su integración con Python

## Bases de datos espaciales

## Tabla de contenido
1. Definiciones preliminares
2. El lenguaje SQL<br>
    2.1. Creación y eliminación de tablas<br>
    2.2. Inserción de datos<br>
    2.3. Consultas básicas con SELECT<br>
    2.4. Eliminación de duplicados con DISTINCT<br>
    2.5. Uso de JOIN para combinar tablas<br>
    2.6. Subconsultas<br>
    2.7. Uso de GROUP BY y HAVING<br>
    2.8. Actualización de datos<br>
    2.9. Eliminar registros<br>
    2.10. Vistas<br>
    2.11. Llaves foráneas<br>
    2.12. Transacciones<br>
3. PostgreSQL<br>
    3.1. Instalación
4. PostGIS<br>
    4.1. Instalación<br>
    4.2. Administración PostGIS<br>
        4.2.1. Modelo de datos espacial<br>
        4.2.2. Tipos de datos geográficos<br>
        4.2.3. Cálculo de atributos geométricos<br>
        4.2.4. Sistemas de referencia espacial<br>
    4.3. Cargar datos espaciales utilizando SQL<br>
        4.3.1. Datos vectoriales<br>
        4.3.2. Extrayendo datos espaciales vectoriales<br>
        4.3.3. Datos ráster<br>
        4.3.4. Extrayendo datos espaciales ráster<br>
5. Integración PostGIS / Python
6. Caso de estudio: Administración de datos para generación de modelo clasificador de Bosque / No Bosque por medio de PostGIS y Python
7. Referencias y recursos


### Definiciones preliminares

**Base de datos**

"...Una base de datos es una recopilación organizada de información o datos estructurados, que normalmente se almacena de forma electrónica en un sistema informático. Normalmente, una base de datos está controlada por un sistema de gestión de bases de datos (DBMS). En conjunto, los datos y el DBMS, junto con las aplicaciones asociadas a ellos, reciben el nombre de sistema de bases de datos, abreviado normalmente a simplemente base de datos...."

**Lenguaje de consulta estructurada (SQL)**
"...El SQL es un lenguaje de programación que utilizan casi todas las bases de datos relacionales para consultar, manipular y definir los datos, y para proporcionar control de acceso...."

**Software de base de datos**
"...El software de base de datos se utiliza para crear, editar y mantener archivos y registros de bases de datos, lo que facilita la creación de archivos y registros, la entrada de datos, la edición de datos, la actualización y la creación de informes. El software también maneja el almacenamiento de datos, las copias de seguridad y la creación de informes, así como el control de acceso múltiple y la seguridad...."

**Sistema de gestión de bases de datos**
"...Normalmente, una base de datos requiere un programa de software de bases de datos completo, conocido como sistema de gestión de bases de datos (DBMS). Un DBMS sirve como interfaz entre la base de datos y sus programas o usuarios finales, lo que permite a los usuarios recuperar, actualizar y gestionar cómo se organiza y se optimiza la información. Un DBMS también facilita la supervisión y el control de las bases de datos, lo que permite una variedad de operaciones administrativas como la supervisión del rendimiento, el ajuste, la copia de seguridad y la recuperación.
Algunos ejemplos de software de bases de datos o DBMS populares incluyen MySQL, Microsoft Access, Microsoft SQL Server, FileMaker Pro, Oracle Database y dBASE..."

Oracle (https://www.oracle.com/co/database/what-is-database/)

**PostgreSQL**
"...PostgreSQL es un sistema de gestión de bases de datos relacionales de objetos ( ORDBMS ) basado en POSTGRES, versión 4.2 , desarrollado en el Departamento de Informática de la Universidad de California en Berkeley. POSTGRES fue pionero en muchos conceptos que solo estuvieron disponibles en algunos sistemas de bases de datos comerciales mucho más tarde...."

PostgreSQL (https://www.postgresql.org/docs/current/intro-whatis.html)

### El lenguaje SQL

"...El lenguaje de consulta estructurada (SQL) es un lenguaje estándar para la creación y manipulación de bases de datos..."

AWS (https://aws.amazon.com/es/what-is/sql/#:~:text=El%20lenguaje%20de%20consulta%20estructurada%20(SQL)%20es%20un%20lenguaje%20est%C3%A1ndar,relacional%20que%20utiliza%20consultas%20SQL.)

#### - Creación y eliminación de tablas

Para crear una tabla en PostgreSQL, usamos `CREATE TABLE`:
```sql
CREATE TABLE weather (
    city        VARCHAR(80),
    temp_lo     INT,       -- Temperatura mínima
    temp_hi     INT,       -- Temperatura máxima
    prcp        REAL,      -- Precipitación
    date        DATE       -- Fecha del registro
);
```
Para eliminar una tabla:
```sql
DROP TABLE weather;
```

#### - Inserción de datos
Podemos insertar datos en la tabla usando `INSERT INTO`
```sql
INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');
```
También podemos especificar columnas específicas
```sql
INSERT INTO weather (city, temp_lo, temp_hi, prcp, date)
    VALUES ('San Francisco', 43, 57, 0.0, '1994-11-29');
```

#### - Consultas básicas con `SELECT`
Seleccionar todos los registros de una tabla:
```sql
SELECT * FROM weather;
```
Seleccionar columnas específicas:
```sql
SELECT city, temp_lo, temp_hi, prcp, date FROM weather;
```
Calcular la temperatura media:
```sql
SELECT city, (temp_hi + temp_lo) / 2 AS temp_avg, date FROM weather;
```
Filtrar registros con condiciones:
```sql
SELECT * FROM weather
    WHERE city = 'San Francisco' AND prcp > 0.0;
```
Ordenar resultados:
```sql
SELECT * FROM weather ORDER BY city;
```
Ordenar por múltiples columnas:
```sql
SELECT * FROM weather ORDER BY city, temp_lo;
```

#### - Eliminación de duplicados con `DISTINCT`
Para obtener los valores únicos
```sql
SELECT DISTINCT city FROM weather;
```
También podemos ordenar
```sql
SELECT DISTINCT city FROM weather ORDER BY city;
```

#### - Uso de `JOIN` para combinar tablas
Si tenemos una tabla **cities**, podemos unirla con **weather**:
```sql
SELECT * FROM weather JOIN cities ON city = name;
```
Para seleccionar columnas específicas:
```sql
SELECT weather.city, weather.temp_lo, weather.temp_hi, weather.prcp, weather.date, cities.location
    FROM weather JOIN cities ON weather.city = cities.name;
```
También se puede hacer con LEFT OUTER JOIN
```sql
SELECT * FROM weather LEFT OUTER JOIN cities ON weather.city = cities.name;
```

#### - Subconsultas
Para obtener la temperatura más baja registrada:
```sql
SELECT max(temp_lo) FROM weather;
SELECT city FROM weather
    WHERE temp_lo = (SELECT max(temp_lo) FROM weather);
```

#### - Uso de `GROUP BY` y `HAVING`
Contar registros por ciudad:
```sql
SELECT city, count(*), max(temp_lo)
    FROM weather
    GROUP BY city;
```
Filtrar grupos usando `HAVING`
```sql
SELECT city, count(*), max(temp_lo)
    FROM weather
    GROUP BY city
    HAVING max(temp_lo) < 40;
```
Aplicar filtros con `FILTER`
```sql
SELECT city, count(*) FILTER (WHERE temp_lo < 45), max(temp_lo)
    FROM weather
    GROUP BY city;
```

#### - Actualización y eliminación de datos
Actualizar valores en la tabla:
```sql
UPDATE weather
    SET temp_hi = temp_hi - 2, temp_lo = temp_lo - 2
    WHERE date > '1994-11-28';
```
#### - Eliminar registros
```sql
DELETE FROM weather WHERE city = 'Hayward';
```

#### - Vistas
```sql
CREATE VIEW myview AS
    SELECT name, temp_lo, temp_hi, prcp, date, location
        FROM weather, cities
        WHERE city = name;
SELECT * FROM myview;
```

#### - Llaves foráneas
```sql
CREATE TABLE cities (
        name     varchar(80) primary key,
        location point
);
CREATE TABLE weather (
        city      varchar(80) references cities(name),
        temp_lo   int,
        temp_hi   int,
        prcp      real,
        date      date
);
ERROR:  insert or update on table "weather" violates foreign key constraint "weather_city_fkey"
DETAIL:  Key (city)=(Berkeley) is not present in table "cities".
```

#### - Transacciones
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100.00
    WHERE name = 'Alice';
SAVEPOINT my_savepoint;
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Bob';
-- oops ... forget that and use Wally's account
ROLLBACK TO my_savepoint;
UPDATE accounts SET balance = balance + 100.00
    WHERE name = 'Wally';
COMMIT;
```

Entre otros... (https://www.postgresql.org/docs/current/)

### PostgreSQL
"...PostgreSQL es un sistema de gestión de bases de datos relacionales de objetos (ORDBMS), desarrollado en el Departamento de Informática de la Universidad de California en Berkeley. POSTGRES fue pionero en muchos conceptos que solo estuvieron disponibles en algunos sistemas de bases de datos comerciales mucho más tarde...Y gracias a la licencia liberal, PostgreSQL puede ser utilizado, modificado y distribuido por cualquier persona de forma gratuita y para cualquier propósito, ya sea privado, comercial o académico"
PostgreSQL (https://www.postgresql.org/docs/current/intro-whatis.html)

##### Proceso de instalación
Visitar la página oficial de PostgreSQL (https://www.postgresql.org/download/)
```{image} Imagenes/PostgreSQL.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 1. Página oficial de PostgreSQL – PostgreSQL. https://www.postgresql.org/download/</strong></p>

Seleccionar el instalador conforme al sistema operativo
```{image} Imagenes/Instalador.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 2. Instalador de Windows – PostgreSQL. https://www.postgresql.org/download/</strong></p>

Al ejecutar el instalador, tener en cuenta algunos puntos importantes:

- Instalación de componentes (pgadmin, stack builder)
```{image} Imagenes/Stack_Builder_Config.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 3. Configutación de Stack Builder</strong></p>
```{image} Imagenes/Stack_Builder.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 4. Stack Builder – PostgreSQL</strong></p>

- Usuario y contraseña del administrador (Para la demostración, se hace uso de postgres/postgres)
```{image} Imagenes/User_Postgres.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 5. Definición de usuario – PostgreSQL</strong></p>

- Seleccionar el puerto que se utilizará (Por defecto 5432)
```{image} Imagenes/Port.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 6. Definición de puerto – PostgreSQL</strong></p>

### PostGIS
"...PostGIS amplía las capacidades de la base de datos relacional PostgreSQL al agregar soporte para almacenar, indexar y consultar datos geoespaciales...."
Las características de PostGIS incluyen:
- **Almacenamiento de datos espaciales:** almacene diferentes tipos de datos espaciales, como puntos, líneas, polígonos y multigeometrías, tanto en datos 2D como 3D.
- **Indexación espacial:** busque y recupere rápidamente datos espaciales en función de su ubicación.
- **Funciones espaciales:** una amplia gama de funciones espaciales que le permiten filtrar y analizar datos espaciales, medir distancias y áreas , intersecar geometrías, crear búferes y más.
- **Procesamiento de geometría:** herramientas para procesar y manipular datos geométricos, como simplificación , conversión y generalización.
- **Soporte de datos ráster:** almacenamiento y procesamiento de datos ráster , como datos de elevación y datos meteorológicos.
- **Geocodificación y geocodificación inversa:** Funciones para geocodificación y geocodificación inversa.
- **Integración:** acceda y trabaje con PostGIS utilizando herramientas de terceros como QGIS , GeoServer , MapServer , ArcGIS, Tableau.

PostGIS (https://postgis.net/)


##### Proceso de instalación
Abrir Stack Builder e instalar la extensión espacial PostGIS
```{image} Imagenes/PostGIS.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 7. Instalación PostGIS</strong></p>

Identificar e instalar los componentes a instalar para complementar PostGIS
```{image} IImagenes/Components_PostGIS.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 8. Componentes de PostGIS </strong></p>

### Administración PostGIS
#### Modelo de datos espacial

**OGC Geometry**
- **Point.** Geometría de 0 dimensiones que representa una única ubicación en el espacio de coordenadas.
```sql
POINT (1 2)
POINT Z (1 2 3)
POINT ZM (1 2 3 4)
```
- **LineString.** Línea unidimensional formada por una secuencia contigua de segmentos. 
```sql
LINESTRING (1 2, 3 4, 5 6)
```
- **LinearRing.** Cadena Lineal cerrada y simple. El primer y el último punto deben ser iguales, y la línea no debe autointersecarse.
```sql
LINEARRING (0 0 0, 4 0 0, 4 4 0, 0 4 0, 0 0 0)
```
- **Polygon.** Región plana bidimensional, delimitada por un límite exterior (la capa) y ninguno o más límites interiores (agujeros).
```sql
POLYGON ((0 0 0,4 0 0,4 4 0,0 4 0,0 0 0),(1 1 0,2 1 0,2 2 0,1 2 0,1 1 0))
```
- **MultiPoint.** Colección de Puntos.
```sql
MULTIPOINT ( (0 0), (1 2) )
```
- **MultiLineString.** Colección de LineStrings.
```sql
MULTILINESTRING ( (0 0,1 1,1 2), (2 3,3 2,5 4) )
```
- **MultiPolygon.** Conjunto de polígonos no superpuestos ni adyacentes. Los polígonos del conjunto solo pueden tocarse en un número finito de puntos.
```sql
MULTIPOLYGON (((1 5, 5 5, 5 1, 1 1, 1 5)), ((6 5, 9 1, 6 1, 6 5)))
```
- **GeometryCollection.** Colección heterogénea (mixta) de geometrías.
```sql
GEOMETRYCOLLECTION ( POINT(2 3), LINESTRING(2 3, 3 4))
```
- **PolyhedralSurface.** Colección contigua de parches o facetas que comparten algunas aristas. Cada parche es un polígono plano. Si las coordenadas del polígono tienen coordenadas Z, la superficie es tridimensional.
```sql
POLYHEDRALSURFACE Z (
  ((0 0 0, 0 0 1, 0 1 1, 0 1 0, 0 0 0)),
  ((0 0 0, 0 1 0, 1 1 0, 1 0 0, 0 0 0)),
  ((0 0 0, 1 0 0, 1 0 1, 0 0 1, 0 0 0)),
  ((1 1 0, 1 1 1, 1 0 1, 1 0 0, 1 1 0)),
  ((0 1 0, 0 1 1, 1 1 1, 1 1 0, 0 1 0)),
  ((0 0 1, 1 0 1, 1 1 1, 0 1 1, 0 0 1)) )
```
- **Triangle.** Polígono definido por tres vértices distintos no colineales. Al ser un polígono, se define mediante cuatro coordenadas, siendo la primera y la cuarta iguales.
```sql
TRIANGLE ((0 0, 0 9, 9 0, 0 0))
```
- **TIN.** Colección de triángulos no superpuestos que representan una red irregular triangulada.
```sql
TIN Z ( ((0 0 0, 0 0 1, 0 1 0, 0 0 0)), ((0 0 0, 0 1 0, 1 1 0, 0 0 0)) )
```

#### Tipos de datos geográficos
**Geographic**
"...El tipo de datos PostGIS geography proporciona compatibilidad nativa con entidades espaciales representadas en coordenadas geográficas (o "lat/lon"). Las coordenadas geográficas son coordenadas esféricas expresadas en unidades angulares (grados)..."

**Geometry**
"...La base del tipo de datos geométricos de PostGIS es un plano...."

#### Cálculo de atributos geométricos
El camino más corto entre dos puntos en el plano es una línea recta. Esto significa que las funciones geométricas (áreas, distancias, longitudes, intersecciones, etc.) se calculan utilizando vectores de línea recta y matemáticas cartesianas. Esto facilita su implementación y agiliza su ejecución, pero también las hace imprecisas para datos sobre la superficie esferoidal de la Tierra.

El tipo de datos geográficos de PostGIS se basa en un modelo esférico. El camino más corto entre dos puntos de la esfera es un arco de círculo máximo. Las funciones sobre geografías (áreas, distancias, longitudes, intersecciones, etc.) se calculan utilizando arcos de la esfera. Al considerar la forma esferoidal del mundo, las funciones proporcionan resultados más precisos.

Creación de tablas de geografía
```sql
CREATE TABLE global_points (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    location geography(POINT, 4326)
  );
```
Utilizando tablas de geografía
```sql
INSERT INTO global_points (name, location) VALUES ('Town', 'SRID=4326;POINT(-110 30)');
INSERT INTO global_points (name, location) VALUES ('Forest', 'SRID=4326;POINT(-109 29)');
INSERT INTO global_points (name, location) VALUES ('London', 'SRID=4326;POINT(0 49)');
```
Consulta de una distancia utilizando una tolerancia de 1000km
```sql
SELECT name FROM global_points WHERE ST_DWithin(location, 'SRID=4326;POINT(-110 29)'::geography, 1000000);
```
**¿Cuándo utilizar el tipo de datos geografía?**
El tipo de datos geografía le permite almacenar datos en coordenadas de longitud/latitud, pero a un costo: hay menos funciones definidas en GEOGRAPHY que en GEOMETRY; las funciones que están definidas toman más tiempo de CPU para ejecutarse.
El tipo de datos que elija debe determinarse según el área de trabajo prevista de la aplicación que esté desarrollando. ¿Sus datos abarcarán todo el mundo, una gran área continental, o son locales, de un estado, condado o municipio?
- Si sus datos están contenidos en un área pequeña, es posible que elegir una proyección adecuada y utilizar GEOMETRÍA sea la mejor solución, en términos de rendimiento y funcionalidad disponibles.
- Si sus datos son globales o cubren una región continental, GEOGRAPHY le permitirá crear un sistema sin preocuparse por los detalles de proyección. Almacene sus datos en longitud/latitud y utilice las funciones definidas en GEOGRAPHY.
- Si no entiendes las proyecciones, no quieres aprender sobre ellas y estás dispuesto a aceptar las limitaciones de funcionalidad de GEOGRAPHY, quizás te resulte más fácil usar GEOGRAPHY que GEOMETRY. Simplemente carga tus datos como longitud/latitud y empieza desde ahí.


#### Sistemas de referencia espacial
Un **Sistema de Referencia Espacial (SRE)** (también llamado **Sistema de Referencia de Coordenadas (SRC)**) define cómo se referencia la geometría a ubicaciones en la superficie terrestre. Existen tres tipos de SRE:
- Un **SRS geodésico** utiliza coordenadas angulares (longitud y latitud) que se asignan directamente a la superficie de la tierra.
- Un **SRS proyectado** utiliza una transformación matemática de proyección para aplanar la superficie de la Tierra esferoidal sobre un plano. Asigna coordenadas de ubicación que permiten la medición directa de magnitudes como la distancia, el área y el ángulo. El sistema de coordenadas es cartesiano, lo que significa que tiene un punto de origen definido y dos ejes perpendiculares (generalmente orientados al norte y al este). Cada SRS proyectado utiliza una unidad de longitud establecida (generalmente metros o pies). Un SRS proyectado puede tener un área de aplicación limitada para evitar distorsiones y ajustarse a los límites de coordenadas definidos.
- Un **SRS local** es un sistema de coordenadas cartesiano que no está referenciado a la superficie terrestre. En PostGIS, esto se especifica mediante un valor SRID de 0.

Tabla **SPATIAL_REF_SYS**
```sql
CREATE TABLE spatial_ref_sys (
  srid       INTEGER NOT NULL PRIMARY KEY,
  auth_name  VARCHAR(256),
  auth_srid  INTEGER,
  srtext     VARCHAR(2048),
  proj4text  VARCHAR(2048)
)
```
srtext
```sql
PROJCS["NAD83 / UTM Zone 10N",
  GEOGCS["NAD83",
	DATUM["North_American_Datum_1983",
	  SPHEROID["GRS 1980",6378137,298.257222101]
	],
	PRIMEM["Greenwich",0],
	UNIT["degree",0.0174532925199433]
  ],
  PROJECTION["Transverse_Mercator"],
  PARAMETER["latitude_of_origin",0],
  PARAMETER["central_meridian",-123],
  PARAMETER["scale_factor",0.9996],
  PARAMETER["false_easting",500000],
  PARAMETER["false_northing",0],
  UNIT["metre",1]
]
```
Sistemas de referencia espacial definidos por el usuario
```sql
INSERT INTO spatial_ref_sys (srid, proj4text)
VALUES ( 990000,
  '+proj=lcc  +lon_0=-95 +lat_0=25 +lat_1=25 +lat_2=25 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'
);
```

#### Cargar datos espaciales utilizando SQL
##### - Datos vectoriales
Si los datos espaciales se pueden convertir a una representación de texto (como WKT o WKB), usar SQL podría ser la forma más sencilla de importarlos a PostGIS. Los datos se pueden cargar masivamente en PostGIS/PostgreSQL cargando un archivo de texto con `INSERT`.
```sql
BEGIN;
INSERT INTO roads (road_id, roads_geom, road_name)
  VALUES (1,'LINESTRING(191232 243118,191108 243242)','Jeff Rd');
INSERT INTO roads (road_id, roads_geom, road_name)
  VALUES (2,'LINESTRING(189141 244158,189265 244817)','Geordie Rd');
INSERT INTO roads (road_id, roads_geom, road_name)
  VALUES (3,'LINESTRING(192783 228138,192612 229814)','Paul St');
INSERT INTO roads (road_id, roads_geom, road_name)
  VALUES (4,'LINESTRING(189412 252431,189631 259122)','Graeme Ave');
INSERT INTO roads (road_id, roads_geom, road_name)
  VALUES (5,'LINESTRING(190131 224148,190871 228134)','Phil Tce');
INSERT INTO roads (road_id, roads_geom, road_name)
  VALUES (6,'LINESTRING(198231 263418,198213 268322)','Dave Cres');
COMMIT;
```

#### Utilizando el Shapefile Loader
El `shp2pgsql` cargador de datos convierte los shapefiles a SQL, aptos para su inserción en bases de datos PostGIS/PostgreSQL, ya sea en formato geométrico o geográfico. El cargador dispone de varios modos de funcionamiento que se seleccionan mediante indicadores de línea de comandos.

`-c`. Crea una nueva tabla y la rellena desde el shapefile. Este es el modo predeterminado.<br>
`-a`. Añade datos del shapefile a la tabla de la base de datos. Tenga en cuenta que para usar esta opción y cargar varios archivos, estos deben tener los mismos atributos y tipos de datos.<br>
`-d`. Elimina la tabla de base de datos antes de crear una nueva tabla con los datos en el Shapefile.<br>
`-p`. Solo genera el código SQL de creación de tablas, sin añadir datos. Esto se puede usar si necesita separar completamente los pasos de creación de tablas y carga de datos.<br>
`-s`. [<FROM_SRID>:]<SRID> Crea y rellena las tablas de geometría con el SRID especificado. Opcionalmente, especifica que el shapefile de entrada utilice el FROM_SRID dado, en cuyo caso las geometrías se reproyectarán al SRID de destino.<br>
`-i`. Convierte todos los números enteros en números enteros estándar de 32 bits, no crea bigints de 64 bits, incluso si la firma del encabezado DBF parece justificarlo.<br>
`-I`. Crea un índice GiST en la columna de geometría.

En la línea de comandos
```sh
shp2pgsql -c -s 4269 -i -I shaperoads.shp myschema.roadstable > carreteras.sql 
psql -d carreterasdb -f carreteras.sql
```

También podría hacerse por medio de la interfaz gráfica. Buscando "PostGIS PostGIS Bundle 1 for PostgreSQL x64 16 Shapefile and DBF Loader Exporter"
- Realizar la conexión a la base de datos
```{image} Imagenes/PostGIS_Connection.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 9. Conexión a PostGIS </strong></p>

- Verificar las opciones de importación según las necesidades del usuario
```{image} Imagenes/Options_Import_PostGIS.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 10. Opciones de importación - PostGIS </strong></p>

- Buscar y cargar el archivo Shapefile verificando el nombre con el cual se guardará la tabla y el SRID
```{image} Imagenes/Options_Import_PostGIS.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> <strong>Fig. 11. Cargar datos desde Shapefile </strong></p>

Consultar más parámetros: https://postgis.net/docs/manual-3.5/using_postgis_dbmanagement.html#loading-data


#### Extrayendo datos espaciales vectoriales
La forma más sencilla de extraer datos espaciales de la base de datos es utilizar una `SELECT` consulta SQL para definir el conjunto de datos que se va a extraer y volcar las columnas resultantes en un archivo de texto analizable.

```sql
SELECT road_id, ST_AsText(road_geom) AS geom, road_name FROM roads;

SELECT road_id, road_name FROM roads
    WHERE ST_Intersects(roads_geom, 'SRID=312;POLYGON((...))');
```

```{image} Imagenes/Functions_PostGIS.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> 
<strong>Fig. 12. Ejemplos de funciones de PostGIS – PostGIS. https://postgis.net/docs/manual-1.5/ch08.html</strong>
</p>

##### - Datos raster
#### Utilizando el Rasters Loader
`raster2pgsql` es un ejecutable de carga de ráster que carga formatos ráster compatibles con GDAL en SQL, aptos para su carga en una tabla ráster PostGIS. Permite cargar carpetas de archivos ráster y crear vistas generales de rásteres. Dado que raster2pgsql se compila generalmente como parte de PostGIS (a menos que compile su propia biblioteca GDAL), los tipos de ráster compatibles con el ejecutable serán los mismos que los compilados en la biblioteca de dependencias de GDAL. 

En la línea de comandos

`-s`. SRID <br>
`-I`. Índice espacial<br>
`-C`. Utilizar restricciones ráster estándar.<br>
`-M`. Análisis de vacíos después de la carga<br>
`-F`. Incluye una columna de nombre de archivo en la tabla ráster.<br>
`-t`. Divide la salida en mosaicos de 100x100.<br>

* *.tif carga todos estos archivos
* public.demelevation cargar en esta tabla
* -d conectarse a esta base de datos
* -f lee este archivo después de conectarse

```sh
raster2pgsql -s 4326 -I -C -M -F -t 100x100 *.tif público.demelevation > elev.sql
psql -d gisdb -f elev.sql
```
```{image} Imagenes/Formats_Raster.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> 
<strong>Fig. 13. Ejemplos de formatos de ráster de PostGIS – PostGIS. https://postgis.net/docs/using_raster_dataman.html</strong>
</p>

Para mayor información (https://postgis.net/docs/using_raster_dataman.html)

#### Extrayendo datos espaciales ráster
PostGIS permite almacenar y consultar datos ráster de manera eficiente. Para extraer información de una tabla que contiene datos ráster, podemos usar funciones especializadas.

Extraer información de un ráster
```sql
SELECT rid, ST_Metadata(rast) FROM raster_table;
```
Obtener el valor de un píxel en una coordenada específica
```sql
SELECT ST_Value(rast, ST_SetSRID(ST_Point(1000, 2000), 4326)) 
FROM raster_table;
```
Consultar rásteres que intersectan con una geometría
```sql
SELECT rid, rast
FROM raster_table
WHERE ST_Intersects(rast, ST_GeomFromText('POLYGON((...))', 4326));
```
Estadísticas de ráster en un área específica
```sql
SELECT ST_SummaryStats(rast) 
FROM raster_table 
WHERE ST_Intersects(rast, ST_GeomFromText('POLYGON((...))', 4326));
```

### Integración PostGIS / Python

* Cargar datos desde Shapefile con librerías de python `Geopandas`, `Shapely` y `psycopg2`


```python
# GeoPandas: Extensión de Pandas para manejar datos geoespaciales (puntos, líneas, polígonos).
# Permite leer, escribir y analizar datos espaciales en formatos como Shapefile, GeoJSON, etc.
import geopandas as gpd
# Psycopg2: Biblioteca para conectar Python con bases de datos PostgreSQL.
# Se usa para ejecutar consultas SQL, manejar transacciones y trabajar con datos espaciales en PostGIS.
import psycopg2
# Shapely: Biblioteca para la manipulación y análisis de geometrías espaciales.
# 'wkt' (Well-Known Text) permite convertir entre texto y objetos geométricos.
from shapely import wkt
```

Leer los datos espaciales con ayuda de Geopandas


```python
shapefile_path = "./Samples/Samples_Point.shp"  # Ruta del archivo .shp con datos geoespaciales
gdf = gpd.read_file(shapefile_path)  # Cargar el archivo en un GeoDataFrame
gdf.head()  # Mostrar las primeras filas del GeoDataFrame para inspección
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Shape_Leng</th>
      <th>Shape_Area</th>
      <th>class</th>
      <th>ORIG_FID</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>Bosque</td>
      <td>0</td>
      <td>POINT (333600.852 710803.978)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>Bosque</td>
      <td>0</td>
      <td>POINT (333797.268 710693.129)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>Bosque</td>
      <td>0</td>
      <td>POINT (333865.332 710844.816)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>Bosque</td>
      <td>0</td>
      <td>POINT (334120.089 710615.341)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>Bosque</td>
      <td>0</td>
      <td>POINT (334166.762 710842.872)</td>
    </tr>
  </tbody>
</table>
</div>



Crear la conexión con la base de datos espacial


```python
DB_CONFIG = {
    "dbname": "DB_GIS",                 # Nombre de la base de datos
    "user": "postgres",                 # Usuario de la base de datos
    "password": "postgres",             # Contraseña del usuario
    "host": "localhost",                # Dirección del servidor (localhost si es local)
    "port": "5432"                      # Puerto predeterminado de PostgreSQL
}
conn = psycopg2.connect(**DB_CONFIG)    # Establecer conexión con la base de datos PostgreSQL
cur = conn.cursor()                     # Crear un cursor para ejecutar comandos SQL
```

Creación de tabla con columnas a cargar


```python
# Crear una tabla en PostGIS si no existe
create_table_query = """
CREATE TABLE IF NOT EXISTS training_sample (
    id SERIAL PRIMARY KEY,              -- Identificador único autoincremental
    class TEXT,                         -- Columna para almacenar la clase del punto
    geom GEOMETRY(Geometry, 32619)      -- Columna geométrica con proyección EPSG:32619 (UTM Zona 19N)
);
"""
cur.execute(create_table_query)     # Ejecutar la consulta SQL para crear la tabla
conn.commit()                       # Confirmar la creación de la tabla en la base de datos
```

```{image} Imagenes/Table_Training_Sample.PNG
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> 
<strong>Fig. 14. Tabla creada "training_sample" en base de datos </strong>
</p>

Insertar los datos


```python
conn.rollback()  # Realizar un rollback por seguridad antes de insertar datos (opcional)
insert_query = "INSERT INTO training_sample (class, geom) VALUES (%s, ST_GeomFromText(%s, 32619))"
# Iterar sobre cada fila del GeoDataFrame y cargar los datos en la base de datos
for _, row in gdf.iterrows():
    class_ = row["class"]                       # Extraer el valor de la columna 'class' (ajustar según los nombres de columnas)
    geom = row["geometry"].wkt                  # Convertir la geometría a formato WKT (Well-Known Text)    
    cur.execute(insert_query, (class_, geom))   # Ejecutar la consulta SQL con los valores extraídos
conn.commit()                                   # Confirmar la inserción de datos en la base de datos
cur.close()                                     # Cerrar el cursor y la conexión con la base de datos
conn.close()
```

* Cargar datos desde archivo .tif con librerías de python `subprocess` y `psycopg2`


```python
import psycopg2     # psycopg2: Librería para conectar Python con bases de datos PostgreSQL. Permite ejecutar consultas SQL, manipular datos y gestionar transacciones.
import subprocess   # subprocess: Módulo para ejecutar comandos del sistema desde Python. Se usa para llamar programas externos como psql, raster2pgsql, etc.
import os
```


```python
DB_CONFIG = {
    "dbname": "DB_GIS",                 # Nombre de la base de datos
    "user": "postgres",                 # Usuario de la base de datos
    "password": "postgres",             # Contraseña del usuario
    "host": "localhost",                # Dirección del servidor (localhost si es local)
    "port": "5432"                      # Puerto predeterminado de PostgreSQL
}
conn = psycopg2.connect(**DB_CONFIG) 
cur = conn.cursor()
# Abrir el archivo raster (.tif)
raster_path = r'C:\Users\JHERNANDEZ\OneDrive - Esri NOSA\Documentos\GitHub\PostGIS_Python\PostGIS_Python\temp_raster.tif'
os.environ["PGPASSWORD"] = DB_CONFIG["password"]
'''
¿Por qué usar PGPASSWORD?
- Evita que psql solicite la contraseña cada vez que se ejecuta un comando.
- Facilita la automatización de tareas en PostgreSQL, como importar datos o ejecutar scripts SQL.
- Es más seguro que escribir la contraseña directamente en el comando, pero aún es recomendable eliminarla después de su uso.'
'''

```




    "\n¿Por qué usar PGPASSWORD?\n- Evita que psql solicite la contraseña cada vez que se ejecuta un comando.\n- Facilita la automatización de tareas en PostgreSQL, como importar datos o ejecutar scripts SQL.\n- Es más seguro que escribir la contraseña directamente en el comando, pero aún es recomendable eliminarla después de su uso.'\n"




```python
# Ruta a la carpeta donde están raster2pgsql y psql
pg_bin_path = r"C:\Program Files\PostgreSQL\16\bin"
sql_output_path = r"C:\Shp_Example\prueba.sql"
# Construir el comando con la ruta completa de raster2pgsql y psql
cmd = fr'"{pg_bin_path}\raster2pgsql.exe" -s 32619 -I -C "{raster_path}" >  {sql_output_path}'
# Ejecutar el comando en la terminal
process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
```


```python
cmd = fr'"{pg_bin_path}\psql.exe" -d {DB_CONFIG["dbname"]} -U {DB_CONFIG["user"]} -h {DB_CONFIG["host"]} -p {DB_CONFIG["port"]} -f "{sql_output_path}"'
# Ejecutar el comando
process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
# Limpiar la variable de entorno después de ejecutar el comando
del os.environ["PGPASSWORD"]
```


```python
print(process.stdout)
```

    BEGIN
    CREATE TABLE
    INSERT 0 1
    CREATE INDEX
    ANALYZE
     addrasterconstraints 
    ----------------------
     t
    (1 fila)
    
    COMMIT
    
    

### Caso de estudio: Administración de datos para generación de modelo clasificador de Bosque / No Bosque por medio de PostGIS y Python

El caso de estudio **"Bosque - No Bosque"** consiste en la clasificación de áreas geográficas en dos categorías: regiones con cobertura boscosa y regiones sin cobertura boscosa. Este análisis es fundamental para la gestión ambiental, la planificación territorial y el monitoreo del cambio climático. Para lograr esta clasificación, se integran **datos ráster y vectoriales** almacenados en una base de datos PostgreSQL, combinados con técnicas de Machine Learning en Python.

El proceso comienza con la extracción de datos ráster almacenados en PostGIS, los cuales contienen información multiespectral de imágenes satelitales. Luego, se combinan con muestras de entrenamiento vectoriales que indican la cobertura real de la tierra, permitiendo entrenar un modelo de clasificación basado en **Random Forest**. Este modelo aprende a diferenciar áreas boscosas y no boscosas a partir de las firmas espectrales de los píxeles.

La **integración de PostGIS y Python** es clave para procesar datos espaciales de manera eficiente. PostGIS permite realizar consultas geoespaciales avanzadas y gestionar datos ráster y vectoriales en una base de datos optimizada, mientras que Python proporciona herramientas avanzadas para el análisis de datos y el entrenamiento de modelos de aprendizaje automático. La combinación de ambas tecnologías permite automatizar la extracción de datos, la clasificación y la visualización de los resultados en mapas interpretables.

Este enfoque facilita la toma de decisiones basadas en datos espaciales, permitiendo la identificación de patrones de deforestación, el monitoreo de la salud de los bosques y la generación de políticas ambientales más efectivas.

Cargar imagen a base de datos espacial

```sh
raster2pgsql.exe -s 32619 -I -C C:\PostGIS_Python\nir_aoi.tif > C:\PostGIS_Python\load_nir_img.sql

psql -d postgis_34_sample -f C:\PostGIS_Python\load_nir_img.sql
```

Importas las liberías necesarias para el caso de uso


```python
import psycopg2                                                                     # Conectar a la base de datos PostgreSQL con PostGIS
import numpy as np                                                                  # Manipulación de arrays numéricos y operaciones matemáticas
import rasterio                                                                     # Manejo y procesamiento de datos ráster
import pandas as pd                                                                 # Manejo de datos tabulares y consultas SQL
from sklearn.model_selection import train_test_split                                # División de datos en entrenamiento y prueba
from sklearn.ensemble import RandomForestClassifier                                 # Algoritmo de clasificación de bosques aleatorios
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report # Evaluación del modelo
import matplotlib.pyplot as plt                                                     # Generación de gráficos
import seaborn as sns                                                               # Visualización de datos con gráficos estadísticos
import matplotlib.colors as mcolors                                                 # Manejo de colores en visualizaciones
from skimage.transform import resize                                                # Redimensionamiento de imágenes

```

Configuración de parámetros para conexión con base de datos local


```python
# Configuración de conexión a la base de datos PostgreSQL con PostGIS
DB_CONFIG = {
    "dbname": "postgis_34_sample",      # Nombre de la base de datos
    "user": "postgres",                 # Usuario de la base de datos
    "password": "postgres",             # Contraseña del usuario
    "host": "localhost",                # Dirección del servidor (localhost si es local)
    "port": "5432"                      # Puerto predeterminado de PostgreSQL
}

def conectar_postgis():
    """
    Establece una conexión a la base de datos PostgreSQL con soporte PostGIS.
    Retorna:
        conn (psycopg2.connection): Objeto de conexión a la base de datos.
    """
    conn = psycopg2.connect(**DB_CONFIG)  # Conectar a la base de datos usando la configuración definida
    return conn
```

Extraer el ráster almacenado en la base de datos espacial


```python
# Establece la conexión con la base de datos PostgreSQL con PostGIS
conn = conectar_postgis()
# Crea un cursor para ejecutar consultas SQL
cur = conn.cursor()
# Ejecuta una consulta SQL para obtener un ráster desde la base de datos en formato GDAL (GeoTIFF)
cur.execute("SELECT ST_AsGDALRaster(rast, 'GTiff') FROM nir_aoi LIMIT 1;")
# Recupera el resultado de la consulta (raster_bin contiene los datos del ráster en formato binario)
raster_bin = cur.fetchone()[0]
# Guarda temporalmente la imagen ráster en un archivo local (GeoTIFF)
with open("temp_raster.tif", "wb") as f:
    f.write(raster_bin)
# Abre la imagen ráster utilizando rasterio
with rasterio.open("temp_raster.tif") as src:
    raster_array = src.read()   # Carga el contenido del ráster como un array NumPy
    transform = src.transform   # Obtiene la transformación del ráster (ubicación y resolución espacial)
# Cierra el cursor y la conexión a la base de datos para liberar recursos
cur.close()
conn.close()
```

Extraer los datos de muestras (Geometría punto. Bosque - No Bosque)


```python
# Establece la conexión con la base de datos PostgreSQL con PostGIS
conn = conectar_postgis()
# Consulta SQL para extraer coordenadas y etiquetas de clasificación desde la tabla de muestras de entrenamiento
query = """
SELECT ST_X(geom) AS lon, ST_Y(geom) AS lat, class FROM training_sample;
"""
# Ejecuta la consulta y almacena los resultados en un DataFrame de pandas
df = pd.read_sql(query, conn)
# Cierra la conexión con la base de datos para liberar recursos
conn.close()
df
```

Extraer los valores de píxel de cada banda del ráster para cada muestra


```python
# Listas para almacenar los valores de los píxeles extraídos y sus respectivas etiquetas
valores_pixeles = []
etiquetas = []
# Iteramos sobre cada fila del DataFrame que contiene las muestras de entrenamiento
for _, row in df.iterrows():
    lon, lat, label = row['lon'], row['lat'], row['class']                              # Extraemos las coordenadas y la clase de la muestra    
    # Convertimos coordenadas geográficas (lon, lat) a índices de píxel en la imagen ráster
    row_idx, col_idx = ~transform * (lon, lat)                                          # Aplicamos la transformación inversa
    row_idx, col_idx = int(row_idx), int(col_idx)                                       # Convertimos a enteros para obtener la posición en la matriz ráster
    # Verificamos que las coordenadas convertidas estén dentro de los límites del ráster
    if 0 <= row_idx < raster_array.shape[1] and 0 <= col_idx < raster_array.shape[2]:
        # Extraemos los valores de las bandas del píxel correspondiente y los almacenamos en la lista
        valores_pixeles.append([
            raster_array[0, row_idx, col_idx],  # Banda 1 (Ej. Rojo)
            raster_array[1, row_idx, col_idx],  # Banda 2 (Ej. Verde)
            raster_array[2, row_idx, col_idx]   # Banda 3 (Ej. Azul)
        ])
        etiquetas.append(label)                                                         # Almacenamos la etiqueta de la muestra en la lista
# Convertimos las listas a arreglos NumPy para su uso en el modelo de Machine Learning
X, y = np.array(valores_pixeles), np.array(etiquetas)

```

Dividir el universo de muestras en grupos de entrenamiento y validación


```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
```

Entrenamiento del modelo de clasificación


```python
# Inicialización del modelo de clasificación Random Forest
modelo = RandomForestClassifier(
    n_estimators=1000,      # Número de árboles en el bosque
    max_depth=10,           # Profundidad máxima de cada árbol para evitar sobreajuste
    max_features="sqrt",    # Número máximo de características consideradas en cada división (raíz cuadrada del total)
    random_state=42,        # Fijamos una semilla para asegurar reproducibilidad de resultados
    n_jobs=-1               # Utiliza todos los núcleos de la CPU disponibles para acelerar el entrenamiento
)
# Entrenamiento del modelo con los datos de entrenamiento
modelo.fit(X_train, y_train)
# Realización de predicciones sobre el conjunto de prueba
y_pred = modelo.predict(X_test)

```

Evaluación del rendimiento del modelo


```python
# Cálculo de la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print("Precisión:", accuracy)  # Imprime la precisión global del modelo
# Cálculo de la exactitud del modelo con formato de 4 decimales
exactitud = accuracy_score(y_test, y_pred)
print(f"Exactitud del modelo: {exactitud:.4f}")
# Cálculo de la matriz de confusión
conf_matrix = confusion_matrix(y_test, y_pred)
# Visualización de la matriz de confusión con Seaborn
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", 
            xticklabels=["No Bosque", "Bosque"], 
            yticklabels=["No Bosque", "Bosque"])
# Etiquetas para los ejes
plt.xlabel("Predicción")            # Etiqueta del eje X
plt.ylabel("Real")                  # Etiqueta del eje Y
plt.title("Matriz de Confusión")    # Título del gráfico
plt.show()                          # Mostrar la matriz de confusión
# Generación del informe de clasificación con métricas detalladas
print(classification_report(y_test, y_pred, target_names=["No Bosque", "Bosque"]))
```

Aplicación del modelo para predecir la clase de cada píxel en la imagen ráster


```python
filas, columnas = raster_array.shape[1], raster_array.shape[2]  # Extraemos el número de filas y columnas del ráster
# Reestructuramos la imagen ráster en una matriz donde cada fila es un píxel y las columnas son las bandas espectrales
raster_reshaped = raster_array.reshape(3, -1).T                 # Convertimos a formato (N, 3), donde N es el número total de píxeles
predicciones = modelo.predict(raster_reshaped)                  # Aplicamos el modelo entrenado para predecir la clase de cada píxel en la imagen ráster
predict_ = predicciones.reshape(filas, columnas)                # Reformateamos las predicciones en la misma estructura de la imagen original (filas, columnas)
```


```python
mapa_clases = {"No_Bosque": 0, "Bosque": 1}                         # Diccionario de mapeo de clases: Asigna valores numéricos a las etiquetas de clasificación
predict_numeric = np.vectorize(mapa_clases.get)(predict_)           # Convierte la matriz de predicciones categóricas a valores numéricos usando el diccionario de mapeo
filas, columnas = raster_array.shape[1], raster_array.shape[2]      # Extraemos las dimensiones de la imagen original
# Redimensionamos la imagen predicha para ajustarla a la resolución original del ráster
predict_resized = resize(
    predict_numeric, (filas, columnas), 
    order=0,                                                        # Mantiene valores discretos sin interpolación
    anti_aliasing=False,                                            # Evita suavizar los bordes para mantener las clases bien definidas
    preserve_range=True                                             # Mantiene los valores originales sin normalización
)
cmap = mcolors.ListedColormap(["green", "white"])                   # Definimos un mapa de colores para visualizar la clasificación. "Bosque" será verde, "No Bosque" será blanco
bounds = [0, 0.5, 1]                                                # Definimos los límites de cada clase en el mapa de colores
norm = mcolors.BoundaryNorm(bounds, cmap.N)
fig, axs = plt.subplots(1, 2, figsize=(14, 7))                      # Creamos una figura con 2 subgráficos (1 fila, 2 columnas)
# Construimos una imagen en color RGB a partir de las bandas del ráster original
raster_rgb = np.stack([
    raster_array[0],  # Banda Roja
    raster_array[1],  # Banda Verde
    raster_array[2]   # Banda Azul
], axis=-1)
raster_rgb = raster_rgb.astype(np.float32)                          # Normalizamos los valores del ráster RGB para mejorar la visualización
raster_rgb /= raster_rgb.max()
axs[0].imshow(raster_rgb)                                           # Mostramos la imagen original en la primera columna
axs[0].set_title("Imagen Original (RGB)")
axs[0].axis("off")                                                  # Oculta los ejes para mejorar la visualización
img = axs[1].imshow(predict_resized, cmap=cmap, norm=norm)          # Mostramos la clasificación "Bosque / No Bosque" en la segunda columna
axs[1].set_title("Clasificación Bosque / No Bosque")
axs[1].axis("off")
plt.tight_layout()                                                  # Ajusta el diseño de la figura para evitar solapamientos
plt.show()                                                          # Muestra la figura con las dos imágenes
```


```python
output_raster_path = "clasificacion_bosque.tif"
transform = rasterio.open("temp_raster.tif").transform  # Extrae la transformación del raster original
# Guardar el resultado en un nuevo raster GeoTIFF
with rasterio.open(
    output_raster_path, "w",
    driver="GTiff",
    height=predict_resized.shape[0], 
    width=predict_resized.shape[1],
    count=1,  # Una sola banda (clasificación)
    dtype=rasterio.uint8,  # Tipo de datos para la clasificación (0 y 1)
    crs="EPSG:32619",  # Asegurar que tenga el mismo CRS que la imagen original
    transform=transform
) as dst:
    dst.write(predict_resized.astype(rasterio.uint8), 1)
```


```python
import psycopg2     # psycopg2: Librería para conectar Python con bases de datos PostgreSQL. Permite ejecutar consultas SQL, manipular datos y gestionar transacciones.
import subprocess   # subprocess: Módulo para ejecutar comandos del sistema desde Python. Se usa para llamar programas externos como psql, raster2pgsql, etc.
import os

DB_CONFIG = {
    "dbname": "postgis_34_sample",      # Nombre de la base de datos
    "user": "postgres",                 # Usuario de la base de datos
    "password": "postgres",             # Contraseña del usuario
    "host": "localhost",                # Dirección del servidor (localhost si es local)
    "port": "5432"                      # Puerto predeterminado de PostgreSQL
}
conn = psycopg2.connect(**DB_CONFIG) 
cur = conn.cursor()
# Abrir el archivo raster (.tif)
raster_path = r'C:\Users\ingju\OneDrive\Escritorio\Repositorios\Tools_ArcGIS\PostGIS_Python\PostGIS_Python\clasificacion_bosque.tif'
os.environ["PGPASSWORD"] = DB_CONFIG["password"]
'''
¿Por qué usar PGPASSWORD?
- Evita que psql solicite la contraseña cada vez que se ejecuta un comando.
- Facilita la automatización de tareas en PostgreSQL, como importar datos o ejecutar scripts SQL.
- Es más seguro que escribir la contraseña directamente en el comando, pero aún es recomendable eliminarla después de su uso.'
'''

# Ruta a la carpeta donde están raster2pgsql y psql
pg_bin_path = r"C:\Program Files\PostgreSQL\16\bin"
sql_output_path = r"C:\Shp_Example\classify_raster.sql"
# Construir el comando con la ruta completa de raster2pgsql y psql
cmd = fr'"{pg_bin_path}\raster2pgsql.exe" -s 32619 -I -C "{raster_path}" >  {sql_output_path}'
# Ejecutar el comando en la terminal
process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

cmd = fr'"{pg_bin_path}\psql.exe" -d {DB_CONFIG["dbname"]} -U {DB_CONFIG["user"]} -h {DB_CONFIG["host"]} -p {DB_CONFIG["port"]} -f "{sql_output_path}"'
# Ejecutar el comando
process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
# Limpiar la variable de entorno después de ejecutar el comando
del os.environ["PGPASSWORD"]
print(process.stdout)
```

```{image} Imagenes/Load_Classify.png
:width: 500px
:align: center
:alt: unidad
```
<p style="text-align: center; font-size: 12px;"> 
<strong>Fig. 15. Conexión a base de datos espacial desde QGIS para visualización de resultados </strong>
</p>

### Referencias y Recursos

##### Bases de Datos
- **Oracle** - [¿Qué es una base de datos?](https://www.oracle.com/co/database/what-is-database/)
- **PostgreSQL** - [Introducción a PostgreSQL](https://www.postgresql.org/docs/current/intro-whatis.html)
- **PostgreSQL - Documentación** - [PostgreSQL Docs](https://www.postgresql.org/docs/current/)

##### SQL
- **SQL en AWS** - [¿Qué es SQL?](https://aws.amazon.com/es/what-is/sql/#:~:text=El%20lenguaje%20de%20consulta%20estructurada%20(SQL)%20es%20un%20lenguaje%20est%C3%A1ndar,relacional%20que%20utiliza%20consultas%20SQL.)
- **Acciones SQL en PostgreSQL** - [Documentación Oficial](https://www.postgresql.org/docs/current/)

##### PostGIS
- **Sitio Oficial de PostGIS** - [PostGIS.net](https://postgis.net/)
- **Carga de datos vectoriales en PostGIS** - [Gestión de datos en PostGIS](https://postgis.net/docs/manual-3.5/using_postgis_dbmanagement.html#loading-data)
- **Formatos Ráster en PostGIS** - [Uso de datos ráster en PostGIS](https://postgis.net/docs/using_raster_dataman)

##### Python y Librerías Científicas
1. **NumPy** - [Sitio Oficial](https://numpy.org/)
2. **Pandas** - [Documentación Oficial](https://pandas.pydata.org/docs/)
3. **GeoPandas** - [Documentación Oficial](https://geopandas.org/en/stable/)
4. **Scikit-Image** - [Documentación Oficial](https://scikit-image.org/docs/stable/)
5. **Scikit-Learn** - [Sitio Oficial](https://scikit-learn.org/stable/)
6. **Rasterio** - [Documentación Oficial](https://rasterio.readthedocs.io/en/latest/)
7. **Shapely** - [Documentación Oficial](https://shapely.readthedocs.io/en/stable/)
8. **Matplotlib** - [Documentación Oficial](https://matplotlib.org/stable/contents.html)

##### Jupyter y Entornos de Desarrollo
- **JupyterBook** - [Documentación Oficial](https://jupyterbook.org/en/stable/content/index.html)
- **Jupyter Notebook** - [Guía Oficial](https://jupyter.org/documentation)
- **VS Code para Python** - [Extensión Oficial](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
