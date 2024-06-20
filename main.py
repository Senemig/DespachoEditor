import PySimpleGUI as sg
import myLib

# All the stuff inside your window.
layout = [
    [
        sg.Text("CNPJ da empresa"),
        sg.InputText(key="cnpj", default_text="57722118000140"),
    ],
    [
        sg.Text("Objeto da contratação"),
        sg.InputText(key="obj", default_text="Alguma coisa muito cara"),
    ],
    [sg.Text("Valor da AF"), sg.InputText(key="val", default_text="1764,55")],
    [sg.Button("Ok"), sg.Button("Cancel")],
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
        elif values["obj"] == "":
            sg.popup(
                "Preencha o campo 'Objeto da contratação'!",
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
                            values["cnpj"], values["obj"], values["val"], folder
                        )
                        sg.popup("Despacho salvo com sucesso!", title="😀")
                        window["cnpj"].update("")
                        window["obj"].update("")
                        window["val"].update("")

window.close()
