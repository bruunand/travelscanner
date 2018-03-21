from concurrent.futures import ThreadPoolExecutor


def crawl_multi_threaded(crawl_function, start_page, max_workers=5):
    ret_travels = set()
    current_page = start_page

    while True:
        workers = []
        initial_length = len(ret_travels)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(0, max_workers):
                workers.append(executor.submit(crawl_function, current_page))
                current_page = current_page + 1

        # Check if any of the travel sets were empty
        # Also add return travels
        had_empty_travels = False
        for i in range(0, max_workers):
            worker_travels = workers[i].result()

            # Skip none-values
            if worker_travels is None:
                continue

            # Check if there were travels from this worker
            # Also check if the intersection of existing travels is equal in length with the new travels
            if len(worker_travels) == 0 or len(ret_travels.intersection(worker_travels)) == len(worker_travels):
                had_empty_travels = True
            else:
                ret_travels.update(worker_travels)

        # Break the loop if empty travel sets were found
        if had_empty_travels:
            break

    return ret_travels
