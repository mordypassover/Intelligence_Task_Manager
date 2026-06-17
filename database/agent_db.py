from database.db_connection import DBConnection
class AgentDB:
    def __init__(self):
        a = DBConnection()
        self. conn = a.get_connection

    def create_agent(self, data):
        conn =self.conn()
        cursor = conn.cursor(dictionary=True)
        query = "INSERT INTO agent_db (name, specialty, agent_rank) VALUES (%s, %s, %s)"
        cursor.execute(query,(data["name"], data["specialty"], data["agent_rank"]))
        new_agent = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_agent

    def get_all_agents(self):
        conn = self.conn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM agent_db"
        cursor.execute(query)
        all = cursor.fetchall()
        cursor.close()
        conn.close()
        return all

    def get_agent_by_id(self, id):
        conn = self.conn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM agent_db WHERE id =%s"
        cursor.execute(query, (id,))
        agent = cursor.fetchone()
        cursor.close()
        conn.close()
        return agent

    def update_agent(self, id, data):
        if "id" in data.keys():
            raise KeyError("cang update id")
        keys = [f"{k}=%s" for k in data.keys()]
        key_string = ", ".join(keys)
        conn =self.conn()
        cursor = conn.cursor()
        query = f"UPDATE agent_db SET {key_string} WHERE id =%s"
        cursor.execute(query, [data[k] for k in data.keys()]+[id])
        is_updated = cursor.rowcount >0
        conn.commit()
        cursor.close()
        conn.close()
        return is_updated



if __name__ == "__main__":
    a = AgentDB()
    #print(a.create_agent({"name":"mordy", "specialty":"qwer","agent_rank":"senior"}))
    print(a.get_all_agents())
    print(a.get_agent_by_id(1))
    # print(a.update_agent(1,{"specialty":"wer"} ))