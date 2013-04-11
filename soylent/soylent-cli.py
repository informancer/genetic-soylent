from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Nutrient, Ingredient
import argparse

def add_nutrient(session, args):
    n = Nutrient(args.name)
    session.add(n)
    session.commit()
    print 'Added Nutrient', args.name

def add_ingredient(session, agrs):
    i = Ingredient(args.name, args.serving_size, args.serving_unit)
    session.add(i)
    session.commit()
    print 'Added Ingredient', args.name

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

# Define a subparser for the add action
add_parser = subparsers.add_parser('add', help='Adds a new entry')
add_subparsers = add_parser.add_subparsers(help='Type to add')

# First type to add, the nutrient
add_nutrient_subparser = add_subparsers.add_parser('nutrient', help='Adds a new nutrient')
add_nutrient_subparser.add_argument('name', type=str, help='Name of the nutrient')
add_nutrient_subparser.set_defaults(func=add_nutrient)

# Second type to add, the ingredients
add_ingredient_subparser = add_subparsers.add_parser('ingredient', help='Adds a new ingredient')
add_ingredient_subparser.add_argument('name', type=str, help='Name of the new ingredient')
add_ingredient_subparser.add_argument('serving_size', type=int, help='Serving size for the nutrients per servings definition')
add_ingredient_subparser.add_argument('serving_unit', type=str, help='Unit for the serving size')
add_ingredient_subparser.set_defaults(func=add_ingredient)

# Second Action: listing the entries
list_subparser = subparsers.add_parser('list', help='Lists a new entry')
list_subparser.add_argument('name', 
                            type=str, 
                            help='Name of the type to list',
                            choices=['nutrient', 'ingredient'])
list_subparser.set_defaults(func=list)

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
