import random
import resource
import threading
import time

import requests
session = requests.session()

########### CONFIGURE INPUTS HERE #####################################################
CIO_NAME = '<CIO_NAME>'                                        ### THIS IS THE CIO USED
FILTER_COLUMN = '<CIO_COLUMN>'           ### THIS IS A COLUMN WHERE A FILTER IS APPLIED
THREAD_COUNT = 10                             ### HOW MANY PARALLEL REQUESTS TO BE MADE
REQUEST_COUNT_PER_THREAD = 1                ### HOW MANY REQUESTS TO BE MADE PER THREAD
INSTANCE_URL = '<OFFCORE URL>'
TOKEN = '<OFFCORE TOKEN>'
#######################################################################################


def executeInsightsQuery(count=0):
    while count > 0:
        try:
            loop_start_time = time.time()
            token, instance_url = TOKEN, INSTANCE_URL
            fetched_token = time.time() - loop_start_time
            http_start_time = time.time()
            url = f'https://{instance_url}/api/v1/insight/calculated-insights/{CIO_NAME}?filters=[{FILTER_COLUMN}=' + str(
                time.time() * 1000) + str(random.random()) + ']'
            headers = {'Authorization': f'Bearer {token}',
                       'Content-Type': 'application/json',
                       'Accept-Encoding': 'gzip'}
            response = session.get(url=url, headers=headers)
        except Exception as e:
            print(e)
        finally:
            request_time = time.time() - http_start_time
            end = time.time()
            print("%s,%s,%s,%f,%s,%f,%f\n" % (
                response.headers.get("x-trace-id"), time.strftime("%b %d %Y %H:%M:%S", time.localtime(loop_start_time)),
                time.strftime("%b %d %Y %H:%M:%S", time.localtime(end)), (end - loop_start_time),
                str(response.status_code),
                fetched_token, request_time))
            count = count - 1


_, hard = resource.getrlimit(resource.RLIMIT_NPROC)
resource.setrlimit(resource.RLIMIT_NPROC, (1, hard))


def parent():
    start = time.time()
    threads = THREAD_COUNT
    count = REQUEST_COUNT_PER_THREAD
    print(f'No of thread {threads}')
    print(f'Requests per thread {count}')
    timeInSeconds = 60 * 60
    thread_list = []
    while threads > 0:
        thread = threading.Thread(target=executeInsightsQuery, args=(count,))
        thread_list.append(thread)
        thread.start()
        threads = threads - 1

    for thread in thread_list:
        thread.join()

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    parent()
