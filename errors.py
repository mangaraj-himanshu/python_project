# define Python user-defined exceptions
class NoMentorInProgram(Exception):
    "Raised when there are no mentors in Program"
    
    def __init__(self, message="Error: No Mentors Present in the Program!!"):
        self.message = message
        super().__init__(self.message)

class NoMenteeInProgram(Exception):
    "Raised when there are no mentee in Program"
    
    def __init__(self, message="No Mentor present in Program"):
        self.message = message
        super().__init__(self.message)

class TableNotFound(Exception):
    "Raised when table is not Found in SQL"
    
    def __init__(self, table_name=None, message="Table is not Present!!"):
        self.table_name = table_name
        self.message = message
        super().__init__(self.message)
    
