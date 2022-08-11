from pydantic import BaseSettings, Field

from database.data_source_name import generate_data_source_name

import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Запуск приложения
# uvicorn main:app --host "0.0.0.0" --port 8000 --reload

class DBSettings(BaseSettings):


    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_DATABASE: str = os.getenv("DB_DATABASE")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")

    #DB_USERNAME: str = Field(env='DATABASE_USERNAME')
    #DB_PASSWORD: str = Field(env='DATABASE_PASSWORD')
    #DB_DATABASE: str = Field(env='DATABASE_NAME')
    #DB_HOST: str = Field(env='DATABASE_HOST')
    #DB_PORT: int = Field(env='DATABASE_PORT')


    @property
    def data_source_name(self):
        return generate_data_source_name(
            user=self.DB_USERNAME, password=self.DB_PASSWORD,
            host=self.DB_HOST, port=self.DB_PORT, database_name=self.DB_DATABASE
        )


db_settings = DBSettings()
