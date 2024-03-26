import time
import json
import requests
from config import base_url, ais_username, ais_password, cert_id, proxies
from crypto import sign_data, verify_signature
from utils import ts, gen_uuid, pr

requests.packages.urllib3.disable_warnings()


class CustomSession(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def request(self, method, url, **kwargs):
        kwargs2 = kwargs
        kwargs2.pop('allow_redirects', None)
        req = requests.Request(method, url, **kwargs2)
        r = req.prepare()
        self.before_request(r.body, method, url)

        return super().request(method, url, **kwargs)

    def before_request(self, body, method, url):
        # Формируем подпись перед каждым запросом
        url_contracts = url.replace(base_url, "")
        timestamp = ts()
        salt = gen_uuid()

        bts = bytes(salt + timestamp + url_contracts, "utf-8")
        bin_data = body + bts if body else bts

        signature = sign_data(bin_data)

        self.headers["X-Inssys-Salt"] = salt
        self.headers["X-Inssys-Timestamp"] = timestamp
        self.headers["X-Inssys-Signature"] = signature
        self.headers["X-Inssys-Certificate-Id"] = cert_id


def generate_contract() -> bytes:
    # Генерируем тело запроса договора
    cisContractId = gen_uuid()
    contractNumber = "PND" + str(int(time.time()))

    with open("request.json", "r") as file:
        json_data = json.load(file)
        json_data["internalIds"]["cisContractId"] = cisContractId
        json_data["insuranceContract"]["contractNumber"] = contractNumber

        return json.dumps(json_data).encode()


def check_response_signature(headers, body: bytes):
    signature = headers["X-Inssys-Signature"]
    salt = headers["X-Inssys-Salt"]
    ts = headers["X-Inssys-Timestamp"]
    cert_id = headers["X-Inssys-Certificate-Id"]

    bin_data = body + bytes(salt + ts, "utf-8")
    is_correct = verify_signature(signature, bin_data)

    print(f"{cert_id=}", f"{salt=}", f"{ts=}", f"{signature=}", sep="\n")
    pr(f'RESPONSE SIGNATURE: {"valid" if is_correct else "invalid"}')


def main():
    with CustomSession() as session:
        session.verify = False
        session.proxies = proxies
        session.headers["Content-Type"] = "application/json"
        session.headers["Accept-Encoding"] = "gzip, deflate, br"

        # Авторизация
        req_data = {"username": ais_username, "password": ais_password}
        resp = session.post(url=base_url + "/login", json=req_data)

        # pr('LOGIN\n', resp.text);

        # Отправка договора
        url_contracts = "/api/policy/kasko/v1/contracts"
        resp = session.post(url=base_url + url_contracts, data=generate_contract())
        pr("CONTRACT RESPONSE\n", resp.status_code, resp.reason, "\n", resp.text)

        # Проверка полученной подписи
        check_response_signature(resp.headers, resp.content)

        resp_json = resp.json()
        requestId = resp_json["requestId"]

        time.sleep(2)

        # Проверка статуса отправленного договора
        url_part = f"/api/policy/kasko/v1/contracts?requestId={requestId}"
        resp = session.get(url=base_url + url_part)
        pr("RESULT RESPONSE\n", resp.status_code, resp.reason, "\n", resp.text)

        # Проверка полученной подписи
        check_response_signature(resp.headers, resp.content)


if __name__ == "__main__":
    main()
