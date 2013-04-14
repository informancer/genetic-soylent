nutrients=["Calcium",
           "Chlorid",
           "Chrom",
           "Copper",
           "Fluorid",
           "Iodine",
           "Iron",
           "Magnesium",
           "Manganese",
           "Molybdän",
           "Phosphorus",
           "Potassium",
           "Selenium",
           "Sodium",
           "Zinc",
           "Vitamin A",
           "Vitamin B1",
           "Vitamin B2",
           "Vitamin B3",
           "Vitamin B5",
           "Vitamin B6",
           "Vitamin B7",
           "Vitamin B9",
           "Vitamin B12",
           "Vitamin C",
           "Vitamin D",
           "Vitamin E",
           "Choline",
           "Vitamin K"]

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine) 


for n in nutrients:
    nutrient = Nutrient(n)
    session.add(nutrient)
session.commit()

