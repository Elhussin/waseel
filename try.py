import requests
import json
from datetime import datetime, timedelta, timezone  # أضف timezone

# متغيرات لحفظ التوكن ووقت الانتهاء
access_token = None
refresh_token = None
token_expiry = None

# دالة لحفظ التوكن ووقت الانتهاء
def save_tokens(response):
    global access_token, refresh_token, token_expiry

    # حفظ التوكن
    access_token = response['access_token']
    refresh_token = response['refresh_token']

    # تحويل تاريخ انتهاء الصلاحية إلى كائن datetime
    expires_in = response['expires_in']  # تاريخ انتهاء الصلاحية
    token_expiry = datetime.strptime(expires_in, "%Y-%m-%dT%H:%M:%S.%f%z")

    # حفظ البيانات في ملف (اختياري)
    with open("tokens.json", "w") as file:
        json.dump({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_expiry": token_expiry.isoformat()
        }, file)

    print("Token save ")

# دالة لتحميل التوكن من ملف (اختياري)
def load_tokens():
    global access_token, refresh_token, token_expiry

    try:
        with open("tokens.json", "r") as file:
            tokens = json.load(file)
            access_token = tokens['access_token']
            refresh_token = tokens['refresh_token']
            token_expiry = datetime.fromisoformat(tokens['token_expiry'])

        # التحقق من صلاحية التوكن
        if is_token_valid():
            
            print("Token Upload Correct")
        else:
            print("Token is expired. Refreshing...")
            refresh_access_token()
    except FileNotFoundError:
        print("No token found")

# دالة للتحقق من صلاحية التوكن
def is_token_valid():
    if not access_token or not token_expiry:
        return False
    # جعل datetime.now() يحتوي على معلومات المنطقة الزمنية
    return datetime.now(timezone.utc) < token_expiry

# دالة لتحديث التوكن
def refresh_access_token():
    global access_token, refresh_token, token_expiry

    # عنوان API لتحديث التوكن
    url = 'https://api.stg-eclaims.waseel.com/oauth/refresh'  # تأكد من أن هذا هو الـ URL الصحيح

    # إرسال طلب لتحديث التوكن
    response = requests.post(url, json={"refresh_token": refresh_token})

    if response.status_code == 200:
        save_tokens(response.json())
        print("Update Token Done")
    else:
        print("Error to update token ", response.status_code)

# دالة للحصول على التوكن (تحديثه إذا انتهت صلاحيته)
def get_access_token():
    if not is_token_valid():
        print("Token not valid..")
        refresh_access_token()
    return access_token

# دالة لاختبار العملية
def test_api_request():
    # الحصول على التوكن
    token = get_access_token()

    # إرسال طلب API باستخدام التوكن
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # استخدم POST بدلاً من GET
    response = requests.post("https://api.eclaims.waseel.com/oauth/authenticate", headers=headers)

    if response.status_code == 200:
        print("Refresh data done", response.json())
    else:
        print("Error can not get ", response.status_code)

# دالة للحصول على التوكن
def getToken():
    # عنوان API
    url = 'https://api.eclaims.waseel.com/oauth/authenticate'

    # البيانات التي تريد إرسالها (بتنسيق JSON)
    body = {
        "username": "hsm01",
        "password": "opt666"
    }

    # إرسال طلب POST مع Body بتنسيق JSON
    response = requests.post(url, json=body)

    # التحقق من نجاح الطلب
    if response.status_code == 200:
        print("SEND")
        responseData = response.json()
        save_tokens(responseData)
        print("Response", response.json())
    else:
        print("Error", response.status_code)


def get_beneficiary_data(provider, patientKey, systemType, token):
    """
    دالة لجلب بيانات المستفيد من API باستخدام Bearer Token.
    :param provider: قيمة {{provider}}.
    :param patientKey: قيمة {{idKey}}.
    :param systemType: قيمة {{key}}.
    :param token: التوكن (Token) المستخدم في الرأس.
    :return: البيانات المستلمة من الـ API (إذا كانت الاستجابة ناجحة).
    """
    # بناء URL باستخدام المعلمات
    url = f"https://api.eclaims.waseel.com/beneficiaries/providers/{provider}/patientKey/{patientKey}/systemType/{systemType}"

    # إضافة التوكن إلى الرأس
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # إرسال طلب GET
    response = requests.get(url, headers=headers)
    # التحقق من نجاح الطلب
    if response.status_code == 200:
        # إرجاع البيانات كـ JSON
        return response.json()
    else:
        # طباعة رسالة خطأ
        print(f"فشل جلب البيانات. رمز الحالة: {response.status_code}")
        return None



import requests
import json

# دالة لإرسال البيانات
def send_eligibility_request(provider_id, data, auth_token):
    # عنوان الرابط مع استبدال {{PROVIDERID}} بالقيمة الممررة
    url = f"https://api.qa-eclaims.waseel.com/eligibilities/providers/{provider_id}/request"
    
    # إعداد الترويسة (Headers)
    headers = {
        "Content-Type": "application/json",  # تحديد نوع المحتوى
        "Authorization": f"Bearer {auth_token}"  # إرسال التوكن في الترويسة
    }

    try:
        # إرسال طلب POST مع البيانات
        response = requests.post(url, headers=headers, json=data)
        
        # التحقق من حالة الاستجابة
        if response.status_code == 200:
            print("Request successful!")
            print("Response Data:", response.json())
        else:
            print(f"Error: {response.status_code}")
            print("Response:", response.json())
    except Exception as e:
        print("An error occurred:", str(e))
        
        


# مثال استخدام
if __name__ == "__main__":
    # تحميل التوكن إذا كان محفوظًا مسبقًا
    load_tokens()
    # إذا لم يتم تحميل التوكن، قم بالحصول على توكن جديد
    if not access_token or not refresh_token:
        getToken()

    # اختبار إرسال طلب API
    # test_api_request()
    
    provider = "917"
    patientKey = "2307701827"
    systemType = 1
    token =access_token  # استبدل هذا بالتوكن الفعلي

    # جلب البيانات
    data = get_beneficiary_data(provider, patientKey, systemType, token)


    provider_id = "12345"  # استبدل بـ ID الخاص بالمزود
    auth_token = "your_access_token_here"  # استبدل بالتوكن الخاص بك
    send_eligibility_request(provider, data, token)
    # طباعة البيانات إذا كانت موجودة
    # if data:
    #     print("البيانات المستلمة:", data)
