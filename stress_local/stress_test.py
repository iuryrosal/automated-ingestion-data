import pandas as pd
from threading import Thread


def build_big_csv(file):
    print(f'Starting the task {file}...')
    pd_series = pd.Series(dtype='str')
    trips_big_dataset = pd.DataFrame({'region': pd_series,
                                      'origin_coord': pd_series,
                                      'destination_coord': pd_series,
                                      'datetime': pd_series,
                                      'datasource': pd_series})
    trips = pd.read_csv("trips_big_dataset.csv")
    count = 10
    while count > 0:
        trips_big_dataset = pd.concat([trips_big_dataset, trips], axis=0)
        count -= 1
        print(f'Work in the task {file}: count ({count})')
    print(f'Work in the task {file}: writing csv')
    trips_big_dataset.to_csv(f"data/stress_test/trips_big_dataset_{file}.csv",
                             chunksize=100000, index=False)
    print(f'The task {file} completed')


threads = []
for n in range(1, 11):
    t = Thread(target=build_big_csv, args=(n,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
