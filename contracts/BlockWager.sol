pragma solidity ^0.5.0;

// Container class to hold account related information for the user
//    - Will be able to dynamically add new users

import "./UserAccounts.sol";
import "./PlaceBets.sol";

contract BlockWager is UserAccounts, PlaceBets {
    address payable cbetOwnerAddr;      // BlockWager contract owner address
    address payable cbetBettingAddr;    // BlockWage betting account (users must first deposit/withdrawal into this account before betting)

    modifier onlyOwner {
        require(msg.sender == cbetOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    // Construct which sets up the BlockWager contract owner address
    constructor ()
        UserAccounts(msg.sender)
        PlaceBets(msg.sender)
        public
    {
        cbetOwnerAddr = msg.sender;                   
    }

    function createMoneylineBet(uint _betId, string memory _sportbook, string memory _team, int _odds, 
                                address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        //CheckBettingFundsForBetting(_addr, _betAmount, _isEther);
        createMoneylineBetInternal(_betId, _sportbook, _team, _odds, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);
    }

    function createSpreadBet(uint _betId, string memory _sportbook, string memory _team, int _odds, int _spread, 
                             address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        //CheckBettingFundsForBetting(_addr, _betAmount, _isEther);
        createSpreadBetInternal(_betId, _sportbook, _team, _odds, _spread, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);
    }

    function createTotalBet(uint _betId, string memory _sportbook, string memory _team, int _odds, bool _isOver, uint _total,
                            address payable _addr, uint _betAmount, bool _isEther)
         public
        onlyOwner
    {
        //CheckBettingFundsForBetting(_addr, _betAmount, _isEther);
        createTotalBetInternal(_betId, _sportbook, _team, _odds, _isOver, _total, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);
    }

    function()
        external
        payable
        onlyOwner
    {}
}


