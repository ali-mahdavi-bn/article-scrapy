from multiprocessing import Pool

from articles.domain.mapper import start_mapper as article_mapper
from articles.workers import workers as article_workers
from backbone.infrastructure.log._logger import Logger

article_mapper()


def worker_function(worker):
    try:
        Logger.info(f"start worker {worker.__name__}")
        return worker()
    except Exception as e:
        Logger.error(e)


if __name__ == '__main__':
    workers = [*article_workers]

    with Pool(len(workers)) as p:
        results = p.map(worker_function, workers)

