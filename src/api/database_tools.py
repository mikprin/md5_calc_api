# Database
import sqlalchemy as db
import sqlalchemy_utils as db_util
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Enum, BigInteger, Integer, String
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()




# Classes for database tables

class FileForProcessing(Base):
    __tablename__ = "files_quene"
    id = Column(Integer,primary_key=True,autoincrement=False)
    filename = Column( String )
    md5_hash = Column(String , nullable=True)
    worker_id = Column( Integer, nullable=True )
    saved_timestamp = Column ( Integer, nullable=True )
    
def __repr__(self):
        return "<User(id='%d', filename='%s')>" % (
                                self.id, self.filename)   












## Work with database (init of SQLAlchemy) ##

def get_postgres_engine(user,password,host,port, pgdb,debug=False):
    url = f"postgresql://{user}:{password}@{host}:{port}/{pgdb}"
    if not db_util.database_exists(url):
        db_util.create_database(url)
        print("No database found, database created")
    engine = db.create_engine(url,pool_size=50, echo=debug)
    print(f"connected to database {engine.url}")
    return engine

def get_session(postgres_credentials):
    engine = get_postgres_engine(
        postgres_credentials['pguser'],
        postgres_credentials['pgpassword'],
        postgres_credentials['pghost'],
        postgres_credentials['pgport'],
        postgres_credentials['pgdb']
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    
    return session,engine
