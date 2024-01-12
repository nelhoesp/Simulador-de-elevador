import os
import time
import random as rd

class Building:
    
    '''
    El objeto Building representa el edificio donde opera el elevador

    Parametros
    ----------
    num_pisos : int
        El número de pisos
        
    num_clientes : int
        El número de clientes

    Atributos
    ---------
    num_pisos : int
        Aquí es donde se guarda num_pisos
    num_clientes: int
        Aquí es donde se guarda num_clientes
    '''
    
    def __init__(self, num_pisos = 0, num_clientes = 0):
        self.num_pisos = num_pisos
        self.num_clientes = num_clientes
        
    def output(self, elevador, clientes):
        
        '''Impresión del edificio

        Parametros
        ----------
        elevador : Elevator
            El elevador del edificio
        clientes : list
            Lista de clientes de la clase Customer

        '''
        
        pisos_aux = [i for i in range(1,self.num_pisos+1)]
        pisos = list(reversed(pisos_aux))         #Lista de pisos en reversa    
        
        #Encabezado
        print("-" * 55)
        print(' ' * 5 + " PISO " + ' ' * 5 + " SUBEN " + ' ' * 5 + " BAJAN " + ' ' * 5 + " ELEVADOR ")
        print("-" * 55)
        
        #Imorimiendo cada piso
        for piso in pisos:
            
            #cli_suben almacena en una lista con los IDs de los clientes que estan en el piso actual, no están en el elevador y aun no llegan a su destino
            cli_suben = [i.ID for i in list(filter(lambda x:x.cur_floor==piso and not(x.in_elevator()) and not(x.finished()),clientes))]
            suben = " ".join(cli_suben)
            
            #cli_bajan almacena en una lista con los IDs de los clientes que estan en su piso destino y se ubican, ahora, fuera del elevador
            cli_bajan = [i.ID for i in list(filter(lambda x:x.dst_floor==piso and x.finished(),clientes))]
            bajan = " ".join(cli_bajan)
            
            #Condicional para imprimir o no el elevador en el piso
            if piso == elevador.cur_floor:
                print(f"{piso:^15}" + f"{suben:^10}" + f"{bajan:^13}" + ' ' * 5 + " X ")
                print("-" * 55)
            else:
                print(f"{piso:^15}" + f"{suben:^10}" + f"{bajan:^13}" + ' ' * 5 + "  ")
                print("-" * 55) 
        
    def run(self):
        
        '''Método para operar el elevador
        '''
        
        ##Algoritmo para crear clientes y elegir aleatoriamente el piso de inicio y destino de cada uno
        clientes = []
        for idx in range(self.num_clientes):
            pisos = [i for i in range(1,self.num_pisos+1)]
            rd.shuffle(pisos)
            cliente = Customer()
            cliente.ID = str(idx + 1)
            cliente.cur_floor = pisos[0]
            cliente.dst_floor = pisos[-1]
            clientes.append(cliente)
            
        #Se declara el elevador iniciando en el piso 1 y moviendose arriba
        elevador = Elevator(self.num_pisos, clientes, 1, 'up')
        contador = 0       #Cuenta los clientes que ya llegaron a su destino
        
        
        #Acción del elevador hasta que baje el último cliente
        while(contador < len(clientes)):
            if elevador.cur_floor <= self.num_pisos: #El elevador sube e imprime hasta el último piso
                os.system("cls") 
                self.output(elevador, clientes)
                for cli in clientes:
                    #Para cada cliente, si está en el mismo piso que el elevador y no ha llegado a su destino, se registra en el elevador
                    if cli.cur_floor == elevador.cur_floor and not(cli.finished()):
                        elevador.register_customer(cli)    #El cliente entra en el elevador
                    #Si no, si un cliente dentro del elevador está en su piso de destino, sale de este
                    elif cli.in_elevator() and cli.dst_floor == elevador.cur_floor:
                        elevador.cancel_customer(cli)      #El cliente sale del elevador
                        contador += 1                      #Cuenta 1 cliente que llegó a su destino
                time.sleep(1)
                elevador.move()                            #El elevador cambia de piso
            else:  #El elevador.move() final deja el elevador en el último piso + 1
                   #Como queremos que baje al penúltimo, se resta dos luego de cambiar la dirección hacia abajo
                elevador.direction = 'down'
                elevador.cur_floor -= 2
        
        #Al bajarse el último cliente, se contrarresta el último elevador.move() porque al no haber clientes se supone
        #que debe quedarse en el piso donde se baja la última persona
        if elevador.direction == 'up':
            elevador.cur_floor -= 1
        else:
            elevador.cur_floor += 1
        #Output final para mostrar a los últimos clientes que se han bajado
        os.system("cls")
        self.output(elevador, clientes)
        
