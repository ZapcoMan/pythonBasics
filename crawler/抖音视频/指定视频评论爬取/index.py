import requests
import json
import time
import os

# 创建输出目录
output_dir = "抖音评论输出"
os.makedirs(output_dir, exist_ok=True)

# 请求 URL
url = "https://www.douyin.com/aweme/v1/web/comment/list/"

# 请求参数（Query Parameters）
params = {
    "device_platform": "webapp",
    "aid": "6383",
    "channel": "channel_pc_web",
    "aweme_id": "7318724406165916963",
    "cursor": "0",
    "count": "20",
    "item_type": "0",
    "whale_cut_token": "",
    "cut_version": "1",
    "rcFT": "",
    "update_version_code": "170400",
    "pc_client_type": "1",
    "pc_libra_divert": "Windows",
    "support_h265": "1",
    "support_dash": "1",
    "cpu_core_num": "4",
    "version_code": "170400",
    "version_name": "17.4.0",
    "cookie_enabled": "true",
    "screen_width": "2560",
    "screen_height": "1440",
    "browser_language": "zh-CN",
    "browser_platform": "Win32",
    "browser_name": "Chrome",
    "browser_version": "137.0.0.0",
    "browser_online": "true",
    "engine_name": "Blink",
    "engine_version": "137.0.0.0",
    "os_name": "Windows",
    "os_version": "10",
    "device_memory": "8",
    "platform": "PC",
    "downlink": "1.25",
    "effective_type": "3g",
    "round_trip_time": "400",
    "webid": "7496768310278981130",
    "uifid": "4be83ecefa579a300714166db9e569bafd8689fc248d1e190e384db8df203b81bd69f2142305ce7b3693840b0e729110646aa6107cef5fe0aa83a8c8ce09f646d4c84fe4abea47929e69166ecc0ef6aaad4b249d32d99dce348648cb0d02fb0ad8cdde79bc04e61f5cd7c71fc3f43e8045f36ce847d54d1a20105c34ceb7b468d55173f7f4cd0c2f12cfab83d80ba9899a1e1693f3ad2dbc5c56dac9d7b36a7a",
    "msToken": "F4T44jrnEeB6JH0ljmnhaLUUHOuaoy99JdvY488bpl3ytEpsW_C54kyXDRW1g3ot6n7O6eZg3zwVI7IzAY0J3QUAY_KpjInX6piHn6RCD3wk9SYfnGhSkyE2flOwK6BK-R-7KJqk-o2cQB2CYMPUSqxwKOV6wr9lNsX2faGYDgjo",
    "a_bogus": "QX4VhH6Jdd5nad%2FtmCbGt5OlG%2FLlNBuy01TxRaaP9xF3TXMcZYNfkNa5boFi4Tc2jRBwhK1HyjUAYxdc%2FTUwZFrkompDSwiy9UVC96XLZ1NgYFJQLqmDCgTFzXBC85sq-QVIiIJIMUrLZfx-hrdE%2FB3CCKOeQmuhK3ORk%2FzSP9aXZzgAD3nePdSkEhiqAf%3D%3D",
    "verifyFp": "verify_mcd86ytp_114CZoh0_P145_411x_9k9D_FPijnA76CiMQ",
    "fp": "verify_mcd86ytp_114CZoh0_P145_411x_9k9D_FPijnA76CiMQ",
    "x-secsdk-web-expire": "1750933212143",
    "x-secsdk-web-signature": "95f0353e72b3161c834f8625ef0bffae"
}

