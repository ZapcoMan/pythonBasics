import json

import requests

cookies = {
    'stockx_device_id': '9259aa4e-6453-4641-9e4a-34bccc918d5a',
    'stockx_session_id': 'b91f667a-ed0a-404d-aec3-1fa916766aab',
    'stockx_session': 'e56b7d01-9e91-439d-9ecb-5f3ee386779c',
    'language_code': 'en',
    'stockx_selected_region': 'CN',
    'chakra-ui-color-mode': 'light',
    'pxcts': '50a31aab-c1c1-11ef-be68-f41e1a29a953',
    '_pxvid': '50a31078-c1c1-11ef-be68-11903af4ea7a',
    'cf_clearance': 'vtC_qeuJhf9cfw8Ge4PIdktIkN3BL4uCnN8k0vhIO74-1735022152-1.2.1.1-oWePI3KH1aQrDZVfwpTeXJjumNzupjpG1OOT.2mYISewxv.yYK8EELvGp.Qq46h7YpneA7Pp_qGRPOoWqZU4mKndRq94VGSEJGYtwGICNKpAGkdaFbEpGXUkh8tTJnf5GMxdk.3wiW0rsd3n9aw_DHVwLxRpkKgWOtYXgVHxOzwlPVjJp9VFAWvWwkOBcV7PZl6g_08no7QjuF09iJ4gtpahlQqU4HlVZUw0wqeAR9hMd2f77h1R.NT5iEk8yYROb5qEJdZuqfyRLsLt7nNu9kfDRk5LCLWeEmngvrrpjQ6W4YTte5dnsruo866lSDqLhf92x9KuMDt6aoQf8s3k76ztBBpQZWkGYUxMXMdRq5cEf1Y_LuRtJ081cjB1s5VjYMgSNhJC3ip1zcn0oxtHHw',
    'stockx_dismiss_modal': 'true',
    'stockx_dismiss_modal_set': '2024-12-24T06%3A35%3A53.754Z',
    'stockx_dismiss_modal_expiration': '2025-12-24T06%3A35%3A53.754Z',
    'display_location_selector': 'false',
    'rskxRunCookie': '0',
    'rCookie': 'orbg0pxfugctqpr1vkhjem523e661',
    '__gads': 'ID=2edfa2703590fd8f:T=1735022156:RT=1735022156:S=ALNI_MbV8oZkQAjcdN90XNeocGSekRvy_Q',
    '__gpi': 'UID=00000fb54795628e:T=1735022156:RT=1735022156:S=ALNI_MYPef-uwxBG0a7G039fTLMj7izzkg',
    '__eoi': 'ID=5f04583e080b5f3a:T=1735022156:RT=1735022156:S=AA-AfjbqeDVZSg6zdiMaCO0d1DFf',
    '_cc_id': 'd92acd57848364413d2fc22d2b9002ad',
    'panoramaId_expiry': '1735626966627',
    'panoramaId': '68b6356dabef84b2a6f63d9c9a74185ca02c06845c6f442751270271008cc8d3',
    'panoramaIdType': 'panoDevice',
    'cto_bundle': 'IFg94V9HSWpveDdNUSUyRllqWUlCYUZRYmNMZTB3ZTY3anpoTGI4UkNhNmgxdWJlQ3NwcXFMUXBaVXd6RUVSeVk4U2wxQ2FGdENxQjkyM3RqNlhiNjRWcXdhTmUwdGtmRzVTb0V0UDBNOUNlakRxM3hheG1xa3B1UjhnamdLUkR3T01OaEVXNG5YWmFvMSUyQlZmSWtZUDFzVngyZk5BJTNEJTNE',
    'lastRskxRun': '1735022190363',
    '_px3': 'e097d8a84daeb7e43bbccf07c57a9b800c8bcdf013999adfa857453b986fcc74:MxZTkZwc2OnDnwEb9Zxzy6u8LTpxQO2WNaSITS2pYFkLG45dE3cMpdp/P422W3zsE9Z6Ou/VfIuMZuuy87Udnw==:1000:0hk6WCIQXEIWOVgFwDA71TJCcAdQNYXTdMIkiUVF0a0iMa6kN7GxhFhkbRTvAGwDfz31vGkvLnnDC4gtKxfLVejcv5fWW+5Yx5Qt3t068XYgJ1n3D+n/opdhAvr9BNl8ltIpgSehxB5i/8tq0Ooyhe8dlcxwNE8rMYEN9j+ZZ0YWlgAOj0YDQShoDhJVIObr0uTz7tWxLl389YYi5xGwTVhCbb+W0d0ZXhMaj2eAbbCQDk66K9xfCN9sOUO0wJ0Q',
    '_pxde': '2c4293115574c98558c940491bc26a8d1b058de6af5a4daee8c42b7fb555d021:eyJ0aW1lc3RhbXAiOjE3MzUwMjIzMTQwNTQsImZfa2IiOjB9',
    'is_gdpr': 'false',
    'stockx_ip_region': 'CN',
    '_dd_s': 'rum=0&expire=1735023214360&logs=1&id=04f244f5-ed86-4114-a0fc-420df8fe7075&created=1735022149989',
    '_pxhd': 'grFFHCUXClJZOD1eqFxq79OIqH05u5p7yLS18s-A7M75cxIKXcAjd5i-ptaKrfxy9nZBxd3sA0lOtgRBs2SYYg==:rbpnSTfZZwfVX1GVDJ/ZQJ9-k1198QTMapHjFKeNQ-LpG8YSs/mmgPSLaolh9hEKCcP9nZb87y1q36NxpgdqY4syieZlMztR6qf-4OQuwoiLZHluFsWksbW/sSFCVnxFphfhiacKhRzFC5zvXHPfwA==',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US',
    'apollographql-client-name': 'Iron',
    'apollographql-client-version': '2024.12.15.01',
    'app-platform': 'Iron',
    'app-version': '2024.12.15.01',
    'content-type': 'application/json',
    # 'cookie': 'stockx_device_id=9259aa4e-6453-4641-9e4a-34bccc918d5a; stockx_session_id=b91f667a-ed0a-404d-aec3-1fa916766aab; stockx_session=e56b7d01-9e91-439d-9ecb-5f3ee386779c; language_code=en; stockx_selected_region=CN; chakra-ui-color-mode=light; pxcts=50a31aab-c1c1-11ef-be68-f41e1a29a953; _pxvid=50a31078-c1c1-11ef-be68-11903af4ea7a; cf_clearance=vtC_qeuJhf9cfw8Ge4PIdktIkN3BL4uCnN8k0vhIO74-1735022152-1.2.1.1-oWePI3KH1aQrDZVfwpTeXJjumNzupjpG1OOT.2mYISewxv.yYK8EELvGp.Qq46h7YpneA7Pp_qGRPOoWqZU4mKndRq94VGSEJGYtwGICNKpAGkdaFbEpGXUkh8tTJnf5GMxdk.3wiW0rsd3n9aw_DHVwLxRpkKgWOtYXgVHxOzwlPVjJp9VFAWvWwkOBcV7PZl6g_08no7QjuF09iJ4gtpahlQqU4HlVZUw0wqeAR9hMd2f77h1R.NT5iEk8yYROb5qEJdZuqfyRLsLt7nNu9kfDRk5LCLWeEmngvrrpjQ6W4YTte5dnsruo866lSDqLhf92x9KuMDt6aoQf8s3k76ztBBpQZWkGYUxMXMdRq5cEf1Y_LuRtJ081cjB1s5VjYMgSNhJC3ip1zcn0oxtHHw; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2024-12-24T06%3A35%3A53.754Z; stockx_dismiss_modal_expiration=2025-12-24T06%3A35%3A53.754Z; display_location_selector=false; rskxRunCookie=0; rCookie=orbg0pxfugctqpr1vkhjem523e661; __gads=ID=2edfa2703590fd8f:T=1735022156:RT=1735022156:S=ALNI_MbV8oZkQAjcdN90XNeocGSekRvy_Q; __gpi=UID=00000fb54795628e:T=1735022156:RT=1735022156:S=ALNI_MYPef-uwxBG0a7G039fTLMj7izzkg; __eoi=ID=5f04583e080b5f3a:T=1735022156:RT=1735022156:S=AA-AfjbqeDVZSg6zdiMaCO0d1DFf; _cc_id=d92acd57848364413d2fc22d2b9002ad; panoramaId_expiry=1735626966627; panoramaId=68b6356dabef84b2a6f63d9c9a74185ca02c06845c6f442751270271008cc8d3; panoramaIdType=panoDevice; cto_bundle=IFg94V9HSWpveDdNUSUyRllqWUlCYUZRYmNMZTB3ZTY3anpoTGI4UkNhNmgxdWJlQ3NwcXFMUXBaVXd6RUVSeVk4U2wxQ2FGdENxQjkyM3RqNlhiNjRWcXdhTmUwdGtmRzVTb0V0UDBNOUNlakRxM3hheG1xa3B1UjhnamdLUkR3T01OaEVXNG5YWmFvMSUyQlZmSWtZUDFzVngyZk5BJTNEJTNE; lastRskxRun=1735022190363; _px3=e097d8a84daeb7e43bbccf07c57a9b800c8bcdf013999adfa857453b986fcc74:MxZTkZwc2OnDnwEb9Zxzy6u8LTpxQO2WNaSITS2pYFkLG45dE3cMpdp/P422W3zsE9Z6Ou/VfIuMZuuy87Udnw==:1000:0hk6WCIQXEIWOVgFwDA71TJCcAdQNYXTdMIkiUVF0a0iMa6kN7GxhFhkbRTvAGwDfz31vGkvLnnDC4gtKxfLVejcv5fWW+5Yx5Qt3t068XYgJ1n3D+n/opdhAvr9BNl8ltIpgSehxB5i/8tq0Ooyhe8dlcxwNE8rMYEN9j+ZZ0YWlgAOj0YDQShoDhJVIObr0uTz7tWxLl389YYi5xGwTVhCbb+W0d0ZXhMaj2eAbbCQDk66K9xfCN9sOUO0wJ0Q; _pxde=2c4293115574c98558c940491bc26a8d1b058de6af5a4daee8c42b7fb555d021:eyJ0aW1lc3RhbXAiOjE3MzUwMjIzMTQwNTQsImZfa2IiOjB9; is_gdpr=false; stockx_ip_region=CN; _dd_s=rum=0&expire=1735023214360&logs=1&id=04f244f5-ed86-4114-a0fc-420df8fe7075&created=1735022149989; _pxhd=grFFHCUXClJZOD1eqFxq79OIqH05u5p7yLS18s-A7M75cxIKXcAjd5i-ptaKrfxy9nZBxd3sA0lOtgRBs2SYYg==:rbpnSTfZZwfVX1GVDJ/ZQJ9-k1198QTMapHjFKeNQ-LpG8YSs/mmgPSLaolh9hEKCcP9nZb87y1q36NxpgdqY4syieZlMztR6qf-4OQuwoiLZHluFsWksbW/sSFCVnxFphfhiacKhRzFC5zvXHPfwA==',
    'origin': 'https://stockx.com',
    'priority': 'u=1, i',
    'referer': 'https://stockx.com/',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'selected-country': 'CN',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-abtest-ids': 'ab_0xdjj_web.true,ab_12dul_all.neither,ab_1ncl6_web.true,ab_2ki60_web.neither,ab_2lofw_web.true,ab_2m3ew_web.true,ab_3opqo_web.true,ab_3qc6g_web.neither,ab_5wzq0_web.true,ab_82d7l_web.neither1,ab_8dhfg_web.neither,ab_8ht34_web.true,ab_8stea_web.neither,ab_8x8am_web.true,ab_8zx87_web.true,ab_90n02_web.true,ab_9v8xl_web.variant,ab_9zi8a_web.true,ab_aa_continuous_all.web_a,ab_account_selling_guidance_web.variant,ab_aoxjj_web.true,ab_ayu9e_web.true,ab_checkout_buying_table_redesign_web.variant,ab_checkout_cutoff_date_web.variant,ab_chk_place_order_verbage_web.true,ab_cs_seller_shipping_extension_web.variant,ab_discovery_color_filter_all.false,ab_drc_chk_sell_intra_zone_all_in_support_web.variant,ab_ebguu_web.true,ab_efoch_web.true,ab_ekirh_web.variant_2,ab_enable_3_CTAs_web.variant,ab_epnox_web.true,ab_eqctr_web.true,ab_eu3zm_web.neither,ab_gift_cards_v1_web.true,ab_growth_appsflyer_smart_banner_web.variant_2,ab_growth_ignore_rv_products_in_rfy_v2_web.true,ab_hex3z_web.true,ab_home_as_seen_on_instagram_v2_web.true,ab_home_carousel_current_asks_bids_web.true,ab_home_page_reordering_web.variant_1,ab_home_show_value_props_web.variant_2,ab_hsaxr_web.true,ab_hzpar_all.neither,ab_i9gt9_web.true,ab_k358k_web.neither,ab_k3z78_web.true,ab_kvcr0_web.true,ab_ljut9_web.true,ab_merchandising_module_pdp_v2_web.variant,ab_mh0wn_web.neither,ab_n0kpl_web.neither,ab_n87do_web.neither,ab_ncs63_web.true,ab_nz3j1_web.true,ab_o95do_web.neither,ab_og9wl_web.true,ab_phx04_web.true,ab_pirate_most_popular_around_you_module_web.neither,ab_pirate_product_cell_favorite_web_v1.true,ab_q2nhm_web.true,ab_q704p_web.true,ab_r84zi_web.variant,ab_sa2jv_web.0,ab_search_static_ranking_v5_web.variant,ab_sx1wr_web.neither,ab_u13ie_web.true,ab_uaa6m_web.true,ab_ubnt3_web.neither,ab_vhfbq_web.neither,ab_w2cvj_web.true,ab_web_aa_continuous.false,ab_xbqne_web.true,ab_xr2kh_web.variant1,ab_y8s2m_web.neither2,ab_z25fu_web.true',
    'x-operation-name': 'FetchProductCollection',
    'x-stockx-device-id': '9259aa4e-6453-4641-9e4a-34bccc918d5a',
    'x-stockx-session-id': 'b91f667a-ed0a-404d-aec3-1fa916766aab',
}

