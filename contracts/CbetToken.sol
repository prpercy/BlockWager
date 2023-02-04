pragma solidity ^0.5.0;

contract CbetToken {
    address payable cbetAccountOwnerAddr;

    string public name = "CBET";
    string public symbol = "CBET";
    uint public exchangeRate;

    uint totalSupply;

    mapping(address => uint) balances;  // Cbet token balance

    // Parameters passed into the constructor must be provided at deployment time
    // When deploy, token name, symbol, and decimals are automatically passed through
    constructor(address payable _cbetAccountOwnerAddr, uint _initialSupply)
        public
    {
        // cbetAccountOwnerAddr will be wallet/address who hit the deploy button
        cbetAccountOwnerAddr = _cbetAccountOwnerAddr;

        // Token properties
        name = "CbetToken";
        symbol = "CBET";    
        exchangeRate = 1;

        mint(_cbetAccountOwnerAddr, _cbetAccountOwnerAddr, _initialSupply);

        totalSupply = _initialSupply;
    }

    // Balance of tokens from the user account/address
    function balance(address _addr) 
        public 
        view 
        returns(uint) 
    {
        return balances[_addr];
    }

    // Transfer tokens from one account to the another
    function transferOf(address _sender, address _recipient, uint _value) 
        public 
    {
        balances[_sender] -= _value;
        balances[_recipient] += _value;
    }

    function mint(address _sender, address _recipient, uint _value) 
        public 
        payable 
    {
        require(_sender == cbetAccountOwnerAddr, "You do not have permission to mint these tokens!");

        uint amount = _value * exchangeRate;
        balances[_recipient] += amount;

        totalSupply += amount;
    }

    function unmint(address _sender, address _recipient, uint _value) 
        public 
        payable 
    {
        require(_sender == cbetAccountOwnerAddr, "You do not have permission to mint these tokens!");

        uint amount = _value * exchangeRate;
        balances[_recipient] -= amount;

        totalSupply -= amount;
    }

    function getTotalSupply(address _sender)
        public
        view
        returns(uint)
    {
        require(_sender == cbetAccountOwnerAddr, "You do not have permission to access the total token supply!");

        return totalSupply;
    }
}
