import os

import PySimpleGUI as sg

from client import Client
from consultant import Consultant
from models import AES
from protocols import setup, upload_storage_server_filename, search_storage_server_filenames
from storage import StorageServer

sg.theme('Dark Blue 3')  # please make your windows colorful

# Create a setup with three clients
consultant = Consultant()
clients = [Client(), Client(), Client()]
server = StorageServer()

setup(consultant, clients)


def select_user() -> str:
    layout = [[sg.Text('Select a user')],
              [sg.Button("Client 1", key='client1'),
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
              [sg.Listbox([], size=(50, 5), key='results', enable_events=True)],
              [sg.Button('Download', key='download', disabled=True)],
              [sg.HorizontalSeparator()],
              [sg.Button('Back')]]
    window = sg.Window(client_text, layout)

    can_upload = False
    can_download = False
    results = []

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Back':
            break

        elif event == 'input':
            filepath = values['input']
            if not os.path.isfile(filepath):
                # Do nothing if this file does not exist
                continue

            can_upload = True

            with open(values['input']) as file:
                doc = file.read()
                keywords = {word.lower() for word in doc.split()}
                window['keywords'].update(", ".join(keywords))

            window['success'].update("")

        elif event == 'upload':
            if not can_upload:
                window['success'].update("Not ready to upload")
                continue

            upload_storage_server_filename(clients[client_index], server, os.path.basename(filepath), doc,
                                           keywords)
            window['success'].update("Uploaded succesfully")
            window['keywords'].update("")
            window['input'].update("")

        elif event == 'search':
            keywords = {kw.lower() for kw in values['search_string'].split()}
            results = search_storage_server_filenames(clients[client_index], server, keywords)
            window['results'].update([title for title, _ in results])

            can_download = False
            window['download'].update(disabled=True)

        elif event == 'results':
            if len(values['results']) > 0:
                can_download = True
                window['download'].update(disabled=False)
            else:
                can_download = False
                window['download'].update(disabled=True)

        elif event == 'download':
            if not can_download:
                continue

            encrypted_title = None
            for title, enc_title in results:
                if title == values['results'][0]:
                    encrypted_title = enc_title
                    break

            doc = server.download_document(encrypted_title, clients[client_index].id)

            key = clients[client_index]._keys.encryption_key
            doc_title = AES.decrypt(doc.encrypted_title, key, doc.title_iv, doc.title_tag).decode()
            doc_contents = AES.decrypt(doc.ciphertext, key, doc.iv, doc.auth_tag).decode()

            with open(f"DWNLD-{doc_title}", mode='w') as file:
                file.write(doc_contents)

            can_download = False
            window['download'].update(disabled=True)

    window.close()


def show_server():
    decrypted = False

    def extract_client_docs(client: Client):
        if client.id not in server._storage:
            return []

        if decrypted:
            return [AES.decrypt(d.encrypted_title, client._keys.encryption_key, d.title_iv, d.title_tag).decode()
                    for d in server._storage[client.id]]
        else:
            return [d.encrypted_title for d in server._storage[client.id]]

    layout = [
        [sg.Checkbox("Decrypted view", key='decrypt', enable_events=True)],
        [sg.Text(key='warning', text_color='darkRed', size=(85, 1))],
        [sg.Text("Client 1's files")],
        [sg.Listbox(extract_client_docs(clients[0]), size=(85, 5))],
        [sg.Text("Client 2's files")],
        [sg.Listbox(extract_client_docs(clients[1]), size=(85, 5))],
        [sg.Text("Client 3's files")],
        [sg.Listbox(extract_client_docs(clients[2]), size=(85, 5))],
        [sg.Button('Back')]]
    window = sg.Window("Storage Server", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Back':
            break

        elif event == 'decrypt':
            if values['decrypt']:
                decrypted = True
                window['warning'].update("This view is normally not possible since it requires knowing a client's key")
            else:
                decrypted = False
                window['warning'].update("")

            window[0].update(extract_client_docs(clients[0]))
            window[1].update(extract_client_docs(clients[1]))
            window[2].update(extract_client_docs(clients[2]))

    window.close()


while True:
    user = select_user()

    if user is None:
        break

    if user.startswith('client'):
        show_client(user)
    else:
        show_server()
