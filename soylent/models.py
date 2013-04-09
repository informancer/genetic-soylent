from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class NutrientName(Base):
    __tablename__ = "NutrientNames"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    def __str__(self):
        return self.name

class Nutrient(Base):
    __tablename__ = "Nutrients"
    
    id = Column(Integer, primary_key=True)
    nutrient_name_id = Column(Integer, ForeignKey("NutrientNames.id"))
    
    canonical_name = relationship("NutrientName")

    def __init__(self, name):
        self.canonical_name = NutrientName(name=name)

    def __str__(self):
        return str(self.canonical_name)
