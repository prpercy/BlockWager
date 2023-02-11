pragma solidity ^0.5.0;

// Container class to hold all the different "Teams" the BlockWager application will support
//    - Will be able to dynamically add new types of teams to be wagered on (e.g. NY Giants, NY Jets, Kansas City Chiefs, etc.)

contract PlaceBets {
    address payable contractOwnerAddr;    // BlockWager contract owner address
    address payable cbetBettingAddr;    // BlockWage betting account (users must first deposit/withdrawal into this account before betting)

    // Keep track of:
    //   PRE_GAME_START: State of game/match before game has started and betting is allowed (default state when the game is initially created)
    //   GAME_IN_PROGRESS: The game has started / in progress.  New bets are no longer accepted.
    //   POST_GAME_END: Game is officillay over. No new bets are accpted, and bet results (losses/winnings) are distributed
    //enum GameStatus { PRE_GAME_START, GAME_IN_PROGRESS, POST_GAME_END }
    enum BetType { MONEYLINE, SPREAD, TOTAL}

    // Betting odds for home and away teams

    // Data structure to hold all "Moneyline" betting parameters
    struct MoneylineBetParams {
        bool activated;
        uint8 sportbookId;
        //GameStatus gameStatus;
        uint16 teamId;
        int16 odds;
        address payable addr;
        uint betAmount;
        bool isEther;
    }

    // Data structure to hold all "Spread" betting parameters
    struct SpreadBetParams {
        bool activated;
        uint8 sportbookId;
        //GameStatus gameStatus;
        uint16 teamId;
        int16 odds;
        int16 spread;
        address payable addr;
        uint betAmount;
        bool isEther;
    }

    // Data structure to hold all "Total Over/Under" betting parameters
    struct TotalBetParams {
        bool activated;
        uint8 sportbookId;
        //GameStatus gameStatus;
        uint16 teamId;
        int16 odds;
        bool isOver;
        uint16 total;
        address payable addr;
        uint betAmount;
        bool isEther;
    }
    
    // Keep track of all betting parameters (for the 3 types of bets) using the betId as the index to the mapping
    mapping(uint32 => MoneylineBetParams) moneylineBets;
    mapping(uint32 => SpreadBetParams) spreadBets;
    mapping(uint32 => TotalBetParams) totalBets;
    mapping(uint32 => BetType) betTypes;

    uint WEI_FACTOR = 10**18;

   // Only the owner/deployer of the BlockWager contract can make any changes to this module
    modifier onlyOwner {
        require(msg.sender == contractOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    modifier onlyHouse {
        require(msg.sender == cbetBettingAddr, "Only the betting account has permissions for this action!");
        _;
    }

    // Construct which sets up the BlockWager contract owner address
    constructor (address payable _contractOwnerAddr)
        public
    {
        contractOwnerAddr = _contractOwnerAddr;
    }

    // Configure the address of the wallet (betting account) that will hold the ether/tokens
    // (Note, this would usually be placed in the constructur, but since the addresses from Ganache are dynamic, will be passed in as
    //        a parameter from the streamlit app)
    function setCbetBettingAddrPlaceBets(address payable _cbetBettingAddr)
        internal
        onlyOwner
    {
        cbetBettingAddr = _cbetBettingAddr;
    }

    // A bet placed should always have a unique betId assigned from the front end application
    function checkUniqueBetId(uint32 _betId)
        internal
        view
        onlyOwner
    {
        require(((moneylineBets[_betId].activated != true) &&
                 (spreadBets[_betId].activated != true) &&
                 (totalBets[_betId].activated != true)), "Cannot create this bet, betId already used!");
    }

    // Create a moneyline bet..
    function createMoneylineBetInternal(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, 
                                        address payable _addr, uint _betAmount, bool _isEther)
        internal
        onlyOwner
    {
        moneylineBets[_betId].activated = true;
        moneylineBets[_betId].sportbookId = _sportbookId;
        //moneylineBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        moneylineBets[_betId].teamId = _teamId;
        moneylineBets[_betId].odds = _odds;
        moneylineBets[_betId].addr = _addr;
        moneylineBets[_betId].betAmount = _betAmount;
        moneylineBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.MONEYLINE;
    }

    // Create a spread bet
    function createSpreadBetInternal(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, int16 _spread, 
                                     address payable _addr, uint _betAmount, bool _isEther)
        internal
        onlyOwner
    {
        spreadBets[_betId].activated = true;
        spreadBets[_betId].sportbookId = _sportbookId;
        //spreadBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        spreadBets[_betId].teamId = _teamId;
        spreadBets[_betId].odds = _odds;
        spreadBets[_betId].spread = _spread;
        spreadBets[_betId].addr = _addr;
        spreadBets[_betId].betAmount = _betAmount;
        spreadBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.SPREAD;
    }

    // Create an over/under bet
    function createTotalBetInternal(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, bool _isOver, uint16 _total,
                                    address payable _addr, uint _betAmount, bool _isEther)
        internal
        onlyOwner
    {
        totalBets[_betId].activated = true;
        totalBets[_betId].sportbookId = _sportbookId;
        //totalBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        totalBets[_betId].teamId = _teamId;
        totalBets[_betId].odds = _odds;
        totalBets[_betId].isOver = _isOver;
        totalBets[_betId].total = _total;
        totalBets[_betId].addr = _addr;
        totalBets[_betId].betAmount = _betAmount;
        totalBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.TOTAL;
    }

    // Getter function to access the type of bet using the betId (assigned when the bet was placed by the front end)
    function getBetType(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return (betTypes[_betId] == BetType.MONEYLINE) ? 0 :
               (betTypes[_betId] == BetType.SPREAD) ? 1 :
               2;
    }

    // Getter function to determine which sportbook was used to determine the odds
    function getBetMoneylineSportbook(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return moneylineBets[_betId].sportbookId;
    }

    /*
    // Getter function to get the bet status (did it start, in progress, end)
    function getBetMoneylineGameStatus(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return (moneylineBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? 0 :
               (moneylineBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? 1 : 2;
    }
    */

    // Getter function to extract the moneyline bet paameters given a betId
    function getBetMoneylineBet(uint32 _betId)
        public
        view
        onlyHouse
        returns (uint16, int16, uint, bool)
    {
        return (moneylineBets[_betId].teamId,
                moneylineBets[_betId].odds,
                moneylineBets[_betId].betAmount,
                moneylineBets[_betId].isEther);
    }

    // Getter function to extract the moneyline bet user address
    function getBetMoneylineAddress(uint32 _betId)
        internal
        view
        onlyHouse
        returns (address payable)
    {
        return (moneylineBets[_betId].addr);
    }

    // Getter function to extract the sportbook paameters given a betId
    function getBetSpreadSportbook(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return (spreadBets[_betId].sportbookId);
    }

    /*
    function getBetSpreadGameStatus(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return ((spreadBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? 0 :
                (spreadBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? 1 : 2);
    }
    */

    // Getter function to extract the spread bet paameters given a betId
    function getBetSpreadBet(uint32 _betId)
        public
        view
        onlyHouse
        returns (uint16, int16, int16, uint, bool)
    {
        return (spreadBets[_betId].teamId,
                spreadBets[_betId].odds,
                spreadBets[_betId].spread,
                spreadBets[_betId].betAmount,
                spreadBets[_betId].isEther);
    }

    // Getter function to extract the spread bet user address
    function getBetSpreadAddress(uint32 _betId)
        internal
        view
        onlyHouse
        returns (address payable)
    {
        return (spreadBets[_betId].addr);
    }

    // Getter function to extract the sportbook paameters given a betId
    function getBetTotalSportbook(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return (totalBets[_betId].sportbookId);
    }

    /*
    function getBetTotalGameStatus(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return ((totalBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? 0 :
                (totalBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? 1 : 2);
    }
    */

    // Getter function to extract the total - over/under bet paameters given a betId
    function getBetTotalBet(uint32 _betId)
        public
        view
        onlyHouse
        returns (uint16, int16, bool, uint16, uint, bool)
    {
        return (totalBets[_betId].teamId,
                totalBets[_betId].odds,
                totalBets[_betId].isOver,
                totalBets[_betId].total,
                totalBets[_betId].betAmount,
                totalBets[_betId].isEther);
    }

    // Getter function to extract the total - over/under bet user address
    function getBetTotalAddress(uint32 _betId)
        internal
        view
        onlyHouse
        returns (address payable)
    {
        return (totalBets[_betId].addr);
    }

    // Game event occurred (end of betting game), the following function will return the results for a moneyline bet
    function gameEventMoneyline(uint32 _betId, uint16 _winningTeamId, uint16 _winningScore, uint16 _losingScore)
        internal
        view
        onlyHouse
        returns (bool, uint, uint, bool)
    {
        bool isWin;
        uint betAmount;
        uint winnings;
        bool isEther;

        uint16 teamId;
        int16 odds;

        // Get the betting parameters used for this moneyline bet
        (teamId,odds,betAmount,isEther) = getBetMoneylineBet(_betId);

        // If the 2 scores of the game are the same, the game ended in a tie.
        if (_winningScore == _losingScore)
        {
            isWin = true;   // IsWin is set to true here as this will be used as qualifier to return funds from escrow back to the users betting virtual wallet (this is true for a tie game)
            winnings = 0;   // for tie game, there are no winning.
        }
        // If the teamId origingally placed a bet on is not the same as the winning team, then lost the bet
        else if (teamId != _winningTeamId)
        {
            isWin = false;
            winnings = 0;
        }
        // Gets here if the better won the bet...
        // The winning amount needs to be handled different if the odds were positive versus if they were negative
        else if (odds > 0)
        {
            isWin = true;
            winnings = (betAmount*uint(odds))/100;
        }
        else
        {
            isWin = true;
            winnings = (betAmount*100)/uint(-odds);
        }

        return (isWin, betAmount, winnings, isEther);
    }    

    // Game event occurred (end of betting game), the following function will return the results for a spread bet
    function gameEventSpread(uint32 _betId, uint16 _winningTeamId, uint16 _winningScore, uint16 _losingScore)
        internal
        view
        onlyHouse
        returns (bool, uint, uint, bool)
    {
        bool isWin;
        uint betAmount;
        uint winnings;
        bool isEther;

        uint16 teamId;
        int16 odds;

        int16 spread;

        // Get the betting parameters used for this spread bet
        (teamId,odds,spread,betAmount,isEther) = getBetSpreadBet(_betId);

        uint16 myScoreWithSpread;
        uint16 otherScore;

        // Determine if the team selected won or lost the game, and apply the spread to the score of the betting team accordingly
        // spread can be positive or negative
        if (teamId == _winningTeamId)
        {
            myScoreWithSpread = uint16(int16(_winningScore) + spread);
            otherScore = _losingScore;
        }
        else
        {
            myScoreWithSpread = uint16(int16(_losingScore) + spread);
            otherScore = _winningScore;
        }
        
        // If with the spread, the betters score equals the other teams score, then a tie bet
        if (myScoreWithSpread == otherScore)
        {
            isWin = true;
            winnings = 0;
        }
        // If with the spread, teh bettors score is less than the other teams score, then lost the bet
        else if (myScoreWithSpread < otherScore)
        {
            isWin = false;
            winnings = 0;
        }
        // Gets here if the better won the bet...
        // The winning amount needs to be handled different if the odds were positive versus if they were negative
        else if (odds > 0)
        {
            isWin = true;
            winnings = (betAmount*uint(odds))/100;
        }
        else
        {
            isWin = true;
            winnings =  (betAmount*100)/uint(-odds);
        }            

        return (isWin, betAmount, winnings, isEther);
    }

    // Game event occurred (end of betting game), the following function will return the results for a total over/under bet
    function gameEventTotal(uint32 _betId, uint16 _winningScore, uint16 _losingScore)
        internal
        view
        onlyHouse
        returns (bool, uint, uint, bool)
    {
        bool isWin;
        uint betAmount;
        uint winnings;
        bool isEther;

        uint16 teamId;
        int16 odds;

        bool isOver;
        uint16 total;

        // Get the betting parameters used for this total over/under bet
        (teamId,odds,isOver,total,betAmount,isEther) = getBetTotalBet(_betId);

        // Combine both scores of the 2 teams playing each other
        uint16 totalScore = _winningScore + _losingScore;

        // If the bettor picked "under" and the combined score was great than the over/under total score, OR
        // If the bettor picked "over" and the combined score was less than the over/under total score,
        // Then the bettor lost
        if ((!isOver && (totalScore > total)) || (isOver && (totalScore < total)))
        {
            isWin = false;
            winnings = 0;
        }
        // If the combined score equals the over/under total, then its a tie (push bet)
        else if (total == totalScore)
        {
            isWin = true;
            winnings = 0;
        }
        // Gets here if the better won the bet...
        // The winning amount needs to be handled different if the odds were positive versus if they were negative
        else if (odds > 0)
        {
            isWin = true;
            winnings = (betAmount*uint(odds))/100;
        }
        else
        {
            isWin = true;
            winnings =  (betAmount*100)/uint(-odds);
        }            

        // Return the results...
        return (isWin, betAmount, winnings, isEther);
    }

}
