    def addCar(self):
        request = {
            "request": "addCar"
        }

        c = self.connectToServer()
        request["name"] = self.entries[0].get().strip().upper()
        request["price"] = self.entries[1].get().upper()

        f = json.dumps(request)
        c.send(f.encode())

        # Recieve the message from server
        message = c.recv(1024).decode()
        self.clientListBox.insert(0, message)

        c.close()