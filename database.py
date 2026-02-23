from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "root"
PASS = "1234"
SERVER = "localhost"
PORT = "3306"
DB = "mysql"         

engine = create_engine(f"mysql+pymysql://{USER}:{PASS}@{SERVER}:{PORT}/{DB}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    author = Column(String(100))
    year = Column(Integer)
    image_url = Column(String(100))