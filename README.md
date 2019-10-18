# airtable-animal-database
A python module that manipulates the Airtable API to automate entries to an animal database.

## Installation
This module first requires installation of gtalarico's [airtable-python-wrapper](https://github.com/gtalarico/airtable-python-wrapper).
```bash
pip install airtable-python-wrapper
```
While this repository is getting set up you can use it by downloading it, adding it to your sys.path and opening up python from your command shell.
```python
from ADP import *
```

## Usage
You can manipulate an animal database table by creating a Manipulate() object.
If you do not provide an api key the class will automatically handle authentication if the environment variable AIRTABLE_API_KEY is set to your api key.
```python
mytable = Manipulate('base_key', 'table_name', 'API_key')
```

Among the most useful automation provided by this module are birth(), SAC_cage(), set_breeding(), and weaned().
```python
# Change status of female in cage_number to 'P: With Pups' and calculate/add weaning date entry
my_table.birth(cage_number, month, day, year)

my_table.birth(5100, 10, 11, 2019)

# Sacrifice all mice in cage
my_table.SAC_cage(cage_number)

my_table.SAC_cage(5332)

# Set mice to breeding, assign them to new cage
my_table.set_breeding(cage_num, month, day, year, male_ID, female_ID, female_ID2=False)

my_table.set_breeding(5202, 10, 11, 2019, '4881-D3', '4727-A2')

# Take weaned mice from cage_num and seperate to new cages based on gender
my_table.weaned(cage_num, strain, female_num=0, female_cage=False, female_cage2=False, 
                max_females = 5, male_num=0, male_cage=False, male_cage2=False, max_males = 5)
                
my_table.weaned(5303, 'WT', female_num=4, female_cage=5401, male_num=8, male_cage=5402, male_cage2=5403)
```

An animal ID (male or female) consists of the parental cage number, followed by a dash, a letter representing the cohort, and a number representing the mouse within that cohort.

### Example: '4881-D3'.

4881 --> parental cage number.

D --> 4th cohort of that parental breeding pair.

3 --> 3rd mouse in the cohort.

## License
[MIT](https://choosealicense.com/licenses/mit/)
