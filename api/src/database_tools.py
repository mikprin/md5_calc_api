# Database
from hashlib import new
import sqlalchemy as db
import time, random
import logging
import sqlalchemy_utils as db_util
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Enum, BigInteger, Integer, String
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()

from settings import *


## Connect to database (init of SQLAlchemy) ##

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

# Classes for database tables

class FileForProcessing(Base):
    __tablename__ = "files_quene"
    id = Column(Integer,primary_key=True,autoincrement=False)
    filename = Column( String )
    md5_hash = Column(String , nullable=True)
    worker_id = Column( Integer, nullable=True )
    saved_timestamp = Column ( Integer, nullable=True )
    
def __repr__(self):
        # return "<User(id='%d', filename='%s')>" % (
        #                         self.id, self.filename)   
        return f"File id={self.id} , filename={self.filename}"


class API_database( ):
    """My own class to interact with database (assuming connected to session and engine"""
    def __init__(self,database_sesstion,database_engine):
        self.engine = database_engine
        self.session = database_sesstion

    def add_file_to_quene(self,id, filename):
        database_record = FileForProcessing(id=id, filename=filename, saved_timestamp = time.time())
        self.session.add( database_record )
        #TODO cach exeptions here
        try:
            self.session.commit()
            logging.info(f'Sucsessfully added file {id} to database.')
            return 1
        except Exception as error:
            logging.error(f"FAILED TO ADD COMMIT TO DATABASE")
            logging.error(f"Error message: {error}")
            self.session.rollback()
            logging.info(f"Database rollback")
            return 0
        
    def get_new_id(self):
        ids =  self.get_all_ids()
        ids.sort()
        try:
            new_id = [x for x in range(ids[0], ids[-1]+1) if x not in ids][0]
        except IndexError:
            new_id = ids[-1] + 1
        return new_id

    def get_all_ids(self):
        ids = self.session.query(FileForProcessing.id).all()
        ids_list = [i[0] for i in ids]
        return ids_list
        
    def drop_all_files(self):
        # FileForProcessing.__table__.drop(self.engine) # NOT WORKING COORECTLY!
        for id in self.get_all_ids():
            self.session.query(FileForProcessing).filter(FileForProcessing.id==id).delete()
            # file_to_delete = FileForProcessing.query.get(id)
            # self.session.delete(file_to_delete)
        self.session.commit()

# def add_file_to_database(id,path):
#     timestamp = int(time.time())




