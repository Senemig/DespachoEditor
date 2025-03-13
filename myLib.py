from docx import Document
import docxedit, requests, locale, datetime

def numberToText(number):
    api_num = (
        "https://api.invertexto.com/v1/number-to-words?token=8218|Vu0cr3TTcZK0F7UpeiVYu5lK19EjG1sy&number="
        + number
        + "&language=pt&currency=BRL"
    )

    response = requests.get(api_num)

    if response.status_code == 200:
        return response.json()["text"]


def editarDespacho(dispensa, cnpj, val, folder):

    locale.setlocale(locale.LC_ALL, "")

    # URL da API
    # api_url = "https://api.cnpja.com/office/"
    api_url = "https://publica.cnpj.ws/cnpj/"

    # CNPJ a ser pesquisado
    # cnpj = input("CNPJ da empresa:\n>>>")

    # Solicitar dados básicos do cadastro do fornecedor pela API
    response = requests.get(api_url + cnpj)
    print(response)

    if response.status_code == 200:
        # Atribuir dados em formato JSON
        dados = response.json()
        print(dados)

        # Data de hoje
        data = datetime.datetime.now()
        data = data.strftime('%d') +  " de " + data.strftime('%B').capitalize() + " de " + data.strftime('%Y')

        # Formatar CNPJ
        cnpjFormat = "%s.%s.%s/%s-%s" % (
            cnpj[0:2],
            cnpj[2:5],
            cnpj[5:8],
            cnpj[8:12],
            cnpj[12:14],
        )
        numExtenso = numberToText(val.replace(",", "."))
        if val.isnumeric():
            val = "{:n}".format(float(val.replace(",", "."))) + ",00"
        else:
            val = "{:.2f}".format(float(val.replace(",", ".")))

        # Abrir documento modelo
        document = Document("despacho.docx")

        # Alterar campos com as novas informações
        # 1 - EMPRESA
        # 2 - CNPJ
        # 3 - VALOR
        # 4 - VALOR POR EXTENSO
        # 5 - DATA
        # 6 - DISPENSA

        # Razão social
        docxedit.replace_string(
            document,
            old_string="#1",
            new_string=dados["razao_social"].upper(),
        )

        # CNPJ formatado
        docxedit.replace_string(document, old_string="#2", new_string=cnpjFormat)

        # Número da dispensa
        docxedit.replace_string(document, old_string="#6", new_string=dispensa + "/" + str(datetime.date.today().year))

        # Valor da compra
        docxedit.replace_string(
            document,
            old_string="#3",
            new_string=val,
        )

        # Valor por extenso
        docxedit.replace_string(document, old_string="#4", new_string=numExtenso)

        # Data de hoje
        docxedit.replace_string(document, old_string="#5", new_string=data)        

        # Salvar novo documento com as informações alteradas
        print('Salvando o documento')
        document.save(folder + "/despacho2.docx")
