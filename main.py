import os
import csv
import lxml
import json
import pandas as pd
from ParsingTools import SearchResult, SearchResultPage, result_page_parser


def main():
    file_directory = "google_upload"
    results_dict = []
    for file_address in os.listdir(file_directory):
        # file_address = "R_1Du16vlds8y3Yb5_work from home jobs - Google Search.html"
        file_extension = file_address.split(".")[-1]
        if file_extension in ["html", "htm", "webarchive"]:  # , "mhtml", "mht"]:
            try:
                results = result_page_parser(f"{file_directory}/{file_address}", file_address.split("_")[1])
                results_dict.append(results)
                # print(results)

            except Exception as e:
                print(file_address)
                print(e)
                print("*******************************")
    merged_results = SearchResultPage.merge_search_result_pages(results_dict)
    with open(f"results/all_results.csv", "w", newline="") as f_csv:
        w = csv.DictWriter(f_csv, fieldnames=merged_results.all_fields)
        w.writeheader()
        w.writerows(merged_results.get_dict())


if __name__ == "__main__":
    main()
