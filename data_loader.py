import json
import mysql.connector
from contextlib import contextmanager

# for terminal colors
from colorama import Fore,Style


#type hinting
import os
from typing import Union
from mysql.connector.connection import MySQLConnection

class DatabaseLoader:
    "Class to load database"
    
    @staticmethod
    def load_config(config_path: Union[str,os.PathLike]  = "config.json") -> dict:
        """Function to load the config file
        
        Parameters
        -----------
            - `config_path` (Union[str,os.PathLike], optional): Path to the config file. Defaults to "config.json".
        
        Raises
        -------
            `FileNotFoundError`: raises if config file is not found.
            `err`: raises if any other error is present.
        
        Returns
        --------
            `dict`: returns data present in config file.
        """                
        try:
            with open(config_path) as f:
                config = json.load(f) # loading the json file
            return config
        except FileNotFoundError:
            print(f"{Fore.RED}Config File Not Found!! {Fore.GREEN}- Function: DatabaseLoader.load_config{Style.RESET_ALL}")
            raise FileNotFoundError("Config File Not Found!!")
        except Exception as err:
            print(f"{Fore.RED}Error occured!! {Fore.GREEN}- Function: DatabaseLoader.load_config{Style.RESET_ALL}")
            raise err
            
    @staticmethod
    @contextmanager
    def load_data(config: dict) -> MySQLConnection:
        try:
            database = mysql.connector.connect(
                host = config["SQL"]["host"],
                port = config["SQL"]["port"],
                user = config["SQL"]["user"],
                passwd = config["SQL"]["password"],
                database = config["SQL"]["database"]
            )
            yield database
            
        except mysql.connector.errors.DatabaseError as err:
            print(f"{Fore.RED}ERROR:\t  Can't connect to the MySQL Server!! {Fore.GREEN}- Function DatabaseLoader.load_data{Style.RESET_ALL}")
            raise mysql.connector.errors.DatabaseError

        except Exception as err:
            print(f"{Fore.RED}Error occured!! {Fore.GREEN}- Function: DatabaseLoader.load_data{Style.RESET_ALL}")
            raise err
        finally:
            try:
                database.close()
            except UnboundLocalError as err:
                pass
