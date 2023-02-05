pragma solidity ^0.5.0;

// Container class to hold all the different "Teams" the BlockWager application will support
//    - Will be able to dynamically add new types of teams to be wagered on (e.g. NY Giants, NY Jets, Kansas City Chiefs, etc.)

contract PlaceBets {
    address payable contractOwnerAddr;    // BlockWager contract owner address

    // Keep track of:
    //   PRE_GAME_START: State of game/match before game has started and betting is allowed (default state when the game is initially created)
    //   GAME_IN_PROGRESS: The game has started / in progress.  New bets are no longer accepted.
    //   POST_GAME_END: Game is officillay over. No new bets are accpted, and bet results (losses/winnings) are distributed
    enum GameStatus { PRE_GAME_START, GAME_IN_PROGRESS, POST_GAME_END }
    enum BetType { MONEYLINE, SPREAD, TOTAL}

    // Betting odds for home and away teams

    struct MoneyLineBetParams {
        string sportbook;
        GameStatus gameStatus;
        string team;
        int odds;
        address payable addr;
        uint betAmount;
        bool isEther;
    }

    struct SpreadBetParams {
        string sportbook;
        GameStatus gameStatus;
        string team;
        int odds;
        int spread;
        address payable addr;
        uint betAmount;
        bool isEther;
    }

    struct TotalBetParams {
        string sportbook;
        GameStatus gameStatus;
        string team;
        int odds;
        bool isOver;
        uint total;
        address payable addr;
        uint betAmount;
        bool isEther;
    }
    
    mapping(uint => MoneyLineBetParams) moneylineBets;
    mapping(uint => SpreadBetParams) spreadBets;
    mapping(uint => TotalBetParams) totalBets;

    mapping(uint => BetType) betTypes;

    uint WEI_FACTOR = 10**18;

   // Only the owner/deployer of the BlockWager contract can make any changes to this module
    modifier onlyOwner {
        require(msg.sender == contractOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    // Construct which sets up the BlockWager contract owner address
    constructor (address payable _contractOwnerAddr)
        public
    {
        contractOwnerAddr = _contractOwnerAddr;
    }

    function createMoneylineBetInternal(uint _betId, string memory _sportbook, string memory _team, int _odds, 
                                        address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        moneylineBets[_betId].sportbook = _sportbook;
        moneylineBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        moneylineBets[_betId].team = _team;
        moneylineBets[_betId].odds = _odds;
        moneylineBets[_betId].addr = _addr;
        moneylineBets[_betId].betAmount = _betAmount;
        moneylineBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.MONEYLINE;
    }

    function createSpreadBetInternal(uint _betId, string memory _sportbook, string memory _team, int _odds, int _spread, 
                                     address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        spreadBets[_betId].sportbook = _sportbook;
        spreadBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        spreadBets[_betId].team = _team;
        spreadBets[_betId].odds = _odds;
        spreadBets[_betId].spread = _spread;
        spreadBets[_betId].addr = _addr;
        spreadBets[_betId].betAmount = _betAmount;
        spreadBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.SPREAD;
    }

    function createTotalBetInternal(uint _betId, string memory _sportbook, string memory _team, int _odds, bool _isOver, uint _total,
                                    address payable _addr, uint _betAmount, bool _isEther)
        public
        onlyOwner
    {
        totalBets[_betId].sportbook = _sportbook;
        totalBets[_betId].gameStatus = GameStatus.PRE_GAME_START;
        totalBets[_betId].team = _team;
        totalBets[_betId].odds = _odds;
        totalBets[_betId].isOver = _isOver;
        totalBets[_betId].total = _total;
        totalBets[_betId].addr = _addr;
        totalBets[_betId].betAmount = _betAmount;
        totalBets[_betId].isEther = _isEther;

        betTypes[_betId] = BetType.TOTAL;
    }

    function getBetType(uint _betId)
        public
        view
        onlyOwner
        returns (string memory)
    {
        return (betTypes[_betId] == BetType.MONEYLINE) ? "Moneyline" :
               (betTypes[_betId] == BetType.SPREAD) ? "Spread" :
               "Total";
    }

    function getBetMoneyLineOdds(uint _betId)
        public
        view
        onlyOwner
        returns (string memory, string memory, string memory, int)
    {
        return (moneylineBets[_betId].sportbook,
                (moneylineBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? "Game not start" :
                (moneylineBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? "Game In Progress" : "Game End",
                moneylineBets[_betId].team,
                moneylineBets[_betId].odds);
    }

    function getBetMoneyLineBet(uint _betId)
        public
        view
        onlyOwner
        returns (address payable, uint, bool)
    {
        return (moneylineBets[_betId].addr,
                moneylineBets[_betId].betAmount,
                moneylineBets[_betId].isEther);
    }

    function getBetSpreadOdds(uint _betId)
        public
        view
        onlyOwner
        returns (string memory, string memory, string memory, int, int)
    {
        return (spreadBets[_betId].sportbook,
                (spreadBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? "Game not start" :
                (spreadBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? "Game In Progress" : "Game End",
                spreadBets[_betId].team,
                spreadBets[_betId].odds,
                spreadBets[_betId].spread);
    }

    function getBetSpreadBet(uint _betId)
        public
        view
        onlyOwner
        returns (address payable, uint, bool)
    {
        return (spreadBets[_betId].addr,
                spreadBets[_betId].betAmount,
                spreadBets[_betId].isEther);
    }

    function getBetTotalOdds(uint _betId)
        public
        view
        onlyOwner
        returns (string memory, string memory, string memory, int, bool, uint)
    {
        return (totalBets[_betId].sportbook,
                (totalBets[_betId].gameStatus == GameStatus.PRE_GAME_START) ? "Game not start" :
                (totalBets[_betId].gameStatus == GameStatus.GAME_IN_PROGRESS) ? "Game In Progress" : "Game End",
                totalBets[_betId].team,
                totalBets[_betId].odds,
                totalBets[_betId].isOver,
                totalBets[_betId].total);
    }

    function getBetTotalBet(uint _betId)
        public
        view
        onlyOwner
        returns (address payable, uint, bool)
    {
        return (totalBets[_betId].addr,
                totalBets[_betId].betAmount,
                totalBets[_betId].isEther);
    }

/*
    // Getter function - return the gameId of the last game/match that has been created
    function getLastGameId()
        public
        view
        onlyOwner
        returns (uint)
    {
        return lastGameId;
    }

    // After the initial game creation, odds of the match can/will change dynamically...

    // Update the moneyline odds
    function updateGameOddsMoneyline(uint _gameId, int _homeTeamOddsMoneyline, int _awayTeamOddsMoneyline)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Only accepting updated odds for games that have not yet started");

        bettingGames[_gameId].oddsMoneyline.homeOdds = _homeTeamOddsMoneyline;
        bettingGames[_gameId].oddsMoneyline.awayOdds = _awayTeamOddsMoneyline;
    }

    // Update the spread odds
    function updateGameSpread(uint _gameId, int _homeTeamSpread, int _awayTeamSpread)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Only accepting updated odds for games that have not yet started");

        bettingGames[_gameId].spread.homeSpread = _homeTeamSpread;
        bettingGames[_gameId].spread.awaySpread = _awayTeamSpread;
    }

    // Update the over/under (total) odds
    function updateGameOddsOverUnder(uint _gameId, bool _isOver, uint _overUnder)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Only accepting updated odds for games that have not yet started");

        bettingGames[_gameId].isOver = _isOver;
        bettingGames[_gameId].overUnder = _overUnder;
    }

    // Action by owner to set the start of the game/match
    function setGameStart(uint _gameId)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Can only change status to games to start for games that have not yet started");
        bettingGames[_gameId].gameStatus = GameStatus.GAME_IN_PROGRESS;
    }

    // Action by the owner to set the game match has ended
    function setGameOver(uint _gameId)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Can only change status to games over for games that have already started");
        bettingGames[_gameId].gameStatus = GameStatus.POST_GAME_END;
    }

    // Getter function to determine if no longer accepting bets (not available during the game or after game completiong)
    function isAcceptingBets(uint _gameId)
        public
        view
        returns (bool)
    {
        return (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START);
    }

    // Getter function to check if the game is in progress
    function isGameInProgress(uint _gameId)
        public
        view
        returns (bool)
    {
        return (bettingGames[_gameId].gameStatus == GameStatus.GAME_IN_PROGRESS);
    }

    // Getter function to check if the game is over
    function isGameOver(uint _gameId)
        public
        view
        returns (bool)
    {
        return (bettingGames[_gameId].gameStatus == GameStatus.POST_GAME_END);
    }

    // Getter function to get the 2 teamId's of the game/match referenced by the gameId
    function getGameTeamIds(uint _gameId)
        public
        view
        returns (uint, uint)
    {
        return (bettingGames[_gameId].homeTeamId, bettingGames[_gameId].awayTeamId);
    }

    // Getter function to get the current moneyline odds
    function getGameMoneylineOdds(uint _gameId)
        public
        view
        returns (int, int)
    {
        return (bettingGames[_gameId].oddsMoneyline.homeOdds, bettingGames[_gameId].oddsMoneyline.awayOdds);
    }

    // Getter function to get the current spread odds
    function getGameSpreadOdds(uint _gameId)
        public
        view
        returns (int, int)
    {
        return (bettingGames[_gameId].spread.homeSpread, bettingGames[_gameId].spread.awaySpread);
    }

    // Getter function to get the current over/under (total) odds
    function getGameOverUnderOdds(uint _gameId)
        public
        view
        returns (bool, uint)
    {
        return (bettingGames[_gameId].isOver, bettingGames[_gameId].overUnder);
    }
*/
}
