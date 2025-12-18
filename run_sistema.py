from multiprocessing import Process
from main_pantalla import main as pantalla_main
from main_control import main as control_main

if __name__ == "__main__":
    p1 = Process(target=pantalla_main)
    p2 = Process(target=control_main)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
