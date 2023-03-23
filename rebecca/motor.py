import pandas as pd
from datetime import datetime, timedelta
import time
#print(pd.__version__)

path = "file.xlsx"
isolados = "Isolados.xlsx"



def resumo_tab():
                #TEMPOS - único output do excel#
    #Lê tabela de resumo que contem duração de cada bay
    tab_A = pd.read_excel(path, "Resumo", index_col='Nível', parse_dates=['B_28','B_24','B_20','B_17','B_14','B_10','B_6','B_2'])
    #print(tab_A)

    return tab_A

def resumo_list(tab_A):
    LA_1 = tab_A.values.tolist()
    LA = []
    for sublist in LA_1:
        for item in sublist:
            LA.append(item)

    #print(LA)
    #print(len(LA))

    return LA

#resumo_list(resumo_tab())

def ordem():
                #ORDEM#
    #Lê tabela que contém a ordem de descarga
    tab_C_O = pd.read_excel(isolados, "Ordem", index_col='Nível')
    #print(tab_C_O)

    LC_O_1 = tab_C_O.values.tolist()
    LC_O = []
    for sublist in LC_O_1:
        for item in sublist:
            LC_O.append(item)

    #print(LC_O)
    #print(len(LC_O))

    return LC_O


def gruas():
                #GRUAS#
    #Lê tabela que contém as descargas de cada Grua
    tab_C_G = pd.read_excel(isolados, "Grua", index_col='Nível')
    #print(tab_C_G)

    LC_G_1 = tab_C_G.values.tolist()
    LC_G = []
    for sublist in LC_G_1:
        for item in sublist:
            LC_G.append(item)

    #print(LC_G)
    #print(len(LC_G))

    return LC_G



def hora_real():
                #HORA REAL#
    #Lê tabela que contem hora real de início da bay
    #Se -1 não tem hora real
    tab_H = pd.read_excel(isolados, "Hora", index_col='Nível', parse_dates=['B_28','B_24','B_20','B_17','B_14','B_10','B_6','B_2'])
    #print(tab_H)

    LH_1 = tab_H.values.tolist()
    LH = []
    for sublist in LH_1:
        for item in sublist:
            LH.append(item)

    #print(LH)
    #print(len(LH))

    return LH


#--------------------------------------------------------#


#Separa as Gruas (A e B)
def gruaA(LA, LC_O, LC_G, LH):

    zero = datetime.strptime('0:0:0', '%H:%M:%S')

    x = 10  #Em minutos, a variação desejada

    LC_G_A = ['Empty']*len(LA)

    for i in range(len(LC_G)):

        if LC_G[i] == 'A' or LC_G[i] == 'a':
            LC_G_A[i] = 1

        if LC_G[i] != 'A' and LC_G[i] != 'a':
            LC_G_A[i] = 0

    #print(LC_G_A)

    #Ordem das descargas de cada Grua
    LC_A = []

    for i1, i2 in zip(LC_O, LC_G_A):
    
        LC_A.append(i1*i2)

    #print(LC_A)

    #Tempos para cada bay da grua
    LA_A = ['Empty']*len(LA)

    for i in range(len(LC_A)):
        if LC_A[i] != 0:
            LA_A[i] = LA[i]

        else:
            LA_A[i] = 0

    #print(LA_A)

    #Converter valores para tempos
    for i in range(len(LA)):
        if LA_A[i] != 0 and  LA_A[i] != '-1':
            LA_A[i] = (datetime.strptime(LA_A[i], '%H:%M:%S'))
            LA_A[i] = LA_A[i] - zero

    #print(LA_A)

    for i in range(len(LA)):
        if LH[i] != '-1':
            LH[i] = (datetime.strptime(LH[i], '%H:%M:%S'))
            LH[i] = LH[i] - zero #Só operações com time deltas

    #print(LH)

    #Tempos de cada bay tendo em conta a ordem de descarga para a grua
    LD_A = [-1]*(len(LA))

    for i in range(len(LA)):
        for j in range(len(LA)):

            #print('--')

            if LC_A[j] == int(i+1):

                if LC_A[j] == 1:
                    LD_A[j] = LA_A[j]
                    
                    k = j

                else:
                    #print(k)
                    LD_A[j] = LD_A[k] + LA_A[j]
                    k = j

                #print(j)
                #print(LD_A)
                break

        if LH[j] != '-1':
            LD_A[j] = LH[j]
            
            #print(LD_A)
    #print('-------')
    #print(LD_A)

    # +/- da duração
    LB_A = []

    for i in range((len(LA))):

        if LD_A[i] == -1:
            LB_A.append(LD_A[i])
            LB_A.append(LD_A[i])
            #Está duas vezes porque aqui duplica as entradas na tabela

        if LD_A[i] != -1:
            
            menos = LD_A[i] - (timedelta(minutes= x))

            LB_A.append(menos)

            mais = LD_A[i] + (timedelta(minutes= x))

            LB_A.append(mais)

        #print(LB_A)

    #print(LB_A)

    return LB_A


