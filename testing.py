"""This file is used to test the functionalities of client server application."""
import unittest
import shutil
import sys
import os
from services import Services

class Test(unittest.TestCase):
    """It consists of all the tests that are to be performed to check the functionality of application."""
    def test_login(self):
        """It is performed to check whether login command log in the user or not."""
        obj = Services()
        username = "testuser1"
        password = "test1"
        obj.register(username,password)
        expected = '\nLogged in testuser1\n'
        resulted = obj.login(username,password)
        self.assertEqual(expected,resulted)
        obj.quit()

    def test_wrong_password(self):
        """It is performed to check whether login command warns user or not when incorrect password is given."""
        obj = Services()
        obj.register("testuser2","test2")
        obj.login("testuser2","wrng")
        expected = "\nIncorrect password entered\n"
        resulted = obj.login("testuser2","wrng")
        self.assertEqual(expected,resulted)

    def test_unregistered(self):
        """It is performed to check whether login command tells user to register when incorrect credentials were entered."""
        obj = Services()
        expected = "\nUser doesn't exist\nPlease register to continue....\n"
        resulted = obj.login("hiiiii","hello")
        self.assertEqual(expected,resulted)

    def test_register(self):
        """It is performed to check whether register command registers in the user or not."""
        obj = Services()
        resulted = obj.register("testuser3","test3")
        expected = '\nRegistered testuser3\nYou can login using login command\n'
        self.assertEqual(expected,resulted)

    def test_exist(self):
        """It is performed to check whether register command tells user it's already registered when already used credentials entered."""
        obj = Services()
        expected = "\nExisting user\nPlease login\n"
        obj.register("testexist","teste")
        resulted = obj.register("testexist","teste")
        self.assertEqual(expected,resulted)

    def test_write_file(self):
        """It is performed to check whether write_file command creates a file and writes data into it."""
        obj = Services()
        obj.register("testuser4","test4")
        obj.login("testuser4","test4")
        resulted = obj.write_file("welcome.txt","welcome")
        expected = "\nCreated file with name welcome.txt and written data into it.\n"
        self.assertEqual(expected,resulted)
        obj.quit()

    def test_create_file(self):
        """It is performed to check whether write_file command creates empty file when no content is given."""
        obj = Services()
        obj.register("testuser5","test5")
        obj.login("testuser5","test5")
        resulted = obj.write_file("hi.txt")
        expected = "File created with name hi.txt\n"
        self.assertEqual(expected,resulted)
        obj.quit()

    def test_clear_file(self):
        """It is performed to check whether write_file command clears the file when no content is given."""
        obj = Services()
        obj.register("testuser6","test6")
        obj.login("testuser6","test6")
        expected = "\nFile cleared\n"
        obj.write_file("welcome.txt","welcome")
        resulted = obj.write_file("welcome.txt")
        self.assertEqual(expected,resulted)
        obj.quit()

    def test_create_folder(self):
        """It is performed to check whether create_folder command creates a folder or not."""
        obj = Services()
        obj.register("testuser7","test7")
        obj.login("testuser7","test7")
        resulted = obj.create_folder("Important")
        expected = "\nFolder created with name Important\n"
        self.assertEqual(expected,resulted)
        obj.quit()
    def test_existing_folder(self):
        """It is performed to check whether create_folder command tells user that given folder name already exists."""
        obj = Services()
        obj.register("testuser8","test8")
        obj.login("testuser8","test8")
        obj.create_folder("Important")
        resulted = obj.create_folder("Important")
        expected = "\nFolder already exists with name Important\n"
        self.assertEqual(expected,resulted)
        obj.quit()

    def test_change_folder(self):
        """It is performed to check whether change_folder command moves the working directory to given folder."""
        obj = Services()
        obj.register("testuser9","test9")
        obj.login("testuser9","test9")
        obj.create_folder("Important")
        expected = "\nMoved current working directory to folder Important\n"
        resulted = obj.change_folder("Important")
        self.assertEqual(expected,resulted)
        obj.quit()

    def test_quit(self):
        """It is performed to check whether quit command logs out the user or not."""
        obj = Services()
        obj.register("testuser10","test10")
        obj.login("testuser10","test10")
        expected = "\nSuccessfully logged out\n"
        resulted = obj.quit()
        self.assertEqual(expected,resulted)
    
    def test_without_login(self):
        """It is performed to check whether commands are denied when user not logged in."""
        obj = Services()
        expected = "\nPlease login to continue.....\n"
        resulted = obj.create_folder("fldr1")
        self.assertEqual(expected,resulted)

def remove():
    """removes all the credentials and directories created while testing."""
    path = os.path.join(os.getcwd(),"Root")
    shutil.rmtree(os.path.join(path,"testexist"))
    shutil.rmtree(os.path.join(path,"testuser1"))
    shutil.rmtree(os.path.join(path,"testuser2"))
    shutil.rmtree(os.path.join(path,"testuser3"))
    shutil.rmtree(os.path.join(path,"testuser4"))
    shutil.rmtree(os.path.join(path,"testuser5"))
    shutil.rmtree(os.path.join(path,"testuser6"))
    shutil.rmtree(os.path.join(path,"testuser7"))
    shutil.rmtree(os.path.join(path,"testuser8"))
    shutil.rmtree(os.path.join(path,"testuser9"))
    shutil.rmtree(os.path.join(path,"testuser10"))
    obj = Services()
    obj.write_file("user_credentials.txt")

def perform_tests(tests):
    """Loads all the tests and performs."""
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTests(test_loader.loadTestsFromTestCase(tests))
    perform_test = unittest.TextTestRunner(verbosity=2)
    outcome = perform_test.run(test_suite)
    if outcome.skipped:
        return False
    return outcome.wasSuccessful()

def init_testing():
    """initialises and performs testing."""
    return perform_tests(Test)

if __name__ == "__main__":
    with open("user_credentials.txt","r") as file:
        data = file.readlines()
    file.close()
    if not init_testing:
        print("\nFailed")
        remove()
        sys.exit(1)
    print(init_testing())
    remove()
    with open("user_credentials.txt","w") as file2:
        for line in data:
            file2.write(line)
    sys.exit()


