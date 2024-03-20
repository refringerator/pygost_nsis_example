# идентификатор своего сертификата
cert_id = "d38fc7dd-8834-48ee-ad69-6b6cdb65c28c"

# открытый ключ НСИС
# взят из сертификата без начальных 0440
nsis_public_key = b"AE1E10FA859CC43CA3DDD2A808834FA4B1D573D2ABE0826F0DFBD837A5E7935D2205F00169A2D395B1B6919DBC54C7CFA2158AE80F819AE6A55143979FDBE254"

# Приватный ключ
private_key = "2205F00169A2D395B1B6919DBC54C7CFA2158AE80F819AE6A55143979FDBE254"

base_url = "https://gw-testnext.ins-sys.ru"
ais_username = "superuser_123"  # имя пользователя АИС
ais_password = "s3cr3tP@ss"  # пароль АИС

# Настройка прокси для запросов описана по ссылке
# https://docs.python-requests.org/en/latest/user/advanced/#proxies
proxies = None
