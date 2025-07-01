from fastapi import FastAPI

app = FastAPI() #Iniciando uma Aplicação do FastAPI

@app.get('/') #Definindo um endpoint com o endereço acessivel pelo metodo HTTP GET
def impares_e_pares():
    pares = []
    impares =[]

    for i in range(10):
        if i%2 ==0:
            pares.append(i)
        else:
            impares.append(i)
   # Transforma a lista em tuplas, pois não são hashables
    tuple_1 = tuple(pares) 
    tuple_2 = tuple(impares)
   
    return{tuple_1,tuple_2}