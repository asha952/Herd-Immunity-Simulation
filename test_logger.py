from logger import Logger

def test_contructor():
    log = Logger("log_test.txt")

    assert log.file_name == "log_test.txt"


def test_metadata():
    log = Logger(100, 0.8, "Ebloa", 0.3,
                       0.3)

    assert log.write_metadata("100 0.8 Ebloa   0.3 0.3")