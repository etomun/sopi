import concurrent.futures.thread
import time
from datetime import datetime

import requests
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.wait import WebDriverWait

cookies = {
    '_gcl_au': '1.1.868810385.1702613048',
    '_med': 'cpc',
    'csrftoken': 'ZCcTQWYsOQOSN3H0tpbgaPPolYhbZXKd',
    'REC_T_ID': 'ff3d89b7-9afe-11ee-85f4-2ae071634f23',
    'SPC_F': 'Ns71b9OVLgr84SYbvAnFTMzpUIEFcsk0',
    '_fbp': 'fb.2.1702613048716.668430754',
    '_sapid': 'f37d5581-dce3-4d81-a28b-e41ba8b78a96',
    'SPC_CLIENTID': 'TnM3MWI5T1ZMZ3I4ngasjmagyueafvpw',
    '_gcl_aw': 'GCL.1702613102.Cj0KCQiA7OqrBhD9ARIsAK3UXh0HwyTvISA0uFcB4sI8E-7mUiDnrJPWZw13jjWX12tmQLmFOHr6L2MaAo0EEALw_wcB',
    'SPC_IA': '1',
    '_gac_UA-61904553-8': '1.1702613103.Cj0KCQiA7OqrBhD9ARIsAK3UXh0HwyTvISA0uFcB4sI8E-7mUiDnrJPWZw13jjWX12tmQLmFOHr6L2MaAo0EEALw_wcB',
    'SPC_U': '1131611004',
    'SPC_R_T_IV': 'SWR2Zkh6OWRjU1RsZ1JFaA==',
    'SPC_T_ID': 'pfGjQInUJ9qKiVfwdP3q01TNrVT9mClx4c4eKOC0nMiGYsHdFLV+kUHhwUYTegDdmWXy/do428HDb03oQywlsQ8jAvgwjPv5rshJLQrodb9QaOgE9BIpyG4XtN1shzDNH4l+xYYWzWm4QnGDLp0E0GQdq5o5ZtOZK5QXqEhW91M=',
    'SPC_T_IV': 'SWR2Zkh6OWRjU1RsZ1JFaA==',
    'SPC_R_T_ID': 'pfGjQInUJ9qKiVfwdP3q01TNrVT9mClx4c4eKOC0nMiGYsHdFLV+kUHhwUYTegDdmWXy/do428HDb03oQywlsQ8jAvgwjPv5rshJLQrodb9QaOgE9BIpyG4XtN1shzDNH4l+xYYWzWm4QnGDLp0E0GQdq5o5ZtOZK5QXqEhW91M=',
    'SPC_SI': 'tm+BZQAAAABweHVlSWhMM+VhMQAAAAAAZXVZSDFCTHo=',
    'SPC_SEC_SI': 'v1-R1VwV0oxdThJY252SXNwN+BDq32bohJlo2CKrRLMId19k/T3qPEw4TcWN05o5702gG077NGb3iHpLyv1/xz/Toyb3zHN1HuIKKtcsWlxcvU=',
    '_gid': 'GA1.3.2131002128.1703308089',
    '_QPWSDCXHZQA': '6ff78088-9721-4c8f-e04f-1230854551a9',
    'REC7iLP4Q': '79144663-9162-4594-bab9-0aed8f6dcc98',
    'AMP_TOKEN': '%24NOT_FOUND',
    'SPC_EC': '.cTFUMG01bmVYUjNlUnowWCeKUs6By89FSrMZISBzc12KY9Rpw/OCAFWz4/9aCl/vdEiGjjqgN/cumr93D8jMBtOTn08a109Q81LcLOx9T+Xd9RK7f69DLPlKjaUY+9jghrZyUSYrrrFxYHP5VrHlB1IzpM1fKPCpsVCHw4Lu+hzdgMByMuc1A3Klq1U7mDHx2zDWDtkSNdtHhPOgTozhxw==',
    'SPC_ST': '.cTFUMG01bmVYUjNlUnowWCeKUs6By89FSrMZISBzc12KY9Rpw/OCAFWz4/9aCl/vdEiGjjqgN/cumr93D8jMBtOTn08a109Q81LcLOx9T+Xd9RK7f69DLPlKjaUY+9jghrZyUSYrrrFxYHP5VrHlB1IzpM1fKPCpsVCHw4Lu+hzdgMByMuc1A3Klq1U7mDHx2zDWDtkSNdtHhPOgTozhxw==',
    '_dc_gtm_UA-61904553-8': '1',
    '_ga_SW6D8G0HXK': 'GS1.1.1703348855.11.1.1703348992.32.0.0',
    '_ga': 'GA1.1.1415049999.1702613050',
    'shopee_webUnique_ccd': 'CZRIAfcXeFF0mRvdj4GgiQ%3D%3D%7CRAvncVbnfTEU6oFgU65t4Ygg0InXo9%2BeQmWIDeFmpqCy%2FP1%2FujHeomM8%2BXZU05ObLDh2HzOFLF0wCg%3D%3D%7CTp3j6nq7Hnj%2Fp8ZI%7C08%7C3',
    'ds': 'd9f592440337eb73f9e589ddd674449e',
}

