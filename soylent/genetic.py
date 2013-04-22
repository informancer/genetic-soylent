from models import Recipe, Ingredient, RecipeIngredient, NutritionGoal
from magnitude import mg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyevolve import G1DList
from pyevolve import GSimpleGA

class GoalEval:
    def __init__(self, session, goal):
        self.session = session
        self.goal = goal

    def chromosome_to_recipe(self, chromosome):
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
        return recipe
    
    def __call__(self, chromosome):
        """The actual evaluation function"""
        score = 0
        
        recipe = self.chromosome_to_recipe(chromosome)
        
        # Handle the energetic goal
        # 10 Points for the exact caloric goal, 0 for a divergence of 100% or more.
        # the decrease is linear
        total_energy = recipe.energy
        energy_percent = (recipe.energy / goal.energy) * 100
        energy_delta = abs(energy_percent - 100)
        energy_factor = 10 - (min(energy_delta, 100)/10)
        score += energy_factor

        # Handle the nutrients
        for nutrient_goal in self.goal.nutrient_goals:
            # Also 10 Points for each exact nutrient goal, 0 for a divergence of 100% or more
            total_nutrient = recipe.get_nutrient(nutrient_goal.nutrient.name)
            if nutrient_goal.goal_amount != 0:
                nutrient_percent = (total_nutrient / nutrient_goal.value) * 100
                nutrient_delta = abs(nutrient_percent - 100)
                nutrient_factor = 10 - (min(nutrient_delta, 100)/10)
                score += nutrient_factor
            else:
                #TODO for stuff that should be avoided.
                pass



        return score

    def print_chromosome(self, chromosome):
        recipe = self.chromosome_to_recipe(chromosome)
        for servings, ingredient in ((chromosome[i], session.query(Ingredient).get(i+1)) for i in range(chromosome.getListSize())):
            print ingredient.name, (servings * ingredient.serving).ounit(ingredient.serving_unit)
        
        total_energy = recipe.energy
        energy_percent = (recipe.energy / goal.energy) * 100

        print '%s (%.2f%%)'%(recipe.energy, energy_percent)

    

if __name__ == '__main__':

    # Initialize our DB connection
    engine = create_engine('sqlite:///blah.db')
    
    Session = sessionmaker(bind=engine)    
    session = Session()
    
    goal = session.query(NutritionGoal).filter(NutritionGoal.name == 'informancer')[0]

    eval_func = GoalEval(session, goal)

    # Genome instance
    genome = G1DList.G1DList(session.query(Ingredient).count())    
    genome.evaluator.set(eval_func)
    genome.setParams(rangemin=0, rangemax=10)
    ga = GSimpleGA.GSimpleGA(genome)
    ga.evolve(freq_stats=1)
    eval_func.print_chromosome(ga.bestIndividual())



