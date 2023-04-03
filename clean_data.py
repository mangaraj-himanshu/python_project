import re
# from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#stopwords
# stopwords_set = set(stopwords.words("english"))

#lemmatizer
lemmatizer = WordNetLemmatizer()


class Cleaner:
    
    @staticmethod
    def removeHTML(text: str) -> str:
        """remove HTML tags from text
        
        Parameters
        -----------
            - `text` (str): text containing HTML tags.
        
        Returns
        --------
            `str`: cleaned text
        """
        html_cleaner = re.compile("<.*?>")
        cleantext = re.sub(html_cleaner, "", text)
        return cleantext
    
    
    @staticmethod
    def cleanText(text: str) -> str:
        """Clean the text

        Args:
            text (str): text

        Returns:
            str: cleaned text
        """
        text = Cleaner.removeHTML(text) # remove HTML from text
        text = re.sub("httpS+s*", " ", text)  # remove URLs
        text = re.sub("RT|cc", " ", text)  # remove RT and cc
        text = re.sub("#S+", " ", text)  # remove hashtags
        text = re.sub("@S+", " ", text)  # remove mentions
        text = re.sub(
            "[%s]" % re.escape("""!"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""), " ", text
        )  # remove punctuations
        text = re.sub(r"[^\x00-\x7f]", r" ", text)
        text = re.sub("\n", " ", text)  # removing new lines
        text = re.sub(" +", " ", text)  # remove extra whitespace
        text = text.lower()  # lowercasing the text
        #lemmetizing inputs
        text = ' '.join((lemmatizer.lemmatize(word) for word in text.split()))
        # print(text,end="\n\n")
        return text
        
        