# 请求头（Headers）
headers = {
    ":authority": "www.douyin.com",
    ":method": "GET",
    ":path": "/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7318724406165916963&cursor=0&count=20&item_type=0&whale_cut_token=&cut_version=1&rcFT=&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&cpu_core_num=4&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=137.0.0.0&browser_online=true&engine_name=Blink&engine_version=137.0.0.0&os_name=Windows&os_version=10&device_memory=8&platform=PC&downlink=1.25&effective_type=3g&round_trip_time=400&webid=7496768310278981130&uifid=4be83ecefa579a300714166db9e569bafd8689fc248d1e190e384db8df203b81bd69f2142305ce7b3693840b0e729110646aa6107cef5fe0aa83a8c8ce09f646d4c84fe4abea47929e69166ecc0ef6aaad4b249d32d99dce348648cb0d02fb0ad8cdde79bc04e61f5cd7c71fc3f43e8045f36ce847d54d1a20105c34ceb7b468d55173f7f4cd0c2f12cfab83d80ba9899a1e1693f3ad2dbc5c56dac9d7b36a7a&msToken=F4T44jrnEeB6JH0ljmnhaLUUHOuaoy99JdvY488bpl3ytEpsW_C54kyXDRW1g3ot6n7O6eZg3zwVI7IzAY0J3QUAY_KpjInX6piHn6RCD3wk9SYfnGhSkyE2flOwK6BK-R-7KJqk-o2cQB2CYMPUSqxwKOV6wr9lNsX2faGYDgjo&a_bogus=QX4VhH6Jdd5nad%2FtmCbGt5OlG%2FLlNBuy01TxRaaP9xF3TXMcZYNfkNa5boFi4Tc2jRBwhK1HyjUAYxdc%2FTUwZFrkompDSwiy9UVC96XLZ1NgYFJQLqmDCgTFzXBC85sq-QVIiIJIMUrLZfx-hrdE%2FB3CCKOeQmuhK3ORk%2FzSP9aXZzgAD3nePdSkEhiqAf%3D%3D&verifyFp=verify_mcd86ytp_114CZoh0_P145_411x_9k9D_FPijnA76CiMQ&fp=verify_mcd86ytp_114CZoh0_P145_411x_9k9D_FPijnA76CiMQ&x-secsdk-web-expire=1750933212143&x-secsdk-web-signature=95f0353e72b3161c834f8625ef0bffae",
    ":scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "hevc_supported=true; SEARCH_RESULT_LIST_TYPE=%22multi%22; fpk1=U2FsdGVkX19T4ScTwn0ZCwe2HVmQywniIe8+13A+p+3g9d+9dplku/Ep5rUqtrxbX3LmAQhm5hIU63zfHkruog==; fpk2=33d0f257a817d1ca4c4381b87f8ad83f; __ac_signature=_02B4Z6wo00f01qVIK5AAAIDDehPY30dA-falaC8AAMFO80; SearchMultiColumnLandingAbVer=2; passport_csrf_token=03ade73158afabb3dfc51d7e8c53b995; passport_csrf_token_default=03ade73158afabb3dfc51d7e8c53b995; enter_pc_once=1; UIFID=4be83ecefa579a300714166db9e569bafd8689fc248d1e190e384db8df203b81bd69f2142305ce7b3693840b0e729110646aa6107cef5fe0aa83a8c8ce09f646d4c84fe4abea47929e69166ecc0ef6aaad4b249d32d99dce348648cb0d02fb0ad8cdde79bc04e61f5cd7c71fc3f43e8045f36ce847d54d1a20105c34ceb7b468d55173f7f4cd0c2f12cfab83d80ba9899a1e1693f3ad2dbc5c56dac9d7b36a7a; dy_swidth=2560; dy_sheight=1440; is_dash_user=1; volume_info=%7B%22isMute%22%3Atrue%2C%22volume%22%3A0.6%7D; __security_mc_1_s_sdk_crypt_sdk=71a38693-434e-818a; bd_ticket_guard_client_web_domain=2; strategyABtestKey=%221750932816.861%22; s_v_web_id=verify_mcd86ytp_114CZoh0_P145_411x_9k9D_FPijnA76CiMQ; ttwid=1%7CNg9hNx0-rpMmViH-KOOKbkQLjxbCLcs167ENvoNwhGc%7C1750932836%7C314b17a9fe0643017b71eec1126ef6c748d9da8903f494dfd98360784b4ff842; biz_trace_id=628cc32e; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSDh0dTdZTzJhdlltME5EN3E5R2o1a1dReUQvaGxBMHFsb3dzaXcyTE43OGViS21uVlRYWGRPTjRuOXM1ZlVVdVlSVlpuSHoyM0o1NEFSeUFIcHpEaTA9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f2737323731363d37363c35303234272927676c715a75776a716a666a69273f2763646976602778; bit_env=WiFB471EBBFxHOFFuG9iLejfb9h572c1lqrb721VdIlVNJD0z1VxP4WzSPldwxzU2vw1y1Sq6QXQtAGTm4t0_AbgZuiJ3OPReZA7swGmV0O5AxQ8Jvg0szH6F_2Ht02W5b2uoYTsW8wK6qLuYzyD4gywnkQkVmxkQ9vD2Fj3c0o8VH_vLbEgCOm50UEqljgO251A3VtkAgWO9JohGqqQ01v74OCMr0W5U5e3K_qb5qAFXKzkrE1S7pG3-g5R0it5d_do2pz5tzl_mlxScNQROPqWvh7yH-qN9ysfeNRDeedQqmTDp-LYT6L2gHTdTOAS-_yGKoqsFcD1XZskVQO9QxlrJ29WoialxDXapmz-o41EiTuh8CyCAabIwgZtsZl78kBb1zRjan-ylnVhddccjmHNrzzXpdD38kbmEuR1zApYcvPVbhER-7SinIjI8s2B5lb6oUCWLEmtPHslssCVmc7OXJGp-Br35FUtHlvzdJVFouuGOgyHMz28-f0DVbK9; gulu_source_res=eyJwX2luIjoiODE4ZmQ4N2E4MDc2ZjQwYjA4ZjJiNjYwZTg5MGFhM2JmYTMyNTg1MzhhODVhZTBlYjZkM2M5YTZkNWU0ZDEzZCJ9; passport_auth_mix_state=cs4i0l3djf6sv37b46gjqn5l129pbbzhq2ytha856rjg4ptg; download_guide=%221%2F20250626%2F0%22; odin_tt=86831be32156ff2f49a991060b88b6fd070911396a49ff233988cda23a626f5d9b1ee218fc107669f83e391ab12c401616de2babe5351f42ce4bdd2e0c744974; passport_assist_user=CkD7IdVfnEke1JyVDe6SY-84VEVrmPj-QACaEtWyy7yMORxB5KK5d-NCUpXeek-VQTX2nBgOPrNR2KYyjNwOGOWvGkoKPAAAAAAAAAAAAABPKaOYbRhvpLQZ3JxQ8cEtjUMMzeFEsYUxq31ySZhbvQWFSp8SeFNsmDX2jSdYM1QoQBDDkPUNGImv1lQgASIBA6PcE-Y%3D; n_mh=h2mcv-yYgGGKdAktKXV0-9I1UjBsChFP5IRxa2LV12s; sid_guard=9ef2236ef4c314be3570419283f5dacb%7C1750932881%7C5184000%7CMon%2C+25-Aug-2025+10%3A14%3A41+GMT; uid_tt=13fee0a9e05b1eb81754105e458230c5; uid_tt_ss=13fee0a9e05b1eb81754105e458230c5; sid_tt=9ef2236ef4c314be3570419283f5dacb; sessionid=9ef2236ef4c314be3570419283f5dacb; sessionid_ss=9ef2236ef4c314be3570419283f5dacb; session_tlb_tag=sttt%7C8%7CnvIjbvTDFL41cEGSg_Xay__________rRgoTAL0HHFm__1n3hnyK7xWZRaXdkGqFMdyB3RCPA9A%3D; is_staff_user=false; sid_ucp_v1=1.0.0-KDVjYzU1MWUzMTRjMWRiMTY0ZDYyNTUwNWU1NDU3YmRjODExMzQ1NzUKIAiepJDfqoxZEJG79MIGGO8xIAww9fyqkQY4B0D0B0gEGgJobCIgOWVmMjIzNmVmNGMzMTRiZTM1NzA0MTkyODNmNWRhY2I; ssid_ucp_v1=1.0.0-KDVjYzU1MWUzMTRjMWRiMTY0ZDYyNTUwNWU1NDU3YmRjODExMzQ1NzUKIAiepJDfqoxZEJG79MIGGO8xIAww9fyqkQY4B0D0B0gEGgJobCIgOWVmMjIzNmVmNGMzMTRiZTM1NzA0MTkyODNmNWRhY2I; login_time=1750932874523; publish_badge_show_info=%220%2C0%2C0%2C1750932875169%22; _bd_ticket_crypt_cookie=315db9f6d951b3ce968c062c4e143638; __security_mc_1_s_sdk_sign_data_key_web_protect=cbdf774e-42ee-b30b; __security_server_data_status=1; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2560%2C%5C%22screen_height%5C%22%3A1440%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A4%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.25%2C%5C%22effective_type%5C%22%3A%5C%223g%5C%22%2C%5C%22round_trip_time%5C%22%3A400%7D%22; SelfTabRedDotControl=%5B%5D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAn_3H_k3YrqzOb0xkfv4mwhGKev5LW4yNmHmonYv9WB0%2F1750953600000%2F0%2F1750932907940%2F0%22",
    "priority": "u=1, i",
    "referer": "https://www.douyin.com/shipin/7270368633061197885",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "uifid": "4be83ecefa579a300714166db9e569bafd8689fc248d1e190e384db8df203b81bd69f2142305ce7b3693840b0e729110646aa6107cef5fe0aa83a8c8ce09f646d4c84fe4abea47929e69166ecc0ef6aaad4b249d32d99dce348648cb0d02fb0ad8cdde79bc04e61f5cd7c71fc3f43e8045f36ce847d54d1a20105c34ceb7b468d55173f7f4cd0c2f12cfab83d80ba9899a1e1693f3ad2dbc5c56dac9d7b36a7a",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

def fetch_comments(cursor=0):
    """请求评论数据"""
    params["cursor"] = str(cursor)
    try:
        response = requests.get(url, headers=headers, params=params, timeout=(5, 10))
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return None


def save_comments(data, filename="comments.json"):
    """保存评论数据为 JSON 文件"""
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"已保存评论数据至 {file_path}")


def extract_and_save_titles(comments_data, filename="comments.txt"):
    """提取评论内容并写入 .txt 文件"""
    comments_list = []

    if not comments_data or "data" not in comments_data:
        print("无有效评论数据")
        return

    for item in comments_data.get("data", []):
        user = item.get("user", {})
        comment = item.get("text")
        nickname = user.get("nickname")
        if comment:
            comments_list.append(f"{nickname}: {comment}")

    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        for c in comments_list:
            f.write(c + "\n")

    print(f"已提取评论并保存至 {file_path}")


def get_all_comments():
    """分页获取所有评论"""
    all_comments = []
    has_more = True
    cursor = 0

    while has_more:
        print(f"正在获取第 {cursor} 批评论...")
        data = fetch_comments(cursor)
        if not data:
            break

        all_comments.extend(data.get("data", []))
        has_more = data.get("has_more", False)
        cursor = data.get("cursor", cursor + 20)
        time.sleep(random.uniform(1, 3))

    # 合并所有评论数据
    full_data = {"data": all_comments}
    save_comments(full_data)
    extract_and_save_titles(full_data)


if __name__ == "__main__":
    get_all_comments()
