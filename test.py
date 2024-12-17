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

@dp.message()
    async def handle_text(message: types.Message):
        user_id = message.from_user.id
        if user_id not in user_data or message.text == '/start':
            await start(message)
        elif 'phone' not in user_data[user_id]:
            await send_code(message)
        elif 'status' not in user_data[user_id]:
            await check_code(message)
        elif 'location' not in user_data[user_id]:
            await info_location(message)
        elif 'kategoriyalar' in user_data[user_id]['holat']:
            await show_menu(message)
        elif 'tovarlar' in user_data[user_id]['holat']:
            await check_menu(message)
        elif 'tovar' in user_data[user_id]['holat']:
            await check_items(message)

 @dp.message(Command("start"))
    async def start(message: types.Message):
        user_id = message.from_user.id
        user_data[user_id] = {}
        button = [
            [types.KeyboardButton(text="Raqam jo'nastish", request_contact=True )]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        await message.answer("Assalomu alaykum! LesAiles yetkazib berish xizmatiga xush kelibsiz:", reply_markup=keyboard)
        print(user_data)

    async def send_code(message: types.Message):
        user_id = message.from_user.id
        i = '+1234567890'
        ok = True
        if message.contact is not None:
            phone_c = message.contact.phone_number
            user_data[user_id]["phone"] = phone_c
            ver_code = randint(100000, 999999)
            user_data[user_id]['verification_code'] = ver_code
            try:
                token = login_and_token(email, password)
                send_sms(token, phone_c)
                await message.answer(f"Nomeringizga tasdiqlash ko'di yuborildi\n"
                                 f"Iltimos kodni kiriting: {ver_code}")
            except Exception as ex:
                await message.answer(f"{ex}")
        elif len(message.text) == 13 and message.text[0:4] == '+998':
            for symbol in message.text:
            if symbol not in i:
                await message.answer('Hato nomer kiritildi')
                ok = False
                break

        if ok == True:
            phone = message.text
            user_data[user_id]["phone"] = phone
            verification_code = randint(10000, 99999)
            user_data[user_id]['verification_code'] = verification_code
            await message.answer(f"Nomeringizga tasdiqlash ko'di yuborildi\n"
                                 f"Iltimos kodni kiriting: {verification_code}")
    else:
        await message.answer("Hato nomer kiritildi")
    print(user_data)