def gruaB(LA, LC_O, LC_G, LH):

    zero = datetime.strptime('0:0:0', '%H:%M:%S')

    x = 10  #Em minutos, a variação desejada

    LC_G_B = ['Empty']*len(LA)

    for i in range(len(LC_G)):
    
        if LC_G[i] == 'B' or LC_G[i] == 'b':
            LC_G_B[i] = 1

        if LC_G[i] != 'B' and LC_G[i] != 'b':
            LC_G_B[i] = 0

    #print(LC_G_B)

    #Ordem das descargas de cada Grua
    LC_B = []
    
    for i1, i2 in zip(LC_O, LC_G_B):

        LC_B.append(i1*i2)
 
    #print(LC_B)

    #Tempos para cada bay da grua
    LA_B = ['Empty']*len(LA)

    for i in range(len(LC_B)):
        if LC_B[i] != 0:
            LA_B[i] = LA[i]

        else:
            LA_B[i] = 0

    #print(LA_B)

    #Converter valores para tempos
    for i in range(len(LA)):
        if LA_B[i] != 0:
            LA_B[i] = (datetime.strptime(LA_B[i], '%H:%M:%S'))
            LA_B[i] = LA_B[i] - zero

    #print(LA_B)

    for i in range(len(LA)):
        if LH[i] != '-1':
            LH[i] = (datetime.strptime(LH[i], '%H:%M:%S'))
            LH[i] = LH[i] - zero #Só operações com time deltas

    #print(LH)

    #Tempos de cada bay tendo em conta a ordem de descarga para a grua
    LD_B = [-1]*(len(LA))

    for i in range(len(LA)):
        for j in range(len(LA)):

            #print('--')

            if LC_B[j] == int(i+1):

                if LC_B[j] == 1:
                    LD_B[j] = LA_B[j]
        
                    k = j

                else:
                    #print(k)
                    LD_B[j] = LD_B[k] + LA_B[j]
                    k = j

                #print(j)
                #print(LD_B)
                break

        if LH[j] != '-1':
            LD_B[j] = LH[j]
      
        #print(LD_B)
    #print('-------')
    #print(LD_B)

    # +/- da duração
    LB_B = []

    for i in range((len(LA))):

        if LD_B[i] == -1:
            LB_B.append(LD_B[i])
            LB_B.append(LD_B[i])
            #Está duas vezes porque aqui duplica as entradas na tabela

        if LD_B[i] != -1:
            
            menos = LD_B[i] - (timedelta(minutes= x))

            LB_B.append(menos)

            mais = LD_B[i] + (timedelta(minutes= x))

            LB_B.append(mais)

        #print(LB_B)

    #print(LB_B)

    return LB_B


def tabela_B(tab_A,LB_A, LB_B):
    #Lista de +/- duração
    LB = []

    for i in range(len(LB_A)):

        if LB_A != -1:
            LB.append(LB_A[i])
        
        if LB_A[i] == -1:
            LB[i] = LB_B[i]
    
    #print(LB)


    #Tabela de +/- duração
    import numpy as np

    num_rows, num_cols = tab_A.shape
    #print(num_rows, num_cols)

    #print(len(LB))
    #print(len(LB)/num_rows)

    B = np.reshape(LB,(num_rows,int((len(LB)/num_rows))))

    #print(B)

    niveis = ['C5','C4','C3','C2','C1','PC','P5','P4','P3','P2','P1']

    Bays = ['B_28_inf','B_28_sup','B_24_inf','B_24_sup','B_20_inf','B_20_sup','B_17_inf','B_17_sup','B_14_inf','B_14_sup','B_10_inf','B_10_sup','B_6_inf','B_6_sup','B_2_inf','B_2_sup']

    tab_B = pd.DataFrame(B, columns=Bays)

    tab_B['Nível'] = niveis

    tab_B = tab_B.set_index('Nível')

    #print(tab_B)

    return tab_B



def ini():
    print("Ini engine")

    global tab_B
    global tab_Plano
    tab_B = tabela_B(resumo_tab(),gruaA(resumo_list(resumo_tab()),ordem(),gruas(),hora_real()),gruaB(resumo_list(resumo_tab()),ordem(),gruas(),hora_real()))
    tab_Plano = pd.read_excel(path, "Plano Simplificado_v2", index_col='Nível', keep_default_na=False)


#CAMIONISTA#
#Lê plano de descarga

#print(tab_Plano)


def procurar(letras, num, fim):
  letras = str(letras.upper())
  num = str(num)
  fim = ('.' + str(fim))

  bay_names = tab_Plano.columns.values.tolist()
  time.sleep(2)
  
  for j in bay_names:
    col_list = tab_Plano[j].values.tolist()
    #print(col_list)
    #print(j)

    for i in range(len(col_list)):
      if col_list[i] == str(letras + ' ' + num + fim):
        if col_list[i] != -1 and col_list[i] != -9:
          
            #print(i)

            out = (tab_Plano.iloc[[i]].index.tolist())
            #print(j)
            #print(out)

            for k in out:

                # print(k)

                _u = 'sup'.join(j.rsplit((j[-1]),1))
                _i = 'inf'.join(j.rsplit((j[-1]),1))
                # print(_u,_i)
                
                superior = tab_B.loc[k,_u]
                inferior = tab_B.loc[k,_i]


                # print(superior, inferior)

                return superior, inferior

                #print(tab_B.loc[out,_u])
    # else:    
    #     print("Carga não encontrada. Por favor inserir os algarismos todos da carga")
    
  return None, None

#sup, inf = procurar('d',2,4)
# sup, inf = procurar('tclu',115365,6)
# print(sup, inf)

def get_table_ordem():
    table_ordem = pd.read_excel(isolados, "Ordem")

    return table_ordem.values.tolist()

    #print(list_ordem)

def get_table_gruas():
    table_gruas = pd.read_excel(isolados, "Grua")

    return table_gruas.values.tolist()

    #print(list_gruas)

def get_table_hora():
    table_hora = pd.read_excel(isolados, "Hora")

    return table_hora.values.tolist()

    #print(list_hora)

#ini()
#print(tab_B)