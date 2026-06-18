from database.db_connection import DBConnection
class MissionDB:
    def __init__(self):
        a = DBConnection()
        self.conn = a.get_connection

    def create_mission(self, data):
        conn = self.conn()
        cursor = conn.cursor(dictionary=True)
        query = "INSERT INTO missions_db (title, description, location, difficulty, importance, risk_level) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (data["title"], data["description"], data["location"],  data["difficulty"],  data["importance"],self.calc_risk_level(data)))
        new_mission = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_mission

    def calc_risk_level(self, data):
        calc = data["difficulty"] * 2 + data["importance"]
        if calc < 10:
            return "LOW"
        elif calc < 18:
            return "MEDIUM"
        elif calc < 25:
            return "HIGH"
        else:
            return "CRITICAL"

    def get_all_missions(self):
        conn = self.conn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM missions_db"
        cursor.execute(query)
        all = cursor.fetchall()
        cursor.close()
        conn.close()
        return all

    def get_mission_by_id(self, id):
        conn = self.conn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM missions_db WHERE id =%s"
        cursor.execute(query, (id,))
        mission = cursor.fetchone()
        cursor.close()
        conn.close()
        return mission

    def assign_mission(self, m_id, a_id):
        conn = self.conn()
        cursor = conn.cursor()
        query = f"UPDATE missions_db SET assigned_agent_id = %s WHERE id =%s"
        cursor.execute(query, (a_id,m_id))
        is_updated = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        self.update_mission_status(m_id,"ASSIGNED")
        return is_updated

    def update_mission_status(self, id, status):
        conn = self.conn()
        cursor = conn.cursor()
        query = f"UPDATE missions_db SET status = %s WHERE id =%s"
        cursor.execute(query, (status, id))
        is_updated = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return is_updated

    def get_open_missions_by_agent(self, id):
        conn = self.conn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM missions_db WHERE status = 'ASSIGNED' AND assigned_agent_id = %s OR status ='IN_PROGRESS' AND assigned_agent_id = %s"
        cursor.execute(query,(id,id))
        opened = cursor.fetchall()
        cursor.close()
        conn.close()
        return opened

    def count_all_missions(self):
        conn = self.conn()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM missions_db"
        cursor.execute(query)
        cnt = cursor.fetchone()
        cursor.close()
        conn.close()
        return cnt[0]

    def count_by_status(self, status):
        conn = self.conn()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM missions_db where status =%s"
        cursor.execute(query,(status,))
        cnt = cursor.fetchone()
        cursor.close()
        conn.close()
        return cnt[0]

    def count_open_missions(self):
        conn = self.conn()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM missions_db WHERE status = 'NEW' OR status = 'ASSIGNED' OR status = 'IN_PROGRESS'"
        cursor.execute(query)
        cnt = cursor.fetchone()
        cursor.close()
        conn.close()
        return cnt[0]

    def count_critical_missions(self):
        conn = self.conn()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM missions_db WHERE risk_level ='CRITICAL'"
        cursor.execute(query)
        cnt = cursor.fetchone()
        cursor.close()
        conn.close()
        return cnt[0]

    def get_top_agent(self):
        conn = self.conn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM missions_db "
        cursor.execute(query)
        all = cursor.fetchall()
        cursor.close()
        conn.close()

        all_agents_compleat ={}
        for i in all():
            if i["status"] == "COMPLETED":
                if i["assigned_agent_id"] in all_agents_compleat:
                    all_agents_compleat[i["assigned_agent_id"]] +=1
                else:
                    all_agents_compleat[i["assigned_agent_id"]] += 1
        max_agent={}
        for key, val in all_agents_compleat.items():
            if not max_agent or val > max_agent["compleat"]:
                max_agent ={"agent":key, "compleat": val}

        return max_agent


if __name__ == "__main__":
    a = MissionDB()
    #print(a.create_mission({"title":"s", "description":"a", "location":"xz", "difficulty":7, "importance":4}))
    print(a.get_all_missions())
    print(a.get_mission_by_id(2))
    #print(a.assign_mission(2,2))
    print(a.get_open_missions_by_agent(2))
    print(a.count_all_missions())
    print(a.count_by_status("NEW"))
    print(a.count_open_missions())
    print(a.count_critical_missions())