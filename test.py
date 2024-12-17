TOKEN = "7255549730:AAHHL7OmAAAmibmtzBsLG_9DNYCsyXpjndA"
bot = Bot(token=TOKEN)
dp = Dispatcher()
user_data = {}
email = 'orzu9083@gmail.com'
password = 'aqQynXFpbW7CSOCDcOj4QzLk2kro0plEr8UyOVWZ'

def login_and_token(email, password):
    url = "https://notify.eskiz.uz/api/auth/login"
    payload = {
        'email': email,
        'password': password
    }
    files = []
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        token = response.json()['data']['token']
        return token
    else:
        print('token kelmadi')

def send_sms(token, phone):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    payload = {
        'mobile_phone': phone,
        'message': 'Bu Eskiz dan test',
        'from': '4546',
        'callback_url': 'http://0000.uz/test.php'
    }
    files = []
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        raise "SMS yuborishda xatolik"

