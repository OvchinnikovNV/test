// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./IERC20.sol";

contract MyWallet is Ownable {

    uint8 public commission;
    address private commissionAdress = 0xdD870fA1b7C4700F2BD7f44238821C26f7392148;

    event Received(address, uint);
    event CommissionChanged(uint8);

    constructor() {
        commission = 10;
        emit CommissionChanged(commission);
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    receive() external payable {
        emit Received(msg.sender, msg.value);
    }

    function sendETH(address payable _receiver, uint256 _amount) public onlyOwner {
        require(_amount >= commission, "Amount ETH too small");
        require(getBalance() >= _amount + _amount * commission / 100, "Not enough ETH");

        (bool sent, bytes memory data) = _receiver.call{value: _amount}("");
        require(sent, "Failed to send ETH");

        (sent, data) = commissionAdress.call{value: _amount * commission / 100}("");
        require(sent, "Failed to send commission");
    }

    function changeCommission(uint8 _commission) public onlyOwner {
        require(_commission <= 100, "Max commission is 100%");
        commission = _commission;
        emit CommissionChanged(commission);
    }

    function tokenBalance(address _token_address, address _owner) public view returns (uint256) {
        return IERC20(_token_address).balanceOf(_owner);
    }

    function tokenAllowance(address _token_address, address _owner, address _spender) public view returns (uint256) {
        return IERC20(_token_address).allowance(_owner, _spender);
    }

    function sendTokens(address _token_address, address _to, uint256 _amount) public onlyOwner returns (bool) {
        require(tokenAllowance(_token_address, address(this), _to) >= _amount, "Insuficient Allowance");
        return IERC20(_token_address).transfer(_to, _amount);
    }

    function tokenApprove(address _token_address, address _spender, uint256 _amount) public onlyOwner returns (bool) {
        return IERC20(_token_address).approve(_spender, _amount);
    }

}
