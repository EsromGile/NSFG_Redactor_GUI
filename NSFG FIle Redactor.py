import PySimpleGUI as sg
import os

def main():

    font = "Arial 14"
    messages = ""

    message_box = [
        [sg.Multiline("Message Box", size=(60,5), enable_events=False, key="MESSAGE_BOX")]
    ]

    centered_button = [
        [sg.Button("Redact Folder", size=(15, 1), disabled=True, key="REDACT_BUTTON")]
    ]

    file_list_column = [
        [
            sg.Text("Folder to Redact"),
            sg.In(size=(68,1), enable_events=True, key="FOLDER"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(values=[], enable_events=False, size=(90, 20), key="FILE_LIST")
        ]
    ]


    layout = [
        [sg.Column(file_list_column)],
        [sg.Column(message_box), sg.Push(), sg.Column(centered_button), sg.Push()]
    ]

    window = sg.Window("File Redactor", layout, font=font)

    def deleteMessage(path, msg, currentText):
        os.remove(path)
        currentText += msg
        window["MESSAGE_BOX"].update(currentText)
        return currentText

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "FOLDER":
            folder = values["FOLDER"]
            try:
                files = os.listdir(folder)
            except:
                files = []

            window["FILE_LIST"].update(files)
            window["REDACT_BUTTON"].update(disabled=False)

        if event == "REDACT_BUTTON":

            folder = values["FOLDER"]
            try:
                files = os.listdir(folder)
                renamedCount = 0
                deletedCount = 0

                for i in range(0, len(files)):

                    # get file extension
                    filePath = os.path.join(folder, files[i])
                    splitFileName = os.path.splitext(files[i])
                    ending = splitFileName[1]

                    # remove non-prossessable files
                    if not (ending == ".docx" or ending == ".doc" or ending == ".pdf"):
                        messages = deleteMessage(filePath, "===== Deleting file of type {}...\n".format(ending), messages)
                        deletedCount += 1
                        continue

                    # check for valid file name
                    dash_count = files[i].count('-')
                    if dash_count <= 3: continue

                    indexes = [pos for pos, char in enumerate(files[i]) if char == '-']

                    if i != 0:
                        currentNumbers = files[i][:indexes[1]-1]
                        previousNumbers = files[i-1][:indexes[1]-1]
                        if currentNumbers == previousNumbers:
                            messages = deleteMessage(os.path.join(folder, files[i-1]), "===== Deleting duplicate...\n", messages)
                            deletedCount += 1
                            continue

                    redactedFile = files[i][:indexes[1]] + files[i][indexes[2]:indexes[3]-1] + ending
                    files[i] = redactedFile
                    os.rename(filePath, os.path.join(folder, redactedFile))
                    renamedCount += 1
                    
                messages += ('===== Successfully renamed {} file(s) from {}\n'.format(renamedCount, folder))
                if deletedCount > 0:
                    messages += ('===== Successfully deleted {} file(s) from {}\n'.format(deletedCount, folder))
                messages += "\n"
                window["MESSAGE_BOX"].update(messages)
            except:
                messages += ("xxxxxx File rename error\n")
                messages +=("       Reload and try again.\n\n")
                window["MESSAGE_BOX"].update(messages)

            files = os.listdir(folder)
            window["FILE_LIST"].update(files)
            
    window.close()

if __name__ == '__main__':
    main()