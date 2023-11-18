from tkinter import *
import socket
import threading
import json
from database import db
from tkinter import messagebox

print("Server is listening....")


class ServerApp:
    createdTable = False

    def __init__(self):
        # Threading
        self.t = threading.Thread(target=self.acceptConnection)
        self.t.daemon = True
        self.t.start()

        # Currently Cars that are in database
        self.cars = []

        # Server interface
        self.serverInterface()

    def acceptConnection(self):
        s = socket.socket()
        s.bind(("localhost", 1234))
        s.listen(5)

        while True:
            c, add = s.accept()
            data = c.recv(1024).decode()
            request = json.loads(data)
            message = ""

            if data:
                # Create a new table to database
                if request["request"] == "createTable":
                    db.createTable()
                    message = "Table has been created"
                    self.clientRequests.insert(
                        0, f"Request from client: create table")
                    ServerApp.createdTable = True
                    c.send(message.encode())

                # If table has not been created,cant use operations like find,update and delete
                if ServerApp.createdTable:

                    # Add car to database
                    if request["request"] == "addCar":
                        if request["name"] != "" and request["price"] != "":
                            db.addCard(
                                request["name"], request["price"])
                            self.cars.append(request["name"])
                            message = f"{request['name']} has been added successfully"
                            self.clientRequests.insert(
                                0, f"Request from client: add a car")

                        else:
                            messagebox.showinfo(
                                "Validation Error", "Please fill inputs with proper values")

                    # Find selected car from database
                    if request["request"] == "findCar":
                        if request["name"] == "":
                            messagebox.showinfo("Please fill input name")
                            self.clientRequests.insert(
                                0, "Request from client: find a car")

                        if request["name"] in self.cars:

                            message = ""
                            res = db.findCar(request["name"])

                            for car in res:
                                carId, carName, carValue = car
                                message += f"---{carName} Price:{carValue}---"

                                self.clientRequests.insert(
                                    0, "Request from client: find a car")

                        elif request["name"] not in self.cars:
                            messagebox.showinfo("Search error",
                                                f"{request['name']} does not exist in database")

                    # Update information about existing car
                    if request["request"] == "updateCar":
                        if request["name"] in self.cars and request["price"] != "":
                            db.updateCar(request["price"], request["name"])
                            message = f"Information about {request['name']} has been updated"
                            self.clientRequests.insert(
                                0, "Request from client: update a car price")

                        elif request["name"] not in self.cars and request["price"] != "":
                            message = f"The {request['name'] } does not exist in database"

                        elif request["name"] == "" or request["price"] == "":

                            messagebox.showinfo("Input error",
                                                "Please fill the form with proper values")

                    # Delete selected car from database
                    if request["request"] == "deleteCar":

                        if request["name"] == "":
                            messagebox.showinfo(
                                "Input Error", "Please fill the car name")
                        elif request["name"] not in self.cars:
                            messagebox.showinfo(
                                "Delete Error", "The car does not exist in database")
                        else:
                            db.deleteCar(request["name"])
                            message = f"The car {request['name']} has been removed"
                            self.cars.pop(self.cars.index(request["name"]))
                            self.clientRequests.insert(
                                0, "Request from client: remove a car from database")

                    # Send the message to the user
                    c.send(message.encode())
                else:
                    messagebox.showinfo("Eror", "Please create a table first")
            c.close()

    def serverInterface(self):
        # Main Server`s window
        self.window = Tk()
        self.window.title("Server")
        self.window.geometry("500x700")

        # Server`s labels
        label = Label(self.window, text="Requests from client: ",
                      font=("Times New Roman", 10, "bold"))
        label.pack()

        footerLabel = Label(self.window, text="Server Side",
                            font=("Times New Roman", 20, "bold"))
        footerLabel.pack(side="bottom")

        # Server`s list of client requests
        self.clientRequests = Listbox(self.window, width=50)
        self.clientRequests.pack()

        self.window.mainloop()


ServerApp()
