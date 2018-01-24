#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:17:25 2017

@author: jorgemauricio
"""

# librerías
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
	print("init procesamiento")
	iniciarProcesamiento()


def iniciarProcesamiento():
	# constantes
	LONG_MIN = -115.65
	LONG_MAX = -107.94
	LAT_MIN = 25.41
	LAT_MAX = 33.06

	# archivos a procesar
	# listaDeArchivos = [x for x in os.listdir('') if x.endswith('')]
	# nombre del archivo
	nombreArchivo = "GBBEPx.emis_co.001.20180122.nc"
	arrayNombreArchivo = nombreArchivo.split(".")
	arrayComponente = arrayNombreArchivo[1].split("_")
	nombreParaMapa = arrayComponente[1]
	rutaArchivo = "../data/2018-01-22/{}".format(nombreArchivo)

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
	fileName = '../temp/2018-01-22.csv'
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

	#%% contour plot
	cs = m.contourf(xi,yi,zi, clevs, zorder=5, alpha=0.5, cmap='PuBu')
	m.readshapefile('../shapes/Estados', 'Estados')

	#%% colorbar
	cbar = m.colorbar(cs, location='right', pad="5%")
	cbar.set_label('mm')
	tituloTemporalParaElMapa = "{} {}".format(nombreParaMapa, "2018-01-17")
	plt.title(tituloTemporalParaElMapa)

	# Mac /Users/jorgemauricio/Documents/Research/proyectoGranizo/Maps/{}_{}.png
	# Linux /home/jorge/Documents/Research/proyectoGranizo/Maps/{}_{}.png
	nombreTemporalParaElMapa = "/Users/jorgemauricio/Documents/Research/proyectoCaborca/maps/{}_2018-01-22.png".format(nombreParaMapa)
	plt.annotate('@2018 INIFAP', xy=(-109,29), xycoords='figure fraction', xytext=(0.45,0.45), color='g', zorder=50)

	plt.savefig(nombreTemporalParaElMapa, dpi=300)
	print('****** Genereate: {}'.format(nombreTemporalParaElMapa))

if __name__ == '__main__':
    main()
