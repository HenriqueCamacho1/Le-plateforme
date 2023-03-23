import pandas as pd

path = "Isolados.xlsx"

#path = "file.xlsx"

def write_ordem(lst):
    table_ordem = pd.read_excel(path, "Ordem")

    top = list(table_ordem.columns)

    #tabela para lista
    list_ordem = lst

    #list_ordem[1][0] = 100000

    #lista para tabela
    table_ordem = pd.DataFrame(list_ordem)

    table_ordem.columns = top

    table_ordem = table_ordem.set_index('Nível')

  

    with pd.ExcelWriter(path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        table_ordem.to_excel(writer, sheet_name="Ordem")
    
    #print(table_ordem)

def write_grua(lst):
    table_grua = pd.read_excel(path, "Grua")

    top = list(table_grua.columns)

    #tabela para lista
    list_grua = lst

    #list_grua[1][0] = 100000

    #lista para tabela
    table_grua = pd.DataFrame(list_grua)

    table_grua.columns = top

    table_grua = table_grua.set_index('Nível')

   

    with pd.ExcelWriter(path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        table_grua.to_excel(writer, sheet_name="Grua")
    
    #print(table_grua)

def write_hora(lst):
    table_hora = pd.read_excel(path, "Hora")

    top = list(table_hora.columns)

    #tabela para lista
    list_hora = lst

    #list_hora[1][0] = 100000

    #lista para tabela
    table_hora = pd.DataFrame(list_hora)

    table_hora.columns = top

    table_hora = table_hora.set_index('Nível')



    with pd.ExcelWriter(path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        table_hora.to_excel(writer, sheet_name="Hora")
    
    #print(table_hora)

