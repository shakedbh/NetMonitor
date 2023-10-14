from sys import exit
from Monitor import Monitor


def main():
    try:
        mon = Monitor()
        mon.run()
    except Exception as e:
        print(e)
        exit()


if __name__ == "__main__":
    main()
