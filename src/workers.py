from multiprocessing import Pool

from articles.domain.mapper import start_mapper as article_mapper
from articles.workers import workers as article_workers

article_mapper()


def worker_function(worker):
    try:
        return worker()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    workers = [*article_workers]

    with Pool(len(workers)) as p:
        results = p.map(worker_function, workers)

