from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Optional
from fastapi.openapi.docs import get_swagger_ui_html

#testecommit

#PRODUCAO
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&opcao=opt_02

#PROCESSAMENTO
#VINIFERAS
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_01&opcao=opt_03
#AMERICANAS_HIBRIDAS
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_02&opcao=opt_03
#UVA_DE_MESA
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_03&opcao=opt_03
#SEM_CLASSIFICACAO
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_04&opcao=opt_03


#COMERCIALIZACAO
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&opcao=opt_04

#IMPORTACAO
#VINHOS DE MESA
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_01&opcao=opt_05
#ESPUMANTES
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_02&opcao=opt_05
#UVAS FRESCAS
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_03&opcao=opt_05
#UVAS PASSAS
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_04&opcao=opt_05
#SUCO DE UVA
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_05&opcao=opt_05

#EXPORTACAO
#VINHOS DE MESA
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_01&opcao=opt_06
#ESPUMANTES
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_02&opcao=opt_06
#UVAS FRESCAS
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_03&opcao=opt_06
#SUCO DE UVA
#http://vitibrasil.cnpuv.embrapa.br/index.php?ano=1995&subopcao=subopt_04&opcao=opt_06

opcao_map = {
    "PRODUCAO": "opt_02",
    "PROCESSAMENTO": "opt_03",
    "COMERCIALIZACAO": "opt_04",
    "IMPORTACAO": "opt_05",
    "EXPORTACAO": "opt_06"
}

subopcao_Processamento_map = {
    "VINIFERAS": "subopt_01",
    "AMERICANAS": "HIBRIDAS subopt_02",
    "UVA_DE_MESA": "subopt_03",
    "SEM_CLASSIFICACAO": "subopt_04"
}

subopcao_Importacao_map = {
    "VINHOS DE MESA": "subopt_01",
    "ESPUMANTES": "subopt_02",
    "UVAS FRESCAS": "subopt_03",
    "UVAS PASSAS": "subopt_04",
    "SUCO DE UVA": "subopt_05"
}

subopcao_Exportacao_map = {
    "VINHOS DE MESA": "subopt_01",
    "ESPUMANTES": "subopt_02",
    "UVAS FRESCAS": "subopt_03",
    "SUCO DE UVA": "subopt_04"
}

app = FastAPI()

class TabelaInput(BaseModel):
    ano: int
    opcao: str
    subopcao: Optional[str] = None
    
def consultar_tabela(ano: int, opcao: Optional[str] = None, subopcao: Optional[str] = None):

    cod_opcao = None
    cod_subopcao = None

    if opcao is not None:
        if opcao in opcao_map:
            cod_opcao = opcao_map[opcao]
        else:
            return "Opcao invalida - " + str(opcao_map)
    else:
        return "Opcao deve ser preechida" 

    if opcao == "PROCESSAMENTO":
        if subopcao is not None:
            if subopcao in subopcao_Processamento_map:
                cod_subopcao = subopcao_Processamento_map[subopcao]
            else:
                return "Subpcao invalida"
        else:
            return "Para PROCESSAMENTO, subopcao deve ser preechida - " + str(subopcao_Processamento_map) 
    elif opcao == "IMPORTACAO":
        if subopcao is not None:
            if subopcao in subopcao_Importacao_map:
                cod_subopcao = subopcao_Importacao_map[subopcao]
            else:
                return "Subpcao invalida"
        else:
            return "Para IMPORTACAO, subopcao deve ser preechida - " + str(subopcao_Importacao_map)
    elif opcao == "EXPORTACAO":
        if subopcao is not None:
            if subopcao in subopcao_Exportacao_map:
                cod_subopcao = subopcao_Exportacao_map[subopcao]
            else:
                return "Subpcao invalida"
        else:
            return "Para EXPORTACAO, subopcao deve ser preechida - " + str(subopcao_Exportacao_map) 

    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}"
    
    if cod_opcao is not None:
        url += f"&opcao={cod_opcao}"
    if cod_subopcao is not None:
        url += f"&subopcao={cod_subopcao}"
        

    print("URL: " + url)

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Tabela não encontrada1")

    soup = BeautifulSoup(response.text, "html.parser")
      
    table = soup.find("table", class_="tb_base tb_dados")
    
    if not table:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")

    data = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            data_row = [cell.text.strip() for cell in cells]
            data.append(data_row)
    
    print(data)
    #print({"table_data": data})
    return {"table_data": data}

@app.post("/consulta_tabela/")
def consulta_tabela(input_data: TabelaInput):
    return consultar_tabela(input_data.ano, input_data.opcao, input_data.subopcao)

@app.get("/")
def read_root():
    return {"message": "API para consultar tabela do link http://vitibrasil.cnpuv.embrapa.br/"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
