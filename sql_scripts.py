#import for nan 
import numpy as np

# error handling
import mysql.connector
from errors import NoMenteeInProgram, NoMentorInProgram, TableNotFound

#type hinting
from typing import Union
from mysql.connector.connection import MySQLConnection

#for terminal colors
from colorama import Fore,Style

# importing custom modules
from data_loader import DatabaseLoader 

class SqlScripts:
    "Class to run SQL Scripts"
    def __init__(self, database: MySQLConnection) -> None:
        self.database = database # mySQL database object
        self.config = DatabaseLoader.load_config() # loading the config file
        self.cursor = self.database.cursor(dictionary=True) # creating a cursor for sql
    
    
    def joined_mentee_data(self, skip:int, limit:int, program_id:int) -> dict:
        """Function to join the mentee tables
        
        Parameters
        -----------
            - `program_id` (int): To get data for only one program
        
        Returns
        --------
            `dict`: Returns a dictionary of joined mentee data for the program_id
        """
        try:        
            # SQL query to join mentee tables
            mentee_sql_query = "select * \
                        from {0} \
                        inner join {1} \
                        on {0}.mentee_id = {1}.menteeprogram_mentee_id\
                        where mentee_deleted = 'n' and mentee_status = 'Active' and \
                        menteeprogram_acceptance_status = 'Accepted' and \
                        menteeprogram_mentor_id is null and menteeprogram_coordinator_id is null \
                        and menteeprogram_program_id = {2} \
                        LIMIT {3} OFFSET {4}"
                        
            mentee_sql_query = mentee_sql_query.format(
                                    self.config["SQL"]["mentees-table-name"],
                                    self.config["SQL"]["mentees-program-table-name"],
                                    program_id,
                                    limit, skip)
            
            self.cursor.execute(mentee_sql_query)
            # print(cursor.description)
            mentee_data = self.cursor.fetchall()
            # mentee_data = mentee_data*100
            if len(mentee_data) == 0:
                print(f"{Fore.RED}No Mentee present in Program {program_id}!! - {Fore.GREEN}Function joined_mentee_data{Style.RESET_ALL}")
                raise NoMenteeInProgram(f"No Mentee present in Program {program_id}!!")
            
            return mentee_data
        
        except mysql.connector.errors.ProgrammingError as err:
            print(f"{Fore.RED}ERROR:\t {self.config['SQL']['mentees-table-name']} or {self.config['SQL']['mentees-program-table-name']} Table not Present!! {Fore.GREEN}- Function grouped_mentees{Style.RESET_ALL}")
            raise TableNotFound(table_name=
                                f"{self.config['SQL']['mentees-table-name']} or {self.config['SQL']['mentees-program-table-name']}",
                                message=f"{self.config['SQL']['mentees-table-name']} or {self.config['SQL']['mentees-program-table-name']} Table not Present!!")
        
        except Exception as err:
            print(f"{Fore.RED}Error occured!! {Fore.GREEN}- Function joined_mentee_data{Style.RESET_ALL}")
            raise err
    
    def joined_mentor_data(self, program_id: int) -> dict:
        """Function to join the mentor tables
        
        Parameters
        -----------
            - `program_id` (int): To get data for only one program
        
        Returns
        --------
            `dict`: Returns a dictionary of joined mentor data for the program_id
        """       
        try:
            # sql query to join mentor data
            mentor_sql_query = "select * \
                        from {0} \
                        inner join {1} \
                        on {0}.mentor_id = {1}.mentorprogram_mentor_id \
                        where mentor_deleted = 'n' and mentor_status = 'Active' and \
                        mentorprogram_acceptance_status = 'Accepted' and \
                        mentorprogram_program_id = {2}"
            
            mentor_sql_query = mentor_sql_query.format(
                                    self.config["SQL"]["mentors-table-name"],
                                    self.config["SQL"]["mentors-program-table-name"],
                                    program_id)
            
            self.cursor.execute(mentor_sql_query)
            # print(cursor.description)
            mentor_data = self.cursor.fetchall()

            if len(mentor_data) == 0:
                print(f"{Fore.RED}No Mentor present in Program {program_id}!! {Fore.GREEN}- Function joined_mentor_data{Style.RESET_ALL}")
                raise NoMentorInProgram(f"No Mentor present in Program {program_id}!!")
            
            return mentor_data
        
        except mysql.connector.errors.ProgrammingError as err:
            print(f"{Fore.RED}ERROR:\t {self.config['SQL']['mentors-table-name']} or {self.config['SQL']['mentors-program-table-name']} Table not Present!! {Fore.GREEN}- Function joined_mentor_data{Style.RESET_ALL}")
            raise TableNotFound(table_name=
                                f"{self.config['SQL']['mentors-table-name']} or {self.config['SQL']['mentors-program-table-name']}",
                                message=f"{self.config['SQL']['mentors-table-name']} or {self.config['SQL']['mentors-program-table-name']} Table not Present!!")
        
        except Exception as err:
            print(f"{Fore.RED}Error occured!! {Fore.GREEN}- Function joined_mentor_data{Style.RESET_ALL}")
            raise err
    
    def grouped_mentors(self, program_id: int) -> dict:
        """Function to get the number of mentees per mentor
        
        Parameters
        -----------
            - `program_id` (int): To get data for one program only
        
        Returns
        --------
            `dict`: Returns a dict of Mentor Id and Mentee Number per mentor 
        """
        try:
            # sql query to get number of mentee's per mentor
            grouped_mentor_sql_query = "select menteeprogram_mentor_id as mentor_id,\
                        count(menteeprogram_mentor_id) as mentee_number \
                        from {0} \
                        inner join {1} \
                        on {0}.mentee_id = {1}.menteeprogram_mentee_id \
                        where mentee_deleted = 'n' and mentee_status = 'Active' and \
                        menteeprogram_acceptance_status = 'Accepted' and \
                        menteeprogram_program_id = {2} \
                        group by menteeprogram_mentor_id"
                
            grouped_mentor_sql_query = grouped_mentor_sql_query.format(
                                    self.config["SQL"]["mentees-table-name"],
                                    self.config["SQL"]["mentees-program-table-name"],
                                    program_id)
            
            self.cursor.execute(grouped_mentor_sql_query)
            # print(cursor.description)
            grouped_mentor_data = self.cursor.fetchall()
            
            if (len(grouped_mentor_data) == 0):
                grouped_mentor_data = [{"mentor_id": np.NAN, "mentee_number": np.NAN}]
            
            return grouped_mentor_data
        
        except mysql.connector.errors.ProgrammingError as err:
            print(f"{Fore.RED}ERROR:\t {self.config['SQL']['mentees-table-name']} or {self.config['SQL']['mentees-program-table-name']} Table not Present!! {Fore.GREEN}- Function grouped_mentors{Style.RESET_ALL}")
            raise TableNotFound(table_name=
                                f"{self.config['SQL']['mentees-table-name']} or {self.config['SQL']['mentees-program-table-name']}",
                                message=f"{self.config['SQL']['mentees-table-name']} or {self.config['SQL']['mentees-program-table-name']} Table not Present!!")
        
        except Exception as err:
            print(f"{Fore.RED}Error occured!! {Fore.GREEN}- Function grouped_mentors{Style.RESET_ALL}")
            raise err
    
    def verify_user(self,user_details: dict) -> bool:
        """Function to verify if user is present in the database or not
        
        Parameters
        -----------
            - `user_details` (dict): user details extracted from JWT Bearer Token
        
        Returns
        --------
            `bool`: Returns True, if user is present in the database or False if user is not present in the database
        """
        try:
            # sql query to extract data from the view
            user_data_query = f"select * from {self.config['SQL']['authentication-view-name']} where user_id = {user_details['userid']}"
            self.cursor.execute(user_data_query)
            
            user_data = self.cursor.fetchall()

            # verifying details of users from the view data
            for data in user_data:
                if (data["user_name"] == user_details["username"]) and \
                (data["user_email"] == user_details["useremail"]):
                    return True
            else:
                return False # return false is user not found in the view
        
        except mysql.connector.errors.ProgrammingError as err:
            print(f"{Fore.RED}ERROR:\t {self.config['SQL']['authentication-view-name']} Table not Present!! {Fore.GREEN}- Function verify-user{Style.RESET_ALL}")
            raise TableNotFound(table_name=self.config['SQL']['authentication-view-name'], message=f"{self.config['SQL']['authentication-view-name']} Table not Present!!")
        
        except Exception as err:
            print(f"{Fore.RED}Error occured!! {Fore.GREEN}- Function verify_user{Style.RESET_ALL}")
            raise err
        
        
        
    
    