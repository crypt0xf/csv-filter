import csv
from datetime import datetime
from openpyxl import Workbook

# input_file = arquivo que envia informação
# output_file = arquivo que recebe informação
# key_words = palavras chaves a serem buscadas
def filtrar_arquivo(input_file, output_file, key_words):

    # cria workbook Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Filtrados"

    # cabeçalho
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
        "CÓDIGO MUNICÍPIO",
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

                # filtro
                if not any((p in nome) or (p in cnpj) for p in key_words):
                    continue

                matriz = row[3]
                situ_cadastral = row[5]

                data_situ_cadatral = datetime.strptime(
                    row[6],
                    "%Y%m%d"
                ).strftime("%d/%m/%Y")

                nome_fantasia = row[8].upper()

                data_abertura_formatada = datetime.strptime(
                    row[10],
                    "%Y%m%d"
                ).strftime("%d/%m/%Y")

                cnae1 = row[11]
                cnae2 = row[12]
                endereco = " ".join(
                    x.strip() for x in row[13:17]
                ).upper()

                bairro = row[17].upper()
                cep = row[18]
                uf = row[19].upper()
                municipioIBGE = row[20]

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

                # adiciona linha no Excel
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
                    municipioIBGE,
                    tel1,
                    tel2,
                    fax,
                    email
                ])

            except:
                continue

    # salva arquivo xlsx
    workbook.save(output_file)

    return total, filtrado