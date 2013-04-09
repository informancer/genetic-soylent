Data Structure
==============

In trhe most basic form,
we have a recipe, 
containing quantities of ingredients.
An ingredient in turn contains certain quantities of nutrients.

In order to avoid creating a new file format,
and to get all the goodies that comes with it,
for example migration scripts,
we will use sqlalchemy to store our data.

Nutrient
========

In order to build up, 
we'll start with the nutrients.
All nutrients have a name, 
but some have more than one.
Some have a minimal amount, 
other are optional.
Some have a maximal amount, 
other can be consumed without problems.
Then there are multiple recommended values, 
according to different guidelines,
like the US recommended `Dietary Reference Intake`_,
or the `EU-Directive 2008-100-EC`_.

.. _`Dietary Reference Intake`: http://fnic.nal.usda.gov/dietary-guidance/dietary-reference-intakes/dri-tables
.. _`EU-Directive 2008-100-EC`: http://ec.europa.eu/food/food/labellingnutrition/nutritionlabel/index_en.htm

This gives us the following Definitions:

.. literalinclude:: ../soylent/models.py
   :linenos:
