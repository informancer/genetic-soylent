Data Structure
##############

.. default-domain:: py

.. module:: models
   :synopsis: Clases to repesent the different components of alimentation

The whole sense of soylent is to provide all the nutrients needed by the body,
in an easy to mix way.

This module contains the different classes we need to represent an alimentation

In the most basic form,
we have a recipe, 
containing quantities of ingredients.
An ingredient in turn contains certain quantities of nutrients.

In order to avoid creating a new file format,
and to get all the goodies that comes with it,
for example migration scripts,
we use :ref:`SQLAlchemy <sqlalchemy:index_toplevel>` to manage the storage.

In order to simplify the management and calculations for the physical quantities,
we use magnitude_

.. _magnitude: http://juanreyero.com/open/magnitude/

Nutrients types
===============

.. class:: Nutrient(name)

   A Nutriment is pretty much anything that the body needs to be fed
   in order to work properly.

   As for the relevant parts, all nutrients have a name, 
   but some have more than one (think translation).
   Some have a minimal amount, 
   other are optional.
   Some have a maximal amount, 
   other can be consumed without problems.
   Then there are multiple recommended values, 
   according to different guidelines,
   like the US recommended `Dietary Reference Intake`_,
   or the `EU-Directive 2008-100-EC`_.

   given that most of these are optional, 
   there is no reason to put them in the class itself.

   They will be added in due time as needed.

   A nitrient by itself doesn't do a lot, 
   so we kept the methods down to a minimum.

.. _Dietary Reference Intake: http://fnic.nal.usda.gov/dietary-guidance/dietary-reference-intakes/dri-tables
.. _EU-Directive 2008-100-EC: http://ec.europa.eu/food/food/labellingnutrition/nutritionlabel/index_en.htm

.. class:: Macronutrient(name, conversion_factor)

   A Macronutrient is the kind of nutrient that can be converted to
   energy by the body, as described in the `Food energy`_ article on
   wikipedia.

   This class derives from :class:`Nutrient`,
   using :ref:`concrete inheritance mapping <sqlalchemy:concrete_inheritance>` 
   to build the relationship.

   .. attribute:: conversion_factor

   .. attribute:: energy_per_weight
   
      per default, the energy per weight is a magnitude expressed in
      Joules per gram.

There are different sources of macro nutrients,
represented as subclasses of :class:`Macronutrient`. 
For the moment, only the :class:`Carbohydrate`, :class:`Fat` and :class:`Protein` are represented.

.. class:: Carbohydrate(name)
   
   This class is used to represent a type of Carbohydrate_.

   It has no specific attribute or method.

.. class:: Fat(name, saturated, monounsaturated, polyunsaturated)

   This class is used to represent different types of Fat_.

   It has three attributes, all Booleans, to indicate kind of saturation of the fat:

   .. attribute:: saturated
   .. attribute:: monounsaturated
   .. attribute:: polyunsaturated

.. class:: Protein(name, essential)

   This class is the result of a misunderstanding on my part.
   Instead of being used to represent Protein_,
   it is used to represent the different `Amino acids`_.

   .. attribute:: essential
      an amino acid is essential if it cannot be synthesized by the body.

.. _Food energy: http://en.wikipedia.org/wiki/Food_energy
.. _Carbohydrate: https://en.wikipedia.org/wiki/Carbohydrate
.. _Fat: https://en.wikipedia.org/wiki/Fat
.. _Protein: http://en.wikipedia.org/wiki/Protein_%28nutrient%29
.. _Amino acids: http://en.wikipedia.org/wiki/Amino_acids#In_human_nutrition

Ingredient
==========

Now that we have the nutrients,
we can pack them in ingredients.

This is done using two classes:

.. class:: Ingredient(name, serving_size, serving_unit)

   An ingredient has a name, logically,
   it is also measured in a specific unit 
   and contains some nutrients per servings.

   .. attribute:: serving

      read/write property for the serving as a physical quantity.

   The instances also contains different read only properties
   representing the different kind of macronutrients 
   contained in the Ingredient as a list of :class:`IngredientNutrient`.

   .. attribute:: macronutrients
   .. attribute:: carbohydrates
   .. attribute:: fats
   .. attribute:: proteins

   .. method:: energy_per_serving(self, serving)

      returns the energy contained in a serving in Joules.
      This is calculated based on the macronutrients contained in the ingredient.
      
      Interrestingly, it sometimes is lower than 
      the energy per serving indicated on the package.   

   In the same way that there are four properties for the macronutrients,
   there are three different methods to return 
   the energy provided by the different kinds of macronutrients for a given serving:
   .. method:: carbohydrates_per_serving(self, serving)
   .. method:: fats_per_serving(self, serving)
   .. method:: proteins_per_serving(self, serving)

.. class:: IngredientNutrient(ingredient, nutrient, serving_amount, serving_size)
  
   This class is an :ref:`association object<sqlalchemy:association_pattern>` 
   to join the ingredients with their nutrients. 

   Both ingredient and nutrient can be references using the corresponding 
   attributes :attr:`ingredient` and :attr:`nutrient`.

   .. attribute:: concentration

      A property representing the concentration of the nutrient for a serving, e.g. '5 g/ml'.

   .. method:: weight_per_serving(serving)
   
      The amount of nutrient of a given serving of the ingredient.

