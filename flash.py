import argparse
import concurrent.futures.thread
import json
import subprocess
import time
from datetime import datetime

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from device import get_device_name


def _get_cookies(usr: str) -> dict:
    try:
        with open(f"data/auth/shop_ee_session_{usr}.json", "r") as f:
            session = json.loads(f.read())
            cookies = session['cookies']
            return {c['name']: c['value'] for c in cookies}
    except FileNotFoundError:
        print(f"Cookies not found for {usr}. Please LOGIN first.")
        return {}
        pass


def wait_to_add_cart():
    while time.time() * 1000 < exec_at:
        remaining_time = int(exec_at - time.time() * 1000)
        minutes, secs = divmod(remaining_time // 1000, 60)
        tf = '{:02d}:{:02d}'.format(minutes, secs)
        print(tf, end='\r')
        time.sleep(1)

    print(f"START")
    command = [
        'curl',
        'https://shopee.co.id/api/v4/cart/add_to_cart',
        '-H', 'authority: shopee.co.id',
        '-H', 'accept: application/json',
        '-H', 'accept-language: en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7,id;q=0.6',
        '-H', 'content-type: application/json',
        '-H', 'if-none-match-: 55b03-dd1d0133e8d963d7deb73f0baac49db3',
        '-H', 'origin: https://shopee.co.id',
        '-H', 'referer: https://shopee.co.id',
        '-H', 'sec-ch-ua: "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        '-H', 'sec-ch-ua-mobile: ?0',
        '-H', 'sec-ch-ua-platform: "macOS"',
        '-H', 'sec-fetch-dest: empty',
        '-H', 'sec-fetch-mode: cors',
        '-H', 'sec-fetch-site: same-origin',
        '-H',
        'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        '-H', 'x-api-source: pc',
        '-H', 'x-csrftoken: ZCcTQWYsOQOSN3H0tpbgaPPolYhbZXKd',
        '-H', 'x-requested-with: XMLHttpRequest',
        '-H', 'x-sap-ri: 995a87651dec5b881f1a543d01011ccab4689e6873d58ba0d1bf',
        '-H',
        'x-sap-sec: XOcbKrvRELxcHLxcSGx3HLvcSGxcHLvcHLxMHLxcLLlcHK/RHLbmHhxcSLxcHcbnfTO3HLxcbLCcH+/QHLxUys44axwDeVMJjhN04/qHrV2vQln75Dxue+nT5aw2DyKC2zYplA3m0BEiDbyQ1owVax+ctOT6HIw4D7NJUssVV6GvYYk4fwIWOWBctNA5dLacNnuvr50VCVd+DDZZq192wO2lAed2aZ/SVT7Kh5qBV//lUX+2p4+n/XCQCm7kNvaDnRBdn5diZAVXMNL+XM/8sAGxf8GaeA9w3EXUbOKm6a/oDDGdTZXvrgshqLEhaNZHSKOI8BhT8AEoAfl51FSrPmMBqI1VitXXcdb21qv8wvLIMAsHoV6u+edkuQdGF6dedWTK+UuRicKSy2+PEMxSBx0/EdhhsGXlmHs27bPX4V30UQ7VkOzYLYjJ+45dfcOaPlyLnMYRptAuMRyu8+i0kvilvy8BQ0Az0e+G4CF36MZSaYyqw/ZxWGdXrgfiUfIxL0h7co+wDZb36lyjWbYzuYB6tZ0zG1Y6jMMms/mT4HjLBJoxLn+C3edZ5ntFXNxnB3dddlhBZ1bdseuomxRupjbYjVa7QJqt9gt+pI/PjgGo11qt1cLW48bafkn4laYUH80n2K1fehagurUC/pMKpFGihetP7h/cHLxAdo/9rYvFPhxcHLaefTrqeLxcHKEcHLxPHLxchJUOVipIChXzdsiEcUONprqoJ2v3HLxckYDDr6gfroxcHLxcxdrqft/cHLxhHLxcoLxcHQc22+SAL441RwngJygbexZXjHI7eLxcH6Ggr6fvkqnAHLxcHL/cELx3HLvceLxcHL/cHLxhHLxcoLxcHNY1FBJFMBu210NSVlpDJz50G63reLxcH0DARbf8RHDUHLxcHK==',
        '-H', 'x-shopee-language: id',
        '-d',
        '{"quantity":1,"checkout":true,"update_checkout_only":false,"donot_add_quantity":false,"source":"{\\"refer_urls\\":[]}","client_source":1,"shopid":494896079,"itemid":23133074344,"modelid":175730839640}',
        '-b',
        '_gcl_au=1.1.868810385.1702613048; _med=cpc; csrftoken=ZCcTQWYsOQOSN3H0tpbgaPPolYhbZXKd; REC_T_ID=ff3d89b7-9afe-11ee-85f4-2ae071634f23; SPC_F=Ns71b9OVLgr84SYbvAnFTMzpUIEFcsk0; _fbp=fb.2.1702613048716.668430754; _sapid=f37d5581-dce3-4d81-a28b-e41ba8b78a96; SPC_CLIENTID=TnM3MWI5T1ZMZ3I4ngasjmagyueafvpw; _gcl_aw=GCL.1702613102.Cj0KCQiA7OqrBhD9ARIsAK3UXh0HwyTvISA0uFcB4sI8E-7mUiDnrJPWZw13jjWX12tmQLmFOHr6L2MaAo0EEALw_wcB; SPC_IA=1; _gac_UA-61904553-8=1.1702613103.Cj0KCQiA7OqrBhD9ARIsAK3UXh0HwyTvISA0uFcB4sI8E-7mUiDnrJPWZw13jjWX12tmQLmFOHr6L2MaAo0EEALw_wcB; SPC_U=1131611004; SPC_R_T_IV=SWR2Zkh6OWRjU1RsZ1JFaA==; SPC_T_ID=pfGjQInUJ9qKiVfwdP3q01TNrVT9mClx4c4eKOC0nMiGYsHdFLV+kUHhwUYTegDdmWXy/do428HDb03oQywlsQ8jAvgwjPv5rshJLQrodb9QaOgE9BIpyG4XtN1shzDNH4l+xYYWzWm4QnGDLp0E0GQdq5o5ZtOZK5QXqEhW91M=; SPC_T_IV=SWR2Zkh6OWRjU1RsZ1JFaA==; SPC_R_T_ID=pfGjQInUJ9qKiVfwdP3q01TNrVT9mClx4c4eKOC0nMiGYsHdFLV+kUHhwUYTegDdmWXy/do428HDb03oQywlsQ8jAvgwjPv5rshJLQrodb9QaOgE9BIpyG4XtN1shzDNH4l+xYYWzWm4QnGDLp0E0GQdq5o5ZtOZK5QXqEhW91M=; SPC_SI=tm+BZQAAAABweHVlSWhMM+VhMQAAAAAAZXVZSDFCTHo=; SPC_SEC_SI=v1-R1VwV0oxdThJY252SXNwN+BDq32bohJlo2CKrRLMId19k/T3qPEw4TcWN05o5702gG077NGb3iHpLyv1/xz/Toyb3zHN1HuIKKtcsWlxcvU=; _gid=GA1.3.2131002128.1703308089; _QPWSDCXHZQA=6ff78088-9721-4c8f-e04f-1230854551a9; REC7iLP4Q=79144663-9162-4594-bab9-0aed8f6dcc98; SPC_EC=.cTFUMG01bmVYUjNlUnowWCeKUs6By89FSrMZISBzc12KY9Rpw/OCAFWz4/9aCl/vdEiGjjqgN/cumr93D8jMBtOTn08a109Q81LcLOx9T+Xd9RK7f69DLPlKjaUY+9jghrZyUSYrrrFxYHP5VrHlB1IzpM1fKPCpsVCHw4Lu+hzdgMByMuc1A3Klq1U7mDHx2zDWDtkSNdtHhPOgTozhxw==; SPC_ST=.cTFUMG01bmVYUjNlUnowWCeKUs6By89FSrMZISBzc12KY9Rpw/OCAFWz4/9aCl/vdEiGjjqgN/cumr93D8jMBtOTn08a109Q81LcLOx9T+Xd9RK7f69DLPlKjaUY+9jghrZyUSYrrrFxYHP5VrHlB1IzpM1fKPCpsVCHw4Lu+hzdgMByMuc1A3Klq1U7mDHx2zDWDtkSNdtHhPOgTozhxw==; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.1.1415049999.1702613050; shopee_webUnique_ccd=zA9nFUFyS2gpnlwvgkRupA%3D%3D%7CPQvncVbnfTEU6oFgU65t4Ygg0InXo9%2BeQmWIDfIHkq%2By%2FP1%2FujHeomM8%2BXZU05ObLDh2HzOFLF0%3D%7CTp3j6nq7Hnj%2Fp8ZI%7C08%7C3; ds=8922018452b39d0a98576006fd8e6492; _ga_SW6D8G0HXK=GS1.1.1703364077.15.1.1703369155.57.0.0',
        '--compressed'
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)


def wait_to_checkout():
    try:
        driver = webdriver.Remote(f"http://127.0.0.1:4723", options=options)
        wait = WebDriverWait(driver, 7)
        rect = driver.get_window_size()
        center_x = rect['width'] // 2
        height = rect['height']
        swipe_start = height * 0.3
        swipe_end = height * 0.7

        wait.until(ec.visibility_of_element_located((By.ID, "com.shopee.id:id/cart_btn"))).click()
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "android.widget.ScrollView")))

        hold_time = int(exec_at - time.time() * 1000)
        hold_time = max(0, hold_time)
        driver.swipe(center_x, swipe_start, center_x, swipe_end, hold_time)
        print("CEK")

        wait.until(ec.visibility_of_element_located(
            (By.XPATH, "//android.view.ViewGroup[@resource-id=\"checkboxTouchableWrapper\"]"))).click()
        wait.until(ec.visibility_of_element_located(
            (By.XPATH, "//android.view.ViewGroup[@resource-id=\"buttonCheckout\"]"))).click()
        wait.until(ec.visibility_of_element_located(
            (By.XPATH, "//android.view.ViewGroup[@resource-id=\"buttonPlaceOrder\"]"))).click()
        wait.until(ec.visibility_of_element_located((By.XPATH,
                                                     "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup[5]/android.view.ViewGroup"))).click()
    except Exception as e:
        print(e)


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        [executor.submit(f) for f in [wait_to_add_cart, wait_to_checkout]]


