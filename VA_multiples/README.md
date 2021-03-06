#           Variables Múltiples 
----------
Modelos Probabilísticos de Señales y Sistemas

Universidad de Costa Rica

Belinda Brown, B61254

Junio, 2020

----------

## Correr el programa
Con el fin de probar el programa, se requieren revisar los paths contenidos en el main.py el cual se encuentra dentro de la carpeta de "src" ya que estos paths están dirigidos a mi máquina. Después de realizar esto se cuenta con un makefile el cual permite probar el algoritmo y limpiar la carpeta de "results" en donde se encuentran los resultados. Se siguen los siguientes comandos.

Para analizar todo lo requerido se debe ingresar:

**1. <path_donde_se_encuentra_el_folder>$ make analize**
 
Para borrar los resultados obtenidos se debe digitar:

**2. <path_donde_se_encuentra_el_folder>$ make clean**

## Paquetes importados
~~~~
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
~~~~

## Definiciones 
~~~~
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
~~~~

## Importanción de los valores en las bases de datos
~~~~
data = pd.read_csv("/Users/belindabrown/Desktop/VA_multiples/data_base/xy.csv", index_col=0)
data_xyp = pd.read_csv("/Users/belindabrown/Desktop/VA_multiples/data_base/xyp.csv")
~~~~

## Curva de mejor ajuste para las funciones de densidad marginales de X & Y
Apartir de los datos en las bases .csv,se encuentra la mejor curva de ajuste (modelo probabilístico) para las funciones de densidad marginales de X y Y. 

Para la curva de mejor ajuste se tiene que:

<img src="https://render.githubusercontent.com/render/math?math=f_{norm}(x) = \frac{1}{\sigma\sqrt{2\cdot\pi}} e^{ -\frac{1}{2} \left(\frac{x-\mu}{\sigma}\right)^2 }">

~~~~
# Se requieren los valores marginales tanto de x como de y
# Columna con la sumatoria de todas las columnas es la probabilidad marginal de X
marg_value_x = [n for n in data.sum(axis=1, numeric_only=True)]
# Fila con la sumatoria de todas las filas es la probabilidad marginal de Y
marg_value_y = [n for n in data.sum(axis=0, numeric_only=True)]
print("\nValor marginal de X: ", marg_value_x)
print("\nValor marginal de Y: ", marg_value_y)
x_curva_modelo, x_mu, x_sigma = ajuste_curva(marg_value_x, 5, 15, distribucion_normal, "Datos que pertenencen a X","Datos_de_X", "Modelos de X(x)", "Modelado_X(x)")
y_curva_modelo, y_mu, y_sigma = ajuste_curva(marg_value_y, 5, 25, distribucion_normal, "Datos que pertenencen a Y","Datos_de_Y", "Modelos de Y(y)", "Modelado_Y(y)")
~~~~

### Para X
![image](https://github.com/brown9804/Modelos_Probabilisticos/blob/master/VA_multiples/results/Datos_de_X.png)

![image](https://github.com/brown9804/Modelos_Probabilisticos/blob/master/VA_multiples/results/Modelado_X(x).png)

### Para Y
![image](https://github.com/brown9804/Modelos_Probabilisticos/blob/master/VA_multiples/results/Datos_de_Y.png)

![image](https://github.com/brown9804/Modelos_Probabilisticos/blob/master/VA_multiples/results/Modelado_Y(y).png)

## Función de densidad conjunta de X & Y

La función de densidad conjunta viene definida por:

<img src="https://render.githubusercontent.com/render/math?math=f_{XY}(x,y) = f_{X}(x) \cdot f_{Y}(y)">

~~~~
probabi_conjuntaX = distribucion_normal(x_curva_modelo,x_mu,x_sigma)
probabi_conjuntaY = distribucion_normal(y_curva_modelo,y_mu,y_sigma)
~~~~

## Valores de correlación , covarianza y coeficiente de correlación de Pearson junto con su significado
Considerando lo investigado en clase y en las lecciones se toma en cuenta "E[Y]*E[X]". 

Recordando la definición de **correlación**, se tiene que: es el grado de similitud que poseen dos variables aleatorias entre sí. Por definición sabemos que las variables aleatorias son deterministas, así como la correlación entre ellas no necesariamente signigica que existe causalidad entre ellas. 

Considerando la siguientes fórmula donde R[XY] es la correlación:

<img src="https://render.githubusercontent.com/render/math?math=R_{XY}=\displaystyle\sum_{i=inferior}^{superior}\displaystyle\sum_{j=inferior}^{superior} x_i y_j P(x_i,y_j)">


Ahora bien, la **covarianza** covarianza nos permite identificar de acuerdo a su valor obtenido si las variables aleatorias son independientes o bien dependientes. De acuerdo a la definición, permite saber la magnitud en la crece una variable aleatoria respecto a otra así como su tendencia ya sea decreciente o creciente siguiendo su analogía con el signo del valor obtenido.

Para esta sección se tiene que C[XY] es la covarianza y R[XY] es la correlación.

<img src="https://render.githubusercontent.com/render/math?math=E[Y] = \sum_{i=1}^{k} y_i p_{y_i}">

<img src="https://render.githubusercontent.com/render/math?math=E[X] = \sum_{i=1}^{k} x_i p_{x_i}">

<img src="https://render.githubusercontent.com/render/math?math=C_{XY} = R_{XY} - E\left[ X \right] E\left[ Y \right]">


Finalemente, **coeficiente de correlación de Pearson** se conoce como uno de los momentos que poseen las variables aleatorias, siento este normalizado entre -1 a 1. Este momento se puede analizar mediante la siguiente lógica: de -1 a 0 refiere a una correlación negativa y de 0 a 1 refiere a una positiva en donde se mantiene lo descrito anteriormente, referido a la correlación. 

Tenemos que el coeficiente Pearson viene dado por:

<img src="https://render.githubusercontent.com/render/math?math=\rho = \frac{C_{XY}}{\sigma_X\sigma_Y}">

~~~~
###### 			OBTENIDOS CON XY.CSV
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
~~~~

Los resultados númericos de esta sección se encuentran en la sección de "Resultados númericos".

## Gráfica en 2D de densidades marginales y gráfica en 3D de la densidad conjunta
Esta sección corresponde a las llamadas de las funciones (anteriormente definidas) por medio del siguiente código:

~~~~
# Dado que se requiere redondear los valores para la gráfica se toma en
# cuenta que los parámetros completos para el modelo serían los ya calculados
distribucion_de_x = grafica_en2d(x_mu, x_sigma, 100,"Distribucion_de_X")
distribucion_de_y = grafica_en2d(y_mu, y_sigma, 100,"Distribucion_de_Y")
dis_cojun3d = grafica_en3d(x_curva_modelo, y_curva_modelo, probabi_conjuntaX, probabi_conjuntaY, "Distribucion_en_3D")
~~~~

### Para densidad marginal en 2D de X
![image](https://github.com/brown9804/Modelos_Probabilisticos/blob/master/VA_multiples/results/Distribucion_de_X.png)

### Para densidad marginal en 2D de Y
![image](https://github.com/brown9804/Modelos_Probabilisticos/blob/master/VA_multiples/results/Distribucion_de_Y.png)

### Para la densidad conjunta en 3D
![image](https://github.com/brown9804/Modelos_Probabilisticos/blob/master/VA_multiples/results/Distribucion_en_3D.png)


## Resultados númericos
![image](https://github.com/brown9804/Modelos_Probabilisticos/blob/master/VA_multiples/results/resultados_numericos.png)


