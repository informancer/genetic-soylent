#!/bin/bash

# Remove the old test db
rm blah.db

# Create the nutrients
nutrients=( Calcium Chlorid Chrom Copper Fluorid Iodine Iron Magnesium Manganese Molybdenum Phosphorus Potassium Selenium Sodium Zinc "Vitamin A" "Vitamin B1" "Vitamin B2" "Niacin" "Pantothenic acid" "Vitamin B6" "Biotin" "Folic acid" "Vitamin B12" "Vitamin C" "Vitamin D" "Vitamin E" "Choline" "Vitamin K" )

for n in "${nutrients[@]}"; do
    #echo p
    python soylent-cli.py --init -s sqlite:///blah.db new nutrient "$n"
done;

# Dummy protein for when the actual amino acid is unknown
python soylent-cli.py --init -s sqlite:///blah.db new protein "Protein"
python soylent-cli.py --init -s sqlite:///blah.db new carbohydrate "Carbohydrate"
python soylent-cli.py --init -s sqlite:///blah.db new fat "Fat"
python soylent-cli.py --init -s sqlite:///blah.db new fat "Saturated fat" --saturated
python soylent-cli.py --init -s sqlite:///blah.db new fat "Monounsaturated fat" --monounsaturated
python soylent-cli.py --init -s sqlite:///blah.db new fat "Polyunsaturated fat" --polyunsaturated

# Create the amino acids
python soylent-cli.py --init -s sqlite:///blah.db new protein "Alanine"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Arginine"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Aspartic acid"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Cysteine"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Glutamic acid"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Glycine"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Histidin"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Isoleucin" --essential
python soylent-cli.py --init -s sqlite:///blah.db new protein "Leucin" --essential
python soylent-cli.py --init -s sqlite:///blah.db new protein "Lysin" --essential
python soylent-cli.py --init -s sqlite:///blah.db new protein "Methionin" --essential
python soylent-cli.py --init -s sqlite:///blah.db new protein "Phenylalanin" --essential
python soylent-cli.py --init -s sqlite:///blah.db new protein "Prolin"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Serin"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Threonin" --essential
python soylent-cli.py --init -s sqlite:///blah.db new protein "Tryptophan" --essential
python soylent-cli.py --init -s sqlite:///blah.db new protein "Tyrosin"
python soylent-cli.py --init -s sqlite:///blah.db new protein "Valin" --essential

# Create the ingredient Multisaft
python soylent-cli.py --init -s sqlite:///blah.db new ingredient Multisaft 100 ml

# Add some nutrients
python soylent-cli.py -s sqlite:///blah.db add nutrient "Protein" 0.3 g Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Carbohydrate" 10.8 g Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Vitamin C" 40 mg Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Niacin" 8 mg Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Vitamin E" 6 mg Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Pantothenic acid" 120 ug Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Vitamin B6" 0.7 mg Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Vitamin B1" 0.55 mg Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Vitamin A" 120 ug Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Folic acid" 100 ug Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Biotin" 25 ug Multisaft
python soylent-cli.py -s sqlite:///blah.db add nutrient "Vitamin B12" 1.25 ug Multisaft

# And show the result of our handywork
python soylent-cli.py -s sqlite:///blah.db show nutrient Multisaft

# Create the ingredient Multisaft
python soylent-cli.py --init -s sqlite:///blah.db new ingredient "Mammut Formel 90 Protein" 100 g 

python soylent-cli.py -s sqlite:///blah.db add nutrient "Protein" 78.3 g "Mammut Formel 90 Protein"
python soylent-cli.py -s sqlite:///blah.db add nutrient "Carbohydrate" 5.7 g "Mammut Formel 90 Protein"
python soylent-cli.py -s sqlite:///blah.db add nutrient "Fat" 1.5 g "Mammut Formel 90 Protein"
python soylent-cli.py -s sqlite:///blah.db add nutrient "Saturated fat" 2.0 g "Mammut Formel 90 Protein"
python soylent-cli.py -s sqlite:///blah.db add nutrient "Sodium" 0.93 g "Mammut Formel 90 Protein"
python soylent-cli.py -s sqlite:///blah.db add nutrient "Vitamin B6" 2.31 mg "Mammut Formel 90 Protein"