def adb_shell(command):
    try:
        result = subprocess.run(['adb', 'shell'] + command, capture_output=True, text=True, check=True)
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Error Output: {e.stderr}")


if __name__ == '__main__':
    device_name = get_device_name()
    if len(device_name) <= 0:
        print("adb device is not set, use 'python device your-adb-device'")
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("productModel", help="shopId-itemId-modelId", type=str)
        parser.add_argument("executionTime", help="year-month-day-hour-minute-second", type=str)
        args = parser.parse_args()

        arg_model = args.productModel.split('-')
        arg_time = list(map(int, args.executionTime.split('-')))

        shop_id, item_id, model_id = arg_model[0], arg_model[1], arg_model[2]
        yyyy, ee, dd, hh, mm, ss = arg_time[0], arg_time[1], arg_time[2], arg_time[3], arg_time[4], arg_time[5]

        exec_at = int(datetime(yyyy, ee, dd, hh, mm, ss).timestamp() * 1000)
        capabilities = {
            "platformName": "android",
            "appium:deviceName": device_name,
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": "com.shopee.id",
            "appium:appActivity": "com.shopee.app.ui.home.HomeActivity_",
            "appium:noReset": True,
            "appium:shouldTerminateApp": True,
            "appium:disableWindowAnimation": True,
            "autoGrantPermissions": True,
            "autoAcceptAlerts": True
        }
        options = UiAutomator2Options().load_capabilities(capabilities)

        if exec_at - (time.time() * 1000) <= 0:
            print("Expired")
        else:
            main()
            # adb_shell(['am', 'start', '-n', "'com.shopee.id'/'com.shopee.app.react.ReactActivity_'"])
