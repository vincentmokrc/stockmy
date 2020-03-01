from bursamy.table import GetTable
import time
from bursamy.file import GetPdf


start_time = time.time()
content_df = GetTable("6633").financial_result()
print(type(content_df.iloc[[0]]))

GetPdf().download_all_pdf(content_df)
print("--- %s seconds ---" % (time.time() - start_time))

