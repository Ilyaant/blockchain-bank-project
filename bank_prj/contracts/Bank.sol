// SPDX-License-Identifier: MIT
pragma solidity >=0.8.2 <0.9.0;
import "./CreditToken.sol";

// Контракт, реализующий функционал банка: возможность регистрации пользователя,
// взятия и возврата кредита пользователем в кастомных токенах
contract Bank {
    // структура, описывающая кредит
    struct Credit {
        uint256 currentSum; // сумма кредита
        uint256 months; // срок в месяцах
        uint256 totalSum; // сумма, которую надо выплатить
    }

    // структура, описывающая клиента
    struct Client {
        address payable id; // адрес клиента
        string login; // логин
        string password; // пароль
        uint256 balance; // баланс клиента
        Credit credit; // кредит, соответствующий данному клиенту
    }

    // uint256 constant percentageRate = 5; // процентная ставка
    uint256 private _storage; // количество токенов в контракте
    uint private numberClient; // количество клиентов
    address payable private owner; // адрес владельца контракта
    Client[] private clients; // массив клиентов
    CreditToken public token; // токен контракта

    // конструктор контракта
    constructor(address _token, uint256 startSum) {
        owner = payable(address(msg.sender));
        token = CreditToken(_token);
        token.mint(address(this), startSum);
        _storage = token.totalSupply();
    }

    // проверка, что зашел владелец контракта
    modifier checkOwner() {
        require(msg.sender == owner);
        _;
    }

    // события: регистрация, отказ в кредите и успешная выдача кредита
    event Register(address id, string message);
    event CreditDenied(address id, string message, address bank_address);
    event TakeCredit(address id, uint percent, uint sum, uint number_month);

    // регистрация нового клиента
    function register(
        string memory login,
        string memory password,
        uint256 startSum
    ) public {
        bool exists = false;

        // обработка попытки регистрации существующего клиента
        for (uint i = 0; i < numberClient; i++) {
            require(clients[i].id != msg.sender);
            if (keccak256(bytes(clients[i].login)) == keccak256(bytes(login))) {
                emit Register(msg.sender, "This login already exists");
                exists = true;
                break;
            }
        }

        // регистрация нового клиента
        if (!exists) {
            emit Register(msg.sender, "Successfully registered");
            token.mint(msg.sender, startSum);
            clients.push(
                Client(
                    payable(address(msg.sender)),
                    login,
                    password,
                    startSum,
                    Credit(0, 0, 0)
                )
            );
            numberClient++;
        }
    }

    // сравнение логинов и паролей
    function checkClient(
        Client memory current,
        string memory login,
        string memory password
    ) private pure returns (bool) {
        return
            (keccak256(bytes(current.login)) == keccak256(bytes(login))) &&
            (keccak256(bytes(current.password)) == keccak256(bytes(password)));
    }

    // взятие кредита
    function takeCredit(
        string memory login,
        string memory password,
        uint256 num,
        uint256 month
    ) public {
        uint256 percentageRate = calcPercentageRate(num);
        for (uint i = 0; i < numberClient; i++) {
            if (checkClient(clients[i], login, password)) {
                if (_storage >= num && clients[i].credit.totalSum == 0) {
                    uint256 totalSum = calculateTotalSum(num, month);
                    if (
                        token.allowance(msg.sender, address(this)) >= totalSum
                    ) {
                        clients[i].balance += num;
                        clients[i].credit = Credit(num, month, totalSum);
                        _storage -= num;
                        token.transfer(clients[i].id, num);
                        emit TakeCredit(
                            msg.sender,
                            percentageRate,
                            clients[i].id.balance,
                            month
                        );
                        break;
                    } else {
                        emit CreditDenied(
                            clients[i].id,
                            "Bank cannot give you a credit (there is no allowance).",
                            address(this)
                        );
                    }
                } else {
                    emit CreditDenied(
                        clients[i].id,
                        "Bank cannot give you a credit (the sum of credit is too big)",
                        address(this)
                    );
                }
            }
        }
    }

    // возврат кредита
    function returnCredit(uint256 payment) public {
        uint256 total = 0;
        for (uint i = 0; i < numberClient; i++) {
            if (clients[i].id == msg.sender) {
                total = clients[i].credit.totalSum;
                if (total <= payment) {
                    clients[i].balance -= total;
                    token.transferFrom(msg.sender, address(this), total);
                    clients[i].credit = Credit(0, 0, 0);
                    _storage += total;
                } else {
                    token.transferFrom(msg.sender, address(this), payment);
                    clients[i].credit.totalSum -= payment;
                    clients[i].balance -= payment;
                    _storage += payment;
                }
                break;
            }
        }
    }

    function calcPercentageRate(uint256 sum) public pure returns (uint256) {
        uint256 percentageRate = 0;
        if (sum < 10) {
            percentageRate = 10;
        } else if (sum >= 10 && sum < 20) {
            percentageRate = 8;
        } else {
            percentageRate = 5;
        }
        return percentageRate;
    }

    // узнать сколько токенов в хранилище
    function getStorage() public view checkOwner returns (uint256) {
        return _storage;
    }

    // добавить в контракт токены
    function addToStorage(uint256 _value) public checkOwner {
        _storage += _value;
        token.mint(address(this), _value);
    }

    function calculateTotalSum(
        uint256 sum,
        uint256 months
    ) public pure returns (uint256) {
        uint256 percentageRate = calcPercentageRate(sum);
        return (sum * ((100 + percentageRate) ** months)) / (100 ** months);
    }

    function getBalance() public view returns (uint256) {
        return token.balanceOf(address(this));
    }

    function getClients() public view returns (Client[] memory) {
        Client[] memory cl = clients;
        return cl;
    }
}
