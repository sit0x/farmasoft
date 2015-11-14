#!/usr/bin/env python
# coding: utf-8
#encoding: latin1

import csv
import os
from operator import itemgetter

list_datos = []
dicc_clientes = {}

def leer_datos(datos):
    '''Funcion que devuelve el siguiente registro o nose si no hay más'''
    try:
        return next(datos)
    except:
        return None

def obtener_indices(cabecera):
    '''Funcion para obtener indices de las columnas de la cabecera'''
    #Limpio el diccionario
    dicc_clientes.clear()
    #for index,row in enumerate(cabecera):
        #print(row)
    #Obtengo indices de las columnas de la cabecera
    try:
        for index,row in enumerate(cabecera):
            if row == 'CLIENTE':
                dicc_clientes['CLIENTE']    = index
            elif row == 'CODIGO':
                dicc_clientes['CODIGO']     = index
            elif row == 'PRODUCTO':
                dicc_clientes['PRODUCTO']   = index
            elif row == 'CANTIDAD':
                dicc_clientes['CANTIDAD']   = index
            elif row == 'PRECIO':
                dicc_clientes['PRECIO']     = index
    except:
        raise IOError('Error al cargar indices')
    #Devuelvo el diccionario con los indices de las columnas
    return dicc_clientes

def cargar_archivo(nombre_archivo):
    ''' Recibe el nombre de un archivo y devuelve una estructura de datos
    con su contenido.
        En caso de error levanta una RunnableException con un mensaje
    descriptivo.
    '''
    if os.path.exists(nombre_archivo):
        archivo = open(nombre_archivo)
        archivo_csv = csv.reader(archivo)
    else:
        raise IOError("""
        Error al abrir el archivo {}, compruebe el nombre o directorio."""
        .format(nombre_archivo))
    ''' Obtengo el indice de las columnas para luego validar datos y sus tipos de
    datos
    '''
    #Leo la cabecera del archivo
    read = False
    #Se valida en caso de que la primer/as lineas sean vacias
    while read == False:
        item = leer_datos(archivo_csv)
        if item != None:
            read = True
        """Valido cantidad de columnas en la cabecera. Debe tener 5 columnas,
        sino capturo error"""
        if len(item) != 5:
            raise IOError("""
            El archivo debe tener 5 columnas y tiene {}""".format(len(item)))
    '''Llamo a la funcion que carga los indices de las columnas del archivo
    csv'''
    #Llamo a la funcion
    obtener_indices(item)

    #Limpio la lista con los datos
    del list_datos[:]

    #Obtengo el archivo completo
    reader = csv.reader(archivo)

    try:
        #Itero el archivo para cargarlo en una lista y poder trabar con ella
        for row in reader:
            if '' in row:
                raise IOError("""
                La línea {} no posee completo todos sus campos. """
                .format(reader.line_num))
            #Valido que el valor de la columna CANTIDAD sea un entero
            try:
                entero = int(row[dicc_clientes['CANTIDAD']])
            except:
                raise IOError("""
                La línea {} posee un valor no entero en la columna 'CANTIDAD'."""
                .format(reader.line_num))
            #Valido que el valor de la columna PRECIO sea un decimal
            try:
                decimal = float(row[dicc_clientes['PRECIO']])
            except:
                raise IOError("""
                La línea {} posee un valor no decimal en la columna 'PRECIO'."""
                .format(reader.line_num))
            #Agrego el registro a la lista
            list_datos.append(row)
        ''' Cierro el archivo '''
        archivo.close()
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(nombre_archivo, reader.line_num, e))
    #Devuelvo la lista con los valores
    return list_datos

def obtener_clientes_con_nombre_incompleto(archivo, nombre_cliente_incompleto):
    ''' Dado el contenido del archivo de datos y un nombre de cliente
    incompleto, devuelve una lista con todos los nombres de clientes sin
    repetir (obtenidos de la columna CLIENTE del archivo) cuyo nombre
    contenga la cadena incompleta pasada por parámetro.
    '''
    list_datos = []
    try:
        #Itero archivo y guardo en una lista los clientes encontrados
        for datos in archivo:
            if nombre_cliente_incompleto in datos[dicc_clientes['CLIENTE']]:
                if datos[dicc_clientes['CLIENTE']] not in list_datos:
                    list_datos.append(datos[dicc_clientes['CLIENTE']])
        #Devuelvo lista con los clientes
        return list_datos
    except:
        raise IOError('Error al buscar clientes con nombre incompleto')

