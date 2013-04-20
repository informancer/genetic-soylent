from models import Recipe, Ingredient, RecipeIngredient, NutritionGoal
from magnitude import mg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyevolve import G1DList
from pyevolve import GSimpleGA

# Initialize our DB connection
engine = create_engine('sqlite:///blah.db')

Session = sessionmaker(bind=engine)    
session = Session()

goal = session.query(NutritionGoal).filter(NutritionGoal.name == 'informancer')[0]

def eval_func(chromosome):
    
    score = 0

    # So our chromosome is a 1D list of ingredients.
    # The ingredient index+1 in the list is the ID in the table, 
    # whereas the content is the number of servings
    # so let's create a recipe out of this.
    recipe = Recipe()
    session.add(recipe)
    session.flush()
    for servings, ingredient in ((chromosome[i], session.query(Ingredient).get(i+1)) for i in range(chromosome.getListSize())):
        r_i = RecipeIngredient(recipe_id = recipe.id, 
                               ingredient_id = ingredient.id,
                               number_of_servings = servings)
        session.add(r_i)
        
    # Handle the energetic goal
    # 10 Points for the exact caloric goal, 0 for a divergence of 100% or more.
    # the decrease is linear
    total_energy = recipe.energy
    energy_percent = (recipe.energy / goal.energy) * 100
    energy_delta = abs(energy_percent - 100)
    energy_factor = 10 - (min(energy_delta, 100)/10)
    score += energy_factor

    # Handle the nutrients

    return score

def print_result(chromosome):
    # TODO refactor
    recipe = Recipe()
    session.add(recipe)
    session.flush()
    for servings, ingredient in ((chromosome[i], session.query(Ingredient).get(i+1)) for i in range(chromosome.getListSize())):
        print ingredient.name, (servings * ingredient.serving).ounit(ingredient.serving_unit)
        r_i = RecipeIngredient(recipe_id = recipe.id, 
                               ingredient_id = ingredient.id,
                               number_of_servings = servings)
        session.add(r_i)
    #TODO end of refactor

    total_energy = recipe.energy
    energy_percent = (recipe.energy / goal.energy) * 100

    print '%s (%.2f%%)'%(recipe.energy, energy_percent)

    

if __name__ == '__main__':
    # Genome instance
    genome = G1DList.G1DList(session.query(Ingredient).count())    
    genome.evaluator.set(eval_func)
    genome.setParams(rangemin=0, rangemax=10)
    ga = GSimpleGA.GSimpleGA(genome)
    ga.evolve(freq_stats=1)
    print_result(ga.bestIndividual())



