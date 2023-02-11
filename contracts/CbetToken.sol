pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

contract CbetToken {
    // (Note, cannot inherit from ERC20 contracts due to the deployment of the contract size has breached upper limit.  
    //  ToDo future work to optimzize contract)
    address payable cbetAccountOwnerAddr;

    string public name;
    string public symbol;

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

        // Mint the initial supply to the account owner
        mint(_cbetAccountOwnerAddr, _cbetAccountOwnerAddr, _initialSupply);
    }

    // Balance of tokens from the user account/address
    function balance(address _addr) 
        public 
        view 
        returns(uint) 
    {
        return balances[_addr];
    }

    // Transfer tokens from one sender account to the recepient account
    function transferOf(address _sender, address _recipient, uint _value) 
        public 
    {
        balances[_sender] -= _value;
        balances[_recipient] += _value;
    }

    // Mint additional CBET tokens (owner mints) and send transfer it to users/bettors wallet (recipient)
    function mint(address _sender, address _recipient, uint _value) 
        public 
        payable 
    {
        require(_sender == cbetAccountOwnerAddr, "You do not have permission to mint these tokens!");

        balances[_recipient] += _value;
    }

}
