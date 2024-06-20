from docx import Document
import docxedit, requests, locale


def numberToText(number):
    api_num = (
        "https://api.invertexto.com/v1/number-to-words?token=8218|Vu0cr3TTcZK0F7UpeiVYu5lK19EjG1sy&number="
        + number
        + "&language=pt&currency=BRL"
    )

    response = requests.get(api_num)

    if response.status_code == 200:
        return response.json()["text"]


def editarDespacho(cnpj, obj, val, folder):

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
            val = "{:n}".format(float(val.replace(",", ".")))

        # Abrir documento modelo
        document = Document("despacho.docx")

        # Alterar campos com as novas informações

        # Razão social
        docxedit.replace_string(
            document,
            old_string="#1",
            new_string=dados["razao_social"].upper(),
        )

        # CNPJ formatado
        docxedit.replace_string(document, old_string="#2", new_string=cnpjFormat)

        # Objeto a ser adquirido
        docxedit.replace_string(document, old_string="#3", new_string=obj.upper())

        # Valor da compra
        docxedit.replace_string(
            document,
            old_string="#4",
            new_string=val,
        )

        # Valor por extenso
        docxedit.replace_string(document, old_string="#5", new_string=numExtenso)

        # Salvar novo documento com as informações alteradas
        document.save(folder + "/despacho2.docx")
