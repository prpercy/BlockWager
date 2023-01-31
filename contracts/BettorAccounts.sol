pragma solidity ^0.5.0;

contract BettorAccounts {
    address payable cbetAccountOwnerAddr;
    address payable cbetAccountWalletAddr;

    struct Balance {
        uint eth;
        uint tokens;
    }
 
    struct BettorAccountParams {
        bool activeAccount;
        string firstName;
        string lastName;
        string username;
        string password;
        Balance balance;
    }

    mapping(address => BettorAccountParams) bettorAccounts;

    modifier onlyOwner {
        require(msg.sender == cbetAccountOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    constructor (address payable _cbetAccountOwnerAddr) 
        public 
    {
        cbetAccountOwnerAddr = _cbetAccountOwnerAddr;
    }

    function setBACbetAccountWalletAddr(address payable _cbetAccountWalletAddr)
        public
        onlyOwner
    {
        require (msg.sender != _cbetAccountWalletAddr, "The escrow account cannot be the same address as contract account");
        cbetAccountWalletAddr = _cbetAccountWalletAddr;
    }

    function createBettorAccount(address payable _addr, 
                                 string memory _firstName, string memory _lastName,
                                 string memory _username, string memory _password)
        public
        onlyOwner
    {
        require (bettorAccounts[_addr].activeAccount == false, "This account is already active");

        bettorAccounts[_addr].activeAccount = true;
        bettorAccounts[_addr].firstName = _firstName;
        bettorAccounts[_addr].lastName = _lastName;
        bettorAccounts[_addr].username = _username;
        bettorAccounts[_addr].password = _password;
        bettorAccounts[_addr].balance.eth = 0;
        bettorAccounts[_addr].balance.tokens = 0;
    }

    function getBettorAccountName(address _addr)
        public
        view
        onlyOwner
        returns(string memory, string memory)
    {
        return (bettorAccounts[_addr].firstName, bettorAccounts[_addr].lastName);
    }

    function getBettorAccountUsername(address _addr)
        public
        view
        onlyOwner
        returns(string memory)
    {
        return (bettorAccounts[_addr].username);
    }

    function getBettorAccountPassword(address _addr)
        public
        view
        onlyOwner
        returns(string memory)
    {
        return (bettorAccounts[_addr].password);
    }

    function isBettorAccountActive(address _addr)
        public
        view
        onlyOwner
        returns (bool)
    {
        return bettorAccounts[_addr].activeAccount;
    }

    function setBetterAccountInactive(address payable _addr)
        public
        onlyOwner
    {
        require (bettorAccounts[_addr].activeAccount == true, "This account is already inactive");
        bettorAccounts[_addr].activeAccount = false;
    }

    function setBetterAccountActive(address payable _addr)
        public
        onlyOwner
    {
        require (bettorAccounts[_addr].activeAccount == false, "This account is already active");
        bettorAccounts[_addr].activeAccount = true;
    }

    function depositBettorAccountEther() 
        public 
        payable 
    {
        require (msg.sender != cbetAccountWalletAddr, "The Cbet account is not allowed to deposit ether to itself");
        require (bettorAccounts[msg.sender].activeAccount == true, "This account is not active");
        bettorAccounts[msg.sender].balance.eth += msg.value;
        cbetAccountWalletAddr.transfer(msg.value);
    }

    function withdrawBettorAccountEther(address payable recipient) 
        public 
        payable 
    {
        //require (msg.sender != cbetAccountWalletAddr, "The Cbet account is not allowed to withdraw ether to itself");
        require (bettorAccounts[recipient].activeAccount == true, "This account is not active");
        bettorAccounts[recipient].balance.eth -= msg.value;
        recipient.transfer(msg.value);
    }

    function getBalanceBettorAccountEther() 
        public 
        view 
        returns (uint) 
    {
        require (bettorAccounts[msg.sender].activeAccount == true, "This account is not active");
        return bettorAccounts[msg.sender].balance.eth;
    }
    
    function() 
        external 
        payable 
        onlyOwner 
    {}    
}
