import pymysql


class Database:

    baseCreated = False

    def __init__(self):
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="1234",

        )
        self.cursor = self.db.cursor()
        self.createDatabase()

    def createTable(self):
        self.cursor.execute("USE carDb")
        sql = "DROP TABLE IF EXISTS automobili"

        self.cursor.execute(sql)

        sql = ''' 
        CREATE TABLE automobili(
            
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            price INT NOT NULL
        );
        
        '''
        self.cursor.execute(sql)
        self.db.commit()

    def addCard(self, name, price):
        sql = '''
        INSERT INTO automobili(name,price)
        VALUES(%s,%s);
        '''
        self.cursor.execute(sql, (name, price))
        self.db.commit()

    def findCar(self, name):
        sql = ''' 
        SELECT * FROM automobili
        WHERE name LIKE %s;
        
        '''
        self.cursor.execute(sql, (f'{name}%'))

        return self.cursor.fetchall()

    def updateCar(self, price, name):
        sql = ''' 
        UPDATE automobili
        SET price=%s
        WHERE name=%s;
        
        '''
        self.cursor.execute(sql, (price, name))
        self.db.commit()

    def deleteCar(self, name):
        sql = ''' 
        DELETE FROM automobili
        WHERE name=%s;
        '''
        self.cursor.execute(sql, (name))
        self.db.commit()

    def createDatabase(self):

        if not Database.baseCreated:
            self.cursor.execute("SHOW DATABASES LIKE 'carDb';")
            result = self.cursor.fetchone()

            if not result:
                sql = '''
                CREATE DATABASE carDb;
                '''
                self.cursor.execute(sql)
                self.cursor.execute("USE carDb")

                self.db.commit()
                Database.baseCreated = True


db = Database()
