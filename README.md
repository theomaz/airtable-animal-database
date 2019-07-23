# airtable-animal-database
A python module that manipulates the Airtable API in order to automate entries to an animal database.

## Installation
This module first requires installation of gtalarico's [airtable-python-wrapper](https://github.com/gtalarico/airtable-python-wrapper).
```bash
pip install airtable-python-wrapper
```
While this repository is getting set up you can use the module by downloading it and opening up python from your command shell
```python
from ADP import *
```

## Usage
You can begin manipulating an animal database table by creating a Manipulate() object.
If you do not provide an api key the class can automatically handle authentication if the environment variable AIRTABLE_API_KEY is set to your api key.
```python
mytable = Manipulate(base_key, table_name, API_key)
```

Among the most useful automation provided by this module are birth(), SAC_cage(), set_breeding(), and weaned().
```python
my_table.birth(cage_number, month, day, year)

my_table.SAC_cage(cage_number)

my_table.set_breeding(cage_number, month, day, year, male_ID, female_ID, optional_female_ID2)

my_table.weaned(cage_number, offspring_strain, female_number, female_cage, optional_2nd_female_cage,
                male_number, male_cage, optional_2nd_male_cage)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
