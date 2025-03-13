import PySimpleGUI as sg
import myLib, datetime

# All the stuff inside your window.
layout = [
    [
        sg.Text("Dispensa"),
        sg.InputText(key="dispensa", default_text=""),
        sg.Text('/' + str(datetime.date.today().year))
    ],
    [
        sg.Text("CNPJ da empresa"),
        sg.InputText(key="cnpj", default_text=""),
    ],
    [sg.Text("Valor da AF"), sg.InputText(key="val", default_text="")],
    [sg.Button("Ok"), sg.Button("Cancel"), sg.Button('Teste', visible=False)],
    [sg.StatusBar('Pronto', text_color='#8fce00', key="-STAT-")],
]

# Create the Window
window = sg.Window("Editor de Despacho", layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if (
        event == sg.WIN_CLOSED or event == "Cancel"
    ):  # if user closes window or clicks cancel
        break
    elif event == "Ok":
        if values["cnpj"] == "" or len(values["cnpj"]) != 14:
            sg.popup("CNPJ inválido!", title="Erro", any_key_closes=True)
        elif values["dispensa"] == "":
            sg.popup(
                "Preencha o campo 'Dispensa'!",
                title="Erro",
                any_key_closes=True,
            )
        elif values["val"] == "":
            sg.popup(
                "Preencha o campo 'Valor da AF'!", title="Erro", any_key_closes=True
            )
        else:
            try:
                float(values["val"].replace(",", "."))
            except:
                sg.popup(
                    "O campo 'Valor da AF' deve ser um número!",
                    title="Erro",
                    any_key_closes=True,
                )
            else:
                window['-STAT-'].update('Trabalhando', text_color='#ffd966')
                folder = ""
                while folder == "":
                    print(folder)
                    folder = sg.popup_get_folder(
                        title="Salvando o despacho",
                        message="Onde quer salvar o despacho?",
                        default_path="",
                    )
                    if folder != "":
                        myLib.editarDespacho(
                            values["dispensa"], values["cnpj"], values["val"], folder
                        )
                        window['-STAT-'].update('Pronto', text_color='#8fce00')
                        sg.popup("Despacho salvo com sucesso!", title="😀")
                        window["cnpj"].update("")
                        window["dispensa"].update("")
                        window["val"].update("")
    elif event == 'Teste': #AÇÕES DO BOTÃO DE TESTE
        # window['-STAT-'].update('Trabalhando', text_color='#ffd966')
        numExtenso = myLib.numberToText(values["val"].replace(",", "."))
        val = values['val']
        if val.isnumeric():
            val = "{:n}".format(float(val.replace(",", "."))) + ",00"
        else:
            val = "{:.2f}".format(float(val.replace(",", ".")))
        sg.popup(val + ' - ' + numExtenso, title='Teste')

window.close()
