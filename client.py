from tkinter import *
import socket
import json
from animation import ImgAnimation


class ClientApp:
    def __init__(self):

        # Main window
        self.window = Tk()
        self.window.geometry("600x700")
        self.window.title("Client")
        self.window.resizable(False, False)

        # Create header
        self.createHeader()

        # Create body
        self.createBody()
        self.clientButtons()

        # Create footer
        self.createFooter()
        self.window.mainloop()

    def connectToServer(self):
        c = socket.socket()
        c.connect(("localhost", 1234))
        return c

    def createHeader(self):
        frame = Frame(self.window, width=500, height=100)
        frame.pack(fill="both")

        # Create an instance of ImageAnimation and place it in the header frame
        image_paths = ["images/car1.jfif",
                       "images/car2.jfif", "images/car3.jfif"]
        header_animation = ImgAnimation(frame, image_paths, duration=1000)

    def createBody(self):
        self.frame = Frame(self.window, width=500, height=300)
        self.frame.pack(fill="both")
        labels = ["Name:", "Price:"]
        self.entries = []

        # Making labels and inputs
        for i, value in enumerate(labels):
            label = Label(self.frame, text=value, font=(
                "Times New Roman", 12, "bold"))
            label.grid(row=i, column=0, pady=10)

            field = Entry(self.frame)
            field.grid(row=i, column=1)
            self.entries.append(field)

        # Create label for server response
        labelResponse = Label(self.frame, text="Answers from server:", font=(
            "Times New Roman", 12, "bold"))
        labelResponse.grid(row=3, column=2)

        # Create listbox that holds server answers
        self.clientListBox = Listbox(self.frame, width=50)
        self.clientListBox.grid(row=4, column=1, columnspan=3)

    def clientButtons(self):
        buttonData = {

            "Create Table": self.createTable,
            "Add Car": self.addCar,
            "Find Car": self.findCar,
            "Update Car": self.updateCar,
            "Delete Car": self.deleteCar

        }

        for i, (key, value) in enumerate(buttonData.items()):
            button = Button(self.frame, text=key, command=value,
                            width=10, font=("Times New Roman", 10, "bold"))
            button.grid(row=2, column=i, padx=10, pady=20)

    def createFooter(self):
        frame = Frame(self.window, width=600, height=100)
        frame.pack(side="bottom", fill="both")
        label = Label(frame, text="Client Side",
                      font=("Times New Roman", 20, "bold"))
        label.place(x=200, y=50)

    # CRUD methods

    def createTable(self):

        request = {
            "request": "createTable"
        }

        c = self.connectToServer()
        f = json.dumps(request)
        c.send(f.encode())

        # Receive the message from the server
        message = c.recv(1024).decode()
        self.clientListBox.insert(0, message)
        c.close()

    def addCar(self):
        request = {
            "request": "addCar"
        }

        c = self.connectToServer()
        request["name"] = self.entries[0].get().strip().upper()
        request["price"] = self.entries[1].get().strip().upper()

        f = json.dumps(request)
        c.send(f.encode())

        # Recieve the message from server
        message = c.recv(1024).decode()
        self.clientListBox.insert(0, message)

        c.close()

    def findCar(self):
        request = {
            "request": "findCar"
        }
        request["name"] = self.entries[0].get().upper()
        c = self.connectToServer()
        f = json.dumps(request)
        c.send(f.encode())

        # Receive the message from server
        message = c.recv(1024).decode()
        self.clientListBox.insert(0, message)

        c.close()

    def updateCar(self):
        request = {
            "request": "updateCar"
        }
        request["name"] = self.entries[0].get().upper()
        request["price"] = self.entries[1].get().upper()

        c = self.connectToServer()
        f = json.dumps(request)
        c.send(f.encode())

        # Receive the message from server
        message = c.recv(1024).decode()
        self.clientListBox.insert(0, message)

        c.close()

    def deleteCar(self):
        request = {
            "request": "deleteCar"
        }
        c = self.connectToServer()
        request["name"] = self.entries[0].get().upper()
        f = json.dumps(request)
        c.send(f.encode())

        # Receive the message from server
        message = c.recv(1024).decode()
        self.clientListBox.insert(0, message)

        c.close()


ClientApp()
