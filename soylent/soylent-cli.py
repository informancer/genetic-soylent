from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Nutrient
import argparse

def add_nutrient(session, args):
    print 'Add Nutrient', args.name
    n = Nutrient(args.name)
    session.add(n)
    session.commit()
    print dir(session)

def list(session, args):
    print 'List', args.name




# Define the main parser
parser = argparse.ArgumentParser(description="CLI for soylent")
parser.add_argument('-s',
                    action='store',
                    help='Connection string for the DB',
                    default='sqlite:///soylent.db')
subparsers = parser.add_subparsers(help='Actions to perform')

# Define a subparser for the add action
add_parser = subparsers.add_parser('add', help='Adds a new entry')
add_subparsers = add_parser.add_subparsers(help='Type to add')

# First type to add, the nutrient
add_nutrient_subparser = add_subparsers.add_parser('nutrient', help='Adds a new nutrient')
add_nutrient_subparser.add_argument('name', type=str, help='Name of the nutrient')
add_nutrient_subparser.set_defaults(func=add_nutrient)

# Second Action: listing the entries
list_subparser = subparsers.add_parser('list', help='Lists a new entry')
list_subparser.add_argument('name', 
                            type=str, 
                            help='Name of the type to list',
                            choices=['nutrient'])
list_subparser.set_defaults(func=list)

if __name__ == '__main__':
    
    args = parser.parse_args()

    # Initialize our DB connection
    engine = create_engine(args.s)
    Session = sessionmaker(bind=engine)    
    session = Session()

    # Check what we need to do
    args.func(session, args)
