pragma solidity ^0.5.0;

// Container class to hold account related information for the user
//    - Will be able to dynamically add new users

import "./UserAccounts.sol";
import "./PlaceBets.sol";

contract BlockWager is UserAccounts, PlaceBets {
    address payable cbetOwnerAddr;      // BlockWager contract owner address
    address payable cbetBettingAddr;    // BlockWage betting account (users must first deposit/withdrawal into this account before betting)

    int lastPayout;  // // Mapping between better wallet address and CBET accounts

    modifier onlyOwner {
        require(msg.sender == cbetOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    modifier onlyHouse {
        require(msg.sender == cbetBettingAddr, "Only the contracts owner has permissions for this action!");
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

    // Configure the address of the wallet (betting account) that will hold the ether/tokens
    // (Note, this would usually be placed in the constructur, but since the addresses from Ganache are dynamic, will be passed in as
    //        a parameter from the streamlit app)
    function setCbetBettingAddr(address payable _cbetBettingAddr)
        public
        onlyOwner
    {
        cbetBettingAddr = _cbetBettingAddr;
        setCbetBettingAddrUserAccounts(_cbetBettingAddr);            
        setCbetBettingAddrPlaceBets(_cbetBettingAddr);            
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
        onlyHouse
    {
        address payable userAddr;

        bool isWin;
        uint betAmount;
        uint winnings;
        bool isEther;

        if (betTypes[_betId] == BetType.MONEYLINE)
        {
            userAddr = getBetMoneylineAddress(_betId);
            (isWin, betAmount, winnings, isEther) = gameEventMoneyline(_betId, _winningTeamId, _winningScore, _losingScore);
        }
        else if (betTypes[_betId] == BetType.SPREAD)
        {
            userAddr = getBetSpreadAddress(_betId);
            (isWin, betAmount, winnings, isEther) = gameEventSpread(_betId, _winningTeamId, _winningScore, _losingScore);
        }
        else
        {
            userAddr = getBetTotalAddress(_betId);
            (isWin, betAmount, winnings, isEther) = gameEventTotal(_betId, _winningScore, _losingScore);
        }

       if (!isWin)
        {
            // Lost Bet

            lastPayout = int(-betAmount);

            removeEscrowFromUser(userAddr, betAmount, isEther);
        }
        else if (winnings == 0)
        {
            // Push Bet (Tie)

            lastPayout = int(betAmount);

            transferEscrowBackToBetting(userAddr, betAmount, isEther);
        }
        else
        {
            // Win Bet

            uint payout = betAmount + winnings;

            lastPayout = int(payout);

            transferEscrowBackToBetting(userAddr, betAmount, isEther);
            transerWinningsFromBettingToUser(userAddr, winnings, isEther);            
        }
    }

    function getLastPayout()
        public
        view
        onlyOwner
        returns (int)
    {
        return lastPayout;
    }


    function()
        external
        payable
        onlyOwner
    {}
}