def obtener_productos_con_nombre_incompleto(archivo, nombre_producto_incompleto):
    ''' Dado el contenido del archivo de datos y un nombre de producto
    incompleto, devuelve una lista con todos los nombres de productos sin
    repetir (obtenidos de la columna PRODUCTO del archivo) cuyo nombre
    contenga la cadena incompleta pasada por parámetro.
    '''
    list_datos = []
    try:
        for datos in archivo:
            if nombre_producto_incompleto in datos[dicc_clientes['PRODUCTO']]:
                if datos[dicc_clientes['PRODUCTO']] not in list_datos:
                    list_datos.append(datos[dicc_clientes['PRODUCTO']])
        return list_datos
    except:
        raise IOError('Error al buscar productos con nombre incompleto')
#    raise NotImplementedError

def obtener_productos_comprados_por_cliente(archivo, nombre_cliente):
    ''' Dado el contenido del archivo de datos y el nombre de un cliente,
    devuelve una lista de todos los nombres de productos comprados por
    el cliente, sin repetir.
    '''
    list_products = []
    #Itero archivo y guardo en una lista los productos comprados por el cliente
    try:
        for datos in archivo:
            if datos[dicc_clientes['CLIENTE']] == nombre_cliente:
                tuple_products = (datos[dicc_clientes['PRODUCTO']])
                list_products += [tuple_products]

        return list_products
    except:
        raise IOError('Error al buscar productos comprados por un cliente')


def obtener_clientes_de_producto(archivo, nombre_producto):
    ''' Dado el contenido del archivo de datos y el nombre de un producto,
    devuelve una lista de todos los compradores del producto, sin repetir.
    '''
    list_clients = []
    #Itero archivo y guardo en una lista los compradores de un producto
    try:
        for datos in archivo:
            if datos[dicc_clientes['PRODUCTO']] == nombre_producto:
                tuple_clients = (datos[dicc_clientes['CLIENTE']])
                list_clients += [tuple_clients]

        return list_clients
    except:
        raise IOError('Error al buscar clientes que compraron un producto')

def obtener_productos_mas_vendidos(archivo, cantidad_maxima_productos):
    ''' Devuelve una lista de tuplas de tamaño pasado por parámetro que
    representan los productos más vendidos, conteniendo como primer elemento
    el nombre del producto y como segundo elemento la cantidad de ventas.
#    '''
    dicc_products = {}

    '''Recorro el archivo para poder identificar los productos  sin repetir y
    totalizarlos. Una vez obtenidos todos los datos en un diccionario, lo sorteo
    en una lista de tuplas de manera descendente para poder tomar la cantidad de
    productos mas vendidos'''
    for datos in archivo:
        #Si el producto no existe lo agrego. De lo contrario sumo cantidad.
        if datos[dicc_clientes['PRODUCTO']] not in dicc_products:
            dicc_products[datos[dicc_clientes['PRODUCTO']]] = int(datos[dicc_clientes['CANTIDAD']])
        else:
            dicc_products[datos[dicc_clientes['PRODUCTO']]] += int(datos[dicc_clientes['CANTIDAD']])

    #Sorteo el diccionario y lo guardo en una lista de tuplas
    sorted_x = sorted(dicc_products.items(), key=itemgetter(1), reverse=True)

    #Elimino los productos que no requiero de la lista de tuplas
    del sorted_x[cantidad_maxima_productos:]
    #Devuelvo lista de tuplas
    return sorted_x

def obtener_clientes_mas_gastadores(archivo, cantidad_maxima_clientes):
    ''' Devuelve una lista de tuplas de tamaño pasado por parámetro que
    representan los clientes que más gastaron, conteniendo como primer
    elemento el nombre del cliente y como segundo elemento el monto gastado.
    '''
    dicc_spenders_clients = {}

    '''Recorro el archivo para poder identificar los clientes sin repetir y
    totalizar su precio. Una vez obtenidos todos los datos en un diccionario,
    lo sorteo en una lista de tuplas de manera descendente para poder tomar la
    cantidad maxima de clientes mas gastadores'''
    for datos in archivo:
        #Si el cliente no existe lo agrego. De lo contrario sumo el precio.
        if datos[dicc_clientes['CLIENTE']] not in dicc_spenders_clients:
            dicc_spenders_clients[datos[dicc_clientes['CLIENTE']]] = \
                                        float(datos[dicc_clientes['PRECIO']])
        else:
            dicc_spenders_clients[datos[dicc_clientes['CLIENTE']]] += \
                                        float(datos[dicc_clientes['PRECIO']])

    #Sorteo el diccionario y lo guardo en una lista de tuplas
    sorted_x = sorted(dicc_spenders_clients.items(), key=itemgetter(1),
                                                                reverse=True)

    #Elimino los productos que no requiero de la lista de tuplas
    del sorted_x[cantidad_maxima_clientes:]
    #Devuelvo lista de tuplas
    return sorted_x
