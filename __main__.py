from multiprocessing import Process
from core.beat import Beat
from core.worker import Worker

if __name__ == '__main__':
    beat = Beat()
    beat_process = Process(target=beat.run)
    beat_process.start()

    worker = Worker()
    worker_process = Process(target=worker.run)
    worker_process.start()

    beat_process.join()
    worker_process.join()