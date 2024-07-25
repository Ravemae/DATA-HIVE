from sqlmodel import create_engine, SQLModel, Session


sql_url = "sqlite:///Archive.db"
engine = create_engine(sql_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
    
def get_session():
    with Session(engine) as session:
        yield session
    