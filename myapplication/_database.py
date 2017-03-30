from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, session_maker
#from sqlalchemy.ext.declarative import declarative_base()

engine = create_engine("sqlite:////tmp", convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

#Base = declarative_base()
#Base.query = db_session.query_property()

#def init_db():
#    import myapplication._models     #myapplication 是文件名
#    Base.matedata.create_all(bind=engine)
def init_db():
    metadata.create_all(bind=engine)