from .db_loader import main as load_database
from .validator import main as validate
from .audit import audit


def run():

    load_database()

    validate()

    audit()

    print("\nETL Completed Successfully")


if __name__ == "__main__":
    run()
