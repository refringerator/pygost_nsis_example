# Пример подписания электронных сообщений и проверки подписи на основе отправки договора

> [!CAUTION]
> Не предназначено для использования на проде
> Это просто пример на замену постман-коллекции


### Используемые библиотеки
1. Для работы с криптографией используется библиотека [PyGOST](http://www.pygost.cypherpunks.ru/)
Установка библиотеки описана на странице [PyGOST - Download](http://www.pygost.cypherpunks.ru/Download.html)
2. [Requests](https://docs.python-requests.org/en/latest/index.html) - для отправки http-запросов

### Пример отправки договора
#### Подготовка окружения
Скрипт должен работать с версией python>=3.8
1. Подготовить виртуальное окружение, чтобы все зависимые пакеты устанавливались в него
```shell
python -m venv venv
```
2. Активировать виртуальное окружение
```shell
source venv/bin/activate
```
3. Установить библиотеку `pygost` как написано в [инструкции](http://www.pygost.cypherpunks.ru/Download.html) (скачать, распаковать, запустить setup)
4. Установить библиотеку `requests`
```shell
pip install requests
```

#### Предварительные настройки
В файле config.py нужно указать свои данные
- имя пользователя и пароль АИС
- идентификатор своего сертификата
- значение приватного ключа
можно посмотреть командой, если у вас ключ в PEM формате 
`openssl pkey -engine gost -inform PEM -in key.pem -text`
#### Запуск скрипта
```shell
python main.py
```

#### Пример результата выполнения
<details>

<summary>Пример результата выполнения</summary>

```
CONTRACT RESPONSE
 202 Accepted 
 {"requestId":"00000000-0000-0000-c8f4-299d9e0a37cd","wait":0}

cert_id='d38fc7dd-8834-48ee-ad69-6b6cdb65c28c'
salt='24423acf-44ce-41ef-8dde-c0519e4a2d04'
ts='2024-03-20T23:04:08.193+03:00'
signature='R8S/CXfiaHnClu1GmfrJTtWScPMCPqJSe1/Ju2mvlEuvOFTUD1+SxbUCGApsyCZ1TnHF/R+MonM35AIn2DIKxw=='
RESPONSE SIGNATURE: valid

RESULT RESPONSE
 200 OK 
 {"requestId":"00000000-0000-0000-c8f4-299d9e0a37cd","responseId":"4438c10b-4324-312c-8be7-1d2a39aca641","statusCode":3,"lastModified":"2024-03-20T20:04:09.192Z","wait":0,"errors":[{"code":"61001273","description":"Не заполнено поле «Масса без нагрузки, кг»","isCritical":false,"exceptionCode":"0","path":"object.vehicle.vehicleDoc"},{"code":"61001275","description":"Не заполнено поле «Цвет ТС»","isCritical":false,"exceptionCode":"0","path":"object.vehicle.vehicleDoc"}],"subjectObjectCheckResults":[{"mdmFoundIndicator":"true","documentCheckStatuses":[{"documentType":"IdentityCard","foivFoundIndicator":"undefined","mdmFoundIndicator":"true","mdmCheckedIndicator":"true","foivCheckedIndicator":"undefined"},{"documentType":"DriverLicense","foivFoundIndicator":"undefined","mdmFoundIndicator":"true","mdmCheckedIndicator":"true","foivCheckedIndicator":"undefined"}],"path":"object.parties[0].person"},{"mdmFoundIndicator":"true","documentCheckStatuses":[{"documentType":"VehicleDocument","foivFoundIndicator":"undefined","mdmFoundIndicator":"true","mdmCheckedIndicator":"true","foivCheckedIndicator":"undefined"}],"path":"object.vehicle"},{"mdmFoundIndicator":"true","documentCheckStatuses":[{"documentType":"IdentityCard","foivFoundIndicator":"undefined","mdmFoundIndicator":"true","mdmCheckedIndicator":"true","foivCheckedIndicator":"undefined"}],"path":"parties[0].person"}],"processingResult":{"requestType":"Contract","internalIds":{"contractId":"a17b73ce-c461-3c4b-8008-d6a2bb0d35e4"},"insuranceContract":{"contractNumber":"PND1710965046"},"parties":[{"partyType":"Person","person":{"primaryRecordId":1105686470}}],"object":{"objectId":"4d2cdeb3-e20f-363b-b8a6-e0b77184c4c6","vehicle":{"primaryRecordId":1048467606},"parties":[{"partyType":"Person","person":{"primaryRecordId":1105686469}}]},"statusCode":"2"}}

cert_id='d38fc7dd-8834-48ee-ad69-6b6cdb65c28c'
salt='3ef8135f-15ba-4a4c-8a84-b5866f650872'
ts='2024-03-20T23:04:10.55+03:00'
signature='byplHMPSNAFc528p/8l20ghKdTrblwlj9FQi7BORzBLbVONgW9xofaA0AYQG69lGqcmzovWHi3jqnKXYbJtulA=='
RESPONSE SIGNATURE: valid
```

</details>
