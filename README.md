# Blockchain Bank Project
Командная курсовая работа по дисциплине "Блокчейн-технологии" (09.04.03 Прикладная информатика, НИТУ МИСИС): Антонов И. А., Исаченко М. К., Парчиев Р. Б. Проект представляет собой прототип десктопного приложения для взаимодействия с блокчейн-банком.
## Стэк использованных инструментов
* Python
* Solidity
* Ganache
* Библиотеки PySimpleGUI, Brownie
## Описание файлов проекта
* **scripts/app.py**: основной файл приложения, содержащий код пользовательского интерфейса;
* **scripts/deploy.py**: код для деплоя смарт-контрактов;
* **scripts/interact.py**: код для проверки работы с контрактами;
* **brownie-config.yaml**: файл конфигурации для brownie;
* **contracts/Bank.sol**: код основного контракта, предоставляющего функционал выдачи и возврата кредитов;
* **contracts/CreditToken.sol**: код контракта, описывающего кастомный токен CreditToken (CRT), необходимый для покупки NFT ювелирных украшений и драгоценностей.
## Демонстрация работы с приложением
Начальное окно входа в систему выглядит следующим образом:

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/43c40a2d-7d7e-4d6a-9f48-2703604b54f1)

Здесь пользователю нужно ввести свой логин и пароль. В приложении зарегистрированы 3 аккаунта из тестовой сети, зайдем под логином и паролем *acc2* и попадем на главное окно:

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/aa7eccd2-c43b-4274-99ed-0e868c5b4d8e)

Здесь отображается текущий баланс пользователя и его задолженность в токенах CRT, а также присутствует возможность взять кредит или вернуть сумму в банк, если кредит взят. Нажав на кнопку "Взять кредит", попадаем в окно выдачи кредита:

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/a00689eb-2639-4c68-a5cc-bc1a08b3d61b)

Введем сумму кредита, количество месяцев, на которое хотим его взять, и нажмем "Рассчитать сумму":

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/0d4d3691-b371-494a-beb6-de3948eb55cf)

Приложение рассчитало, какую сумму на таких условиях будет необходимо вернуть в банк. Нажмем на кнопку "Взять кредит", выводится окно об успехе, и баланс на аккаунте становится на 50 CRT больше:

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/c84564f0-b5af-4ba5-a244-b77422c1bdc6)
![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/19f88ad5-0045-4f8f-af87-6d43c6a1e863)

Затем будем вносить платежи по кредиту. Из главного окна перейдем в соответствующий раздел по кнопке "Вернуть кредит":

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/1b94af20-f9e4-4ef7-9098-452a7c548db7)

Введем первую сумму платежа в размере 20 CRT и нажмем "Внести платеж":

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/3d3e2825-5a04-4c2b-b5bf-9c8cfd3b0fde)

Баланс уменьшился, как и сумма к погашению. Внесем оставшиеся токены:

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/f817cd36-1ff4-4b38-b2d2-10d9b8abe82b)
![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/2ad22304-974e-4cc9-b1b7-f73c8bc3cc79)

Задолженность клиента на главном окне снова составляет 0 CRT:

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/72f668e8-bda7-45f8-b6f3-7a7f5ccfa710)

Важно заметить, что если баланс клиента меньше, чем первый взнос по кредиту (сумма кредита, разделенная на количество месяцев), то в кредите ему будет откзано. Проверим это на аккаунте с нулевым балансом:

![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/b98a8201-4680-4b4d-a16b-a8dd2db3e52c)
![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/e7bd0075-a245-42dc-9718-1f8b776be16a)
![image](https://github.com/Ilyaant/blockchain-bank-project/assets/21258800/48d04107-67f5-434d-b6dc-82a2e8c28ea7)

Процентная ставка по кредиту рассчитывается следующим образом:
* если сумма меньше 10 CRT, ставка составляет 10%;
* если сумма от 10 CRT до 20 CRT, ставка составляет 8%;
* если сумма больше или равна 20 CRT, ставка составляет 5%.

## Инструкция по установке
1. Установить Ganache: https://archive.trufflesuite.com/ganache/
2. Установить библиотеку brownie: `pip install eth-brownie`
3. Установить библиотеку PySimpleGUI: `pip install pysimplegui`
4. Создать пустую папку и выполнить в ней `brownie init`
5. Копировать файлы контрактов из этого репозитория в папку `contracts/`
6. Копировать файлы скриптов из этого репозитория в папку `scripts/`
7. Копировать файл `brownie-config.yaml` в созданную папку проекта
8. Создать в папке проекта файл .env, в котором определить переменные `PRIVATE_KEY`, `PRIVATE_KEY1`, `PRIVATE_KEY2`, присвоив им приватные ключи 0-го, 1-го и 2-го адресов тестовой сети Ganache соответственно в формате `PRIVATE_KEY = "0x..."`
9. Выполнить `brownie compile` в папке проекта
10. Выполнить `brownie networks add Ethereum ganache-local host=http://127.0.0.1:7545 chainid=5777`, где `host` и `chainid` берутся из проекта Ganache.
11. Выполнить `brownie run scripts/deploy.py --network ganache-local`
12. Из вывода предыдущей команды скопировать адреса задеплоенных контрактов и заменить ими имеющиеся адреса в файлах `app.py` и `interact.py`
13. Выполнить `brownie run scripts/interact.py`
14. Установка завершена, для работы с программой запустить файл `app.py`
