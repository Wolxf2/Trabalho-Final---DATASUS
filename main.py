import csv
import pandas as pd

arquivos_csv = ['mortes_1999.csv', 'mortes_2004.csv', 'mortes_2009.csv', 'mortes_2014.csv', 'mortes_2019.csv']

for arquivo in arquivos_csv:

    # Dicionário para armazenar os dados
    dados_dict = {}

    # Abre o arquivo CSV e lê os dados
    with open(arquivo, newline='', encoding='utf-8') as csvfile:
        # Cria um objeto leitor de CSV
        leitor = csv.reader(csvfile, delimiter=';')
        
        # Itera pelas linhas do CSV
        for linha in leitor:
            # O primeiro item da linha é usado como índice no dicionário
            indice = linha[0]
            # Os demais itens da linha são os valores associados ao índice
            valores = linha[1:]
            
            # Armazena no dicionário
            dados_dict[indice] = valores

    # Agora 'dados_dict' contém os dados do CSV organizados como um dicionário
    # Cada chave é o índice e cada valor é uma lista de valores correspondentes

    # Personalizando os nomes das colunas
    nomes_colunas = [
        "Regiões",
        "I. Algumas doenças infecciosas e parasitárias",
        "II. Neoplasias (tumores)",
        "III. Doenças do sangue, órgãos hematopoéticos e transtornos imunológicos",
        "IV. Doenças endócrinas, nutricionais e metabólicas",
        "V. Transtornos mentais e comportamentais",
        "VI. Doenças do sistema nervoso",
        "VII. Doenças do olho e anexos",
        "VIII. Doenças do ouvido e da apófise mastóide",
        "IX. Doenças do aparelho circulatório",
        "X. Doenças do aparelho respiratório",
        "XI. Doenças do aparelho digestivo",
        "XII. Doenças da pele e do tecido subcutâneo",
        "XIII. Doenças do sistema osteomuscular e do tecido conjuntivo",
        "XIV. Doenças do aparelho geniturinário",
        "XV. Gravidez, parto e puerpério",
        "XVI. Algumas afecções originadas no período perinatal",
        "XVII. Malformações congênitas, deformidades e anomalias cromossômicas",
        "XVIII. Sintomas, sinais e achados anormais de exames clínicos e de laboratório",
        "XX. Causas externas de morbidade e mortalidade",
        "Total"
    ]

    # Convertendo o dicionário para um DataFrame do pandas
    # O primeiro passo é extrair os valores
    indices = list(dados_dict.keys())
    valores = list(dados_dict.values())

    # Criando a lista de linhas para o DataFrame
    linhas = [[indice] + valor for indice, valor in zip(indices, valores)]

    # Certificando-se de que o número de nomes de colunas corresponde ao número de colunas nos dados
    if len(nomes_colunas) != len(linhas[0]):
        raise ValueError("O número de nomes de colunas não corresponde ao número de colunas nos dados")
    # Criando o DataFrame
    df = pd.DataFrame(linhas, columns=nomes_colunas)

    # Calculando as porcentagens
    # Convertendo os valores para números
    for col in nomes_colunas[1:]:  # Exclui a primeira coluna que é o índice
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Pegando o valor da coluna "Total" e calculando as porcentagens
    if "Total" in df.columns:
        df_percentual = df.copy()
        total_coluna = df["Total"]
        for col in nomes_colunas[1:-1]:  # Exclui a primeira e a última coluna
            df_percentual[col] = (df[col] / total_coluna) * 100

        # Substituindo os valores originais pelas porcentagens
        df_percentual = df_percentual.fillna(0)  # Substitui NaN por 0
    else:
        raise ValueError("A coluna 'Total' não existe no DataFrame")

    # Salvando o DataFrame em um arquivo Excel
    df_percentual.to_excel(arquivo+"_output_percentual.xlsx", index=False)

    print("Arquivo Excel '"+arquivo+'_output_percentual.xlsx'+"' criado com sucesso!")