def generate_data_source_name(user: str, password: str, host: str, port: int, database_name: str):
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database_name}"
