#!/bin/bash

# Remove the old test db
rm blah.db

# Create the nutrients
nutrients=( Calcium Chlorid Chrom Copper Fluorid Iodine Iron Magnesium Manganese Molybdenum Phosphorus Potassium Selenium Sodium Zinc "Vitamin A" "Vitamin B1" "Vitamin B2" "Vitamin B3" "Vitamin B5" "Vitamin B6" "Vitamin B7" "Vitamin B9" "Vitamin B12" "Vitamin C" "Vitamin D" "Vitamin E" "Choline" "Vitamin K" )

for n in "${nutrients[@]}"; do
    #echo p
    python soylent-cli.py --init -s sqlite:///blah.db new nutrient "$n"
done;

# Create the ingredient Multisaft
python soylent-cli.py --init -s sqlite:///blah.db new ingredient Multisaft 100 ml

# Add some nutrients
python soylent-cli.py -s sqlite:///blah.db add nutrient "Vitamin A" 120 ug Multisaft
