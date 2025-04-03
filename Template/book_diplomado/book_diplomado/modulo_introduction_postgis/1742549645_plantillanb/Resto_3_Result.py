import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import os

# ---------- CONFIGURACIÓN ----------
ruta_shapefile = "./Samples/Samples_Point.shp"  # Cambiar según corresponda
DB_URL = "postgresql://postgres:postgres@localhost:5432/postgis_34_sample"
SRID = 32619  # Sistema de referencia espacial (modifica según tu caso)

# Leer archivo y reproyectar si es necesario
gdf = gpd.read_file(ruta_shapefile)
gdf = gdf.to_crs(epsg=SRID)

# Detectar el tipo de geometría principal
tipo_geom = gdf.geom_type.unique()
if len(tipo_geom) > 1:
    print("Advertencia: el shapefile contiene múltiples tipos de geometría. Se tomará el primero.")
geometry_type = tipo_geom[0].upper()  # Por ejemplo: POINT, LINESTRING, POLYGON

# ---------- MAPEO DE TIPOS DE COLUMNA ----------
def map_dtype_to_sqlalchemy(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return Integer
    elif pd.api.types.is_float_dtype(dtype):
        return Float
    elif pd.api.types.is_bool_dtype(dtype):
        return Boolean
    else:
        return String

# ---------- CREAR CLASE ORM DINÁMICAMENTE ----------
Base = declarative_base()
columnas = [col for col in gdf.columns if col != "geometry"]

atributos = {
    '__tablename__': 'muestras_generales',
    'id': Column(Integer, primary_key=True, autoincrement=True),
    'geom': Column(Geometry(geometry_type=geometry_type, srid=SRID))
}

for col in columnas:
    atributos[col] = Column(map_dtype_to_sqlalchemy(gdf[col].dtype))

# Crear clase ORM
TablaMuestras = type("TablaMuestras", (Base,), atributos)

# ---------- CONECTAR Y CARGAR DATOS ----------
engine = create_engine(DB_URL)
Base.metadata.drop_all(engine)  # Opcional
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Insertar registros
for _, fila in gdf.iterrows():
    datos = {col: fila[col] for col in columnas}
    datos["geom"] = fila.geometry.wkt
    session.add(TablaMuestras(**datos))

session.commit()
session.close()
