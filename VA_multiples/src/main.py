##--------------------------------Main file------------------------------------
##
## Copyright (C) 2020 by Belinda Brown Ramírez (belindabrownr04@gmail.com)
##			June, 2020
##		   timna.brown@ucr.ac.cr
##-----------------------------------------------------------------------------

#            Variables aleatorias múltiples
# Se consideran dos bases de datos las cuales contienen los descrito
# a continuación:
# 1. ****** Registro de la frecuencia relativa de dos variables aleatorias
# conjuntas en forma de tabla:  xy.csv
# 2. ****** Pares (x, y) y su probabilidad asociada: xyp.csv
# Recordando que variable aleatoria es una función determinista.

####   ****************         Algoritmo            ****************   ####

#******************************************************
#               IMPORTANDO PAQUETES
#******************************************************
# Es importante considerar que notas son necesarias pero si
# fueron usadas durante el desarrollo de la tarea por diversas
# razones por lo cual se mantiene dentro del algortimo en forma
# comentario.
# from __future__ import division
# from pylab import *
# from sklearn import *
# from sklearn.preprocessing import PolynomialFeatures
# import math
# import decimal
# import pandas as pd
# from scipy.stats import norm
# from scipy.stats import rayleigh
# import csv
import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from mpl_toolkits.mplot3d import axes3d
from numpy import *
import numpy as np
from matplotlib import cm
import scipy.stats as stats
from scipy.optimize import curve_fit

#******************************************************
#               DEFINICIONES
#******************************************************
def distribucion_normal(va, mu, sigma):
	dist_normal = 1/(np.sqrt(2*np.pi*sigma**2)) * np.exp(-(va-mu)**2/(2*sigma**2))
	return dist_normal

def densidad_conjunta(va0,va1,mu0,sigma0,mu1,sigma1):
	val_conjunto = 1/((np.sqrt(2*np.pi*sigma0**2)) * np.exp(-(va0-mu0)**2/(2*sigma0**2)) * (1/(np.sqrt(2*np.pi*sigma1**2)) * np.exp(-(va1-mu1)**2/(2*sigma1**2))))
	return val_conjunto


def ajuste_curva(marginal, par1, par2, distri_norm, graph_label_dis, distri_x_name_img, func_graph_label, function_va_img):
	va = np.linspace(par1,par2,len(marginal))
	plt.bar(va, marginal, label= graph_label_dis)
	plt.legend()
	plt.savefig("/Users/belindabrown/Desktop/VA_multiples/results/" + distri_x_name_img + ".png")		
	parametros_va, _ = curve_fit(distri_norm, va, marginal)
	mu, sigma = parametros_va[0], parametros_va[1]
	print("\n\nMu " + distri_x_name_img + " =		", mu)
	print("Sigma " + distri_x_name_img + "  = 		", sigma)
	va_function = stats.norm(mu,sigma)
	curva_ajustada = np.linspace(va_function.ppf(0.01), va_function.ppf(0.99), 100)
	plt.plot(curva_ajustada,va_function.pdf(curva_ajustada),label=func_graph_label)
	plt.legend()
	plt.savefig("/Users/belindabrown/Desktop/VA_multiples/results/" + function_va_img+".png")		
	# #                   Limpia el area de graficacion
	plt.cla()
	return curva_ajustada, mu, sigma

def valor_esperado(marginal,lim_inferior,lim_superior, de_quien_v_valor_esperado):
	dominio = []
	valor_esperado_marginal = 0
	for k in range (5, lim_superior +1):
		dominio.append(k)
	dominio = list(OrderedDict.fromkeys(dominio))
	print("\n\nEl dominio es de:		", dominio)
	for i in range (0,len(marginal)):
	    valor_esperado_marginal = valor_esperado_marginal + dominio[i]*marginal[i]
	print("\n" +de_quien_v_valor_esperado +" tiene un valor de:	", valor_esperado_marginal)
	return valor_esperado_marginal

def grafica_en2d(mu_va, sigma_va, par1_modelo, nombre2d):
	va_funcion_distri = stats.norm(mu_va,sigma_va)
	curve = np.linspace(va_funcion_distri.ppf(0.01), va_funcion_distri.ppf(0.99), par1_modelo)
	plt.plot(curve,va_funcion_distri.pdf(curve),label=nombre2d)
	plt.legend()
	plt.savefig("/Users/belindabrown/Desktop/VA_multiples/results/" + nombre2d+".png")		
	# #                   Limpia el area de graficacion
	plt.cla()
	return

def grafica_en3d(VA0_modelo, VA1_modelo, VA0, VA1, nombre):
	Z = []
	for i in VA0:
		XY = []
		for j in VA1:
			XY.append(i*j)
		Z.append(XY)
	fig = plt.figure()
	eje_x= plt.axes(projection='3d')
	VA0,VA1 = np.meshgrid(VA0_modelo,VA1_modelo)
	eje_x.plot_surface(VA0,VA1,np.array(Z),cmap=cm.coolwarm)
	plt.savefig("/Users/belindabrown/Desktop/VA_multiples/results/" + nombre+".png")		
	return
