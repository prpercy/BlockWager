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
    enum GameStatus { PRE_GAME_START, GAME_IN_PROGRESS, POST_GAME_END }
    enum BetType { MONEYLINE, SPREAD, TOTAL}

    // Betting odds for home and away teams

    struct MoneylineBetParams {
        uint8 sportbookId;
        GameStatus gameStatus;
        uint16 teamId;
        int16 odds;
        address payable addr;
        uint betAmount;
        bool isEther;
    }

    struct SpreadBetParams {
        uint8 sportbookId;
        GameStatus gameStatus;
        uint16 teamId;
        int16 odds;
        int16 spread;
        address payable addr;
        uint betAmount;
        bool isEther;
    }

    struct TotalBetParams {
        uint8 sportbookId;
        GameStatus gameStatus;
        uint16 teamId;
        int16 odds;
        bool isOver;
        uint16 total;
        address payable addr;
        uint betAmount;
        bool isEther;
    }
    
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

    function createMoneylineBetInternal(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, 
                                        address payable _addr, uint _betAmount, bool _isEther)
        internal
        onlyOwner
    {
        moneylineBets[_betId].sportbookId = _sportbookId;
        moneylineBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        moneylineBets[_betId].teamId = _teamId;
        moneylineBets[_betId].odds = _odds;
        moneylineBets[_betId].addr = _addr;
        moneylineBets[_betId].betAmount = _betAmount;
        moneylineBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.MONEYLINE;
    }

    function createSpreadBetInternal(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, int16 _spread, 
                                     address payable _addr, uint _betAmount, bool _isEther)
        internal
        onlyOwner
    {
        spreadBets[_betId].sportbookId = _sportbookId;
        spreadBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        spreadBets[_betId].teamId = _teamId;
        spreadBets[_betId].odds = _odds;
        spreadBets[_betId].spread = _spread;
        spreadBets[_betId].addr = _addr;
        spreadBets[_betId].betAmount = _betAmount;
        spreadBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.SPREAD;
    }

    function createTotalBetInternal(uint32 _betId, uint8 _sportbookId, uint16 _teamId, int16 _odds, bool _isOver, uint16 _total,
                                    address payable _addr, uint _betAmount, bool _isEther)
        internal
        onlyOwner
    {
        totalBets[_betId].sportbookId = _sportbookId;
        totalBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        totalBets[_betId].teamId = _teamId;
        totalBets[_betId].odds = _odds;
        totalBets[_betId].isOver = _isOver;
        totalBets[_betId].total = _total;
        totalBets[_betId].addr = _addr;
        totalBets[_betId].betAmount = _betAmount;
        totalBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.TOTAL;
    }

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

    function getBetMoneylineSportbook(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return moneylineBets[_betId].sportbookId;
    }

    function getBetMoneylineGameStatus(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return (moneylineBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? 0 :
               (moneylineBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? 1 : 2;
    }

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

    function getBetMoneylineAddress(uint32 _betId)
        internal
        view
        onlyHouse
        returns (address payable)
    {
        return (moneylineBets[_betId].addr);
    }

    function getBetSpreadSportbook(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return (spreadBets[_betId].sportbookId);
    }

    function getBetSpreadGameStatus(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return ((spreadBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? 0 :
                (spreadBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? 1 : 2);
    }

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

    function getBetSpreadAddress(uint32 _betId)
        internal
        view
        onlyHouse
        returns (address payable)
    {
        return (spreadBets[_betId].addr);
    }

    function getBetTotalSportbook(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return (totalBets[_betId].sportbookId);
    }

    function getBetTotalGameStatus(uint32 _betId)
        public
        view
        onlyOwner
        returns (uint8)
    {
        return ((totalBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? 0 :
                (totalBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? 1 : 2);
    }

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

    function getBetTotalAddress(uint32 _betId)
        internal
        view
        onlyHouse
        returns (address payable)
    {
        return (totalBets[_betId].addr);
    }

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

        (teamId,odds,betAmount,isEther) = getBetMoneylineBet(_betId);

        if (_winningScore == _losingScore)
        {
            isWin = true;
            winnings = 0;
        }
        else if (teamId != _winningTeamId)
        {
            isWin = false;
            winnings = 0;
        }
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
        (teamId,odds,spread,betAmount,isEther) = getBetSpreadBet(_betId);

        uint16 myScoreWithSpread;
        uint16 otherScore;
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
        
        if (myScoreWithSpread == otherScore)
        {
            isWin = true;
            winnings = 0;
        }
        else if (myScoreWithSpread < otherScore)
        {
            isWin = false;
            winnings = 0;
        }
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
        (teamId,odds,isOver,total,betAmount,isEther) = getBetTotalBet(_betId);

        uint16 totalScore = _winningScore + _losingScore;

        if ((!isOver && (totalScore > total)) || (isOver && (totalScore < total)))
        {
            isWin = false;
            winnings = 0;
        }
        else if (total == totalScore)
        {
            isWin = true;
            winnings = 0;
        }
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

}
