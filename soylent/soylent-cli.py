from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Nutrient, Ingredient, IngredientNutrient, Protein, Carbohydrate, Fat, UpperNutrientLimit, LowerNutrientLimit, NutritionGoal, NutrientGoal
import argparse

from magnitude import mg


def new_nutrient(session, args):
    n = Nutrient(args.name)
    session.add(n)
    session.commit()
    print 'Added Nutrient', args.name

def new_protein(session, args):
    n = Protein(args.name, args.essential)
    session.add(n)
    session.commit()
    print 'Added Protein', args.name

def new_carbohydrate(session, args):
    n = Carbohydrate(args.name)
    session.add(n)
    session.commit()
    print 'Added Carbohydrate', args.name

def new_fat(session, args):
    n = Fat(args.name, args.saturated, args.monounsaturated, args.polyunsaturated)
    session.add(n)
    session.commit()
    print 'Added Fat', args.name

def new_ingredient(session, agrs):
    i = Ingredient(args.name, args.serving_size, args.serving_unit)
    session.add(i)
    session.commit()
    print 'Added Ingredient', args.name

def new_goal(session, args):
    energy = mg(args.energy_amount, args.energy_unit)
    n = NutritionGoal(name=args.name, 
                      energy=energy,
                      carbohydrates_percentage = args.carbs,
                      fats_percentage = args.fats,
                      proteins_percentage = args.proteins)
    session.add(n)
    session.commit()
    print 'Added Nutrition Goal', args.name

def add_nutrient(session, args):
    # TODO Add error handling/
    #  - unknown nutrient
    #  - unknown ingredient
    #  - unknown unit
    ingredient = session.query(Ingredient).filter(Ingredient.name == args.ingredient)[0]
    nutrient = session.query(Nutrient).filter(Nutrient.name == args.nutrient)[0]
    ingredient_nutrient = IngredientNutrient(session,
                                             ingredient = ingredient,
                                             nutrient = nutrient,
                                             serving_amount=args.quantity,
                                             serving_unit=args.unit)
    session.add(ingredient_nutrient)
    session.commit()

def add_limit(session, args):
    limit_type = {'upper': UpperNutrientLimit,
                  'lower': LowerNutrientLimit}
    try:
        nutrient = session.query(Nutrient).filter(Nutrient.name == args.nutrient)[0]
    except IndexError:
        print "Nutrient not found %s"%args.nutrient
    else:
        limit = limit_type[args.type](nutrient_id = nutrient.id,
                                      type = args.type,
                                      effect = args.effect,
                                      limit_value=args.quantity,
                                      limit_unit=args.unit)
        session.add(limit)
        session.commit()

def add_goal(session, args):
    # TODO Add error handling/
    #  - unknown nutrient
    #  - unknown ingredient
    #  - unknown unit
    goal = session.query(NutritionGoal).filter(NutritionGoal.name == args.goal)[0]
    nutrient = session.query(Nutrient).filter(Nutrient.name == args.nutrient)[0]
    nutrient_goal = NutrientGoal(goal,
                                 nutrient,
                                 mg(args.quantity, args.unit))
    session.add(nutrient_goal)
    session.commit()


def show_nutrients(session, args):
    ingredient = session.query(Ingredient).filter(Ingredient.name == args.ingredient)[0]
    serving = ingredient.serving
    print '%s (%s):'%(ingredient.name, ingredient.serving)
    for name, nutrient in ingredient.ingredient_nutrients.iteritems():
        print ' -', name, nutrient.weight_per_serving(serving)

    print ingredient.energy_per_serving(serving)

def list(session, args):
    # Get the class for the query
    query_class = eval(args.name.capitalize())
    for item in session.query(query_class).order_by('name'):
        print item

# Define the main parser
parser = argparse.ArgumentParser(description="CLI for soylent")
parser.add_argument('-s',
                    action='store',
                    help='Connection string for the DB',
                    default='sqlite:///soylent.db')
parser.add_argument('--init',
                    action='store_true',
                    help='Initialize the DB')

subparsers = parser.add_subparsers(help='Actions to perform')

# Define a subparser for the new action
new_parser = subparsers.add_parser('new', help='Adds a new entry')
new_subparsers = new_parser.add_subparsers(help='Type to add')

# First type to add, the nutrient
new_nutrient_subparser = new_subparsers.add_parser('nutrient', help='Adds a new nutrient')
new_nutrient_subparser.add_argument('name', type=str, help='Name of the nutrient')
new_nutrient_subparser.set_defaults(func=new_nutrient)

