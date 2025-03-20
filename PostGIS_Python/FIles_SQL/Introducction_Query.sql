CREATE EXTENSION postgis;

SELECT postgis_version();

CREATE TABLE antenas (
	id_antena SERIAL PRIMARY KEY,
	nombre VARCHAR(50),
	geom GEOMETRY(Point, 4326)
);

INSERT INTO antenas(nombre, geom)
VALUES
('Antena A', ST_GeomFromText('POINT(-74.005 40.7128)', 4326)),
('Antena B', ST_GeomFromText('POINT(-73.98 40.75)', 4326));


SELECT * FROM antenas;
SELECT nombre, ST_AsText(geom) FROM antenas;

SELECT nombre FROM antenas
	WHERE ST_DWithin(geom, ST_GeomFromText('POINT(-74.00 40.71)', 4326), 10);
	
	
/* Ejercicio: Selección de muestras según AOI para entrenamiento de algoritmo */

CREATE TABLE muestras_suelo(
	id_muestra SERIAL PRIMARY KEY,
	tipo_suelo VARCHAR(50),
	geom GEOMETRY(Polygon, 4326)
);

INSERT INTO muestras_suelo (tipo_suelo, geom) VALUES 
('Arcilloso', ST_GeomFromText('POLYGON((-74.1 40.7, -74.1 40.8, -74.0 40.8, -74.0 40.7, -74.1 40.7))', 4326)),
('Arenoso', ST_GeomFromText('POLYGON((-74.2 40.6, -74.2 40.7, -74.1 40.7, -74.1 40.6, -74.2 40.6))', 4326)),
('Rocoso', ST_GeomFromText('POLYGON((-74.3 40.7, -74.3 40.8, -74.2 40.8, -74.2 40.7, -74.3 40.7))', 4326));

SELECT tipo_suelo, ST_AsText(geom), geom FROM muestras_suelo;

WITH aoi AS (
    SELECT ST_GeomFromText('POLYGON((-74.15 40.65, -74.15 40.75, -74.05 40.75, -74.05 40.65, -74.15 40.65))', 4326) AS geom
)
SELECT m.id_muestra, m.tipo_suelo, ST_AsText(m.geom)
FROM muestras_suelo m, aoi
WHERE ST_Intersects(m.geom, aoi.geom);

