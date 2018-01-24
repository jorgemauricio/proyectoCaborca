#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:17:25 2017

@author: jorgemauricio
"""

# librerías
import os
import urllib.request
import time
from time import gmtime, strftime
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from numpy import meshgrid
from scipy.interpolate import griddata as gd
import os
from netCDF4 import Dataset
import numpy as np
import pandas as pd


# programa principal
def main():
	# descargar información
	print("Iniciar descarga de archivos")
	iniciarDescarga()

	# procesamiento información
	print("Iniciar procesamiento de archivos")
	iniciarProcesamiento()

def iniciarDescarga():
	
	# ***** constantes
	URL_DESCARGA = "http://satepsanone.nesdis.noaa.gov/pub/FIRE/GBBEPx"
	
	# elementos
	arrayElementos = ['bc','co', 'co2','oc','pm25','so2']
	# Mac /Users/jorgemauricio/Documents/Research/proyectoCaborca
	# Linux /home/jorge/Documents/Research/proyectoCaborca
	URL_CARPETA = "/Users/jorgemauricio/Documents/Research/proyectoCaborca"
	
	# fecha actual
	fechaActual = strftime("%Y-%m-%d")

	# fecha -1
	anio, mes, dia = generarDiaAnterior(fechaActual)

	# nombre de la ruta para la descarga
	rutaDeCarpetaParaDescarga = '{}/data/{}-{:02d}-{:02d}'.format(URL_CARPETA,anio,mes,dia)

	# nombre de la ruta para guardar temporales
	rutaDeCarpetaParaTemporales = '{}/temp/{}-{:02d}-{:02d}'.format(URL_CARPETA,anio,mes,dia)

	# nombre de la ruta para guardar mapas
	rutaDeCarpetaParaMapas = '{}/maps/{}-{:02d}-{:02d}'.format(URL_CARPETA,anio,mes,dia)

	# crear carpeta para descarga
	os.mkdir(rutaDeCarpetaParaDescarga)

	# crear carpeta para guardar mapas
	os.mkdir(rutaDeCarpetaParaMapas)

	# crear carpeta para guardar archivos temporales
	os.mkdir(rutaDeCarpetaParaTemporales)

	# cambiar a carpeta de descarga
	os.chdir(rutaDeCarpetaParaDescarga)

	# ciclo de descarga
	for i in arrayElementos:
		# crear nombre temporal de archivo a descargar
		urlDescarga = "{}/GBBEPx.emis_{}.001.{}{:02d}{:02d}.nc".format(URL_DESCARGA,i,anio,mes,dia)
		nombreDelArchivo =  "GBBEPx.emis_{}.001.{}{:02d}{:02d}.nc".format(i,anio,mes,dia)
		print("***** Descarga de archivo: {}".format(nombreDelArchivo))
		descargaArchivo(urlDescarga, nombreDelArchivo)


def descargaArchivo(ud, na):
	"""
	Función que permite la descarga del archivo indicado
	param: ud: url de descarga
	param: na: nombre del archivo
	"""
	urllib.request.urlretrieve(ud, na)


def generarDiaAnterior(f):
	"""
	Función que permite conocer el día anterior para descargar el archivo
	param: f: fecha actual
	"""
	anio, mes, dia = f.split('-')
	anio = int(anio)
	mes = int(mes)
	dia = int(dia)

	dia -= 1

	if dia == 0:
		mes -= 1
		if mes == 0:
			anio -= 1
			mes = 12
			diasEnElMes = numeroDeDiasEnElMes(mes)
	
	return (anio, mes, dia)

def numeroDeDiasEnElMes(m):
	"""
	Función que permite saber el número de días en un mes
	param: m: mes actual
	"""
	if mes == 2 and anio % 4 == 0:
		return 29
	elif mes == 2 and anio % 4 != 0:
		return 28
	elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
		return 31
	elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
		return 30

def iniciarProcesamiento():
	
	# Mac /Users/jorgemauricio/Documents/Research/proyectoCaborca
	# Linux /home/jorge/Documents/Research/proyectoCaborca
	URL_CARPETA = "/Users/jorgemauricio/Documents/Research/proyectoCaborca"
	
	# coordenadas estaciones
	dataEstaciones = pd.read_csv("/Users/jorgemauricio/Documents/Research/proyectoCaborca/data/coordenadas_estaciones.csv")
	
	# fecha actual
	fechaActual = strftime("%Y-%m-%d")

	# fecha -1
	anio, mes, dia = generarDiaAnterior(fechaActual)

	# nombre de la ruta para la descarga
	rutaDeCarpetaParaElProcesamiento = '{}/data/{}-{:02d}-{:02d}'.format(URL_CARPETA,anio,mes,dia)

	# constantes
	LONG_MIN = -115.65
	LONG_MAX = -107.94
	LAT_MIN = 25.41
	LAT_MAX = 33.06

	# archivos a procesar
	listaDeArchivos = [x for x in os.listdir(rutaDeCarpetaParaElProcesamiento) if x.endswith('.nc')]
	
	# ciclo de procesamiento
	for archivo in listaDeArchivos:
		# nombre del archivo
		# nombreArchivo = "GBBEPx.emis_so2.001.20180118.nc"
		arrayNombreArchivo = archivo.split(".")
		arrayComponente = arrayNombreArchivo[1].split("_")
		nombreParaMapa = arrayComponente[1]
		rutaArchivo = "{}/{}".format(rutaDeCarpetaParaElProcesamiento, archivo)

		# leer el archivo netcdf
		dataset = Dataset(rutaArchivo)

		# generar las arreglos de las variables
		biomass = dataset.variables['biomass'][:]
		Latitude = dataset.variables['Latitude'][:]
		Longitude = dataset.variables['Longitude'][:]

		# variable para generar CSV
		dataText = "Long,Lat,Biomass\n"

		# procesamiento de información
		for i in range(Longitude.shape[0]):
		    for j in range(Latitude.shape[0]):
		        tempText = "{},{},{}\n".format(Longitude[i], Latitude[j], biomass[0,j,i])
		        dataText += tempText

		# generar archivo temporal csv
		fileName = "{}/temp/{}-{:02d}-{:02d}/{}.csv".format(URL_CARPETA, anio, mes, dia, nombreParaMapa)
		textFile = open(fileName, "w")
		textFile.write(dataText)
		textFile.close()

		# leer el archivo temporal csv
		data = pd.read_csv(fileName)

		# limites longitud > -115.65 y < -107.94
		data = data.loc[data['Long'] > LONG_MIN]
		data = data.loc[data['Long'] < LONG_MAX]

		# limites latitud > 25.41 y < 33.06
		data = data.loc[data['Lat'] > LAT_MIN]
		data = data.loc[data['Lat'] < LAT_MAX]

		# obtener valores de x, y
		lons = np.array(data['Long'])
		lats = np.array(data['Lat'])

		#%% iniciar la gráfica
		plt.clf()

		# agregar locación de estaciones
		xC = np.array(dataEstaciones['Long'])
		yC = np.array(dataEstaciones['Lat'])

		m = Basemap(projection='mill',llcrnrlat=LAT_MIN,urcrnrlat=LAT_MAX,llcrnrlon=LONG_MIN,urcrnrlon=LONG_MAX,resolution='h')

		# generar lats, lons
		x, y = m(lons, lats)

		# numero de columnas y filas
		numCols = len(x)
		numRows = len(y)

		# generar xi, yi
		xi = np.linspace(x.min(), x.max(), numCols)
		yi = np.linspace(y.min(), y.max(), numRows)

		# generar el meshgrid
		xi, yi = np.meshgrid(xi, yi)

		# generar zi
		z = np.array(data['Biomass'])
		zi = gd((x,y), z, (xi,yi), method='cubic')

		# generar clevs
		stepVariable = 1
		step = (z.max() - z.min()) / 10

		# verificar el valor del intervalo
		if step <= 1:
		    stepVariable = 1

		clevs = np.linspace(z.min(), z.max() + stepVariable , 10)
		#clevs = [1,2,3,4,5,6,7,8,9,10]

		# contour plot
		cs = m.contourf(xi,yi,zi, clevs, zorder=5, alpha=0.5, cmap='PuBu')
		
		# agregar archivo shape de estados
		m.readshapefile('shapes/Estados', 'Estados')

		# agregar puntos de estaciones
		m.scatter(xC, yC, latlon=True,s=1, marker='o', color='r', zorder=25)

		# colorbar
		cbar = m.colorbar(cs, location='right', pad="5%")
		cbar.set_label('mm')
		tituloTemporalParaElMapa = "{} {}-{:02d}-{:02d}".format(nombreParaMapa,anio,mes,dia)
		plt.title(tituloTemporalParaElMapa)

		# Mac /Users/jorgemauricio/Documents/Research/proyectoGranizo/Maps/{}_{}.png
		# Linux /home/jorge/Documents/Research/proyectoGranizo/Maps/{}_{}.png
		nombreTemporalParaElMapa = "/Users/jorgemauricio/Documents/Research/proyectoCaborca/maps/{}-{:02d}-{:02d}/{}.png".format(anio, mes, dia, nombreParaMapa)
		plt.annotate('@2018 INIFAP', xy=(-109,29), xycoords='figure fraction', xytext=(0.45,0.45), color='g', zorder=50)

		plt.savefig(nombreTemporalParaElMapa, dpi=300)
		print('****** Genereate: {}'.format(nombreTemporalParaElMapa))

if __name__ == '__main__':
    main()