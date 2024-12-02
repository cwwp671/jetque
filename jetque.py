# jetque.py
import logging
import sys
from jetque.jetque import JetQue

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

    app = JetQue(sys.argv)
    app.run()