json_data = {
    'query': 'query FetchProductCollection($id: String, $country: String!, $currencyCode: CurrencyCode!, $limit: Int!, $marketName: String, $page: Int!) {\n  productCollection(id: $id) {\n    tileType\n    priceType\n    footnotesType\n    trackingEvent\n    helpMessage\n    ...ResultsFragment\n    seeAllCTA {\n      title\n      url\n      urlType\n    }\n    title\n  }\n}\n\nfragment ResultsFragment on ProductCollection {\n  results(page: $page, limit: $limit) {\n    edges {\n      isAd\n      adIdentifier\n      adInventoryId\n      adServiceLevel\n      node {\n        ... on Product {\n          ...HomeProductDetailsFragment\n        }\n        ... on Variant {\n          __typename\n          id\n          sizeChart {\n            baseSize\n            baseType\n            displayOptions {\n              size\n              type\n            }\n          }\n          product {\n            ...HomeProductDetailsFragment\n          }\n          market(currencyCode: $currencyCode) {\n            ...HomeMarketFragment\n          }\n          ...FavoriteVariantFragment\n        }\n      }\n    }\n    pageInfo {\n      total\n    }\n  }\n}\n\nfragment HomeProductDetailsFragment on Product {\n  __typename\n  id\n  title\n  brand\n  browseVerticals\n  gender\n  productCategory\n  categories {\n    default {\n      alias\n    }\n  }\n  primaryCategory\n  listingType\n  name\n  urlKey\n  uuid\n  sizeDescriptor\n  ...FavoriteProductFragment\n  variants {\n    id\n  }\n  media {\n    smallImageUrl\n  }\n  market(currencyCode: $currencyCode) {\n    state(country: $country, market: $marketName) {\n      askServiceLevels {\n        expressExpedited {\n          count\n          lowest {\n            amount\n          }\n        }\n        expressStandard {\n          count\n          lowest {\n            amount\n          }\n        }\n      }\n    }\n    ...HomeMarketFragment\n  }\n  traits(filterTypes: [RELEASE_DATE, RETAIL_PRICE]) {\n    name\n    value\n  }\n}\n\nfragment HomeMarketFragment on Market {\n  currencyCode\n  state(country: $country, market: $marketName) {\n    highestBid {\n      amount\n      updatedAt\n    }\n    lowestAsk {\n      amount\n      updatedAt\n    }\n    askServiceLevels {\n      expressExpedited {\n        lowest {\n          amount\n        }\n      }\n      expressStandard {\n        lowest {\n          amount\n        }\n      }\n    }\n  }\n  statistics {\n    lastSale {\n      amount\n    }\n    last72Hours {\n      salesCount\n    }\n    annual {\n      salesCount\n    }\n    last90Days {\n      averagePrice\n    }\n  }\n}\n\nfragment FavoriteProductFragment on Product {\n  favorite\n}\n\nfragment FavoriteVariantFragment on Variant {\n  favorite\n}',
    'variables': {
        'id': 'blt5392ddf45c086b81',
        'limit': 6,
        'country': 'CN',
        'currencyCode': 'USD',
        'marketName': 'US',
        'page': 0,
    },
    'operationName': 'FetchProductCollection',
}

