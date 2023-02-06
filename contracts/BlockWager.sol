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

    function createMoneylineBet(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, 
                                address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        CheckBettingFundsAvailability(_addr, _betAmount, _isEther);
        createMoneylineBetInternal(_betId, _sportbookId, _teamId, _odds, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);
    }

    function createSpreadBet(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, int16 _spread, 
                             address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        CheckBettingFundsAvailability(_addr, _betAmount, _isEther);
        createSpreadBetInternal(_betId, _sportbookId, _teamId, _odds, _spread, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);
    }

    function createTotalBet(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, bool _isOver, uint16 _total,
                            address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        CheckBettingFundsAvailability(_addr, _betAmount, _isEther);
        createTotalBetInternal(_betId, _sportbookId, _teamId, _odds, _isOver, _total, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);
    }

    function gameEvent(uint32 _betId, uint16 _winningTeamId, uint16 _winningScore, uint16 _losingScore)
        public
        onlyOwner
        returns (int8, int)
    {
        address payable userAddr;

        bool isWin;
        uint betAmount;
        int winnings;
        bool isEther;

        if (betTypes[_betId] == BetType.MONEYLINE)
        {
            (isWin, betAmount, winnings, isEther) = gameEventMoneyline(_betId, _winningTeamId, _winningScore, _losingScore);
        }
        else if (betTypes[_betId] == BetType.MONEYLINE)
        {
            (isWin, betAmount, winnings, isEther) = gameEventSpread(_betId, _winningTeamId, _winningScore, _losingScore);
        }
        else
        {
            userAddr = getBetTotalAddress(_betId);
            (isWin, betAmount, winnings, isEther) = gameEventTotal(_betId, _winningScore, _losingScore);
        }

        int8 winStatusId;
        int payout;
        if (!isWin)
        {
            winStatusId = -1;
            payout = int(-betAmount);

            // Lost bet, 
            // ToDo: move ether/cbet...
            //transferEscrowToUser(userAddr, betAmount, isEther);
        }
        else if (winnings == 0)
        {
            winStatusId = 0;
            payout = int(betAmount);

            // Push bet.
            transferEscrowToBetting(userAddr, betAmount, isEther);
        }
        else
        {
            winStatusId = 1;
            payout = int(betAmount) + winnings;

            // Win bet
            // ToDo: move ether/cbet...
        }
        return (winStatusId, payout);
    }

    function()
        external
        payable
        onlyOwner
    {}
}


