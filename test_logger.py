from logger import Logger
import os
from person import Person

def test_contructor():
    log = Logger("log_test.txt")

    assert log.file_name == "log_test.txt"


def test_metadata():
    log = Logger("test.txt")
    log.write_metadata(1000, 0.90, "Ebola", 0.70, 0.25)

    with open("test.txt", "r") as f:
        test_content = f.read()

    assert test_content == f"Pop_size: 1000\t Vacc_Percentage: 0.9\tVirus Name: Ebola\tMortality Rate: 0.7\t Reproductive Rate: 0.25\n"

    os.remove("test.txt")

def test_log_infection_survial():
    log = Logger("test2.txt")
    person1 = Person(1, True)

    log.log_infection_survival(person1, True)


    with open("test2.txt", "r") as f:
        test_content = f.readlines()

    assert test_content[0] == ("Person ID: 1 died from infection\n")

    os.remove("test2.txt")
                

