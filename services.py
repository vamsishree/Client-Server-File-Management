"""This file consists of a class which handles the commands passed by client to server. """
import os
import time
class Services:
    """It consists of all the methods that are responsible for performing operations required by server."""
    def __init__(self):
        """Used to initialize variables."""
        self.login_status = None
        self.username = ""
        self.working_directory = os.getcwd()+"/Root"

    def login(self,username,password):
        """This method used to log in the user when given username and password matches credentials used while registering.
        Attributes:
                    username : str
                        Holds username given by user.

                    password : str
                        Holds password given by user.
        Returns: str
            returns a message stating the action performed."""
        if self.login_status is True:
            return f"\n{username} already logged in\n"
        credentials = f'{username} {password}'
        file = open("user_credentials.txt","r")
        data = file.read()
        logfile = open("logfile.txt","r+")
        i = logfile.read()
        if username in i:
            return f"\nAlready logged in {username}\n"
        if credentials in data and username not in i:
            logfile.write(f'{username}\n')
            self.login_status = True
            self.username = username
            self.working_directory = os.path.join(self.working_directory,self.username)
            return f'\nLogged in {username}\n'
        if credentials not in data and username in data:
            return "\nIncorrect password entered\n"
        if credentials not in data:
            return "\nUser doesn't exist\nPlease register to continue....\n"

    def register(self,username,password):
        """This method is used to register a new user.
        Attributes:
                    username : str
                        Holds username given by user.
                    password : str
                        Holds password given by user.
        Returns: str
            returns a message stating the action performed."""
        credentials = f'{username} {password}'
        file = open("user_credentials.txt","r+")
        data = file.read()
        if credentials in data:
            return "\nExisting user\nPlease login\n"
        if username in data:
            return "\nUsername already exists\nPlease choose another username\n"
        if credentials not in data:
            file.write(f'{username} {password}\n')
            path = os.path.join(self.working_directory,username)
            os.mkdir(path)
            return f'\nRegistered {username}\nYou can login using login command\n'

    def create_folder(self,folder_name):
        """This method is used to create folder in current working directory.
        Attributes:
                    folder_name : str
                        Holds the name of the folder to be created.
        Returns : str
            returns a message stating the action performed."""
        if self.login_status is not True:
            return "\nPlease login to continue.....\n"
        path = os.path.join(self.working_directory,folder_name)
        try:
            os.mkdir(path)
        except FileExistsError:
            return f"\nFolder already exists with name {folder_name}\n"
        return f"\nFolder created with name {folder_name}\n"

    def read_file(self,filename):
        """This method is used to read the contents in the given file.
        Attributes:
                    filename : str
                        Holds the name of the file which has to be read.
        Returns: str
            returns a message stating the action performed
            if file found and has data in it, returns the data in addition to action."""
        if self.login_status is not True:
            return "\nPlease login to continue.....\n"
        path = os.path.join(self.working_directory,filename)
        try:
            with open(path,'r') as file:
                data = file.read()
                return f"\nFile read.....\n{data}"
        except FileNotFoundError:
            return f"\nFile doesn't exist with name {filename}\n"

    def write_file(self,filename,content=None):
        """This method is used to write contents into the file.
        It creates file when given file name doesn't exist.
        It clears the contents in the file when no data is given to write.
        Attributes:
                    filename : str
                        Holds the name of file given by user.
                    content : str
                        Holds the data which has to be written inside given file.
                        By default it is initialised to None.
        Returns : str
            returns a message stating the action performed."""
        if self.login_status is not True:
            return "\nPlease login to continue.....\n"
        path = os.path.join(self.working_directory,filename)
        file_exists = os.path.exists(path)
        if file_exists is True:
            if content is not None:
                with open(path,"w") as file:
                    file.write(content)
                    return f"\nSuccessfully written data into file {filename}\n"
            elif content is None:
                os.remove(path)
                with open(path,"w") as file:
                    pass
                return "\nFile cleared\n"
        elif file_exists is False:
            if content is not None:
                with open(path,"w") as file:
                    file.write(content)
                    return f"\nCreated file with name {filename} and written data into it.\n"
            elif content is None:
                with open(path,"w") as file:
                    file.write("")
                return f"File created with name {filename}\n"

    def change_folder(self,foldername):
        """This method is used to move the current working directory to the given folder.
        Attributes:
                    foldername : str
                        Holds the name of the folder to which the working directory has to be moved.
        Returns:
            returns a message stating the action performed."""
        if self.login_status is not True:
            return "\nPlease login to continue.....\n"
        path = os.path.join(self.working_directory,foldername)
        folder_exists = os.path.exists(path)
        if folder_exists is True:
            self.working_directory = path
            return f"\nMoved current working directory to folder {foldername}\n"
        if folder_exists is False:
            return "\nFolder doesn't exist\n"

    def list_files(self):
        """This method is used to list all the files & folders in the current working directory.
        This method also gives the information about size of the file and last date modified.
        Returns: str
            returns all the files in working directory with name of file, size and last date modified."""
        if self.login_status is not True:
            return "\nPlease login to continue.....\n"
        fldrs = []
        try:
            for name in os.listdir(self.working_directory):
                details = os.stat(os.path.join(self.working_directory,name))
                fldrs.append([name,str(details.st_size),str(time.ctime(details.st_ctime))])
        except NotADirectoryError:
            return "\nGiven path isn't a directory\n"
        output = "\nName\tSize\tLast modified date\n"
        for i in fldrs:
            line = "".join([i[0],"\t"," ",i[1],"\t",i[2]])+"\n"
            output += "\n" + line
        return output

    def commands(self):
        """This function is used to list all the commands available.
        Returns : str
            returns all the available commands with description and example format of command."""
        commands_list = ["""\nCommand : login <username> <password>\nUsed to login user\n""",
                """\nCommand : register <username> <password>\nUsed to register new user\n"""
                """\nCommand : list\nUsed to list all the files in current directory.\n""",
                """\nCommand : write_file <name> <content>\nTo write content into file,if file doesn't exist creates file and if content is empty it clears file.\n""",
                """\nCommand : create_folder <name>\nUsed to create folder.\n""",
                """\nCommand : change_folder <name>\nUsed to move the working directory to given folder.\n""",
                """\nCommand : read_file <name>\nUsed to read given file.\n""",
                """\nCommand : quit\nUsed to logout user and, closes the connection to the server.\n"""]
        return "".join(commands_list)

    def quit(self):
        """This method is used to logout the user and close the connection. 
        Returns : str
            returns a message stating the action performed."""
        if self.login_status is not True:
            return ""
        with open("logfile.txt","r+") as file:
            lines = file.readlines()
            file.close()
            for line in lines:
                if line == self.username+"\n":
                    lines.remove(line)
                    os.remove("logfile.txt")
            file = open("logfile.txt","w")
            for i in lines:
                file.write(i)
        self.login_status = False
        self.username = ""
        return "\nSuccessfully logged out\n"