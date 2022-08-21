# Database
from hashlib import new
import sqlalchemy as db
import time, random, pickle
import logging
import sqlalchemy_utils as db_util
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Enum, BigInteger, Integer, String
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()

from settings import *


## Connect to database (init of SQLAlchemy) ##

def get_postgres_engine(user,password,host,port, pgdb,debug=False):
    """Postgres session init"""
    url = f"postgresql://{user}:{password}@{host}:{port}/{pgdb}"
    logging.info(f"Connecting to `{url}` database")
    if not db_util.database_exists(url):
        db_util.create_database(url)
        logging.info(f"No database found, database created")
    engine = db.create_engine(url,pool_size=50, echo=debug)
    logging.info(f"connected to database {engine.url}")
    return engine

def get_session(postgres_credentials, debug=False):
    """Postgres session init"""
    engine = get_postgres_engine(
        postgres_credentials['pguser'],
        postgres_credentials['pgpassword'],
        postgres_credentials['pghost'],
        postgres_credentials['pgport'],
        postgres_credentials['pgdb'],
        debug=debug
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return session,engine

# Classes for database tables

class FileForProcessing(Base):
    """API file quene class. Creates and works with `files_quene`"""
    __tablename__ = "files_quene"
    id = Column(Integer,primary_key=True,autoincrement=False)
    filename = Column( String )
    md5_hash = Column(String , nullable=True)
    worker_id = Column( String, nullable=True )
    saved_timestamp = Column ( Integer, nullable=True )
    
    def __repr__(self):
            return f"File id={self.id} , filename={self.filename}"


class API_database( ):
    """My own class to interact with database (assuming connected to session and engine"""
    def __init__(self,database_sesstion,database_engine):
        self.engine = database_engine
        self.session = database_sesstion

    def add_file_to_quene(self,id, filename):
        """Create new file object in database"""
        database_record = FileForProcessing(id=id, filename=filename, saved_timestamp = time.time())
        self.session.add( database_record )
        #TODO cach exeptions here
        return self.commit_database(id)
        
    def get_new_id(self):
        """Invent new ID"""
        ids =  self.get_all_ids()
        ids.sort()
        try:
            new_id = [x for x in range(ids[0], ids[-1]+1) if x not in ids][0]
        except IndexError:
            if len(ids) > 0:
                new_id = ids[-1] + 1
            else: new_id = 1
        return new_id

    def add_worker_id(self,id,worker_id):
        """add celery task ID to quene database table"""
        self.session.query(FileForProcessing).filter(FileForProcessing.id == id).update({'worker_id': worker_id})
        return self.commit_database(id)

    def get_all_ids(self):
        """Get all ids from quene table"""
        ids = self.session.query(FileForProcessing.id).all()
        ids_list = [i[0] for i in ids]
        return ids_list
    
    def commit_database(self, id = None):
        """Cearfully commit to database. No sudden moves."""
        try:
            self.session.commit()
            logging.info(f'Sucsessfully commited record {id}.')
            return 1
        except Exception as error:
            logging.error(f"FAILED TO ADD COMMIT TO DATABASE when working with {id}")
            logging.error(f"Error message: {error}")
            self.session.rollback()
            logging.info(f"Database rollback")
            return 0

    def get_hashing_results(self, id):
        """Get hash results of request file id"""
        logging.debug(f"Looking for worker for element {id}")
        with self.engine.connect() as conn:
            result = conn.execute(f"SELECT * from files_quene WHERE id = '{id}'").all()
        if result != []:
            worker_id = self.session.query(FileForProcessing).get(id).worker_id
            logging.debug(f"Worker for  `{id}` found: {worker_id}")

            with self.engine.connect() as conn:
                result = conn.execute(f"SELECT task_id,status,result from celery_taskmeta WHERE task_id = '{worker_id}'").all()
            if result != []:
                result_row = result[0]
                status = result_row[1]
                if status == "SUCCESS":
                    hash = pickle.loads(result_row[2])
                    logging.debug(f"Status {status} for element {id} with hash {hash}")
                    return { "status" : status , "hash" : hash }
                else:
                    return { "status" : status , "hash" : None }
            else:
                # No worker found
                return { "status" : "FIND_WORKER_ERROR" , "hash" : None }
        else:
            return { "status" : "INVALID_ID" , "hash" : None }
    
    def drop_all_files(self):
        """Delete database table. Cruel."""
        for id in self.get_all_ids():
            self.session.query(FileForProcessing).filter(FileForProcessing.id==id).delete()
            # file_to_delete = FileForProcessing.query.get(id)
            # self.session.delete(file_to_delete)
        self.session.commit()





