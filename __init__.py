from bursamy.download import BursaFileDownloader
import time

start_time = time.time()
BursaFileDownloader("0208").get_financial_result()
print("--- %s seconds ---" % (time.time() - start_time))

