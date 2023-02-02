pragma solidity ^0.5.0;

// Container class to hold account related information for the user/bettor
//    - Will be able to dynamically add new users

contract UserAccounts {
    address payable cbetAccountOwnerAddr;    // BlockWager contract owner address

    // Balance of ETHER and CBET (custom) tokens
    struct Balance {
        uint eth;
        uint tokens;
    }

    // Per account information
    struct UserAccountParams {
        bool activeAccount;
        string firstName;
        string lastName;
        string username;
        string password;
        Balance balance;
    }

    mapping(address => UserAccountParams) userAccounts;  // // Mapping between better wallet address and CBET accounts

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

    // Create a new user/better
    function createUserAccount(address payable _addr,
                                 string memory _firstName, string memory _lastName,
                                 string memory _username, string memory _password)
        public
        onlyOwner
    {
        require (userAccounts[_addr].activeAccount == false, "This account is already active");

        userAccounts[_addr].activeAccount = true;
        userAccounts[_addr].firstName = _firstName;
        userAccounts[_addr].lastName = _lastName;
        userAccounts[_addr].username = _username;
        userAccounts[_addr].password = _password;
        userAccounts[_addr].balance.eth = 0;
        userAccounts[_addr].balance.tokens = 0;
    }

    // Getter function to get the user accounts name (first and last) given the wallet address of the user
    function getUserAccountName(address _addr)
        public
        view
        onlyOwner
        returns(string memory, string memory)
    {
        return (userAccounts[_addr].firstName, userAccounts[_addr].lastName);
    }

    // Getter function to get the users username given the wallet address of the user
    function getUserAccountUsername(address _addr)
        public
        view
        onlyOwner
        returns(string memory)
    {
        return (userAccounts[_addr].username);
    }

    // Getter function to get the users password given the wallet address of the user
    function getUserAccountPassword(address _addr)
        public
        view
        onlyOwner
        returns(string memory)
    {
        return (userAccounts[_addr].password);
    }

    // Gettor function to check if a user account is active (which can be activated/de-activated dynamically by the BlockWager contract owner)
    function isUserAccountActive(address _addr)
        public
        view
        onlyOwner
        returns (bool)
    {
        return userAccounts[_addr].activeAccount;
    }

    // Set by the BlockWager account owner to deactivate a users account
    function setBetterAccountInactive(address payable _addr)
        public
        onlyOwner
    {
        require (userAccounts[_addr].activeAccount == true, "This account is already inactive");
        userAccounts[_addr].activeAccount = false;
    }

    // Set by the BlockWager account owner to (re)activate a users account
    function setBetterAccountActive(address payable _addr)
        public
        onlyOwner
    {
        require (userAccounts[_addr].activeAccount == false, "This account is already active");
        userAccounts[_addr].activeAccount = true;
    }

    // Allow the user/user to deposit ETHER into the CBET account to be used for betting
    function depositUserAccountEther(address payable _cbetAccountWalletAddr)
        public
        payable
    {
        require (msg.sender != _cbetAccountWalletAddr, "The Cbet account is not allowed to deposit ether to itself");
        require (userAccounts[msg.sender].activeAccount == true, "This account is not active");
        userAccounts[msg.sender].balance.eth += msg.value;  // Keep local track of the amount of ETHER in the CBET account/wallet that belongs to this user
        _cbetAccountWalletAddr.transfer(msg.value);  // Transfer ETEHR from the user (msg.sender) to the CBET account/wallet (_cbetAccountWalletAddr)
    }

    // Allow the user/bettor to withdraw ETHER from the CBET account
    // ToDo: only ETHER that is not being used in active betting will be allowed to be withdrawn
    function withdrawUserAccountEther(address payable recipient)
        public
        payable
    {
        require (userAccounts[recipient].activeAccount == true, "This account is not active");
        userAccounts[recipient].balance.eth -= msg.value;  // Keep local track of the amount of ETHER in the CBET account/wallet that belongs to this user
        recipient.transfer(msg.value); // Transfer ETHER from the CBET account/wallet (msg.sender) to the user/bettor account (recipient)
    }

    // Getter function to get the local ETHER balance for a specific user/better (based the caller msg.sender address)
    function getBalanceUserAccountEther()
        public
        view
        returns (uint)
    {
        require (userAccounts[msg.sender].activeAccount == true, "This account is not active");
        return userAccounts[msg.sender].balance.eth;
    }

    function()
        external
        payable
        onlyOwner
    {}
}


