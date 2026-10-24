from datetime import date
from decimal import Decimal, InvalidOperation
import xml.etree.ElementTree as ET
import os
import pandas as pd
import shutil



ns = {'nfe': "http://www.portalfiscal.inf.br/nfe"} #Identifica o namespace declarado no xmlns, no caso de uma nota real seria o site da nfe.fazenda
notas = []


for arquivo in os.listdir('notas'):
    if arquivo.lower().endswith('.xml'):
        caminho = os.path.join('notas', arquivo)
        try:
            xmls = ET.parse(caminho)
            raiz_xmls = xmls.getroot()
        
        except ET.ParseError as erro:
            print(f'XML inválido: {arquivo}. Motivo: {erro}')
            continue
        except OSError as erro:
            print(f'Não foi possível ler: {arquivo}. Motivo: {erro}')
            continue           

        nome = raiz_xmls.findtext('.//nfe:emit/nfe:xNome', namespaces=ns)
        cnpj = raiz_xmls.findtext('.//nfe:emit/nfe:CNPJ', namespaces=ns)
        data = raiz_xmls.findtext('.//nfe:ide/nfe:dhEmi', namespaces=ns)
        valor = raiz_xmls.findtext('.//nfe:total/nfe:ICMSTot/nfe:vNF', namespaces=ns)

        campos = {
            'Nome':nome,
            'CNPJ': cnpj,
            'Data': data,
            'Valor': valor
        }

        print(f'Arquivos: {arquivo}')
        print(campos)

        ausentes = []

        for campo,conteudo in campos.items():
             if conteudo is None or conteudo.strip() == '':
                 ausentes.append(campo)

        if ausentes:
            print(f'Nota ignorada: {arquivo}. Campos ausentes ou vazios: {','.join(ausentes)}')
            continue

        data_nota = data.split('T')[0]
        partes = data_nota.split('-')
        try:
            if len(partes) != 3:
                raise ValueError('O formato é diferente de AAAA-MM-DD')
            
            ano,mes,dia = partes

            if len(ano) !=4 or len(mes) != 2 or len(dia) != 2:
                raise ValueError ('O formato é diferente de AAAA-MM-DD')

            date(int(ano),int(mes),int(dia))

        except ValueError as erro:
            print(f'Nota ignorada: {arquivo}. Data inválida: {data_nota}. Motivo: {erro}')
            continue

        try:
            valor_decimal = Decimal(valor)
        except InvalidOperation:
            print(f'Nota ignorada: {arquivo}. Valor inválido: {valor}')
            continue
        
        if not valor_decimal.is_finite() or valor_decimal < 0:
            print(f'Nota ignorada: {arquivo}. Valor inválido: {valor}')
            continue

        
        pasta_destino = os.path.join('organizadas',ano,mes)
        os.makedirs(pasta_destino,exist_ok=True)

        arquivo_destino = os.path.join(pasta_destino,arquivo)

        if not os.path.exists(arquivo_destino):
            shutil.copy2(caminho, arquivo_destino)
            print('Nota copiada para ', pasta_destino)
        else:
            print('Arquivo já existente em ', pasta_destino)

        notas.append({
            'Arquivo': arquivo,
            'Nome': nome,
            'CNPJ': cnpj,
            'Data': data,
            'Valor': valor,
            'Destino': arquivo_destino
        })

tabela = pd.DataFrame(notas)

# print (tabela)



tabela.to_csv(
    'resumo.csv',
    index=False,
    sep=';',
    encoding='utf-8-sig',
)

