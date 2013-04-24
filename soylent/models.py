from sqlalchemy import Column, Boolean, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm.session import object_session

from magnitude import mg, Magnitude, new_mag

# TODO: find a better place for this
# Because we'll need it for some ingredients
pc = Magnitude(1)
new_mag('pc', pc)

Base = declarative_base()

# Definition of nutrient

class Nutrient(Base):
    __tablename__ = "Nutrients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type = Column(String) 

    __mapper_args__ = {
        'polymorphic_identity': 'nutrient',
        'polymorphic_on': type
        }

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
    def macronutrients(self):
        return object_session(self).query(IngredientNutrient).with_parent(self).join(MacroNutrient)

    @property
    def proteins(self):
        return object_session(self).query(IngredientNutrient).with_parent(self).join(Protein)

    @property
    def carbohydrates(self):
        return object_session(self).query(IngredientNutrient).with_parent(self).join(Carbohydrate)

    @property
    def fats(self):
        return object_session(self).query(IngredientNutrient).with_parent(self).join(Fat)

    @property
    def serving(self):
        return mg(self.serving_size, self.serving_unit)

    @serving.setter
    def serving(self, value):
        self.serving_size = value.toval()
        self.serving_unit = value.out_unit

    def energy_per_serving(self, serving):
        total = mg(0, 'J')
        # somehow, sum does not work on magnitudes
        for i in [m.weight_per_serving(serving) * m.nutrient.energy_per_weight for m in self.macronutrients]:
            total += i
        return total

    def carbohydrates_per_serving(self, serving):
        total = mg(0, 'J')
        # somehow, sum does not work on magnitudes
        for i in [m.weight_per_serving(serving) * m.nutrient.energy_per_weight for m in self.carbohydrates]:
            total += i
        return total

    def fats_per_serving(self, serving):
        total = mg(0, 'J')
        # somehow, sum does not work on magnitudes
        for i in [m.weight_per_serving(serving) * m.nutrient.energy_per_weight for m in self.fats]:
            total += i
        return total

    def proteins_per_serving(self, serving):
        total = mg(0, 'J')
        # somehow, sum does not work on magnitudes
        for i in [m.weight_per_serving(serving) * m.nutrient.energy_per_weight for m in self.proteins]:
            total += i
        return total

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

    # TODO: remove session parameter
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

    def weight_per_serving(self, serving):
        amount = self.concentration * serving
        amount.ounit(self.amount_unit)
        return amount

# End of ingedients nutrients association definition

# Macronutrient class
class MacroNutrient(Nutrient):
    __tablename__ = 'MacroNutrients'

    id = Column(Integer, ForeignKey('Nutrients.id'), primary_key=True)
    conversion_factor = Column(Integer)
    
    __mapper_args__ = {
        'polymorphic_identity': 'macronutrient'
        }

    def __init__(self, name, conversion_factor):
        Nutrient.__init__(self, name)
        self.conversion_factor = conversion_factor

    @property
    def energy_per_weight(self):
        return mg(self.conversion_factor * 1000 * 4.184, "J/g")

class Protein(MacroNutrient):
    __tablename__ = 'Proteins'
    
    id = Column(Integer, ForeignKey('MacroNutrients.id'), primary_key=True)
    essential = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'protein'
        }
    
    def __init__(self, name, essential):
        MacroNutrient.__init__(self, name, 4)
        self.essential = essential

class Carbohydrate(MacroNutrient):
    __tablename__ = 'Carbohydrates'
    
    id = Column(Integer, ForeignKey('MacroNutrients.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'carbohydrate'
        }

    def __init__(self, name):
        MacroNutrient.__init__(self, name, 4)

class Fat(MacroNutrient):
    __tablename__ = 'Fats'
    
    id = Column(Integer, ForeignKey('MacroNutrients.id'), primary_key=True)
    saturated = Column(Boolean)
    monounsaturated = Column(Boolean)
    polyunsaturated = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'fat'
        }

    def __init__(self, name, saturated, monounsaturated, polyunsaturated):
        MacroNutrient.__init__(self, name, 9)
        self.saturated = saturated
        self.monounsaturated = monounsaturated
        self.polyunsaturated = polyunsaturated

