pragma solidity ^0.5.0;

contract CbetAccount {
    address payable cbetAccountOwnerAddr;
    address payable cbetAccountWalletAddr;

    modifier onlyOwner {
        require(msg.sender == cbetAccountOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    constructor (address payable _cbetAccountOwnerAddr) 
        public 
    {
        cbetAccountOwnerAddr = _cbetAccountOwnerAddr;
    }

    function setCACbetAccountWalletAddr(address payable _cbetAccountWalletAddr)
        public
        onlyOwner
    {
        require (msg.sender != _cbetAccountWalletAddr, "The escrow account cannot be the same address as contract account");
        cbetAccountWalletAddr = _cbetAccountWalletAddr;
    }

    function getBalanceCbetAccountEther() 
        public 
        view
        onlyOwner 
        returns (uint) 
    {
        return cbetAccountWalletAddr.balance;
    }
    
    function() 
        external 
        payable 
        onlyOwner 
    {}    
}
