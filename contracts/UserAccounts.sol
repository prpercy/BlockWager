pragma solidity ^0.5.0;

// Container class to hold account related information for the user
//    - Will be able to dynamically add new users

import "./CbetToken.sol";
import "./PlaceBets.sol";

// Commenting out since inherited from ERC20
//import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

contract UserAccounts is CbetToken {
    address payable cbetOwnerAddr;      // BlockWager contract owner address
    address payable cbetBettingAddr;    // BlockWage betting account (users must first deposit/withdrawal into this account before betting)

    using SafeMath for uint;

    // Balance of ETHER and CBET (custom) tokens
    struct Balance {
        uint eth;
        uint token;
    }

    // Per account information data structure
    struct UserAccountParams {
        bool activeAccount;
        Balance bettingBalance;
        Balance escrowBalance;
    }

    Balance houseBettingBalance;    // Balance of user betting accounts 
    Balance houseEscrowBalance;     // Balance of escrow accounts (funds actively involved in betting)

    mapping(address => UserAccountParams) userAccounts;  // // Mapping between better wallet address and CBET accounts

    uint WEI_FACTOR = 10**18;

    modifier onlyOwner {
        require(msg.sender == cbetOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    modifier onlyHouse {
        require(msg.sender == cbetBettingAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    // Construct which sets up the BlockWager contract owner address
    constructor (address payable _contractOwnerAddr)
        CbetToken(msg.sender, 200*WEI_FACTOR)   // Owner will initially mint 200 CBET tokens
        public
    {
        cbetOwnerAddr = _contractOwnerAddr;
        
        // Initialize all house (i.e. total of all user accounts) balances

        houseBettingBalance.eth = 0;                  
        houseBettingBalance.token = 0;  
        
        houseEscrowBalance.eth = 0;                  
        houseEscrowBalance.token = 0;                          
    }

    // Configure the address of the wallet (betting account) that will hold the ether/tokens
    // (Note, this would usually be placed in the constructur, but since the addresses from Ganache are dynamic, will be passed in as
    //        a parameter from the streamlit app)
    function setCbetBettingAddrUserAccounts(address payable _cbetBettingAddr)
        internal
        onlyOwner
    {
        cbetBettingAddr = _cbetBettingAddr;

        if (houseBettingBalance.token < 100*WEI_FACTOR)
        {
            mint(cbetOwnerAddr, msg.sender, 100*WEI_FACTOR);
            houseBettingBalance.token += 100*WEI_FACTOR;
            transferOf(cbetOwnerAddr, cbetBettingAddr, 100*WEI_FACTOR);
        }

    }

    // Create a new user account
    function createUserAccount(address payable _addr)
        public
        onlyOwner
    {
        require (userAccounts[_addr].activeAccount == false, "This account is already active");

        userAccounts[_addr].activeAccount = true;
        userAccounts[_addr].bettingBalance.eth = 0;
        userAccounts[_addr].bettingBalance.token = 0;
        userAccounts[_addr].escrowBalance.eth = 0;
        userAccounts[_addr].escrowBalance.token = 0;
    }

    // Getter function to check if a user account is active (which can be activated/de-activated dynamically by the BlockWager contract owner)
    function isUserAccountActive(address _addr)
        public
        view
        onlyOwner
        returns (bool)
    {
        return userAccounts[_addr].activeAccount;
    }

    // Allow the user to purchase CBET Tokens
    function purchaseCbetTokens()
        public
        payable
    {
        require (userAccounts[msg.sender].activeAccount == true, "This account is not active");

        // Need to mint the tokens to the users account
        mint(cbetOwnerAddr, msg.sender, msg.value);
        cbetBettingAddr.transfer(msg.value);
    }

    // Allow the user to sell CBET tokens
    function sellCbetTokens(address payable _addr)
        public
        payable
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        // Need to remove the tokens from the open token pool (unmint)
        transferOf(_addr, cbetBettingAddr, msg.value);
        houseBettingBalance.token = houseBettingBalance.token.add(msg.value);
        _addr.transfer(msg.value);
    }

    // Getter function to find the CBET token balance for a particular user
    function balanceCbetTokens(address payable _addr)
        public
        view
        returns (uint)
    {
        return balance(_addr);
    }

    // Allow the user to deposit ether into the betting account (to be used for betting in the future)
    function depositIntoBettingEther()
        public
        payable
    {
        require (msg.sender != cbetBettingAddr, "The Cbet account is not allowed to deposit ether to itself");
        require (userAccounts[msg.sender].activeAccount == true, "This account is not active");

        // Keep local track of the amount of ether in the betting account
        userAccounts[msg.sender].bettingBalance.eth = userAccounts[msg.sender].bettingBalance.eth.add(msg.value);
        // Keep track of the house (total) betting account ether balance
        houseBettingBalance.eth = houseBettingBalance.eth.add(msg.value);
        cbetBettingAddr.transfer(msg.value);   // Transfer ether from the user to the betting account 
    }

    // Allow the suer to deposit cbet custom tokens into the betting account (to be used for betting in the future)
    function depositIntoBettingToken(address payable _addr, uint _value)
        public
        payable
    {
        require (_addr != cbetBettingAddr, "The Cbet account is not allowed to deposit ether to itself");
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        // Keep local track of the amount of tokens in the betting account
        userAccounts[_addr].bettingBalance.token = userAccounts[_addr].bettingBalance.token.add(_value);
        houseBettingBalance.token = houseBettingBalance.token.add(_value); // Keep track of the house (total) betting account token balance
        transferOf(_addr, cbetBettingAddr, _value); // Transfer tokens from the user to the betting account 
    }

    // Allow the user to withdraw ether from the betting account
    function withdrawFromBettingEther(address payable recipient)
        public
        payable
    {
        require (userAccounts[recipient].activeAccount == true, "This account is not active");

        // Keep local track of the amount of ether in the betting account
        userAccounts[recipient].bettingBalance.eth = userAccounts[recipient].bettingBalance.eth.sub(msg.value);
        // Keep track of the house (total) betting account ether balance
        houseBettingBalance.eth = houseBettingBalance.eth.sub(msg.value);
        recipient.transfer(msg.value);                            // Transfer ether from the betting account to the user account
    }

    // Allow the user to withdraw tokens from the betting account
    function withdrawFromBettingToken(address payable recipient, uint _value)
        public
        payable
    {
        require (userAccounts[recipient].activeAccount == true, "This account is not active");

        // Keep local track of the amount of tokens in the betting account
        userAccounts[recipient].bettingBalance.token = userAccounts[recipient].bettingBalance.token.sub(_value);
        // Keep track of the house (total) betting account tokens balance
        houseBettingBalance.token = houseBettingBalance.token.sub(_value);
        transferOf(cbetBettingAddr, recipient, _value);  // Transfer tokens from the betting account to the user account
    }

    // When a game is bet on, need to transfer the ether/tokens to an escrow account (not to be touched until the conlusion of the game)
    function transferBettingToEscrow(address payable _addr, uint _value, bool _isEther)
        public
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        // Check if betting with ether or tokens...
        if (_isEther)
        {
            // Transfer the ether from betting account to escrow account
            // Remove ether to betting account...
            userAccounts[_addr].bettingBalance.eth = userAccounts[_addr].bettingBalance.eth.sub(_value);
            houseBettingBalance.eth = houseBettingBalance.eth.sub(_value);
            // Add ether from escrow account...
            userAccounts[_addr].escrowBalance.eth = userAccounts[_addr].escrowBalance.eth.add(_value);
            houseEscrowBalance.eth = houseEscrowBalance.eth.add(_value);
        } else 
        {
            // Transfer the tokens from betting account to escrow account
            userAccounts[_addr].bettingBalance.token -= _value;     // Remove tokens to betting account...
            houseBettingBalance.token -= _value;
            userAccounts[_addr].escrowBalance.token += _value;      // Add tokens from escrow account...         
            houseEscrowBalance.token += _value;
        }
    }

    // When a game is over, will need to transfer the escrow eth/tokens back into the betting account
    function transferEscrowBackToBetting(address payable _addr, uint _value, bool _isEther)
        public
        payable
        onlyHouse
    {
        require (((userAccounts[_addr].activeAccount == true) ||
                  (_addr == cbetOwnerAddr)), "This account is not active");

        // Check if betting with ether or tokens...
        if (_isEther)
        {
            // Transfer ether from escrow account back to the betting account
            userAccounts[_addr].bettingBalance.eth += _value;       // Add ether to betting account...
            houseBettingBalance.eth +=_value;
            userAccounts[_addr].escrowBalance.eth -= _value;        // Remove ether from escrow account..
            houseEscrowBalance.eth -= _value;
        } else 
        {
            // Transfer tokens from escrow account back to the betting account
            userAccounts[_addr].bettingBalance.token += _value;     // Add tokens to betting account...
            houseBettingBalance.token += _value;
            userAccounts[_addr].escrowBalance.token -= _value;      // Remove tokens from escrow account...          
            houseEscrowBalance.token -= _value;
        }
    }

    // When a user wins a bet, need to transfer ether or tokens to the user virtual accounts.
    function transerWinningsFromBettingToUser(address payable _addr, uint _value, bool _isEther)
        public
        payable
        //onlyHouse
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");
        
        if (_isEther)
        {
            userAccounts[_addr].bettingBalance.eth += _value;
        }
        else
        {
            userAccounts[_addr].bettingBalance.token += _value;
        }
    }

    // At the conclusion of a betting game, required to remove the funds originally placed in escrow at the start of the bet
    function removeEscrowFromUser(address payable _addr, uint _value, bool _isEther)
        public
        payable
        onlyHouse
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        // Handle both ether and token betting scenarios
        if (_isEther)
        {
            userAccounts[_addr].escrowBalance.eth -= _value;        // Remove ether from escrow account..
            houseEscrowBalance.eth -= _value;
            // Keep the houseBettingBalance untouched (the betting escrow is not real, just a variable)
        }
        else
        {
            userAccounts[_addr].escrowBalance.token -= _value;      // Remove tokens from escrow account...          
            houseEscrowBalance.token -= _value;
            houseBettingBalance.token += _value;                    // For tokens, unlike ether, escrow is real, so need to move back to Betting
                                                                    // ToDo: Make ether and tokens similar approach (if have time)
        }
    }

    // Allow the user to withdraw tokens from the betting account
    function transferFromEscrowToOwnerToken(address payable _addr, uint _value)
        public
        payable
        onlyHouse
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        userAccounts[_addr].escrowBalance.token -= _value;      // Remove tokens from escrow account...          
        houseEscrowBalance.token -= _value;
    }

    // Getter function to get their ether/token balances from the betting account
    function getBalanceUserBetting(address payable _addr)
        public
        view
        returns (uint, uint)
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        return (userAccounts[_addr].bettingBalance.eth, userAccounts[_addr].bettingBalance.token);
    }

    // Getter function to get their ether/token balances from the betting account
    function getBalanceUserBettingEth(address payable _addr)
        public
        view
        returns (uint)
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        return userAccounts[_addr].bettingBalance.eth;
    }

    // Getter function to get their ether/token balances from the betting account
    function getBalanceUserBettingCbet(address payable _addr)
        public
        view
        returns (uint)
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        return userAccounts[_addr].bettingBalance.token;
    }

    // Getter function to get their ether/token balances from the escrow account
    function getBalanceUserEscrow(address payable _addr)
        public
        view
        returns (uint, uint)
    {
        require (userAccounts[_addr].activeAccount == true, "This account is not active");

        return (userAccounts[_addr].escrowBalance.eth, userAccounts[_addr].escrowBalance.token);
    }

    // Getter function to get the house (or total) ether/tokens currently sitting in the betting account
    function getBalanceHouseBetting()
        public
        view
        returns (uint, uint)
    {
        return (houseBettingBalance.eth, houseBettingBalance.token);
    }

    // Getter function to get the house (or total) ether/tokens currently sitting in the escrow account
    function getBalanceHouseEscrow()
        public
        view
        returns (uint, uint)
    {
        return (houseEscrowBalance.eth, houseEscrowBalance.token);
    }

    // When a bet is place by the user, will need to validate if the user has enough funds in the betting account to bet with.
    function CheckBettingFundsAvailability(address payable _addr, uint _betAmount, bool _isEther)
        internal
        view
        onlyOwner
    {
        uint userBalanceBetting;
        if (_isEther)
        {
            userBalanceBetting = getBalanceUserBettingEth(_addr);
        } else
        {
            userBalanceBetting = getBalanceUserBettingCbet(_addr);
        }
        require (userBalanceBetting >= _betAmount, "Do not have enough funds in betting account for this transaction");
    }

    function()
        external
        payable
        onlyOwner
    {}
}
