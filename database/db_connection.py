import mysql.connector


class DBConnection:
    def __init__(self):
        self.database = "Intelligence_db"
        self.password = "1234"
        self.user = "root"
        self.host = "localhost"
        self.create_database()
        self.create_tables()

    def get_connection(self):
        return mysql.connector.connect(
            database = self.database,
            password = self.password,
            user = self.user,
            host = self.host
        )

    def create_database(self):
        conn = mysql.connector.connect(
            password = self.password,
            user = self.user,
            host = self.host)
        cursor = conn.cursor()
        query = "CREATE DATABASE IF NOT EXISTS Intelligence_db"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = ("""CREATE TABLE IF NOT EXISTS agent_db (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 name VARCHAR(50) NOT NULL,
                 specialty VARCHAR(50) NOT NULL,
                 is_active BOOLEAN DEFAULT TRUE,
                 completed_missions INT DEFAULT 0,
                 failed_missions INT DEFAULT 0,
                 agent_rank ENUM("Junior", "Senior", "Commander") NOT NULL)""",
                """CREATE TABLE IF NOT EXISTS missions_db (
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 title VARCHAR(50) NOT NULL,
                 description TEXT NOT NULL,
                 location VARCHAR(50) NOT NULL,
                 difficulty INT CHECK(difficulty < 11 AND difficulty > 0) NOT NULL,
                 importance INT CHECK(importance < 11 AND importance > 0) NOT NULL,
                 status ENUM('NEW','ASSIGNED','IN_PROGRESS','COMPLETED','FAILED','CANCELLED') DEFAULT 'NEW',
                 risk_level VARCHAR(50) NOT NULL,
                 assigned_agent_id INT NULL DEFAULT NULL)""")


        for i in query:
            cursor.execute(i)
            conn.commit()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    a = DBConnection()
    a.create_database()
    a.create_tables()