headers = {
    'authority': 'shopee.co.id',
    'accept': 'application/json',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7,id;q=0.6',
    'af-ac-enc-dat': 'AAczLjMuMC0yAAABjJeC970AABBIAyAAAAAAAAAAAv0CU/axxHG/NVDiUQlegXtyZ3c8l/82EyfDx/bVRcPaaRvYm5f/NhMnw8f21UXD2mkb2JuY38EmlKYPJcQ+v7qJyMilBF5wb3V9GObUwbJ+Ls6wDaipgEx3p0EMGmjhd8nTvVkszTqUOA7K8GuyW+4+W0X54xn9vHlAIn5XHju19BnhVZf/NhMnw8f21UXD2mkb2JvJGAA5AcImJXH0MA9YzzgVBwvvs2WErk0OFrfXCTEcHkWp+KOsMG49WlUfad0aZT0F/jvWI528weWYgWihMcbmc2NAWiW1KmGaWA1Wi3nisUgD9O1aYGgjmjuYbekv+r99mhL6X5cQVi4bjfSv/rbQwxf8tfsapumpCcVeJZROdx5rsMhC5B1UhYZ8o8pJVeaW38rMUaphJQhe1b6bMu59xcLwyolN4wxXqA2uOCt0f6ibuJZ2/43YLeYD0PE2g3gw1RkhTQLj1MCJzsob0uPG29tC2N2PAoqeSIHBuLYKQHV8jOXlXDedshTIf9JERLkc2kVzFOs6/hKGpRAoZCzeqpExEy29FuEwzpc9xWPvyQf4anIo+9IPdsxe8jOHF3kvAbpR4myCheReQSMnwfQiqf4u/zYSNBVyt6/mnwKbnUckfn/aqZ2EUBMC3PvgG/VvNgVjhrb40sNy/RF0/6sddvrx2cDNAh/WiazMgcgB2IpWoI3lzvoPKDx96WVQBxHBKrOR6ojP0xrX1eHLs+YTdvrx2cDNAh/WiazMgcgB2IpWoI3lzvoPKDx96WVQBxGSFYO4/MZDy1ymy64bfkpv6bulLTY4m8Qhuucz/q6VcozaSwO/1GXe2Xe6/gfPKa+Y+OsoYB7a6LHleVveG5+MI07m/lc2lPIx0qGVaRMubozaSwO/1GXe2Xe6/gfPKa+TlNdrUAO5AUCSrX/MPBeiioUDBId86zqvcR0Zz7OCdjp0CAv1iHLrwTFoxMGGOhQF6bxAFCTOs0lACdIOVC5wiXMz12p/YiA+8e7LXdwj1o04XADFqxYP5F8HUfGYVxJQuXj+5KghzHR4XD9PvWQN+gYColtH858iwwULGxIxFg==',
    'af-ac-enc-sz-token': 'CZRIAfcXeFF0mRvdj4GgiQ==|RAvncVbnfTEU6oFgU65t4Ygg0InXo9+eQmWIDeFmpqCy/P1/ujHeomM8+XZU05ObLDh2HzOFLF0wCg==|Tp3j6nq7Hnj/p8ZI|08|3',
    'content-type': 'application/json',
    # 'cookie': '_gcl_au=1.1.868810385.1702613048; _med=cpc; csrftoken=ZCcTQWYsOQOSN3H0tpbgaPPolYhbZXKd; REC_T_ID=ff3d89b7-9afe-11ee-85f4-2ae071634f23; SPC_F=Ns71b9OVLgr84SYbvAnFTMzpUIEFcsk0; _fbp=fb.2.1702613048716.668430754; _sapid=f37d5581-dce3-4d81-a28b-e41ba8b78a96; SPC_CLIENTID=TnM3MWI5T1ZMZ3I4ngasjmagyueafvpw; _gcl_aw=GCL.1702613102.Cj0KCQiA7OqrBhD9ARIsAK3UXh0HwyTvISA0uFcB4sI8E-7mUiDnrJPWZw13jjWX12tmQLmFOHr6L2MaAo0EEALw_wcB; SPC_IA=1; _gac_UA-61904553-8=1.1702613103.Cj0KCQiA7OqrBhD9ARIsAK3UXh0HwyTvISA0uFcB4sI8E-7mUiDnrJPWZw13jjWX12tmQLmFOHr6L2MaAo0EEALw_wcB; SPC_U=1131611004; SPC_R_T_IV=SWR2Zkh6OWRjU1RsZ1JFaA==; SPC_T_ID=pfGjQInUJ9qKiVfwdP3q01TNrVT9mClx4c4eKOC0nMiGYsHdFLV+kUHhwUYTegDdmWXy/do428HDb03oQywlsQ8jAvgwjPv5rshJLQrodb9QaOgE9BIpyG4XtN1shzDNH4l+xYYWzWm4QnGDLp0E0GQdq5o5ZtOZK5QXqEhW91M=; SPC_T_IV=SWR2Zkh6OWRjU1RsZ1JFaA==; SPC_R_T_ID=pfGjQInUJ9qKiVfwdP3q01TNrVT9mClx4c4eKOC0nMiGYsHdFLV+kUHhwUYTegDdmWXy/do428HDb03oQywlsQ8jAvgwjPv5rshJLQrodb9QaOgE9BIpyG4XtN1shzDNH4l+xYYWzWm4QnGDLp0E0GQdq5o5ZtOZK5QXqEhW91M=; SPC_SI=tm+BZQAAAABweHVlSWhMM+VhMQAAAAAAZXVZSDFCTHo=; SPC_SEC_SI=v1-R1VwV0oxdThJY252SXNwN+BDq32bohJlo2CKrRLMId19k/T3qPEw4TcWN05o5702gG077NGb3iHpLyv1/xz/Toyb3zHN1HuIKKtcsWlxcvU=; _gid=GA1.3.2131002128.1703308089; _QPWSDCXHZQA=6ff78088-9721-4c8f-e04f-1230854551a9; REC7iLP4Q=79144663-9162-4594-bab9-0aed8f6dcc98; AMP_TOKEN=%24NOT_FOUND; SPC_EC=.cTFUMG01bmVYUjNlUnowWCeKUs6By89FSrMZISBzc12KY9Rpw/OCAFWz4/9aCl/vdEiGjjqgN/cumr93D8jMBtOTn08a109Q81LcLOx9T+Xd9RK7f69DLPlKjaUY+9jghrZyUSYrrrFxYHP5VrHlB1IzpM1fKPCpsVCHw4Lu+hzdgMByMuc1A3Klq1U7mDHx2zDWDtkSNdtHhPOgTozhxw==; SPC_ST=.cTFUMG01bmVYUjNlUnowWCeKUs6By89FSrMZISBzc12KY9Rpw/OCAFWz4/9aCl/vdEiGjjqgN/cumr93D8jMBtOTn08a109Q81LcLOx9T+Xd9RK7f69DLPlKjaUY+9jghrZyUSYrrrFxYHP5VrHlB1IzpM1fKPCpsVCHw4Lu+hzdgMByMuc1A3Klq1U7mDHx2zDWDtkSNdtHhPOgTozhxw==; _dc_gtm_UA-61904553-8=1; _ga_SW6D8G0HXK=GS1.1.1703348855.11.1.1703348992.32.0.0; _ga=GA1.1.1415049999.1702613050; shopee_webUnique_ccd=CZRIAfcXeFF0mRvdj4GgiQ%3D%3D%7CRAvncVbnfTEU6oFgU65t4Ygg0InXo9%2BeQmWIDeFmpqCy%2FP1%2FujHeomM8%2BXZU05ObLDh2HzOFLF0wCg%3D%3D%7CTp3j6nq7Hnj%2Fp8ZI%7C08%7C3; ds=d9f592440337eb73f9e589ddd674449e',
    'referer': 'https://shopee.co.id/Manja-Girl-Lingerie-Sexy-Wanita-One-Set-Kimono-Bigsize-928-no-i.198946183.5866185087?sp_atk=ec03e20f-a02e-4aa7-b5d7-c09e855f3cad&xptdk=ec03e20f-a02e-4aa7-b5d7-c09e855f3cad',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sz-token': 'CZRIAfcXeFF0mRvdj4GgiQ==|RAvncVbnfTEU6oFgU65t4Ygg0InXo9+eQmWIDeFmpqCy/P1/ujHeomM8+XZU05ObLDh2HzOFLF0wCg==|Tp3j6nq7Hnj/p8ZI|08|3',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-api-source': 'pc',
    'x-csrftoken': 'ZCcTQWYsOQOSN3H0tpbgaPPolYhbZXKd',
    'x-requested-with': 'XMLHttpRequest',
    'x-sap-ri': '000b87653beed46395ec8d3c01018176de6ef2d58edce1a2b945',
    'x-sap-sec': 'kp8vPZQgJwDj4wDj52Dw4wlj52Dj4wlj4wDf4wDjSwvj4mDi4wDz4wDjwlNEGpIj4wAj4uDjnwWj4woQwbKDhKiKnKK4v4jWdw5sxQ2w96ZPbxuEFzrIWtSBcGjnG5XB/4TdiG6q1yeaDqxU8gs/KQCDfFLqTCFVBY7k+wBMe1ZVpakEzVVzD7nakF8pPn7p6Lpaw9m4RM7o7vUdaCUxeqEn2EjaFKumHeiupIEyjSnEEvBD272SakrW5GDOOQqPMeEXXGbVN/uUMbhaAdLpTcR8nBWF+16tB1XnzgDKagJ59C3CHCYUfKJrE8Abs5RSHQCHHWiDQd3Ne4HK2XHw+NBbV7fzvYjPVHBKpWcwlPSWfyVmGu8QTCG9gvt4OlBXZNYEwxzMDnV8SJyLmmWoZSz/onrMuujncdlsDEGBiz7SrhEBGl6ZzFs4jASCuTc08R1NYRIK7k1jdDaOtgRqgncVaBXUIFK87osE4XdMt9qcx7oDyjig1HBfIWwIqkWgPm2YhMG0lOmPKqe3+WugpnyPvQP9iXhem6CuDjFb0jPtWcqTuFvlrdV3HBK2mjgTb3SNX/f5Onmnm6+rRtCZmw5sK/uJzT7u419hGRFhEQ7Y6ylyQqH3ak+EN9dAzb7znFXvNSiKnVuvn3DPHv3I1J9WIwDj4ZZ+7elJ6KDp4wDj4zREGIKw4wDjPwDj4Ylj4wFXNEK6MdyX2wVJSJ+snslEqKjZvpIj4wFRsUm+7eWoo2Dj4wDw4wQjIwDz4wIj4wDw4wDjPwDj4Ylj4wASj26wZ9ZlABhqLyeijvedxlpNMpIj4wD4pUnp7UUBppDj4wD=',
    'x-shopee-language': 'id',
    'x-sz-sdk-version': '3.3.0-2&1.6.10',
}


