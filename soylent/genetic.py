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
        score += self.valuate_percentage(self.goal.energy, recipe.energy)/10

        # About the amounts of protein, fat, etc:
        score += self.valuate_percentage((self.goal.energy * goal.carbohydrates_percentage /100),
                                         recipe.carbohydrates_energy)/10
        score += self.valuate_percentage((self.goal.energy * goal.fats_percentage /100),
                                         recipe.fats_energy)/10
        score += self.valuate_percentage((self.goal.energy * goal.proteins_percentage /100),
                                         recipe.proteins_energy)/10

        # Handle the nutrients
        for nutrient_goal in self.goal.nutrient_goals:
            # Also 10 Points for each exact nutrient goal, 0 for a divergence of 100% or more
            total_nutrient = recipe.get_nutrient(nutrient_goal.nutrient.name)
            if nutrient_goal.goal_amount != 0:
                score += self.valuate_percentage(nutrient_goal.value, total_nutrient)/10

            # Do not ever go over the limit, that's a 10 points loss
            if nutrient_goal.nutrient.upper_limit:
                try:
                    if nutrient_goal.nutrient.upper_limit[0].value < total_nutrient:
                        score -= 10
                except AttributeError:
                    print nutrient_goal.nutrient
                    print nutrient_goal.upper_limit
                    print dir(nutrient_goal.upper_limit[0])
                    raise

        return max(0, score)

    def valuate_percentage(self, goal, actual):
        # The valuation should no be linear, so let's try x**2
        percentage = (actual / goal) * 100
        delta = abs(percentage - 100)
        raw = 100 - min(delta, 100)
        return (raw**2)/100

    def print_chromosome(self, chromosome):
        recipe = self.chromosome_to_recipe(chromosome)
        
        total_energy = recipe.energy
        energy_percent = (recipe.energy / goal.energy) * 100
        print 'Energy: %s (%.2f%%)'%(recipe.energy, energy_percent)
        
        carbohydrates_percent = (recipe.carbohydrates_energy / recipe.energy) * 100
        print 'Carbohydrate actual/goal: %.2f/%.2f'%(carbohydrates_percent, goal.carbohydrates_percentage)

        fats_percent = (recipe.fats_energy / recipe.energy) * 100
        print 'Fat actual/goal: %.2f/%.2f'%(fats_percent, goal.fats_percentage)

        proteins_percent = (recipe.proteins_energy / recipe.energy) * 100
        print 'Protein actual/goal: %.2f/%.2f'%(proteins_percent, goal.proteins_percentage)

        print '\nIngredients:'

        for servings, ingredient in ((chromosome[i], session.query(Ingredient).get(i+1)) for i in range(chromosome.getListSize())):
            print ingredient.name, (servings * ingredient.serving).ounit(ingredient.serving_unit)

        print '\nNutrients:'
        for nutrient_goal in self.goal.nutrient_goals:
            # Also 10 Points for each exact nutrient goal, 0 for a divergence of 100% or more
            print nutrient_goal.nutrient.name, '%.2f'%recipe.get_nutrient(nutrient_goal.nutrient.name).ounit(nutrient_goal.goal_unit), 
            if nutrient_goal.goal_amount != 0:
                print '%.2f'%(recipe.get_nutrient(nutrient_goal.nutrient.name)/nutrient_goal.value*100)
    

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



