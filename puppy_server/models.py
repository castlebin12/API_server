from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Puppy(Base):
    '''
    puppy table로 puppies.db에 테이블 생성 및 serialize를 통해 데이터 통합
    '''
    __tablename__ = 'puppy'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description
        }

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)

