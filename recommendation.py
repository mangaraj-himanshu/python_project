import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#for terminal colors
from colorama import Fore,Style

# custom module
from clean_data import Cleaner

#error module
from errors import NoMentorInProgram

class RecommendMentors:
    "Class to recommend mentors to mentees"
    def __init__(self, config: dict, mentor_data: dict, mentee_data: dict, grouped_data: dict, 
                 zero_mentee: bool = False ) -> None:
        self.config = config
        # converting dict to dataframe
        self.mentor_data = pd.DataFrame().from_dict(mentor_data)
        self.mentee_data = pd.DataFrame().from_dict(mentee_data)
        grouped_data = pd.DataFrame().from_dict(grouped_data)
        self.mentor_data = pd.merge(self.mentor_data, grouped_data, on="mentor_id", how="left")
        self.mentor_data["mentee_number"] = self.mentor_data["mentee_number"].fillna(0)
        self.vectorizer = CountVectorizer()
        if zero_mentee:
            self.mentor_data = self.mentor_data[
                self.mentor_data["mentee_number"] == 0]
        # print(self.mentor_data)
            if not len(self.mentor_data.index):
                raise NoMentorInProgram()
        
    
    def clean_data(self):
        "Function to clean the text columns of mentors and mentees"
        try:
            # filling empty text columns values with " "
            self.mentor_data[self.config["mentor_text_columns"]] = self.mentor_data[self.config["mentor_text_columns"]].fillna(" ") 
            self.mentor_data["cleanedMentorData"] = self.mentor_data[self.config["mentor_text_columns"]].apply(lambda x: Cleaner.cleanText(" ".join(x)), axis=1)
            
            self.mentee_data[self.config["mentee_text_columns"]] = self.mentee_data[self.config["mentee_text_columns"]].fillna(" ")
            self.mentee_data["cleanedMenteeData"] = self.mentee_data[self.config["mentee_text_columns"]].apply(lambda x: Cleaner.cleanText(" ".join(x)), axis=1)
                        
            # replacing null values to avoid error
            self.mentor_data = self.mentor_data.fillna("")
            self.mentee_data = self.mentee_data.fillna("")
        
        except Exception as err:
            print(f"{Fore.RED}ERROR!!\t  {Fore.GREEN}- Function recommendation.clean_data{Style.RESET_ALL}")
            raise err
        
    
    def similarity_percentage(self):
        "Function to find similarity percentage for each mentor then recommend top-3 mentors for each mentee"
        try:
            result = []
            # vectorizer = CountVectorizer()
            mentor_not_fluent_in_English = self.mentor_data[
                self.mentor_data["mentor_fluency_in_english"] == "No"]
            mentor_fluent_in_English = self.mentor_data[
                self.mentor_data["mentor_fluency_in_english"] == "Yes"]
            
            length_mentor_not_fluent_in_English = len(mentor_not_fluent_in_English.index)
            length_mentor_fluent_in_English = len(mentor_fluent_in_English.index)
            
            for mentee_data in self.mentee_data.to_dict(orient="records"):
                similarity_list = []
                # print(mentee_data["mentee_id"])
                if (mentee_data["mentee_fluency_in_english"] == "No"):
                    if (length_mentor_not_fluent_in_English == 0):
                        continue
                        # pass
                    else:
                        for mentor_data in mentor_not_fluent_in_English.to_dict(orient="records"):
                            if (bool(set(mentee_data["mentee_languages"].split(",")).intersection(mentor_data["mentor_languages"].split(",")))):
                                # vectorizer = CountVectorizer()
                                # print(val)
                                vec_data = [mentor_data["cleanedMentorData"] ,mentee_data["cleanedMenteeData"]]
                                vecs = self.vectorizer.fit_transform(vec_data).toarray()
                                similarity = cosine_similarity(vecs[0].reshape(1, -1), vecs[1].reshape(1, -1))[0][0]
                                # print("{:.2f}".format(similarity*100))
                                mentor_data["similarity"] = float("{:.2f}".format(similarity*100))
                                similarity_list.append(mentor_data)
                
                else:
                    if (length_mentor_fluent_in_English == 0):
                        continue
                    else:  
                        for mentor_data in mentor_fluent_in_English.to_dict(orient="records"):
                            # print(val)
                            vec_data = [mentor_data["cleanedMentorData"] ,mentee_data["cleanedMenteeData"]]
                            vecs = self.vectorizer.fit_transform(vec_data).toarray()
                            similarity = cosine_similarity(vecs[0].reshape(1, -1), vecs[1].reshape(1, -1))[0][0]
                            # print("{:.2f}".format(similarity*100))
                            mentor_data["similarity"] = float("{:.2f}".format(similarity*100))
                            similarity_list.append(mentor_data)
                
                if (len(similarity_list) != 0):
                    mentee_data["recommendation"] = sorted(similarity_list,key= lambda x: x["similarity"], reverse=True)[0:3]
                else:
                    mentee_data["recommendation"] = []

                # print(mentee_data)
                result.append(mentee_data)

            return result
        
        except Exception as err:
            print(f"{Fore.RED}ERROR!!\t  {Fore.GREEN}- Function similarity_percentage{Style.RESET_ALL}")
            raise err
            
            
        
        
        