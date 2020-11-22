import os

import PySimpleGUI as sg

from client import Client
from consultant import Consultant
from models import AES
from protocols import setup, upload_storage_server, upload_storage_server_filename, search_storage_server_filenames
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
               sg.Button("Client 3", key='client3'),
               sg.Button("Storage Server", key='server')]]

    window = sg.Window('User Selection', layout)

    event, _ = window.read()
    window.close()

    return event if event != sg.WIN_CLOSED else None


def show_client(key: str):
    client_text = f'Client {key[6]}'
    client_index = int(key[6]) - 1

    # Create window
    layout = [[sg.Text('User actions', font='bold')],
              [sg.HorizontalSeparator()],
              [sg.Text('Upload a document')],
              [sg.Input(size=(50, 1), key='input', enable_events=True), sg.FileBrowse()],
              [sg.Text('Keywords: '), sg.Text(size=(80, 1), key='keywords')],
              [sg.Button('Upload', key='upload'), sg.Text(size=(20, 1), key='success')],
              [sg.HorizontalSeparator()],
              [sg.Text('Search for documents')],
              [sg.Input(size=(50, 1), key='search_string'), sg.Button('Search', key='search')],
              [sg.Text('Results:')],
              [sg.Listbox([], size=(50, 5), key='results')],
              [sg.Button('Download', key='download', disabled=True)],
              [sg.HorizontalSeparator()],
              [sg.Button('Back')]]
    window = sg.Window(client_text, layout)

    ready = False
    results = []

    while True:
        event, values = window.read()
        print(event, values)

        if event == sg.WIN_CLOSED or event == 'Back':
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

            upload_storage_server_filename(clients[client_index], server, os.path.basename(filepath), document,
                                           keywords)
            window['success'].update("Uploaded succesfully")

        elif event == 'search':
            keywords = {kw.lower() for kw in values['search_string'].split()}
            results = search_storage_server_filenames(clients[client_index], server, keywords)
            window['results'].update([title for title, _ in results])

    window.close()


def show_server():
    def extract_client_docs(client: Client):
        if client.id not in server._storage:
            return []

        return [AES.decrypt(d.encrypted_title, client._keys.encryption_key, d.title_iv, d.title_tag).decode()
                for d in server._storage[client.id]]

    layout = [
        [sg.Text("This view is normally not possible since it requires knowing a client's key", text_color='darkRed')],
        [sg.Text("Client 1's files")],
        [sg.Listbox(extract_client_docs(clients[0]), size=(35, 5))],
        [sg.Text("Client 2's files")],
        [sg.Listbox(extract_client_docs(clients[1]), size=(35, 5))],
        [sg.Text("Client 3's files")],
        [sg.Listbox(extract_client_docs(clients[2]), size=(35, 5))],
        [sg.Button('Back')]]
    window = sg.Window("Storage Server", layout)

    event, _ = window.read()
    window.close()


def show_consultant():
    pass


while True:
    user = select_user()

    if user is None:
        break

    if user.startswith('client'):
        show_client(user)
    elif user == 'consultant':
        show_consultant()
    else:
        show_server()
