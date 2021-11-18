from database_operations import create_connection
from database_operations import services_near_postcode
import PySimpleGUI as sg

def main():
    conn = create_connection('data.db')
    sg.theme('LightBlue')  
    # All the stuff inside your window.


    layout = [  [sg.Text('Enter Postcode:'), sg.InputText()],
                [sg.Text('Enter Distance:'), sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel')], [sg.Text('Service, Name, Address, Postcode, Distance(Miles)')], [sg.Multiline( size=(100, 20), key="-TEXT-")], 
                ]

    # Create the Window
    window = sg.Window('NHS Service Search', layout, size=(600,600))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        distance = 5
        try:
            distance = int(values[1])
        except:
            print('Invalid input')
        services = services_near_postcode(conn, values[0], distance)
        services_formatter = []
        for service in services:
            for i in range(1,7):
                services_formatter.append(str(service[i]))
                services_formatter.append(" ")
                if i == 6:
                    services_formatter.append("\n")
        services_formatter = "".join(services_formatter)
        window["-TEXT-"].update(services_formatter)
    window.close()

if __name__ == "__main__":
    main()

