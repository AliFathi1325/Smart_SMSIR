from sms_ir import SmsIr

class SmartSMSir:

    def __init__(self, api: str, linenumber: str, adminnumber: str):
        self.connect = SmsIr(api, linenumber)
        self.linenumber = linenumber
        self.adminnumber = adminnumber
        self.credit = None

    def credit_check(self):
        response = self.connect.get_credit()
        try:
            response_data = response.json()
            if response_data.get('message') == 'موفق':
                self.credit = int(response_data.get('data')) - 1
                return True
            else:
                return False
        except ValueError:
            return False

    def send_sms(self, message: str):
        if self.credit is None:
            return False, "اعتبار بررسی نشده است."

        if self.credit <= 5:
            message += '\n\n' + f"از اعتبار شما {self.credit} عدد باقی مانده است.\nلطفا حساب خود را شارژ کنید."

        response = self.connect.send_sms(self.adminnumber, message, self.linenumber)
        try:
            response_data = response.json()
            if response_data.get('message') == 'موفق':
                return True, "پیام با موفقیت ارسال شد."
            else:
                return False, response_data.get('message')
        except ValueError:
            return False, "خطای ناشناخته در تجزیه پاسخ."