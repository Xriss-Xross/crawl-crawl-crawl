import os, sqlite3


class db_utils:
    def __init__(self):
        if not os.path.exists("db"):
            os.makedirs("db")
        
        self.conn = sqlite3.connect("db/data.db")
        self.cursor = self.conn.cursor()
        self.create_character()
    

    def create_character(self):
        self.execute("""
            CREATE TABLE "Characters" (
                "CharacterID"   INTEGER,
                "Max_Health"    INTEGER,
                "Max_Shield"    INTEGER,
                "Damage"    INTEGER,
                "Speed" INTEGER,
                "XP"    INTEGER,
                "Enemies_Defeated"  INTEGER,
                "Enemies_Spawned"   INTEGER
            )
        """)

    def execute(self, query):
        try:
            val = self.cursor.execute(query)
            self.conn.commit()
            return val
        except Exception as e:
            print(f"Error: {e}")
