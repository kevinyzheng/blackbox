import os
from bs4 import BeautifulSoup
from quopri import decodestring
from ParsingTools.config import ROOT_DIR, DIV_CLASS
from ParsingTools.searchresult import SearchResult, SearchResultPage


def result_page_parser(file_address: str, respondent_id: str):
    with open(os.path.join(ROOT_DIR, file_address), 'r') as file:
        if file_address.endswith(".mhtml") or file_address.endswith(".mht"):
            # content = decodestring(file.read()).decode()
            # soup = BeautifulSoup(file, 'lxml')
            # print(soup.text)
            pass
        else:
            soup = BeautifulSoup(file, "html.parser")
    try:
        center_col_divs = soup.find_all("div", {"class": "GyAeWb"})[0].find_all("div", {"class": "s6JM6d"})
        center_col_div = center_col_divs[0]
    except IndexError as e:
        raise Exception(f"Found {len(center_col_divs)} main divs in {file_address}")

    search_result_page = SearchResultPage(respondent_id)

    for div in center_col_div.find_all("div", recursive=True):
        try:
            div.get("class")
        except AttributeError as e:
            continue

        if div is not None and div.get("class") is not None:
            class_string = " ".join(list(div.get("class")))

            if class_string in ["uEierd", "MjjYud"]:
                search_result = result_item_parser_helper(respondent_id, div, class_string)
                if search_result is not None:
                    search_result_page.add_search_result(search_result)
                center_col_div.find_all("div", {"class": class_string})[0].decompose()

    return search_result_page


def result_item_parser_helper(respondent_id, item_element, class_string: str = None):
    if class_string is None:
        class_string = " ".join(list(item_element.get("class")))

    if class_string == "uEierd":  # ads
        return ad_item_parser(respondent_id, item_element)
    elif class_string == "MjjYud":  # results
        return
        # return result_item_parser(respondent_id, item_element)
    else:
        raise Exception(f"item element with class string {class_string} not parseable")


def ad_item_parser(respondent_id, item_element):
    elements = item_element.find_all("div", {"class": DIV_CLASS["ad_block"]})
    if len(elements) == 1:
        website_name, website_breadcrumb, page_title, page_url, sublinks, page_description, ad_seller_rating = None, None, None, None, None, None, None
        ad_block_element = elements[0]
        heading_elements = ad_block_element.find_all("div", {"class": DIV_CLASS["ad_block_heading"]})
        if len(heading_elements) == 1:
            heading_element = heading_elements[0]
            page_title_block = heading_element.find("a", {"class": DIV_CLASS["ad_block_page_title"]})
            page_title = page_title_block.find("div", {"role": "heading"}).text
            page_url = page_title_block.get("href")

            website_elements = heading_element.find_all("span", {"class": DIV_CLASS["ad_block_heading_website"]})
            if len(website_elements) > 0:
                website_name = website_elements[0].find("span", {"class": DIV_CLASS["ad_block_heading_website_name"]}).text
                website_breadcrumb = website_elements[0].find("span", {"class": DIV_CLASS["ad_block_heading_website_breadcrumb"]}).text

        sublink_elements = ad_block_element.find_all("div", {"class": DIV_CLASS["ad_block_sublinks"]})
        if len(sublink_elements) == 1:
            sublinks = []
            for sublink_element in sublink_elements[0].find_all("a"):
                sublinks.append({
                    "title": sublink_element.text,
                    "url": sublink_element.get("href")
                })
        elif len(sublink_elements) == 0:
            deeplink_elements = ad_block_element.find_all("div", {"class": DIV_CLASS["ad_block_deeplinks"]})
            if len(deeplink_elements) == 1:
                sublinks = []
                for deeplink_element in deeplink_elements[0].find_all("div", {"class": DIV_CLASS["ad_block_deeplink_element"]}):
                    sublinks.append({
                        "title": deeplink_element.find("a").text,
                        "url": deeplink_element.find("a").get("href"),
                        "description": deeplink_element.find("div", {"class": DIV_CLASS["ad_block_deeplink_element_description"]}).text
                    })

        detailed_sublink_elements = ad_block_element.find_all("div", {"class": DIV_CLASS["ad_block_detailed_sublink"]})
        if len(detailed_sublink_elements) > 0:
            if sublinks is None:
                sublinks = []
            for detailed_sublink_element in detailed_sublink_elements:
                sublinks.append({
                    "title": detailed_sublink_element.find("a").text,
                    "url": detailed_sublink_element.find("a").get("href"),
                    "description": detailed_sublink_element.text
                })

        description_elements = ad_block_element.find_all("div", {"class": DIV_CLASS["ad_description"]})
        if len(description_elements) == 1:
            page_description = description_elements[0].text

        ad_seller_rating_elements = ad_block_element.find_all("w-ad-seller-rating")
        if len(ad_seller_rating_elements) == 1:
            ad_seller_rating = ad_seller_rating_elements[0].text

        return SearchResult(respondent_id=respondent_id, result_type="ad_block", is_sponsored=True, website_name=website_name,
                            website_breadcrumb=website_breadcrumb, page_title=page_title, page_url=page_url,
                            sublinks=sublinks, page_description=page_description, ad_seller_rating=ad_seller_rating)
    else:
        raise Exception(f"Found {len(elements)} ad blocks")


def organic_result_parser(item_element):
    website_name, website_breadcrumb, page_title, page_description, page_url, sublinks = None, None, None, None, None, None


    return {
        "website_name": website_name,
        "website_breadcrumb": website_breadcrumb,
        "page_title": page_title,
        "page_description": page_description,
        "page_url": page_url,
    }


def result_item_parser(respondent_id, item_element):
    elements = item_element.find_all("div", {"data-hveid": DIV_CLASS["organic_result"]})
    # if len(elements) == 1:


    return

        #     center_col_div.find({"class": DIV_CLASS["ad_block"]}).decompose()
        #     div.decompose()
        # elif div.get("class") == DIV_CLASS["job_box"]:
        #     print(div.text)
        #     div.decompose()
        # elif div.get("class") == DIV_CLASS["people_also_ask"]:
        #     print(div.text)
        #     div.decompose()
        # elif div.get("class") == DIV_CLASS["custom_search"]:
        #     print(div.text)
        #     div.decompose()
        # elif div.get("class") == DIV_CLASS["search_result"]:
        #     print(div.text)
        #     div.decompose()
        # else:
        #     pass


        # print(div.get("class"))



    # center_column_soup = soup.select('div[id="center_col"]')
    # if len(center_column_soup) != 1:
    #     print(f"{len(center_column_soup)} {file_address}")
    # else:
    #     job_box = center_column_soup[0].select(DIV_CLASS["job_box"])
    #     if len(job_box) != 1:
    #         print(f"{len(job_box)} job box elements in {file_address}")
    #
    #     top_ads = center_column_soup[0].select(DIV_CLASS['top_ads'])
    #     if len(top_ads) != 1:
    #         print(f"{len(top_ads)} top_ads elements in {file_address}")
    #     else:
    #         top_ad_elements = top_ads[0].select('div[class="uEierd"]')
    #         # print(f"{len(top_ad_elements)} ad results in {file_address}")
    #         for top_ad_element in top_ad_elements:
    #             if top_ad_element.text not in center_column_soup[0].text:
    #                 print(False)
    #                 print(f"{len(top_ad_elements)} ad results in {file_address}")
        # else:
        #     print(job_box[0].text)
    #     print(center_column_soup[0].text)
    return


