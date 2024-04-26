import numpy as np
import matplotlib.pyplot as plt

#Se empieza defininiendo el dataset el cual se va a usar, en este caso se realizara una compuerta and
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([-1,-1,-1,1]) # En este caso se va a trabajar con un escalon bipolar, por lo que se define de esa manera

# # Graficar los datos de la tabla AND
# plt.scatter(X[0:3, 0], X[0:3, 1],
#             color='red', marker='o', label='Clase 0')
# plt.scatter(X[3, 0], X[3, 1],
#             color='blue', marker='x', label='Clase 1')

# #Activar la grilla (líneas menores de la cuadrícula)
# plt.minorticks_on()

# #Activar la grilla principal, mantener la principal y las líneas menores, estilo punteado --, color gris y grosor .5
# plt.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)

# #Colocar las etiquetas
# plt.xlabel('Característica A ($X_1$)')
# plt.ylabel('Característica B ($X_2$)')

# #plt.savefig('AND_space.png', dpi=300)
# plt.show()

#Ahora se va a crear la clase Perceptron, la cual tendra toda la logica de como es el funcionamiento de este

class Perceptron(object):
    """"
    Se empieza definiendo una funcion con los parametros los cuales se usaran de entrada, y los cuales son modificables si lo desea la persona
    Tenemos el learning rate el cual es un parametro que nos ayuda a poder modificar el tamaño de los pasos que va a dar en el momento de hacer el entrenamiento para poder buscar una convergencia
    Un tamaño alto de learning rate puede hacer que aprenda rapido o en otros casos se salte el minimo global, y un tamaño bajo hara que se demore mas lo que significa un gasto computacional mayor
    los numeros de iteraciones es la cantidad de veces que se repitara el proceso
    la funcion de activacion es esa funcion donde definimos si va a ser unipolar o bipolar
    y una semilla la cual nos permite hacer los procesos mas reproducibles
    """
    def __init__(self, learning_rate=0.01,n_iterations=50, af='step_function',Rw=0,random_state=1):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.af = af
        self.Rw = Rw
        self.random_state = random_state
    
    """
    Ahora se procede a hacer el entrenamiendo, donde lo primero que se define es la semilla que se usa, la cual se genera de una manera random
    Despues tenemos la definicion de como se manejaran los pesos de la cual hay dos maneras diferentes para poder hacerlo
    donde por ultimo tenemos ese entrenamiento que se hace a el modelo, esto se hace gracias a una funcion la cual es predict, que con los lo que hace es que gracias a la funcion de activacion 
    va a ir dando una prediccion del valor de entrenamiento, y depues este valor se resta al de la prediccion real obteniendo asi ese error el cual se busca disminuir hasta llegar a 0,
    estos valores de los errores se almacenan y ayudan a ir mejorando la prediccion de las siguientes iteraciones

    La funcion predict gracias a su funcion de producto  punto ayuda a poder realizar esas predicciones las cuales se buscaran mejorar con ayuda de las iteraciones

    """

    def fit(self,X,y):
        rgen = np.random.RandomState(self.random_state)

        if(self.Rw == 0):
            self.w_ = rgen.normal(loc=0.0, scale=0.01,size=1 + X.shape[1])
        elif(self.Rw == 1):
            lower_bound = -25
            upper_bond = 25
            self.w_ = rgen.uniform(low=lower_bound, high=upper_bond, size = 1 + X.shape[1])
            self.w_[1:] = np.where(self.w_[1:] == 0, np.random.choice([-1, 1], size=self.w_[1:].shape) * 0.0001, self.w_[1:])
        else:
            print("Numero diferente a 0 o 1")
        
        self.errors_ = []
        self.w_historical = [self.w_.copy()]

        for _ in range(self.n_iterations):
            errors = 0
            for x1,target in zip(X,y):
                update = self.learning_rate * (target - self.predict(x1))
                self.w_[1:] += update * x1
                self.w_[0] += update
                errors += int(update != 0)
            self.errors_.append(errors)
            self.w_historical.append(self.w_.copy())
        return self

    def net_input(self,X):
        return np.dot(X,self.w_[1:]) + self.w_[0]
    
    def predict(self, X):
        activation_function = self.af

        if(activation_function == 'step_function'):
            return np.where(self.net_input(X) >= 0.0 , 1.0, 0)
        elif(activation_function == 'bipolar_step_function'):
            return np.where(self.net_input(X) >= 0.0, 1.0, -1.0)
        else:
            print("Error, solo puede ser 'step_function', o 'bipolar_step_function'")


ppn =Perceptron(learning_rate=0.2, n_iterations=100, af='bipolar_step_function', Rw=1)
ppn.fit(X,y)
print(ppn.w_historical)
print(ppn.errors_)

plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, marker='o')

#Activar la grilla (líneas menores de la cuadrícula)
plt.minorticks_on()

#Activar la grilla principal, mantener la principal y las líneas menores, estilo punteado --, color gris y grosor .5
plt.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)

plt.xlabel('Épocas')
plt.ylabel('Error')

plt.savefig('Grafico del error.png', dpi=300)

# Graficar los datos de la tabla AND
plt.scatter(X[0:3, 0], X[0:3, 1],
            color='red', marker='o', label='Clase 0')
plt.scatter(X[3, 0], X[3, 1],
            color='blue', marker='x', label='Clase 1')

#Activar la grilla (líneas menores de la cuadrícula)
plt.minorticks_on()

#Activar la grilla principal, mantener la principal y las líneas menores, estilo punteado --, color gris y grosor .5
plt.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)

# Obtener valores mínimo y máximo de la columna 1 de X
x1_min = np.min(X[:, 0])
x1_max = np.max(X[:, 0])

# Generar valores equiespaciados para X1
X1 = np.arange(x1_min - 0.1, x1_max + 0.1, 0.1)

Lw_historical = len(ppn.w_historical)

vectorW_temp = ppn.w_historical[0]

b= vectorW_temp[0]
w1= vectorW_temp[1]
w2= vectorW_temp[2]


# Calcular los valores correspondientes de X2
X2 = -(w1/w2) * X1 - (b/w2)

# Graficar la ecuación
plt.plot(X1, X2, color='green', linestyle='--', label='Ecuación')


#Colocar las etiquetas
plt.xlabel('Característica A ($X_1$)')
plt.ylabel('Característica B ($X_2$)')
#Colocar títulos
plt.title('Linea de separación para pesos iniciales aleatorios')

