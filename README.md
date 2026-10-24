# Organizador de NF-e com Python

Projeto de estudo que lê arquivos XML de notas fiscais, extrai seus dados e copia os arquivos para pastas por ano e mês da emissão.

Utiliza exemplos fictícios e simplificados, sem validade fiscal.

## Funcionalidades

- Extrai nome do emitente, CNPJ, data de emissão e valor total.
- Organiza os XMLs em pastas por ano e mês.
- Preserva os arquivos originais.
- Evita sobrescrever arquivos com o mesmo nome no destino.
- Exporta um resumo para `resumo.csv`.
- Ignora XMLs malformados e notas com campos obrigatórios ausentes ou vazios.
- Rejeita datas inexistentes e valores negativos, não numéricos ou não finitos.
- Continua processando as demais notas após identificar uma entrada inválida.

## Tecnologias

- Python 3.14
- pandas
- Bibliotecas padrão: xml.etree.ElementTree, os, shutil, datetime e decimal.

## Como executar

No terminal, dentro da pasta do projeto:

### 1. Crie e ative o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instale as dependências

Com o ambiente virtual ativo, execute:

```powershell
python -m pip install -r requeriments.txt
```

Esse comando instala as dependências nas versões registradas no arquivo.

### 3. Adicione os XMLs

Coloque os arquivos na pasta `notas/`.

O projeto inclui exemplos fictícios, inclusive arquivos com erros para demonstrar as validações.

### 4. Execute

```powershell
python leitor.py
```

## Estrutura

```text
.
├── leitor.py
├── notas/
├── requeriments.txt
├── .gitignore
└── README.md
```

Após executar, o programa gera:

```text
organizadas/
├── 2025/
│   ├── 11/
│   └── 12/
└── 2026/
    ├── 01/
    └── ...

resumo.csv
```

## Resumo CSV

O arquivo contém as colunas:

- Arquivo
- Nome
- CNPJ
- Data
- Valor
- Destino

Usa ponto e vírgula como separador e codificação UTF-8 com BOM.

Ao importar em uma planilha, defina a coluna CNPJ como texto para preservar os zeros iniciais.

## Limitações

- Processa os XMLs diretamente em `notas/`, sem percorrer subpastas.
- Valida somente a data da emissão, sem verificar horário ou fuso.
- Verifica arquivos existentes pelo nome, sem comparar conteúdo ou chave de acesso.
- Substitui `resumo.csv` a cada execução.
- Não remove cópias de execuções anteriores quando uma entrada passa a ser rejeitada.
- Não valida assinatura digital, situação fiscal ou autorização na SEFAZ.
- Não é um sistema de produção para processar XMLs de fontes não confiáveis.