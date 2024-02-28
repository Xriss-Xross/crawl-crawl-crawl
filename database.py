import os, sqlite3


class db_utils:
    def __init__(self):
        self.init = False
        if not os.path.exists("db"):
            self.init = True
            os.makedirs("db")
        
        self.conn = sqlite3.connect("db/data.db")
        self.cursor = self.conn.cursor()
        self.create_character()
        if self.init == True:
            self.first_create()
            self.init = False


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
                "Enemies_Spawned"   INTEGER,
                "Time"   INTEGER,
                "Map"   STRING
            )
        """)

    def first_create(self):
        self.execute("""
            INSERT INTO "Characters" (CharacterID, Max_Health, Max_Shield, Damage, Speed, XP, Enemies_Defeated, Enemies_Spawned, Time)
            VALUES (1, 4, 10, 1, 3, 0, 0, 0, 0)
        """)
        self.execute("""
            INSERT INTO "Characters" (CharacterID, Max_Health, Max_Shield, Damage, Speed, XP, Enemies_Defeated, Enemies_Spawned, Time)
            VALUES (2, 4, 10, 1, 3, 0, 0, 0, 0)
        """)
        self.execute("""
            INSERT INTO "Characters" (CharacterID, Max_Health, Max_Shield, Damage, Speed, XP, Enemies_Defeated, Enemies_Spawned, Time)
            VALUES (3, 4, 10, 1, 3, 0, 0, 0, 0)
        """)
        self.execute("""
            INSERT INTO "Characters" (CharacterID, Max_Health, Max_Shield, Damage, Speed, XP, Enemies_Defeated, Enemies_Spawned, Time)
            VALUES (4, 4, 10, 1, 3, 0, 0, 0, 0)
        """)

    def execute(self, query):
        try:
            val = self.cursor.execute(query)
            self.conn.commit()
            return val
        except Exception as e:
            print(f"Error: {e}")
