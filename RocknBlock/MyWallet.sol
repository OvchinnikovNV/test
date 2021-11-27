// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract MyWallet {

    address private owner;
    uint256 public commission;
    address private commissionAdress = 0xdD870fA1b7C4700F2BD7f44238821C26f7392148;

    constructor() {
        owner = msg.sender;
        commission = 10;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function getETH() public payable returns (uint256) {
        return msg.value;
    }

    function sendETH(address payable receiver, uint256 amount) public onlyOwner {
        require(amount >= commission, "Amount ETH too small");
        require(getBalance() >= amount + amount / commission, "Not enough ETH");

        (bool sent, bytes memory data) = receiver.call{value: amount}("");
        require(sent, "Failed to send ETH");

        (sent, data) = commissionAdress.call{value: amount / commission}("");
        require(sent, "Failed to send commission");
    }

    function changeCommission(uint new_commission) public onlyOwner {
        // require(new_commission <= 100, "Commision too big");
        commission = new_commission;
    }

}

