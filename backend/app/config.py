DATABASE_URL = "postgresql://username:password@localhost/dbname"

class Settings:
    def __init__(self):
        self.database_url = DATABASE_URL

settings = Settings()