response = requests.post('https://stockx.com/api/p/e', cookies=cookies, headers=headers, json=json_data)
json_data = response.json()
# 注意：json_data不会被请求序列化
# 与原始请求完全相同。
# #data = '{"query":"query FetchProductCollection（$id: String, $country: String）$currencyCode: currencyCode ！$limit: Int！， $marketName: String, $page: Int!) {\\n productCollection(id: $id) {\\n tileType\\n priceType\\n footnotesType\\n trackingEvent\\n helpMessage\\n…ResultsFragment\\n seeAllCTA \\n title\\n url\\n urlType\\n \n title\\n \n\ n\ n\ n\ nfragment ResultsFragment on ProductCollection {\\n results(page: $page, limit: $limit) {\\n edges \\n isAd\\n adIdentifier\\n adInventoryId\\n adServiceLevel\\n node {\\n…产品{\\n…HomeProductDetailsFragment\\n}\\n…on Variant {\\n __typename\\n id\\n sizeChart {\\n baseSize\\n baseType\\n displayOptions {\\n size\\n type\\n}\\n \n product {\\n…HomeProductDetailsFragment\\n}\\n market(currencyCode: $currencyCode) {\\n…\\n}\\n…FavoriteVariantFragment\\n \n\ n\ n\ n\ n pageInfo \\n\ n total\\n \n\ n\ n\ n\ n\ n\ n\ n title\\n brand\\n browseVerticals\\n gender\\n productCategory\\n categories \\n categories \\n default \\n alias\\n \\n\ n primaryCategory\\n listingType\\n name\\n urlKey\\n uuid\\n sizeDescriptor\\n…FavoriteProductFragment \ \ n变体{\ \ \ n \ n id} \ \ n媒体{\ \ n smallImageUrl \ \} \ \ n市场(currencyCode: $ currencyCode) {\ \ n状态(国家:国家,美元市场:美元marketName) {\ \ n askServiceLevels {\ \ n expressExpedited {\ \ n           数\ \ n           {\ \ n最低             \ \ n量           }\\ n         }\\ n expressStandard {\ \ n           数\ \ n           {\ \ n最低             \ \ n量           }\\ n         }\\ n} \ \ n} \ \ n…\\n}\\n traits(filterTypes: [RELEASE_DATE, RETAIL_PRICE]) {\\n name\\n value\\n}\\n\\n \\n\\n \\nfragment homarketfragment on Market {\\n currencyCode\\n state(国家：$country，市场：$marketName) {\\n highestBid {\\n amount\\n updatedAt\\n \n \n lowestAsk {\\n amount\\n \\n \n \n \n askServiceLevels {\\n expressExpedited {\\n最低价\\n amount\\n \n \n \n \n \n \n \n \n \n \n \n statistics {\\n lastSale {\\n amount\\n \n \\n \ 72hours {\\n \n salesCount\\n \n \n annual {\\n \n \n \n \n \nlast90Days {\\n averagePrice\\n}\\n}\\n\ n\ n\ nfragment FavoriteProductFragment on Product {\\n favorite\\n}\\n\\n \nfragment favoriteevariantfragment on Variant {\\n favorite\\n}","variables":{"id":"blt5392ddf45c086b81","limit":6,"country":"CN","currencyCode":"USD","marketName":"US","page":0},"operationName":"FetchProductCollection“} ”
# #response = requests.post（'https://stockx.com/api/p/e', cookies=cookies, headers=headers, data=data）
# print(json_data)
# json_data 保存成 json 格式的文件
with open('data.json', 'w') as f:
    json.dump(json_data, f)
    print(json_data)