# Second type to add, the ingredients
new_ingredient_subparser = new_subparsers.add_parser('ingredient', help='Adds a new ingredient')
new_ingredient_subparser.add_argument('name', type=str, help='Name of the new ingredient')
new_ingredient_subparser.add_argument('serving_size', type=float, help='Serving size for the nutrients per servings definition')
new_ingredient_subparser.add_argument('serving_unit', type=str, help='Unit for the serving size')
new_ingredient_subparser.set_defaults(func=new_ingredient)

# Add the protein
new_protein_subparser = new_subparsers.add_parser('protein', help='Adds a new protein')
new_protein_subparser.add_argument('name', type=str, help='Name of the protein')
new_protein_subparser.add_argument('--essential', action='store_true')
new_protein_subparser.set_defaults(func=new_protein)

# Add the carbohydrate
new_carbohydrate_subparser = new_subparsers.add_parser('carbohydrate', help='Adds a new carbohydrate')
new_carbohydrate_subparser.add_argument('name', type=str, help='Name of the carbohydrate')
new_carbohydrate_subparser.set_defaults(func=new_carbohydrate)

# Add the fat
new_fat_subparser = new_subparsers.add_parser('fat', help='Adds a new fat')
new_fat_subparser.add_argument('name', type=str, help='Name of the fat')
saturation_group = new_fat_subparser.add_mutually_exclusive_group()
saturation_group.add_argument('--saturated', action='store_true')
saturation_group.add_argument('--monounsaturated', action='store_true')
saturation_group.add_argument('--polyunsaturated', action='store_true')
new_fat_subparser.set_defaults(func=new_fat)

new_goal_subparser = new_subparsers.add_parser('goal', help='Adds a new goal')
new_goal_subparser.add_argument('name', type=str, help='Name of the goal')
new_goal_subparser.add_argument('energy_amount', type=float)
new_goal_subparser.add_argument('energy_unit', type=str)
new_goal_subparser.add_argument('carbs', type=float)
new_goal_subparser.add_argument('fats', type=float)
new_goal_subparser.add_argument('proteins', type=float)
new_goal_subparser.set_defaults(func=new_goal)

# Second Action: listing the entries
list_subparser = subparsers.add_parser('list', help='Lists a new entry')
list_subparser.add_argument('name', 
                            type=str, 
                            help='Name of the type to list',
                            choices=['nutrient', 'ingredient'])
list_subparser.set_defaults(func=list)

# Adding nutrients to an ingredient
add_parser = subparsers.add_parser('add')
add_subparsers = add_parser.add_subparsers()
add_nutrient_parser = add_subparsers.add_parser('nutrient')
add_nutrient_parser.add_argument('nutrient', help='nutrient to add')
add_nutrient_parser.add_argument('quantity', type=float, help='quantity per serving')
add_nutrient_parser.add_argument('unit', help='unit per serving')
add_nutrient_parser.add_argument('ingredient', help='ingredient containing the nutrient')
add_nutrient_parser.set_defaults(func=add_nutrient)

# Adding limits to nutrients
add_limit_parser  = add_subparsers.add_parser('limit')
add_limit_parser.add_argument('nutrient', type=str)
add_limit_parser.add_argument('type', type=str, choices=['upper', 'lower'])
add_limit_parser.add_argument('quantity', type=float, help='quantity per serving')
add_limit_parser.add_argument('unit', help='unit per serving')
add_limit_parser.add_argument('effect', help='What happens when you go past the limit')
add_limit_parser.set_defaults(func=add_limit)

# Adding a goal for a specific nutrient
add_goal_parser = add_subparsers.add_parser('goal')
add_goal_parser.add_argument('nutrient', help='nutrient to add')
add_goal_parser.add_argument('quantity', type=float)
add_goal_parser.add_argument('unit')
add_goal_parser.add_argument('goal', help='goal containing the nutrient')
add_goal_parser.set_defaults(func=add_goal)

# Show the nutrients in an ingredient
show_parser = subparsers.add_parser('show')
show_subparsers = show_parser.add_subparsers()
show_nutrient_parser = show_subparsers.add_parser('nutrient')
show_nutrient_parser.add_argument('ingredient', help='ingredient containing the nutrients')
show_nutrient_parser.set_defaults(func=show_nutrients)


if __name__ == '__main__':
    
    args = parser.parse_args()

    # Initialize our DB connection
    engine = create_engine(args.s)
    if args.init:
        Base.metadata.create_all(engine) 

    Session = sessionmaker(bind=engine)    
    session = Session()

    # Do what we need to do
    args.func(session, args)
