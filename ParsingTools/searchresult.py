import json
from ParsingTools.config import DIV_CLASS


class SearchResult:
    def __init__(self, respondent_id, result_type, is_sponsored, website_name = None, website_breadcrumb = None, page_title = None,
                 page_description = None, page_url = None, sublinks = None, ad_seller_rating = None, index = None):
        self.respondent_id = respondent_id
        self.result_type = result_type
        self.is_sponsored = is_sponsored

        self.website_name = website_name
        self.website_breadcrumb = website_breadcrumb

        self.page_title = page_title
        self.page_description = page_description
        self.page_url = page_url

        self.sublinks = sublinks

        self.ad_seller_rating = ad_seller_rating

        self.index = index

    def get_dict(self):
        result_dict = {
            "respondent_id": self.respondent_id,
            "index": self.index,
            "result_type": self.result_type,
            "is_sponsored": self.is_sponsored,
            "website_name": self.website_name,
            "website_breadcrumb": self.website_breadcrumb,
            "page_title": self.page_title,
            "page_description": self.page_description,
            "page_url": self.page_url,
            "ad_seller_rating": self.ad_seller_rating
        }
        if self.sublinks is not None:
            for i, sublink in enumerate(self.sublinks):
                for key, value in sublink.items():
                    result_dict[f"sublink_{i}_{key}"] = value
        return result_dict

    def set_index(self, index):
        self.index = index

    def __str__(self):
        return json.dumps(self.get_dict(), indent=4)



class SearchResultPage:
    def __init__(self, respondent_id):
        self.respondent_id = respondent_id
        self.search_results = []
        self.all_fields = []
        self.page_position = 0

    def add_search_result(self, search_result: SearchResult, merge = False):
        if not merge:
            search_result.set_index(self.page_position)
            self.page_position += 1
        for key in [key for key in search_result.get_dict().keys() if key not in self.all_fields]:
            self.all_fields.append(key)
        self.search_results.append(search_result)


    def get_dict(self):
        results_all_fields = []
        for search_result_dict in [search_result.get_dict() for search_result in self.search_results]:
            for key in list(filter(lambda x: x not in search_result_dict.keys(), self.all_fields)):
                search_result_dict[key] = None
            results_all_fields.append(search_result_dict)
        return results_all_fields

    def __str__(self):
        return json.dumps(self.get_dict(), indent=4)

    @staticmethod
    def merge_search_result_pages(search_result_pages):
        merged_search_result_pages = SearchResultPage("merge")
        for search_result_page in search_result_pages:
            for search_result in search_result_page.search_results:
                merged_search_result_pages.add_search_result(search_result, merge=True)
        return merged_search_result_pages