class Elevator:
    
    '''
    La clase Elevator representa al elevador

    Parametros
    ----------
    num_pisos : int
        Número de pisos del edificio
    register_list : list
        Lista de clientes en el elevador
    cur_floor : int
        El piso actual del elevador
    direction : int
        La dirección del elevador

    Attributes
    ----------
    num_pisos : int
        Aquí se guarda num_pisos
    register_list : list
        Aquí se guarda register_list
    cur_floor : int
        Aquí se guarda cur_floor
    direction : int
        Aquí se guarda direction
    '''
    
    def __init__(self, num_pisos, register_list, cur_floor, direction):
        self.num_pisos = num_pisos
        self.register_list = register_list
        self.cur_floor = cur_floor
        self.direction = direction
        
    def move(self):
        
        '''Método que mueve el elevador un piso
        '''
        
        if self.direction=='up':
            self.cur_floor += 1
        else:
            self.cur_floor -= 1
    
    def register_customer(self, customer):
        
        '''El cliente sube en el elevador

        Parametros
        ----------
        customer : Customer
            El cliente que sube
        '''
        
        customer.inside = True
    
    def cancel_customer(self, customer):
        
        '''El cliente baja del elevador

        Parametros
        ----------
        customer : Customer
            El cliente que baja
        '''
        
        customer.inside = False
        customer.outside = True

class Customer:
    
    '''
    La clase Customer representa y almacena los atributos del cliente

    Parametros
    ----------
    cur_floor : int
        El piso desde donde el cliente espera el elevador
    dst_floor : int
        El piso destino del cliente
    ID : int
        El ID numérico del cliente

    Atributos
    ---------
    cur_floor : int
        Aquí se almacena cur_floor
    dst_floor : int
        Aquí se almacena dst_floor
    ID : int
        Aquí se almacena ID
    self.inside : bool
        Aquí se almacena un booleano
    self.outside : bool
        Aquí se almacena un booleano
    '''
    
    def __init__(self, cur_floor = 0, dst_floor = 0, ID = 0):
        self.cur_floor = cur_floor
        self.dst_floor = dst_floor
        self.ID = ID
        self.inside = False
        self.outside = False   
    
    def in_elevator(self):
        
        '''Función que retorna el booleano self.inside

        Returns
        -------
        self.inside
            Booleano que indica si el cliente está o no en el elevador
        '''
        
        return self.inside
    
    def finished(self):
        
        '''Función que retorna el booleano self.outside

        Returns
        -------
        self.outside
            Booleano que indica si el cliente ha llegado a su piso destino
        '''
        
        return self.outside
    
    def __repr__(self):
        return f"Cliente {self.ID}: (Piso actual: {self.cur_floor}, Piso destino: {self.dst_floor}, En elevador: {self.inside}, Fuera de elevdor: {self.outside})"

def main():
    # Script de ejecución del script
    Edificio = Building()
    while(1):
        num_pisos = input("Ingrese el numero de pisos [3 - 12]: ")
        try:
            num_pisos = int(num_pisos)
            if 3 <= num_pisos <= 12:
                Edificio.num_pisos = num_pisos
                break
            else:
                print("Debe ingresar un numero de pisos entre 3 y 12")
        except:
            print("Debe ingresar un valor numerico entre 3 y 12")
            
    while(1):
        num_clientes = input("Ingrese el numero de clientes [1 - 12]: ")
        try:
            num_clientes = int(num_clientes)
            if 1 <= num_clientes <= 12:
                Edificio.num_clientes = num_clientes
                break
            else:
                print("Debe ingresar un numero de usuarios entre 1 y 12")
        except:
            print("Debe ingresar un valor numerico entre 1 y 12")
        
    Edificio.run()
    
# Guarda de control para la ejecución del script
if __name__ == "__main__":
    main()