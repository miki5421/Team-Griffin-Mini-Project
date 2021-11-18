from database_operations import create_connection
from database_operations import services_near_postcode
import PySimpleGUI as sg


def main():
    conn = create_connection('data.db')
    sg.theme('LightBlue')
    # All the stuff inside your window.

    layout = [[sg.Text('Enter Postcode:'), sg.InputText()],
              [sg.Text('Enter Distance:'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Clear')], [sg.Checkbox('Doctors', default=True, key = 'doc')], [sg.Checkbox('Dentists', default=True, key = 'dent')], [sg.Checkbox('Optitions', default=True, key = 'opt')], [
        sg.Checkbox('Nurserys', default=True, key = 'nur')],[sg.Text('Service, Name, Address, Postcode, Distance(Miles)')],  [sg.Multiline(size=(100, 20), key="-TEXT-")],
    ]

    # Create the Window
    window = sg.Window('NHS Service Search', layout, size=(600, 600))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        what_services = []
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window
            break
        if values['doc'] == True:
            what_services.append(1)
        if values['dent'] == True:
            what_services.append(2)
        if values['opt'] == True:
            what_services.append(3)
        if values['nur']:
            what_services.append(4)
        distance = 5
        try:
            distance = int(values[1])
        except:
            print('Invalid input')
        window["-TEXT-"].update("")
        if event != 'Clear':
            services = services_near_postcode(
                conn, values[0], distance, what_services)
            services_formatter = []
            for service in services:
                for i in range(1, 7):
                    services_formatter.append(str(service[i]))
                    services_formatter.append(" ")
                    if i == 6:
                        services_formatter.append("\n")
            services_formatter = "".join(services_formatter)
            window["-TEXT-"].update(services_formatter)
    window.close()


if __name__ == "__main__":
    main()

