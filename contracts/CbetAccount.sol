pragma solidity ^0.5.0;

contract CbetAccount {
    address payable cbetAccountOwnerAddr;

    modifier onlyOwner {
        require(msg.sender == cbetAccountOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    constructor (address payable _cbetAccountOwnerAddr) 
        public 
    {
        cbetAccountOwnerAddr = _cbetAccountOwnerAddr;
    }

    function getBalanceCbetAccountEther(address payable _cbetAccountWalletAddr) 
        public 
        view
        onlyOwner 
        returns (uint) 
    {
        return _cbetAccountWalletAddr.balance;
    }
    
    function() 
        external 
        payable 
        onlyOwner 
    {}    
}
