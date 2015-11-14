#!/usr/bin/env python
# coding: utf-8
#encoding: latin1

import time
import os
import sys
import csv

def obtener_nombre_archivo():
    ''' Devuelve una cadena con el nombre de archivo de salida con el
    formato resultados_MMDD_HHSSMM.txt, correspondiente a la fecha y hora
    actual del sistema.
    '''
    return "resultados_" + time.strftime("%m%d_%H%M%S") + ".csv"


def exportar_resultados(resultados, cabecera, descripcion):
    ''' Graba en un archivo una descripción de la consulta realizada y los
    resultados en forma tabulada, agregando la cabecera correspondiente.
        Descripción debe ser una cadena descriptiva de la consulta
    realizada. Cabecera debe ser una tupla con el contenido de cada columna
    que va a tener la tabla de salida. Resultados debe ser una lista de
    tuplas.
        Devuelve el nombre del archivo que se grabó.
    '''
    file_out = obtener_nombre_archivo()
    '''Convierto el string a una tupla. De esta manera puedo insertar la
    descripcion de la la consulta realizada al CSV sin romperlo'''
    description = ()
    description = (descripcion,)
    #Capturo errores si los hay
    try:
        #Creo el archivo para file_out
        with open(file_out, mode='w', newline = '') as csvfile:

            f_out = csv.writer(csvfile, delimiter=',',
                                    quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            #Escribo en archivo descripcion en una sola celda
            f_out.writerow(description)
            #Escribo en archivo la cabecera (descripcion de columnas)
            f_out.writerow(cabecera)
            #Recorro lista de tuplas con los valores para escribir en el archivo
            for datos in resultados:
                f_out.writerow(datos)
            # Limpio areas de trabajo
            del f_out
    except:
        raise IOError('Error en el archivo {}'.format(file_out))
    #Si todo salio bien, retorno el archivo
    return file_out
