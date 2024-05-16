// SPDX-License-Identifier: MIT
pragma solidity >=0.8.2 <0.9.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Контракт, описывающий используемые в работе уникальные токены,
// которые можно взять в кредит. Токены описаны по стандарту ERC-20.
// Назначение токенов: виртуальная валюта, за которую можно купить виртуальные и
// NFT- ювелирные украшения и драгоценности. Соответственно, контракт Bank реализует
// возможность выдачи таких токенов в кредит
contract CreditToken is ERC20 {
    constructor(address initialOwner) ERC20("CreditToken", "CRT") {}

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }
}
