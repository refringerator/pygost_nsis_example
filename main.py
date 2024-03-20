import time
import json
import requests
from config import base_url, ais_username, ais_password, cert_id, proxies
from crypto import sign_data, verify_signature
from utils import ts, gen_uuid, pr

requests.packages.urllib3.disable_warnings()


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
    # Формируем подпись
    bin_request_body = generate_contract()
    url_contracts = "/api/policy/kasko/v1/contracts"
    timestamp = ts()
    salt = gen_uuid()

    bin_data = bin_request_body + bytes(salt + timestamp + url_contracts, "utf-8")
    signature = sign_data(bin_data)

    with requests.Session() as session:
        session.verify = False
        session.proxies = proxies
        session.headers["Content-Type"] = "application/json"
        session.headers["Accept-Encoding"] = "gzip, deflate, br"

        # Авторизация
        req_data = {"username": ais_username, "password": ais_password}
        resp = session.post(url=base_url + "/login", json=req_data)

        # pr('LOGIN\n', resp.text);

        # Отправка договора
        session.headers["X-Inssys-Salt"] = salt
        session.headers["X-Inssys-Timestamp"] = timestamp
        session.headers["X-Inssys-Signature"] = signature
        session.headers["X-Inssys-Certificate-Id"] = cert_id

        resp = session.post(url=base_url + url_contracts, data=bin_request_body)
        pr("CONTRACT RESPONSE\n", resp.status_code, resp.reason, "\n", resp.text)

        # Проверка полученной подписи
        check_response_signature(resp.headers, resp.content)

        resp_json = resp.json()
        requestId = resp_json["requestId"]

        time.sleep(2)

        # Проверка статуса отправленного договора
        url_part = f"/api/policy/kasko/v1/contracts?requestId={requestId}"
        timestamp = ts()
        salt = gen_uuid()
        signature = sign_data(bytes(salt + timestamp + url_part, "utf-8"))

        session.headers["X-Inssys-Salt"] = salt
        session.headers["X-Inssys-Timestamp"] = timestamp
        session.headers["X-Inssys-Signature"] = signature
        session.headers["X-Inssys-Certificate-Id"] = cert_id

        resp = session.get(url=base_url + url_part)
        pr("RESULT RESPONSE\n", resp.status_code, resp.reason, "\n", resp.text)

        # Проверка полученной подписи
        check_response_signature(resp.headers, resp.content)


if __name__ == "__main__":
    main()
