from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Nutrient, Ingredient, IngredientNutrient
import argparse

def new_nutrient(session, args):
    n = Nutrient(args.name)
    session.add(n)
    session.commit()
    print 'Added Nutrient', args.name

def new_ingredient(session, agrs):
    i = Ingredient(args.name, args.serving_size, args.serving_unit)
    session.add(i)
    session.commit()
    print 'Added Ingredient', args.name

def add_nutrient(session, args):
    # TODO Add error handling/
    #  - unknown nutrient
    #  - unknown ingredient
    #  - unknown unit
    ingredient = session.query(Ingredient).filter(Ingredient.name == args.ingredient)[0]
    nutrient = session.query(Nutrient).filter(Nutrient.name == args.nutrient)[0]
    ingredient_nutrient = IngredientNutrient(ingredient_id=ingredient.id,
                                             nutrient_id=nutrient.id,
                                             quantity=args.quantity,
                                             unit=args.unit)
    session.add(ingredient_nutrient)
    session.commit()

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
new_ingredient_subparser.add_argument('serving_size', type=int, help='Serving size for the nutrients per servings definition')
new_ingredient_subparser.add_argument('serving_unit', type=str, help='Unit for the serving size')
new_ingredient_subparser.set_defaults(func=new_ingredient)

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
add_nutrient_parser.add_argument('quantity', help='quantity per serving')
add_nutrient_parser.add_argument('unit', help='unit per serving')
add_nutrient_parser.add_argument('ingredient', help='ingredient containing the nutrient')
add_nutrient_parser.set_defaults(func=add_nutrient)

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