class NutrientLimit(Base):
    __tablename__ = 'NutrientLimit'

    id = Column(Integer, primary_key=True)
    nutrient_id = Column(Integer, ForeignKey('Nutrients.id'))
    type = Column(String)
    effect = Column(String)
    limit_value = Column(Float)
    limit_unit = Column(String)

    @property
    def value(self):
        return mg(self.limit_value, self.limit_unit)

    @value.setter
    def value(self, value):
        self.limit_value = value.toval()
        self.limit_unit = value.out_unit


    __mapper_args__ = {
        'polymorphic_on': 'type',
        }

class UpperNutrientLimit(NutrientLimit):
    __mapper_args__ = {
        'polymorphic_identity': 'upper'
        }

    relationship = relationship(Nutrient, backref=backref('upper_limit'))

class LowerNutrientLimit(NutrientLimit):
    __mapper_args__ = {
        'polymorphic_identity': 'lower'
        }

    relationship = relationship(Nutrient, backref=backref('lower_limit'))

class NutrientGoal(Base):
    __tablename__ = 'NutrientGoals'
    
    nutrition_goal_id = Column(Integer, ForeignKey('NutritionGoals.id'), primary_key=True)
    nutrient_id = Column(Integer, ForeignKey('Nutrients.id'), primary_key=True)
    goal_amount = Column(Float)
    goal_unit = Column(String)

    nutrition_goal = relationship('NutritionGoal')
    nutrient = relationship(Nutrient)

    def __init__(self, nutrition_goal, nutrient, goal):
        self.nutrition_goal = nutrition_goal
        self.nutrient = nutrient
        self.value = goal

    @property
    def value(self):
        return mg(self.goal_amount, self.goal_unit)

    @value.setter
    def value(self, value):
        self.goal_amount = value.toval()
        self.goal_unit = value.out_unit

class NutritionGoal(Base):
    __tablename__ = "NutritionGoals"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    energy_amount = Column(Float)
    energy_unit = Column(String)
    carbohydrates_percentage = Column(Float)
    fats_percentage = Column(Float)
    proteins_percentage = Column(Float)
    
    #TODO: Build Saturated fat, cholesterol and (alpha-)linoleic acid

    nutrient_goals = relationship(NutrientGoal)

    @property
    def energy(self):
        return mg(self.energy_amount, self.energy_unit)

    @energy.setter
    def energy(self, value):
        self.energy_amount = value.toval()
        self.energy_unit = value.out_unit

class Recipe(Base):
    __tablename__ = 'Recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    recipe_ingredients = relationship('RecipeIngredient')
    
    @property
    def energy(self):
        total = mg(0, 'J')
        for i in self.recipe_ingredients:
            total += i.ingredient.energy_per_serving(i.number_of_servings * i.ingredient.serving)
        return total

    @property
    def carbohydrates_energy(self):
        total = mg(0, 'J')
        for i in self.recipe_ingredients:
            total += i.ingredient.carbohydrates_per_serving(i.number_of_servings * i.ingredient.serving)
        return total

    @property
    def fats_energy(self):
        total = mg(0, 'J')
        for i in self.recipe_ingredients:
            total += i.ingredient.fats_per_serving(i.number_of_servings * i.ingredient.serving)
        return total

    @property
    def proteins_energy(self):
        total = mg(0, 'J')
        for i in self.recipe_ingredients:
            total += i.ingredient.proteins_per_serving(i.number_of_servings * i.ingredient.serving)
        return total

    def get_nutrient(self, nutrient_name):
        # TODO, make the unit dynamic
        total = mg(0, 'g')
        # TODO: use a join
        for i in self.recipe_ingredients:
            try: 
                total += i.ingredient.ingredient_nutrients[nutrient_name].weight_per_serving(i.number_of_servings * i.ingredient.serving)                
            except KeyError:
                pass
        return total

class RecipeIngredient(Base):
    __tablename__ = 'RecipeIngredients'
    
    recipe_id = Column(Integer, ForeignKey('Recipes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('Ingredients.id'), primary_key=True)
    number_of_servings = Column(Float)

    ingredient = relationship(Ingredient)