#******************************************************
#               OBTENIENDO VALORES
#		   DE LOS CSV
#******************************************************
data = pd.read_csv("/Users/belindabrown/Desktop/VA_multiples/data_base/xy.csv", index_col=0)
data_xyp = pd.read_csv("/Users/belindabrown/Desktop/VA_multiples/data_base/xyp.csv")
#******************************************************
#               CURVA DE MEJOR AJUSTE
#		 DE LAS FUNCIONES DE
#             DENSIDAD MARGINALES X & Y
#******************************************************
# Se requieren los valores marginales tanto de x como de y
# Columna con la sumatoria de todas las columnas es la probabilidad marginal de X
marg_value_x = [n for n in data.sum(axis=1, numeric_only=True)]
# Fila con la sumatoria de todas las filas es la probabilidad marginal de Y
marg_value_y = [n for n in data.sum(axis=0, numeric_only=True)]
print("\nValor marginal de X: ", marg_value_x)
print("\nValor marginal de Y: ", marg_value_y)
x_curva_modelo, x_mu, x_sigma = ajuste_curva(marg_value_x, 5, 15, distribucion_normal, "Datos que pertenencen a X","Datos_de_X", "Modelos de X(x)", "Modelado_X(x)")
y_curva_modelo, y_mu, y_sigma = ajuste_curva(marg_value_y, 5, 25, distribucion_normal, "Datos que pertenencen a Y","Datos_de_Y", "Modelos de Y(y)", "Modelado_Y(y)")
#******************************************************
#               FUNCION DE DENSIDAD
#		   CONJUNTA DE
#       	     X & Y
#******************************************************
probabi_conjuntaX = distribucion_normal(x_curva_modelo,x_mu,x_sigma)
probabi_conjuntaY = distribucion_normal(y_curva_modelo,y_mu,y_sigma)
#******************************************************
#           VALORES DE CORRELACION, COVARIANZA
#	  COEFICIENTE DE CORRELACION (PEARSON)
#       	  Y SIGNIFICADO
#******************************************************
###### 	OBTENIDOS CON XY.CSV
# Se requieren los valores anteriormente calculados. Para calcular
# E[X] & E[Y] lo que se conoce como los valores.
# Valores inicializados de los valores de X y Y (E[X] y E[Y])
# Este rango es de [x0, x1], es decir, incluye los limites
e_x =  valor_esperado(marg_value_x,5,15, "X")
e_y =  valor_esperado(marg_value_y,5,25, "Y")
multi_valor_esperados =  e_x*e_y
# Se calcula E[X]*E[Y]
print("\n\nEl valor de E[X]E[Y] es de: ", multi_valor_esperados)
###### 	OBTENIDOS CON XYP.CSV
# Dado que la primera fila contiene las etiquetas de x, y, p
todos_mu_sum = data_xyp.x * data_xyp.y * data_xyp.p
# La sumatoria de E[XY] nos brinda su correlación
correlacion = todos_mu_sum.sum()
# Ahora para la covarianza, de acuerdo a lo visto en clase la
# covarianza es la correlacion menos la multiplicacion de los
# valores.
covarianza = correlacion - multi_valor_esperados
# Se requiere calcular el coeficiente de correlacion de
# Pearson en el cual se utilizan los valores de la data brindada de
# obtenidos entonces ...
# De acuerdo a los resultados obtenidos al correr el programa
# se ve que:
# SigmaDatos_de_X  = 		 3.2994428707078436
# SigmaDatos_de_Y  = 		 6.0269377486808775
# Para el coeficiente pearson se calcula como la covarianza
# divida entre la multiplicacion de los sigmas
coef_pearson = covarianza/(3.2994428707078436*6.0269377486808775)
print("\nEl resultado de la correlación es de: ", correlacion)
print("\nEl resultado de la covarianza es de: ",covarianza)
print("\nDe acuerdo a los datos obtenidos y considerando todo sus decimales se tiene que el coeficiente de Pearson es de: ", coef_pearson)
#******************************************************
#           GRAFICA EN 2D DE LAS FUNCIONES
#		DE DENSIDAD MARGINALES
#		        &
#	     GRAFICA EN 3D DE LA FUNCION
# 		DE DENSIDAD CONJUNTA
#******************************************************
# Dado que se requiere redondear los valores para la gráfica se toma en
# cuenta que los parámetros completos para el modelo serían los ya calculados
distribucion_de_x = grafica_en2d(x_mu, x_sigma, 100,"Distribucion_de_X")
distribucion_de_y = grafica_en2d(y_mu, y_sigma, 100,"Distribucion_de_Y")
dis_cojun3d = grafica_en3d(x_curva_modelo, y_curva_modelo, probabi_conjuntaX, probabi_conjuntaY, "Distribucion_en_3D")