def add_to_cart():
    json_data = {
        'quantity': 1,
        'checkout': True,
        'update_checkout_only': True,
        'donot_add_quantity': True,
        'source': '{"refer_urls":[]}',
        'client_source': 1,
        'shopid': shop_id,
        'itemid': item_id,
        'modelid': model_id,
    }
    for _ in range(3):
        r = requests.post('https://shopee.co.id/api/v4/cart/add_to_cart', cookies=cookies, headers=headers,
                          json=json_data)
        err = r.json()['error']
        if err <= 0:
            break


def wait_to_checkout():
    driver = webdriver.Remote(f"http://127.0.0.1:4723", options=options)
    wait = WebDriverWait(driver, 7)
    time.sleep(10)


def main():
    time_difference = exec_at - (time.time() * 1000)
    if time_difference > 0:
        while time.time() * 1000 < exec_at:
            remaining_time = int(exec_at - time.time() * 1000)
            minutes, secs = divmod(remaining_time // 1000, 60)
            tf = '{:02d}:{:02d}'.format(minutes, secs)
            print(tf, end='\r')
            time.sleep(1)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            [executor.submit(f) for f in [add_to_cart, wait_to_checkout]]
    else:
        print("Expired")


if __name__ == '__main__':
    shop_id = 182286375
    item_id = 21485793821
    model_id = 204699335545
    exec_at = int(datetime(2023, 12, 24, 00, 51, 00).timestamp() * 1000)

    capabilities = {
        "platformName": "android",
        "appium:deviceName": "localhost:40915 (13)",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": "com.shopee.id",
        "appium:appActivity": "com.shopee.app.ui.home.HomeActivity_",
        "appium:noReset": True,
        "appium:shouldTerminateApp": True,
        "appium:disableWindowAnimation": True
    }
    options = UiAutomator2Options().load_capabilities(capabilities)
    main()
