from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn
import mysql.connector
from mysql.connector import errorcode

#security
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

#for terminal colors
from colorama import Fore,Style

# custom modules
from data_loader import DatabaseLoader 
from sql_scripts import SqlScripts
from recommendation import RecommendMentors

#error module
from errors import NoMentorInProgram, NoMenteeInProgram, TableNotFound

#downloading important libraries
import nltk
# nltk.download("stopwords")
nltk.download("wordnet")
from nltk.corpus import wordnet as wn
wn.ensure_loaded()


# loading config file
try:
    config = DatabaseLoader.load_config()
except FileNotFoundError as err:
    print(f"{Fore.RED}Not able to load config file!!{Style.RESET_ALL}")

# authentication function
security = HTTPBearer()
async def authenticate_user(request: Request,
                      credentials: HTTPAuthorizationCredentials= Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, config["jwt"]["key"], algorithms=config["jwt"]["algorithms"])
        # print(payload)
        request["state"]["user_details"] = payload
    
    except jwt.exceptions.InvalidSignatureError as err:
        raise HTTPException(status_code=403, detail="Invalid Signature!!")

# loading the app
app = FastAPI(title="Mentor Mentee Recommendation",
              description="API to Recommend Mentees with Mentors",
              dependencies=[Depends(authenticate_user)])


@app.get("/{program_id}")
def similarity(program_id: int, request: Request, skip: int = 0, limit: int = 10):
    try:
        with DatabaseLoader.load_data(config) as database:
            sql_obj = SqlScripts(database)
            # verify whether user exists in database or not
            verify = sql_obj.verify_user(request["state"]["user_details"])
            # print(verify)
            if not verify:
                raise HTTPException(status_code=401, detail="Not Authorized!!")
            mentor_data = sql_obj.joined_mentor_data(program_id=program_id)
            mentee_data = sql_obj.joined_mentee_data(program_id=program_id, 
                                                     limit=limit, 
                                                     skip=skip)
            grouped_data = sql_obj.grouped_mentors(program_id)
            
        if config["zero_mentee"]:
            # recommend mentors with zero mentee
            recommend = RecommendMentors(config=config, 
                                        mentor_data=mentor_data, 
                                        mentee_data=mentee_data,
                                        grouped_data=grouped_data,
                                        zero_mentee=True)

        else:
            recommend = RecommendMentors(config=config, 
                                        mentor_data=mentor_data, 
                                        mentee_data=mentee_data,
                                        grouped_data=grouped_data)
        recommend.clean_data()
        result = recommend.similarity_percentage()
        
        # print(len(mentor_data.index), len(grouped_data.index), len(data_check.index))
            
        return JSONResponse(content = jsonable_encoder(result))
     
    except NoMentorInProgram as err:
        print(f"{Fore.RED}ERROR:\t  No Mentor present in Program {program_id}!!{Style.RESET_ALL}")
        raise HTTPException(status_code=404, detail= f"No Mentor present in Program {program_id}!!")
    
    except NoMenteeInProgram as err:
        print(f"{Fore.RED}ERROR:\t  No Mentee present in Program {program_id}!!{Style.RESET_ALL}")
        raise HTTPException(status_code=404, detail= f"No Mentee present in Program {program_id}!!")

    except TableNotFound as err:
        print(f"{Fore.RED}ERROR:\t  {err.table_name} Table not Present!!{Style.RESET_ALL}")
        raise HTTPException(status_code=500, detail= f"{err.table_name} Table not Present!!")

    except mysql.connector.errors.DatabaseError as err:
        print(f"{Fore.RED}ERROR:\t  Can't connect to the MySQL Server!!{Style.RESET_ALL}")
        raise HTTPException(status_code=500, detail= "Can't connect to the MySQL Server!!")
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f"{Fore.RED}ERROR:\t  Something is wrong with User Name or Password!!{Style.RESET_ALL}")
            raise HTTPException(status_code=500, detail="Something is wrong with User Name or Password!!")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            # raise err
            raise HTTPException(status_code=500, detail="Database does not exist!!")
        else:
            print(f"{Fore.RED}ERROR Occurred!{Style.RESET_ALL}\n", err)
            
            raise HTTPException(status_code=500, detail="Something Went Wrong!!!")
    
    
    except Exception as err:
        print("Error Occurred!\n")
        print(err)
        # raise err
        raise HTTPException(status_code=500, detail="Something Went Wrong!!!")
    
    
if __name__ == "__main__":
    try:
        uvicorn.run("app:app", 
                    host=config["server"]["host"], 
                    port=config["server"]["port"], 
                    reload=config["server"]["reload"])
    except NameError as err:
        print(f"{Fore.RED}Not able to Fetch Server details from Config File!!{Style.RESET_ALL}")
    except Exception as err:
        print(f"{Fore.RED}Error Occurred!\n{Style.RESET_ALL}", err)
        # raise err