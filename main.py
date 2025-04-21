# main.py
import multiprocessing
import bot1
import bot2
import bot3
import bot4

if __name__ == "__main__":
    processes = [
        multiprocessing.Process(target=bot1.run),
        multiprocessing.Process(target=bot2.run),
        multiprocessing.Process(target=bot3.run),
        multiprocessing.Process(target=bot4.run),
    ]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
