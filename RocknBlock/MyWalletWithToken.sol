// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract MyWallet {

    address private owner;
    uint256 public commission;
    address private commissionAdress = 0xdD870fA1b7C4700F2BD7f44238821C26f7392148;

    // token var
    string private name;
    string private symbol;
    uint256 private totalSupply;
    mapping(address => uint256) private balances;

    event Transfer(address indexed _sender, address indexed _receiver, uint256 _amount);

    constructor() {
        owner = msg.sender;
        commission = 10;

        name = "MyToken";
        symbol = "MTKN";
        totalSupply = 1100000;
        balances[address(this)] = 1000000;
        balances[owner] = 100000;
        emit Transfer(address(this), owner, balances[owner]);
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
        commission = new_commission;
    }

    receive() external payable {
        require(balances[address(this)] > 0, "Have no tokens");
        uint256 tokensPerEther = 10000;
        uint256 tokens = tokensPerEther * msg.value / 1000000000000000000;

        if (tokens > balances[address(this)]) {
            tokens = balances[address(this)];
            uint256 valueWei = tokens * 1000000000000000000 / tokensPerEther;
            (bool sent, bytes memory data) = msg.sender.call{value: msg.value - valueWei}("");
            require(sent, "Failed to return extra wei");
        }

        require(tokens > 0, "Not enough wei for token");
        balances[msg.sender] += tokens;
        balances[address(this)] -= tokens;
        emit Transfer(address(this), msg.sender, tokens);
    }

    function balanceOf(address account) public view returns (uint256) {
        return balances[account];
    }

    function transfer(address receiver, uint256 amount) public {
            require(balances[msg.sender] >= amount);
            balances[msg.sender] -= amount;
            balances[receiver] += amount;
            emit Transfer(msg.sender, receiver, amount);
    }

}

