pragma solidity ^0.5.0;

// Container class to hold account related information for the user
//    - Will be able to dynamically add new users

import "./UserAccounts.sol";
import "./PlaceBets.sol";

contract BlockWager is UserAccounts, PlaceBets {
    address payable cbetOwnerAddr;      // BlockWager contract owner address
    address payable cbetBettingAddr;    // BlockWage betting account (users must first deposit/withdrawal into this account before betting)

    // Variables to hold the "last" winning bet (to be used to generate/emit an event to the front end application)
    int8 lastWinStatus;
    int lastPayout;  // Mapping between better wallet address and CBET accounts

    modifier onlyOwner {
        require(msg.sender == cbetOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    modifier onlyHouse {
        require(msg.sender == cbetBettingAddr, "Only the house betting account has permissions for this action!");
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

    // Bettor selected a moneyline bet in the front end application, assign all the bet parameters to the bet id
    function createMoneylineBet(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, 
                                address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        checkUniqueBetId(_betId);  // Confirm that this betId is unique (not used before)
        CheckBettingFundsAvailability(_addr, _betAmount, _isEther); // Make sure the bettor has enough funds to cover the bet
        createMoneylineBetInternal(_betId, _sportbookId, _teamId, _odds, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);   // Transer the funds to an escrow account
    }

    // Bettor selected a spread bet in the front end application, assign all the bet parameters to the bet id
    function createSpreadBet(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, int16 _spread, 
                             address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        checkUniqueBetId(_betId);  // Confirm that this betId is unique (not used before)
        CheckBettingFundsAvailability(_addr, _betAmount, _isEther); // Make sure the bettor has enough funds to cover the bet
        createSpreadBetInternal(_betId, _sportbookId, _teamId, _odds, _spread, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);  // Transer the funds to an escrow account
    }

    // Bettor selected a total over/under bet in the front end application, assign all the bet parameters to the bet id
    function createTotalBet(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, bool _isOver, uint16 _total,
                            address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        checkUniqueBetId(_betId);  // Confirm that this betId is unique (not used before)
        CheckBettingFundsAvailability(_addr, _betAmount, _isEther); // Make sure the bettor has enough funds to cover the bet
        createTotalBetInternal(_betId, _sportbookId, _teamId, _odds, _isOver, _total, _addr, _betAmount, _isEther);                               
        transferBettingToEscrow(_addr, _betAmount, _isEther);  // Transer the funds to an escrow account
    }

    // Configure an event function (that will be emitted at the conclusion of the game)
    event gameEventPayout(address _addr, uint32 _betId, int8 _winStatus, int _payout);

    // Called by the front end application to distribute the bet winnings or losses.
    function gameEvent(uint32 _betId, uint16 _winningTeamId, uint16 _winningScore, uint16 _losingScore)
        public
        onlyHouse
    {
        require(_winningScore >= _losingScore, "The winning score cannot be < than the losing score!");

        address payable userAddr;

        bool isWin;
        uint betAmount;
        uint winnings;
        bool isEther;

        // Based on the 3 types of betting options (moneyline, spread, total over/under), go determine if bet status (win, loss, tie)
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

            lastWinStatus = -1;
            lastPayout = int(-betAmount);

            // Remove funds from escrow (by default will remain in the house betting account)
            removeEscrowFromUser(userAddr, betAmount, isEther);
        }
        else if (winnings == 0)
        {
            // Push Bet (Tie)

            lastWinStatus = 0;
            lastPayout = int(betAmount);

            // Transfer the escrow funds back to the bettors virtual betting account)
            transferEscrowBackToBetting(userAddr, betAmount, isEther);
        }
        else
        {
            // Win Bet

            lastWinStatus = 1;
            uint payout = betAmount + winnings;

            lastPayout = int(payout);

            // Transfer the escrow funds back to the bettors virtual betting account)
            transferEscrowBackToBetting(userAddr, betAmount, isEther);
            // AND additionally, since won the bet, transfer funds from the house betting virtual account to the bettors virtual account
            transerWinningsFromBettingToUser(userAddr, winnings, isEther);            
        }

        // Emit the payout back to the front end application
        emit gameEventPayout(userAddr, _betId, lastWinStatus, lastPayout);
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

