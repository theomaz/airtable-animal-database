"""
Module for updating airtable animal database.

All airtable column names can be modified according to the layout a lab
chooses to uses.

Default Column Categories & Example Entries:
 ______________________________________________________________________________________________________________________________________________________
|_ID_|___Status____|_Strain_|_Cage Card_|_Animal_ID_|___Born____|_Gender_|___Partner ID__|_Breeding Date_|__Father ID__|__Mother ID__|__Weaning Date___|
|1512|B: Breeding  |   WT   |    6000   |  1071-A1  | 4/10/2019 |   M    |   1071-A2_WT  |   5/12/2019   |  1023-C1_WT |  1020-A2_WT |                 |
|1513|P: With Pups |   WT   |    6001   |  1071-A2  | 4/10/2019 |   F    |   1071-A1_WT  |   5/12/2019   |  1023-C1_WT |  1053-C1_WT |   6/20/2019     |
|1514|S: Sacrificed|   WT   |    6002   |  1071-A3  | 4/10/2019 |   M    |               |               |  1023-C1_WT |  1020-A1_WT |                 |
|1515|A: Availble  |   WT   |    6002   |  1071-A4  | 4/10/2019 |   M    |               |               |  1023-C1_WT |  1060-D2_WT |                 |
|    |             |        |           |           |           |        |               |               |             |             |                 |
|____|_____________|________|___________|___________|___________|________|_______________|_______________|_____________|_____________|_________________|                                                                                                                                             |

Classes:
    Manipulate: A Session object used to manipulate a specific airtable data table.

Functions:
    get_max_ID: 
        Get the max ID.
    SAC_mouse: 
        A mouse is SACed (i.e. sacrificed).
    SAC_cage: 
        All mice within a cage are SACed (i.e. sacrificed).
    set_breeding: 
        A male and 1-2 female(s) are put in a cage for breeding.
    birth: 
        A cage's litter is born.
    weaned: 
        A cage's litter has weaned and is moved to seperate cages.
    get_date_born: 
        Uses the weaning date entry of a mother to calculate date born.
    group_by_gender: 
        Group cage into list of males and females.
    get_next_cohort: 
        Find the next cohort's letter ("A"--> 1st, "B"--> 2nd, etc.).
    assign_weaned_mice: 
        Use parameters from weaned() to assign mice to cages.
    get_mother: 
        Given a breeding cage, returns the mother's record.
    genotype_maintenance: 
        Assigns maintenance status to mice that require genotyping.
"""

import string
import sys
import datetime
from datetime import timedelta

from airtable import Airtable
from session_dir.session_object import *

