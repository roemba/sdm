import os

import PySimpleGUI as sg

from client import Client
from consultant import Consultant
from protocols import setup, upload_storage_server, upload_storage_server_filename
from storage import StorageServer

sg.theme('Dark Blue 3')  # please make your windows colorful


# Create a setup with three clients
consultant = Consultant()
clients = [Client(), Client(), Client()]
server = StorageServer()

setup(consultant, clients)


def select_user() -> str:
    layout = [[sg.Text('Select a user')],
              [sg.Button("Consultant", key='consultant'),
               sg.Button("Client 1", key='client1'),
               sg.Button("Client 2", key='client2'),
               sg.Button("Client 3", key='client3')]]

    window = sg.Window('User Selection', layout)

    event, _ = window.read()
    window.close()

    return event if event != sg.WIN_CLOSED else None


def show_client(key: str):
    client_text = f'Client {key[6]}'
    client_index = int(key[6]) - 1

    # Create window
    layout = [[sg.Text('Upload a document')],
              [sg.Input(size=(50, 1), key='input', enable_events=True), sg.FileBrowse()],
              [sg.Text('Keywords: '), sg.Text(size=(80, 1), key='keywords')],
              [sg.Button('Upload', key='upload'), sg.Text(size=(20, 1), key='success')],
              [sg.Button('Exit')]]
    window = sg.Window(client_text, layout)

    ready = False

    while True:
        event, values = window.read()
        print(event, values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        elif event == 'input':
            filepath = values['input']
            if not os.path.isfile(filepath):
                # Do nothing if this file does not exist
                continue

            ready = True

            with open(values['input']) as file:
                document = file.read()
                keywords = {word.lower() for word in document.split()}
                window['keywords'].update(keywords)

        elif event == 'upload':
            if not ready:
                window['success'].update("Not ready to upload")
                continue

            upload_storage_server_filename(clients[client_index], server, os.path.basename(filepath), document, keywords)
            window['success'].update("Uploaded succesfully")

    window.close()


def show_consultant():
    pass


while True:
    user = select_user()

    if user is None:
        break

    if user.startswith('client'):
        show_client(user)
    else:
        show_consultant()
