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

def main():
	print("Init")

def iniciarDescarga():
	# Constantes
	URL_DESCARGA = "http://satepsanone.nesdis.noaa.gov/pub/FIRE/GBBEPx"
	arrayElementos = ['bc','co', 'co2','oc','pm25','so2']
	# Mac /Users/jorgemauricio/Documents/Research/proyectoCaborca
    # Linux /home/jorge/Documents/Research/proyectoCaborca
	URL_CARPETA_DATA = "/Users/jorgemauricio/Documents/Research/proyectoCaborca/data"

	# fecha actual
	fechaPronostico = strftime("%Y-%m-%d")

	# fecha - 1
	anio, mes, dia = generarDiaAnterior(fechaPronostico)

	# nombre de la ruta para la descarga
	rutaDeCarpetaParaDescarga = '{}/{}-{:02d}-{:02d}'.format(URL_CARPETA_DATA,anio,mes,dia)

	# crear carpeta apra descarga
	os.mkdir(rutaDeCarpetaParaDescarga)

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

