import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS productes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            preu REAL NOT NULL,
            quantitat INTEGER NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def get_all_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM productes")
        return cursor.fetchall()

    def add_product(self, nom, preu, quantitat):
        query = "INSERT INTO productes (nom, preu, quantitat) VALUES (?, ?, ?)"
        self.conn.execute(query, (nom, preu, quantitat))
        self.conn.commit()

    def update_product(self, product_id, nom, preu, quantitat):
        query = "UPDATE productes SET nom=?, preu=?, quantitat=? WHERE id=?"
        self.conn.execute(query, (nom, preu, quantitat, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        query = "DELETE FROM productes WHERE id=?"
        self.conn.execute(query, (product_id,))
        self.conn.commit()
