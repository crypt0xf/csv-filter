import csv
from datetime import datetime
from openpyxl import Workbook
import json


def carregar_municipios(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    municipios = {}

    for item in dados:
        # JSON gerado tem "codigo_siafi", zero-padded com 4 dígitos
        codigo = str(item["codigo_siafi"]).strip().zfill(4)
        municipio = item["municipio"].strip().upper()
        municipios[codigo] = municipio

    return municipios


def filtrar_arquivo(input_file, output_file, key_words, municipios_json):

    # carrega dicionário SIAFI -> município
    municipios = carregar_municipios(municipios_json)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Filtrados"

    sheet.append([
        "CNPJ", "MATRIZ", "NOME", "SITUAÇÃO CADASTRAL",
        "DATA SITUAÇÃO CADASTRAL",
        "NOME FANTASIA",
        "DATA DE INÍCIO DE ATIVIDADE",
        "CNAE PRINCIPAL",
        "CNAE SECUNDÁRIO",
        "ENDERECO",
        "BAIRRO",
        "CEP",
        "UF",
        "MUNICÍPIO",
        "TELEFONE1",
        "TELEFONE2",
        "FAX",
        "EMAIL"
    ])

    total = 0
    filtrado = 0

    with open(input_file, "r", encoding="latin-1", newline="") as infile:

        reader = csv.reader(infile, delimiter=";")

        for row in reader:
            total += 1

            try:
                cnpj = "".join(x.strip() for x in row[0:3])
                nome = row[4].upper()

                if not any((p in nome) or (p in cnpj) for p in key_words):
                    continue

                matriz = row[3]
                situ_cadastral = row[5]

                data_situ_cadatral = datetime.strptime(
                    row[6], "%Y%m%d"
                ).strftime("%d/%m/%Y")

                nome_fantasia = row[8].upper()

                data_abertura_formatada = datetime.strptime(
                    row[10], "%Y%m%d"
                ).strftime("%d/%m/%Y")

                cnae1 = row[11]
                cnae2 = row[12]

                endereco = " ".join(
                    x.strip() for x in row[13:17]
                ).upper()

                bairro = row[17].upper()
                cep = row[18]
                uf = row[19].upper()

                # lê o código SIAFI e normaliza para 4 dígitos
                codigo_siafi = row[20].strip().zfill(4)

                # converte código SIAFI em nome do município
                municipio = municipios.get(
                    codigo_siafi,
                    f"Código não encontrado ({codigo_siafi})"
                )

                tel1 = " ".join(
                    x.strip() for x in row[21:23]
                )

                tel2 = " ".join(
                    x.strip() for x in row[23:25]
                )

                fax = " ".join(
                    x.strip() for x in row[25:27]
                )

                email = row[27].lower()

                filtrado += 1

                sheet.append([
                    cnpj,
                    matriz,
                    nome,
                    situ_cadastral,
                    data_situ_cadatral,
                    nome_fantasia,
                    data_abertura_formatada,
                    cnae1,
                    cnae2,
                    endereco,
                    bairro,
                    cep,
                    uf,
                    municipio,
                    tel1,
                    tel2,
                    fax,
                    email
                ])

            except Exception:
                continue

    workbook.save(output_file)

    return total, filtrado