class Manipulate(Session):
    """ 
    Changes to a session's database are done through the Manipulate class
    """

    def __init__(self, *args, **kwargs):
        super(Manipulate, self).__init__(*args, **kwargs)
        # Column Categories
        self.ID_col = "ID"
        self.status_col = "Status"
        self.strain_col = "Strain"
        self.cage_card_col = "Cage Card"
        self.animal_ID_col = "Animal ID"
        self.born_col = "Born"
        self.gender_col = "Gender"
        self.partner_ID_col = "Partner ID"
        self.breeding_date_col = "Breeding Date"
        self.father_ID_col = "Father ID"
        self.mother_ID_col = "Mother ID"
        self.weaning_date_col = "Weaning Date"

        # Mouse status types
        self.available = "A: Available"
        self.breeding = "B: Breeding"
        self.dead = "D: Died"
        self.SACed = "S: Sacrificed"
        self.pups = "P: With Pups"
        self.maintenance = "CM: Colony Maintenance"

        # Mouse Sex
        self.male = "M"
        self.female = "F"
    
    def get_max_ID(self):
        """
        Returns the max ID.
        """
        airtable = self.Authenticate(self.base_key, self.table_name, self.API_key)
        max_ID = airtable.get_all(sort="-" + self.ID_col, 
                                  max_records=1)[0]["fields"][self.ID_col]
        return max_ID

    def SAC_mouse(self, animal_ID):
        """
        Set a mouse"s status to "S: Sacrificed".

        Arg:
            animal_ID: Animal ID of selected mouse
        """
        airtable = self.Authenticate(self.base_key, self.table_name,
                                     self.API_key)
        # Get the mouse record
        record = airtable.search(self.animal_ID_col, animal_ID)[0]["fields"]
        # Mouse must exist and not already be SACed
        assert record[self.animal_ID_col] != [], "ID does not exist"
        assert record[self.status_col] != self.SACed, "Mouse is already SACed"

        airtable.update_by_field(self.animal_ID_col, animal_ID,\
                                {self.status_col: self.SACed})
        # animal_IDS is animal_ID + strain
        animal_IDS = (animal_ID + "_" + record[self.strain_col])
        print("--------------------")
        print(str(animal_IDS) + " mouse SACed")
        print("--------------------")

    def SAC_cage(self, cage_num):
        """
        Set status of all mice within a cage to "S: Sacrificed".

        Arg:
            cage_num: The assigned cage number.
        """
        airtable = self.Authenticate(self.base_key, self.table_name,
                                     self.API_key)

        # Cage must exist
        assert airtable.search(self.cage_card_col, cage_num) != [],\
                               "Cage does not exist"
        # At least one mouse must still be alive for SAC command
        # to be applicable
        alive = False
        for record in airtable.search(self.cage_card_col, cage_num):
            if record["fields"][self.status_col] != self.SACed\
                and record["fields"][self.status_col] != self.dead:
                alive = True
                break
        if alive:
            pass
        else:
            print("--------------------")
            print("Error: All mice in cage " + str(cage_num) \
                  + " are already dead")
            print("--------------------")
            return
        # All live mice are set to SAC status
        for record in airtable.search(self.cage_card_col, cage_num):
            if record["fields"][self.status_col] != self.SACed\
                and record["fields"][self.status_col] != self.dead:  
                airtable.update(record["id"], {self.status_col: self.SACed})
                animal_IDS = record["fields"][self.animal_ID_col]\
                             + "_" + record["fields"][self.strain_col]
                print("--------------------")
                print(animal_IDS + " was SACed")

        print("--------------------")
        print("Cage " + str(cage_num) + " SACed")
        print("--------------------")

    def set_breeding(self, cage_num, month, day, year, male_ID,
                     female_ID, female_ID2=False):
        """
        A male and 1 or 2 females have been put in a cage for breeding.

        Change record of male and female mouse to new cage.
        Set breeding date for all mice.
        Set each other as partner_ID (if there are 2 females
        then the male's partner ID entry will be the first
        female).

        Args:
            cage_num: The assigned cage number.
            month/day/year: The date breeding began, MM/DD/YYYY format.
            male_ID: Male's "Animal ID".
            female_ID: First female's "Animal ID".
            female_ID2: Second female's (if applicable) "Animal ID".
        """
        airtable = self.Authenticate(self.base_key, self.table_name,
                                     self.API_key)
        date = datetime.date(year, month, day) 

        male_record = airtable.search(self.animal_ID_col, male_ID)
        female_record = airtable.search(self.animal_ID_col, female_ID)
        if female_ID2:
            female_record2 = airtable.search(self.animal_ID_col, female_ID2)
        # Make sure male_ID/female_ID/female_ID2 exist, are alive
        # and correct gender
        assert male_record, "Male Animal ID does not exist"
        assert female_record, "Female Animal ID does not exist"
        if female_ID2:
            assert female_record2, "Second female Animal ID does not exist"
        assert male_record[0]["fields"][self.gender_col] == self.male,\
               "Male Animal ID does not belong to a male"
        assert male_record[0]["fields"][self.gender_col] != self.SACed\
            and male_record[0]["fields"][self.status_col] != self.dead,\
            "Male is dead and cannot breed"
        assert female_record[0]["fields"][self.gender_col] == self.female,\
               "Female Animal ID does not belong to a female"
        assert female_record[0]["fields"][self.status_col] != self.SACed\
               and female_record[0]["fields"][self.status_col] != self.dead,\
               "Female is dead and cannot breed"
        if female_ID2:
            assert female_record2[0]["fields"][self.gender_col] == self.female,\
                "Second female Animal ID does not belong to a female"
            assert female_record2[0]["fields"][self.status_col] != self.SACed\
                and female_record2[0]["fields"][self.status_col] != self.dead,\
                "Second female is dead and cannot breed"

        if airtable.search(self.cage_card_col, cage_num) != []:
            verify = input("Cage already alocated. Continue? y/n > ")
            if verify == "y":
                pass 
            else:
                print("--------------------")
                print("Ending function call prematurely")
                print("--------------------")
                return

        cage_num = str(cage_num)
        # IDS is the animal_ID + strain as it is used for "Partner ID" column
        male_IDS = (male_ID + "_"
                    + male_record[0]["fields"][self.strain_col])
        female_IDS = (female_ID + "_"
                    + female_record[0]["fields"][self.strain_col])
        # Update male's info
        update_male = {
            self.partner_ID_col: female_IDS, self.status_col: self.breeding,
            self.cage_card_col: cage_num, self.breeding_date_col:
            str(date.month) + "/" + str(date.day) + "/" + str(date.year)
        }
        airtable.update_by_field(self.animal_ID_col, male_ID, update_male)
        # Update first female's info
        update_female = {
            self.partner_ID_col: male_IDS, self.status_col: self.breeding,
            self.cage_card_col: cage_num, self.breeding_date_col:
            str(date.month) + "/" + str(date.day) + "/" + str(date.year)
        }
        airtable.update_by_field(self.animal_ID_col, female_ID, update_female)
        # Update second female's (if there is one) info
        if female_ID2:
            update_female2 = {
                self.partner_ID_col: male_IDS, self.status_col: self.breeding,
                self.cage_card_col: cage_num, self.breeding_date_col:
                str(date.month) + "/" + str(date.day) + "/" + str(date.year)
            }
            airtable.update_by_field(self.animal_ID_col, female_ID2, update_female2)

        print("--------------------")
        if female_ID2:
            print("At cage " + str(cage_num) + ", " + str(male_ID) + " (MALE), "
                + str(female_ID) + " and " + str(female_ID2) + " (FEMALES) "
                + "were set to breeding on " + str(date.month) + "/"
                + str(date.day) + "/" + str(date.year))
        elif not female_ID2:
            print("At cage " + str(cage_num) + ", " + str(male_ID) + " (MALE), "
                + str(female_ID) + " (FEMALE)" + " were set to breeding on "
                + str(date.month) + "/" + str(date.day) + "/" + str(date.year))
        print("--------------------")

    def birth(self, cage_num, month, day, year):
        """
        A cage's litter is born.

        Set the female mouse's status to "P: With Pups".
        Set weaning date to 3 weeks from now.
        API does not yet support functionality for "*Date* pups weaned"
        comment.

        Args:
            cage_num: The assigned cage number.
            month/day/year: The date that the litter was born.
        """
        airtable = self.Authenticate(self.base_key, self.table_name, 
                                     self.API_key)
        assert airtable.search(self.cage_card_col, cage_num) != [],\
                               "Cage does not exist"

        # Calculate weaning date, i.e. date born plus 3 weeks
        date_born = datetime.date(year, month, day)
        date_weaned = date_born + timedelta(days = 21)

        # Female from cage_num with the lowest ID number
        # will always be chosen as marked "P: With Pups"
        matches = airtable.search(self.cage_card_col, cage_num)
        females = []
        for record in matches:
            if record["fields"][self.gender_col] == self.female:
                females.append(record)
        females = sorted(females, key = lambda i: i["fields"][self.ID_col])
        mother_ID = females[0]["fields"][self.animal_ID_col]
        # Checking female was breeding
        assert females[0]["fields"][self.status_col] == self.breeding,\
               "Female was not originally set to breeding"
        airtable.update_by_field(self.animal_ID_col, mother_ID,
                                {self.status_col: self.pups})
        airtable.update_by_field(self.animal_ID_col, mother_ID,
                                {self.weaning_date_col:
                                str(date_weaned.month) + "/"
                                + str(date_weaned.day)
                                + "/" + str(date_weaned.year)})
        print("--------------------")
        print("Pups born at cage " + str(cage_num) + " on " 
              + str(date_born.month) + "/" + str(date_born.day) + "/" 
              + str(date_born.year))
        print("--------------------")

    def group_by_gender(self, cage_num):
        """
        Group cage's mice records based on gender

        Args:
            cage_num: cage number

        Returns:
            2 lists, one for males and one for females
        """
        airtable = self.Authenticate(self.base_key, self.table_name, self.API_key)

        matches = airtable.search(self.cage_card_col, cage_num)
        females = []
        males = []
        for record in matches:
            if record["fields"][self.gender_col] == self.female:
                females.append(record)
            else:
                males.append(record)
        
        return males, females

    def get_next_cohort(self, cage_num):
        """
        Find the next cohort's letter.

        "A" --> 1st cohort, "B" --> 2nd cohort, etc.

        Returns: Cohort letter
        """
        airtable = self.Authenticate(self.base_key, self.table_name, self.API_key)

        i = 0
        match = None
        while match != []:
            uppercase = list(string.ascii_uppercase)
            # If a mouse with this cohort letter doesnt exist,
            # we have found our next cohort
            candidate = str(cage_num) + "-" + uppercase[i] + "1"
            match = airtable.search(self.animal_ID_col, candidate)
            cohort = uppercase[i]
            i +=1

        return cohort

    def assign_weaned_mice(self, max_ID, record, cage_num, cohort,
                           female_num=0, female_cage=False, 
                           female_cage2=False, max_females=5, male_num=0,
                           male_cage=False, male_cage2=False, max_males=5):
        """
        Seperate the weaned mice from the parental cage based on gender.

        Args:
            max_ID: The maximum ID number already assigned in database.
            record: A dictionary of column-value pairs that apply to all mice
                    (e.g. Father ID).
            cage_num: The parental cage number.
            cohort: The cohort the mice are apart of ("A" --> 1st, "B" --> 2nd,...)
            female_num: The number of weaned female mice.
            female_cage: The cage number where the females (max 5) are transferred.
            female_cage2: The cage number where the remaining females are transferred.
            max_females: Amount of females assigned to 1st cage (default is 5).
            male_num: The number of weaned male mice.
            male_cage: The cage number where the males (max 5) are transferred.
            male_cage2: The cage number where the remaining males are transferred.
            max_males: Amount of males assigned to 1st cage (default is 5).
        
        """
        
        airtable = self.Authenticate(self.base_key, self.table_name, self.API_key)

        # Update ID (i) and animal_ID incrementally
        counter = 1
        mice_in_cohort = 1
        for ID in range(int(max_ID) + 1, int(max_ID) + 1 + male_num + female_num):
            ID = str(ID)
            # If cohort reaches 10th mouse, move onto next cohort (e.g. "B"-->"C")
            # Move onto next cohort if 10 < male_num + female_num 
            # and all females are assigned
            if mice_in_cohort >= 11 or (10 - male_num) < female_num == counter - 1:
                cohort = chr(ord(cohort) + 1)
                mice_in_cohort = 1
            # animal_ID is animal_ID[0:-1] (e.g. 1057-B) + counter (e.g. 4)
            animal_ID = str(cage_num) + "-" + str(cohort) + str(mice_in_cohort)
            record[self.ID_col] = ID
            record[self.animal_ID_col] = animal_ID
            # If counter is larger than female_num,
            # all females have been assigned
            if counter <= female_num:
                record[self.gender_col] = self.female
            else:
                record[self.gender_col] = self.male
            # If (based on counter) we are still assigning females and 
            # we haven"t reached max amount of females in first cage
            # assign to 1st cage
            if counter <= max_females and counter <= female_num:
                record[self.cage_card_col] = str(female_cage)
                print(animal_ID + " goes to cage " + str(female_cage))
            # elif cage 1 is full (has reached max_females) but not all 
            # females are assigned
            elif counter <= female_num:
                record[self.cage_card_col] = str(female_cage2)
                print(animal_ID + " goes to cage " + str(female_cage2))
            # If counter remaining for males is under max_males
            # assign to 1st cage
            elif counter - female_num <= max_males:
                record[self.cage_card_col] = str(male_cage)
                print(animal_ID + " goes to cage " + str(male_cage))
            else:
                record[self.cage_card_col] = str(male_cage2)
                print(animal_ID + " goes to cage " + str(male_cage2))
            airtable.insert(record)
            counter += 1
            mice_in_cohort += 1 

    def get_parents(self, males, females): 

        """
        Find mother (i.e. lowest ID female) in cage.

        Args:
            females: List of female mice records within a cage.

        Returns:
            Record (dictionary) of mother.
        """

        # mother_ID is the cage's female with the lowest ID
        # unless mouse is dead
        females = sorted(females, key = lambda i: i["fields"][self.ID_col])
        with_pups_index = 0
        for i in range(0, len(females)):
            if (females[i]["fields"][self.status_col] != self.SACed\
                and females[i]["fields"][self.status_col] != self.dead):
                with_pups_index = i
                break
            else:
                pass
        # If female is alive, check if status is "P: With Pups"
        assert (females[with_pups_index]["fields"][self.status_col]\
                == self.pups), "Mother did not have P: With Pups status"
        mother_record = females[with_pups_index]

        for i in range(0, len(males)):
            # Make sure Father ID is asigned to alive male
            if (males[i]["fields"][self.status_col] != self.SACed\
                and males[i]["fields"][self.status_col] != self.dead):
                father_index = i
                break
            else:
                pass
        assert(males[father_index]["fields"][self.status_col]\
               == self.breeding), "Father was not set to breeding"
        father_record = males[father_index]

        return father_record, mother_record
    
    def genotype_maintenance(self, offspring_strain, need_genotyping, record):
        """
        If strain of weaned mice requires genotyping, change status of weaned
        mouse entries to colony maintenance

        Args:
            offspring_strain: The strain of the weaned offspring (e.g. DF16A x WT)
            need genotyping: A list of strains that require genotyping
            record: A dictionary of column-value pairs shared by the cohort's mice
                    (e.g. Father ID)

        """
        # Mice are not available while these lines get genotyped
        # Which in this case is for weaned -Cre or DF16A strains
        for strain in need_genotyping:
            if offspring_strain.find(strain) >= 0:
                record[self.status_col] = self.maintenance

        return record    

    def weaned(self, cage_num, strain, female_num=0, female_cage=False,
               female_cage2=False, max_females = 5, male_num=0, 
               male_cage=False, male_cage2=False, max_males = 5):
        """
        A cage's litter has been weaned and is being moved to seperate
        cages.

        Change mother's status back to "B: Breeding".
        Remove mother's weaning date entry.
        Check largest ID number and assign subsequent ID(s) to new mice
        (not to be confused with animal_ID).
        Enter information for new mice (ID, Status, Strain, Cage Card,
        Animal ID, Born, Gender, Father ID, Mother ID).
        API does not yet provide functionality for adding comment
        "*Date* pups weaned" for mother.
        Check for -Cre and DF16A lines that are need to be genotyped.

        Note: Mice are not entered into the database until they have been
        weaned. Often if there are 6 or 8 weaned mice of the same gender
        they might be seperated by placing half in one cage and half in
        another, hence "max males/max females" signifies max amount per cage. 
        Normally, however, the 5 first mice of each gender are placed in the 
        first cage and any remaining are placed in the second.
        The letter in an animal ID (e.g. 1057-B1) signifies the cohort it is
        from (A -> 1st cohort, B -> 2nd,...), while the number before the 
        dash is the parental cage it is from. However, if a litter of 
        weaned pups goes past the number 10 (e.g. 1057-A10), then the 
        following pups are assigned starting from the next letter 
        (i.e. 1057-B1, 1057-B2,...). It isn't a perfect system, but it's 
        the system our lab uses.

        Args:
            cage_num: The parental cage number.
            strain: The weaned litter's genetic strain (e.g. WT for wild-type).
            female_num: The number of weaned female mice.
            female_cage: The cage number where the females (max 5) are transferred.
            female_cage2: The cage number where the remaining females are transferred.
            max_females: Amount of females assigned to 1st cage (default is 5).
            male_num: The number of weaned male mice.
            male_cage: The cage number where the males (max 5) are transferred.
            male_cage2: The cage number where the remaining males are transferred.
            max_males: Amount of males assigned to 1st cage (default is 5).
        """
        airtable = self.Authenticate(self.base_key, self.table_name, self.API_key)

        # Original cage must exist and new ones must not
        assert airtable.search(self.cage_card_col, cage_num) != [],\
               "Cage does not exist"
        if male_cage:
            assert airtable.search(self.cage_card_col, male_cage) == [],\
                   "Cage already alocated"
            assert male_cage not in [male_cage2, female_cage, female_cage2],\
                   "Cage has been assigned twice"
        if male_cage2:
            assert airtable.search(self.cage_card_col, male_cage2) == [],\
                   "Cage already alocated"
            assert male_cage2 not in [male_cage, female_cage, female_cage2],\
                   "Cage has been assigned twice"                    
        if female_cage:
            assert airtable.search(self.cage_card_col, female_cage) == [],\
                   "Cage already alocated"
            assert female_cage not in [male_cage, male_cage2, female_cage2],\
                   "Cage has been assigned twice"
        if female_cage2:
            assert airtable.search(self.cage_card_col, female_cage2) == [],\
                   "Cage already alocated"
            assert female_cage2 not in [male_cage, male_cage2, female_cage],\
                   "Cage has been assigned twice"
        if male_num > 5:
            assert male_cage2 is not False, "Not enough cages to assign males"
        if female_num > 5:
            assert female_cage2 is not False,\
                   "Not enough cages to assign females"
        if airtable.search(self.strain_col, strain) == []:
            verify = input("You are about to enter a new strain that" +
                           " is not in the database. Continue? y/n >")
            if verify == "y":
                pass
            else:
                print("--------------------")
                print("Ending function call prematurely")
                print("--------------------")
                return

        males, females = self.group_by_gender(cage_num)
        father_record, mother_record = self.get_parents(males, females)
        mother_ID = mother_record["fields"][self.animal_ID_col]

        # "IDS" signifies Animal ID + Strain
        mother_IDS = (mother_ID + "_"
                      + mother_record["fields"][self.strain_col])
        father_IDS = (father_record["fields"][self.animal_ID_col] + "_"
                      + father_record["fields"][self.strain_col])
        # Calculate when pups were born (weaning date - 21 days):
        date_weaned = mother_record["fields"][self.weaning_date_col]
        date_born = get_date_born(date_weaned)
        # Set mother's status back to breeding and remove weaning date
        airtable.update_by_field(self.animal_ID_col, mother_ID,
                                {self.status_col: self.breeding})
        airtable.update_by_field(self.animal_ID_col, mother_ID,
                                {self.weaning_date_col: None})

        max_ID = self.get_max_ID()
        # Get next cohort letter
        cohort = self.get_next_cohort(cage_num)
        # All offspring share these values
        record = {
            self.status_col: self.available, self.strain_col: str(strain),
            self.father_ID_col: father_IDS, self.mother_ID_col: mother_IDS,
            self.born_col: date_born
        }

        # Change record's status to colony maintenance if genotyping is necessary
        record = self.genotype_maintenance(strain, ['-Cre','DF16A'], record)

        self.assign_weaned_mice(max_ID, record, cage_num, cohort, female_num, female_cage,
                                female_cage2, max_females, male_num,
                                male_cage, male_cage2, max_males)

def get_date_born(date_weaned):
    """
    Calculate the date pups were born based on weaning date entry

    Args:
        date_weaned: MM/DD/YYYY format; equals date born + 21 days

    Returns: 
        Date born in MM/DD/YYYY format
    """
    date_weaned = date_weaned.split("/")
    month = int(date_weaned[0])
    day = int(date_weaned[1])
    year = int(date_weaned[2])
    date_weaned = datetime.date(year, month, day)
    date_born = date_weaned - timedelta(days = 21)
    date_born = (str(date_born.month) + "/" + str(date_born.day)
                + "/" + str(date_born.year))

    return date_born