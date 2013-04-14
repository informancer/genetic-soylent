from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

# Definition of nutrient

class Nutrient(Base):
    __tablename__ = "Nutrients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

# End of Nutrient definition

# Definition of Ingredient
class Ingredient(Base):
    __tablename__ = "Ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    serving_size = Column(Integer)
    serving_unit = Column(String)

    def __init__(self, name, serving_size, serving_unit):
        self.name = name
        self.serving_size = serving_size
        self.serving_unit = serving_unit

    def __str__(self):
        return self.name
        
# End of ingredient definition

# Association between ingredient and nutrients
class IngredientNutrient(Base):
    __tablename__ = "IngredientsNutrients"
    
    ingredient_id = Column(Integer, ForeignKey("Ingredients.id"), primary_key=True)
    nutrient_id = Column(Integer, ForeignKey("Nutrients.id"), primary_key=True)
    quantity = Column(Integer)
    unit = Column(String)

# End of ingedients nutrients association definition

