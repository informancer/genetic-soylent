from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.collections import attribute_mapped_collection

from magnitude import mg

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
    serving_size = Column(Float)
    serving_unit = Column(String)

    nutrients = association_proxy("ingredient_nutrients", "nutrient")

    def __init__(self, name, serving_size, serving_unit):
        self.name = name
        
        # use the magnitude in order to ensure that the unit is known
        self.serving = mg(serving_size, serving_unit)

    @property
    def serving(self):
        return mg(self.serving_size, self.serving_unit)

    @serving.setter
    def serving(self, value):
        self.serving_size = value.toval()
        self.serving_unit = value.out_unit

    def __str__(self):
        return self.name
        
# End of ingredient definition

# Association between ingredient and nutrients
class IngredientNutrient(Base):
    __tablename__ = "IngredientsNutrients"
    
    ingredient_id = Column(Integer, ForeignKey("Ingredients.id"), primary_key=True)
    nutrient_id = Column(Integer, ForeignKey("Nutrients.id"), primary_key=True)
    concentration_quantity = Column(Float)
    concentration_unit = Column(String)
    amount_unit = Column(String)
    ingredient = relationship(Ingredient,
                              backref=backref("ingredient_nutrients",
                                              collection_class=attribute_mapped_collection("nutrient.name"),
                                              cascade="all, delete-orphan")
                              )
    nutrient = relationship(Nutrient)

    def __init__(self, session, ingredient, nutrient, serving_amount, serving_unit):
        self.ingredient = ingredient
        self.nutrient = nutrient
        self.amount_unit = serving_unit

        quantity_per_serving = mg(serving_amount, serving_unit)    
        concentration = quantity_per_serving / ingredient.serving
        concentration.ounit('%s/%s'%(quantity_per_serving.out_unit, 
                                     ingredient.serving.out_unit))
        self.concentration = concentration

    @property
    def concentration(self):
        return  mg(self.concentration_quantity, self.concentration_unit)

    @concentration.setter
    def concentration(self, value):
        self.concentration_quantity = value.toval()
        self.concentration_unit = value.out_unit

    def per_serving(self, serving):
        amount = self.concentration * serving
        amount.ounit(self.amount_unit)
        return amount

# End of ingedients nutrients association definition

