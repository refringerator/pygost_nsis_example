import base64
from pygost import gost34112012256
from pygost.gost3410 import CURVES
from pygost.gost3410 import sign, verify
from pygost.gost3410 import pub_unmarshal
from pygost.utils import hexdec
from config import private_key, nsis_public_key

# рабочие параметры B алгоритма подписи по ГОСТ Р 34.10-2012 с ключом 256
# он же id-GostR3410-2001-CryptoPro-A-ParamSet
# он же id-GostR3410-2001-CryptoPro-XchA-ParamSet
# он же id-tc26-gost-3410-2012-256-paramSetB
curve = CURVES["id-tc26-gost-3410-12-256-paramSetB"]

# Преобразуем приватный ключ из hex в int(long)
prv_key = int(private_key, 16)

# Открытый ключ для проверки
public_key = pub_unmarshal(hexdec(nsis_public_key))


def digest(bin_data: bytes):
    # Стрибог (ГОСТ Р 34.11-2012) 256 бит
    return gost34112012256.new(bin_data).digest()[::-1]


def sign_data(bin_data: bytes):
    # Рассчитываем хэш
    dgst = digest(bin_data)

    # Подписываем
    signature = sign(curve, prv_key, dgst)

    base64_sing = base64.b64encode(signature).decode("utf-8")
    return base64_sing


def verify_signature(signature: str, bin_data: bytes):
    sign = base64.b64decode(signature)
    dgst = digest(bin_data)
    return verify(curve, public_key, dgst, sign)
