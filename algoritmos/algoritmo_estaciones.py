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
import numpy as np
import pandas as pd

# programa principal
def main():
	# constantes
	RUTA_CARPETA = "/home/jorge/Documents/Research/proyectoCaborca"
	
	# fecha actual
	fechaActual = strftime("%Y-%m-%d")

	# fecha -1
	anio, mes, dia = generarDiaAnterior(fechaActual)
	
	# generar ruta de archivos
	# rutaCarpetaDeArchivos = "{}/estaciones/{}-{:02d}-{:02d}".format(RUTA_CARPETA, anio, mes, dia)

	# ruta carpeta
	rutaCarpetaEstacionesMapas = "{}/estaciones/maps/{}-{:02d}-{:02d}".format(RUTA_CARPETA, anio, mes, dia)

	# crear carpeta de mapas
	if not os.path.exists(rutaCarpetaEstacionesMapas):
		os.mkdir(rutaCarpetaEstacionesMapas)	
	else:
		print("***** Carpeta ya existe")
	

	# datos de estaciones
	rutaArchivoEstaciones = "{}/estaciones/coor_est.csv".format(RUTA_CARPETA)
	dataEstaciones = pd.read_csv(rutaArchivoEstaciones)
		
	# ciclo
	# generar frame
	frames = []
	for i in range(1,6,1):
		print("valor de i:", i)
		# datos a procesar 
		rutaDatosEstaciones = "{}/estaciones/{}-{:02d}-{:02d}/{}.csv".format(RUTA_CARPETA, anio, mes, dia,i)
		print(rutaDatosEstaciones)
		dataTemp = pd.read_csv(rutaDatosEstaciones)
		print(dataTemp.head())
		
		# valor de longitud
		# latTemp = dataEstaciones.loc[dataEstaciones["ID"]==i]["Lat"]
		latTemp = dataEstaciones.iloc[i-1]["Lat"]
		print("***** lat", latTemp)
		dataTemp["Lat"] = latTemp
		
		# valor de latitud
		# lonTemp = dataEstaciones.loc[dataEstaciones["ID"]==i]["Long"]
		lonTemp = dataEstaciones.iloc[i-1]["Long"]
		dataTemp["Lon"] = lonTemp
		print("***** Lon", lonTemp)
		frames.append(dataTemp)
		print(dataTemp.head())

	# merge frames
	data =  pd.concat(frames)

	# array columnas a evaluar
	arrayColumns = ["PM1_1M", "PM1_5M","PM1_15M","PM2P5_1M","PM2P5_5M","PM2P5_15M","PM2P5_1H","PM1_1H","PM10_1M","PM10_5M","PM10_15M","PM10_1H"]

	# tiempos a mapear
	tiempos = np.array(data["Time"])
	tiempos = np.unique(tiempos)

	# ciclo de procesamiento
	for t in tiempos:
		# clasificar valores
		dataProcesamiento = data.loc[data["Time"] == t]

		for columna in arrayColumns:
			# determinar valores de x y y
			x_values = np.array(dataProcesamiento["Lon"])
			y_values = np.array(dataProcesamiento["Lat"])

			# ordenar valores
			x_values.sort()
			y_values.sort()

			# print
			print(x_values)
			print(y_values)

			# limites min y max
			LONG_MIN = x_values[0] - 0.1
			LONG_MAX = x_values[-1] + 0.1

			LAT_MIN = y_values[0] - 0.1
			LAT_MAX = y_values[-1] + 0.1

			# limites longitud > -115.65 y < -107.94
			dataProcesamiento = dataProcesamiento.loc[dataProcesamiento['Lon'] > LONG_MIN]
			dataProcesamiento = dataProcesamiento.loc[dataProcesamiento['Lon'] < LONG_MAX]

			# limites latitud > 25.41 y < 33.06
			dataProcesamiento = dataProcesamiento.loc[dataProcesamiento['Lat'] > LAT_MIN]
			dataProcesamiento = dataProcesamiento.loc[dataProcesamiento['Lat'] < LAT_MAX]

			# obtener valores de x, y
			lons = np.array(dataProcesamiento['Lon'])
			lats = np.array(dataProcesamiento['Lat'])

			
			# iniciar la gráfica
			#plt.clf()

			# agregar locación de estaciones
			xC = np.array(dataEstaciones['Long'])
			yC = np.array(dataEstaciones['Lat'])

			m = Basemap(projection='mill',llcrnrlat=LAT_MIN,urcrnrlat=LAT_MAX,llcrnrlon=LONG_MIN,urcrnrlon=LONG_MAX,resolution='h')

			# generar lats, lons
			#x, y = m(lons, lats)

			# numero de columnas y filas
			#numCols = len(x)
			#numRows = len(y)

			# generar xi, yi
			#xi = np.linspace(x.min(), x.max(), numCols)
			#yi = np.linspace(y.min(), y.max(), numRows)

			# generar el meshgrid
			#xi, yi = np.meshgrid(xi, yi)

			# generar zi
			z = np.array(dataProcesamiento[columna])
			#zi = gd((x,y), z, (xi,yi), method='cubic')

			# generar clevs
			#stepVariable = 1
			#step = (z.max() - z.min()) / 10

			# verificar el valor del intervalo
			#if step <= 1:
			#    stepVariable = 1

			#clevs = np.linspace(z.min(), z.max() + stepVariable , 10)
			#clevs = [1,2,3,4,5,6,7,8,9,10]

			# contour plot
			#cs = m.contourf(xi,yi,zi, clevs, zorder=5, alpha=0.5, cmap='PuBu')
			
			# agregar archivo shape de estados
			m.readshapefile('../shapes/Estados', 'Estados')

			# agregar puntos de estaciones
			m.scatter(xC, yC, latlon=True,s=z, cmap='coolwarm', marker='o', zorder=25)

			# colorbar
			#cbar = m.colorbar(cs, location='right', pad="5%")
			#cbar.set_label('mm')
			tituloTemporalParaElMapa = "{} {}-{:02d}-{:02d}".format(columna,anio,mes,dia)
			(tituloTemporalParaElMapa)

			# Mac /Users/jorgemauricio/Documents/Research/proyectoGranizo/Maps/{}_{}.png
			# Linux /home/jorge/Documents/Research/proyectoGranizo/Maps/{}_{}.png
			nombreTemporalParaElMapa = "{}/estaciones/maps/{}-{:02d}-{:02d}/{}.png".format(RUTA_CARPETA, anio, mes, dia, columna)
			plt.annotate('@2018 INIFAP', xy=(-109,29), xycoords='figure fraction', xytext=(0.45,0.45), color='g', zorder=50)

			plt.savefig(nombreTemporalParaElMapa, dpi=300)
			print('****** Genereate: {}'.format(nombreTemporalParaElMapa))
		

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

if __name__ == '__main__':
    main()