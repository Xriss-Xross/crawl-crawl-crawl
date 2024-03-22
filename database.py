import os, sqlite3


class db_utils:
    def __init__(self):
        self.init = False
        if not os.path.exists("db"):  # database is being created for the first time
            self.init = True          
            os.makedirs("db")

        self.conn = sqlite3.connect("db/data.db")  # boiler plate
        self.cursor = self.conn.cursor()
        self.create_character()  # attempts to create table

        if self.init == True:
            self.first_create()  # if the default values weren't created
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
                "Final_Time"   INTEGER,
                "Level"   INTEGER,
                "Map"   STRING
            )
        """)

    def first_create(self):
        self.execute("""
            INSERT INTO "Characters" (CharacterID, Max_Health, Max_Shield, Damage, Speed, XP, Enemies_Defeated, Enemies_Spawned, Time, Final_Time, Level)
            VALUES (1, 4, 10, 1, 3, 0, 0, 0, 0, 0, 0)
        """)    
        self.execute("""
            INSERT INTO "Characters" (CharacterID, Max_Health, Max_Shield, Damage, Speed, XP, Enemies_Defeated, Enemies_Spawned, Time, Final_Time, Level)
            VALUES (2, 4, 10, 1, 3, 0, 0, 0, 0, 0, 0)
        """)
        self.execute("""
            INSERT INTO "Characters" (CharacterID, Max_Health, Max_Shield, Damage, Speed, XP, Enemies_Defeated, Enemies_Spawned, Time, Final_Time, Level)
            VALUES (3, 4, 10, 1, 3, 0, 0, 0, 0, 0, 0)
        """)
        self.execute("""
            INSERT INTO "Characters" (CharacterID, Max_Health, Max_Shield, Damage, Speed, XP, Enemies_Defeated, Enemies_Spawned, Time, Final_TIme, Level)
            VALUES (4, 4, 10, 1, 3, 0, 0, 0, 0, 0, 0)
        """)

    def execute(self, query):
        try:
            value = self.cursor.execute(query)
            self.conn.commit()  # makes sure the database isn't locked
            return value
        except Exception as e:
            print(f"Error: {e}")  # error handling for if a request is bad

