pragma solidity ^0.5.0;

// Container class to hold account related information for the user/bettor
//    - Will be able to dynamically add new users

contract BettorAccounts {
    address payable cbetAccountOwnerAddr;    // BlockWager contract owner address
    address payable cbetAccountWalletAddr;   // Address of wallet that will (temporarilty) hold funds that are deposited by the user/bettor to bet on

    // Balance of ETHER and CBET (custom) tokens
    struct Balance {
        uint eth;
        uint tokens;
    }

    // Per account information
    struct BettorAccountParams {
        bool activeAccount;
        string firstName;
        string lastName;
        string username;
        string password;
        Balance balance;
    }

    mapping(address => BettorAccountParams) bettorAccounts;  // // Mapping between better wallet address and CBET accounts

    modifier onlyOwner {
        require(msg.sender == cbetAccountOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    // Construct which sets up the BlockWager contract owner address
    constructor (address payable _cbetAccountOwnerAddr)
        public
    {
        cbetAccountOwnerAddr = _cbetAccountOwnerAddr;
    }

    // Assign the BlockWager contract owner address
    function setBACbetAccountWalletAddr(address payable _cbetAccountWalletAddr)
        public
        onlyOwner
    {
        require (msg.sender != _cbetAccountWalletAddr, "The escrow account cannot be the same address as contract account");
        cbetAccountWalletAddr = _cbetAccountWalletAddr;
    }

    // Create a new user/better
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

    // Getter function to get the user accounts name (first and last) given the wallet address of the user
    function getBettorAccountName(address _addr)
        public
        view
        onlyOwner
        returns(string memory, string memory)
    {
        return (bettorAccounts[_addr].firstName, bettorAccounts[_addr].lastName);
    }

    // Getter function to get the users username given the wallet address of the user
    function getBettorAccountUsername(address _addr)
        public
        view
        onlyOwner
        returns(string memory)
    {
        return (bettorAccounts[_addr].username);
    }

    // Getter function to get the users password given the wallet address of the user
    function getBettorAccountPassword(address _addr)
        public
        view
        onlyOwner
        returns(string memory)
    {
        return (bettorAccounts[_addr].password);
    }

    // Gettor function to check if a user account is active (which can be activated/de-activated dynamically by the BlockWager contract owner)
    function isBettorAccountActive(address _addr)
        public
        view
        onlyOwner
        returns (bool)
    {
        return bettorAccounts[_addr].activeAccount;
    }

    // Set by the BlockWager account owner to deactivate a users account
    function setBetterAccountInactive(address payable _addr)
        public
        onlyOwner
    {
        require (bettorAccounts[_addr].activeAccount == true, "This account is already inactive");
        bettorAccounts[_addr].activeAccount = false;
    }

    // Set by the BlockWager account owner to (re)activate a users account
    function setBetterAccountActive(address payable _addr)
        public
        onlyOwner
    {
        require (bettorAccounts[_addr].activeAccount == false, "This account is already active");
        bettorAccounts[_addr].activeAccount = true;
    }

    // Allow the user/bettor to deposit ETHER into the CBET account to be used for betting
    function depositBettorAccountEther()
        public
        payable
    {
        require (msg.sender != cbetAccountWalletAddr, "The Cbet account is not allowed to deposit ether to itself");
        require (bettorAccounts[msg.sender].activeAccount == true, "This account is not active");
        bettorAccounts[msg.sender].balance.eth += msg.value;  // Keep local track of the amount of ETHER in the CBET account/wallet that belongs to this user
        cbetAccountWalletAddr.transfer(msg.value);  // Transfer ETEHR from the user (msg.sender) to the CBET account/wallet (cbetAccountWalletAddr)
    }

    // Allow the user/bettor to withdraw ETHER from the CBET account
    // ToDo: only ETHER that is not being used in active betting will be allowed to be withdrawn
    function withdrawBettorAccountEther(address payable recipient)
        public
        payable
    {
        //require (msg.sender != cbetAccountWalletAddr, "The Cbet account is not allowed to withdraw ether to itself");
        require (bettorAccounts[recipient].activeAccount == true, "This account is not active");
        bettorAccounts[recipient].balance.eth -= msg.value;  // Keep local track of the amount of ETHER in the CBET account/wallet that belongs to this user
        recipient.transfer(msg.value); // Transfer ETHER from the CBET account/wallet (msg.sender) to the user/bettor account (recipient)
    }

    // Getter function to get the local ETHER balance for a specific user/better (based the caller msg.sender address)
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


