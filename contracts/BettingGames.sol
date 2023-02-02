pragma solidity ^0.5.0;

// Container class to hold all the different "Teams" the BlockWager application will support
//    - Will be able to dynamically add new types of teams to be wagered on (e.g. NY Giants, NY Jets, Kansas City Chiefs, etc.)

contract BettingGames {
    address payable contractOwnerAddr;    // BlockWager contract owner address
    uint currGameId = 1;                  // Free running counter used to generate a unique gameId for every new game match created that can be bet on. (e.g. NY Knicks vs. NY Nets)
    uint lastGameId;                      // ID of the "last" game/match that was created (required to be called after afer new game/match has been created)

    // Keep track of:
    //   PRE_GAME_START: State of game/match before game has started and betting is allowed (default state when the game is initially created)
    //   GAME_IN_PROGRESS: The game has started / in progress.  New bets are no longer accepted.
    //   POST_GAME_END: Game is officillay over. No new bets are accpted, and bet results (losses/winnings) are distributed
    enum GameStatus { PRE_GAME_START, GAME_IN_PROGRESS, POST_GAME_END }

    // Betting odds for home and away teams

    struct Odds {
        int homeOdds;
        int awayOdds;
    }

    struct Spread {
        int homeSpread;
        int awaySpread;
    }

    struct BettingGameParams {
        GameStatus gameStatus;

        uint sportId;

        uint homeTeamId;
        uint awayTeamId;

        Odds oddsMoneyline;      // Moneyline betting odds
        Odds oddsSpread;         // Spread odds
        Odds oddsOverUnder;      // Over/Under (Total) odds
 
        Spread spread;           // Spread
        uint overUnder;          // Total points for over/under bet
    }

    mapping(uint => BettingGameParams) bettingGames;  // Mapping between gameId and Betting odds

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

    // Create a single betting game/match that users/bettors can bet on
    // (fills in the details of the betting odds)
    function createGame(uint _sportId, uint _homeTeamId, uint _awayTeamId,
                        int _homeTeamOddsMoneyline, int _awayTeamOddsMoneyline,
                        int _homeTeamOddsSpread, int _awayTeamOddsSpread, int _homeTeamSpread, int _awayTeamSpread,
                        int _homeTeamOddsOverUnder, int _awayTeamOddsOverUnder, uint _overUnder)
        public
        onlyOwner
        returns (uint)
    {
        BettingGameParams memory bettingGameParams;

        bettingGameParams.gameStatus = GameStatus.PRE_GAME_START;

        bettingGameParams.sportId = _sportId;

        bettingGameParams.homeTeamId = _homeTeamId;
        bettingGameParams.awayTeamId = _awayTeamId;

        bettingGameParams.oddsMoneyline.homeOdds = _homeTeamOddsMoneyline;
        bettingGameParams.oddsMoneyline.awayOdds = _awayTeamOddsMoneyline;

        bettingGameParams.oddsSpread.homeOdds = _homeTeamOddsSpread;
        bettingGameParams.oddsSpread.awayOdds = _awayTeamOddsSpread;
        bettingGameParams.spread.homeSpread = _homeTeamSpread;
        bettingGameParams.spread.awaySpread = _awayTeamSpread;

        bettingGameParams.oddsOverUnder.homeOdds = _homeTeamOddsOverUnder;
        bettingGameParams.oddsOverUnder.awayOdds = _awayTeamOddsOverUnder;
        bettingGameParams.overUnder = _overUnder;

        uint gameId = currGameId++;  // increment the gameId for "next" sport creation

        bettingGames[gameId] = bettingGameParams;

        lastGameId = gameId;  // Store the gameId.  The caller of the createGame function must follow up that call with the call to "getLastGameId" to get the gameID for this match
        return gameId;
    }

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
    function updateGameOddsSpread(uint _gameId, int _homeTeamOddsSpread, int _awayTeamOddsSpread, int _homeTeamSpread, int _awayTeamSpread)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Only accepting updated odds for games that have not yet started");

        bettingGames[_gameId].oddsSpread.homeOdds = _homeTeamOddsSpread;
        bettingGames[_gameId].oddsSpread.awayOdds = _awayTeamOddsSpread;
        bettingGames[_gameId].spread.homeSpread = _homeTeamSpread;
        bettingGames[_gameId].spread.awaySpread = _awayTeamSpread;
    }

    // Update the over/under (total) odds
    function updateGameOddsOverUnder(uint _gameId, int _homeTeamOddsOverUnder, int _awayTeamOddsOverUnder, uint _overUnder)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Only accepting updated odds for games that have not yet started");

        bettingGames[_gameId].oddsOverUnder.homeOdds = _homeTeamOddsOverUnder;
        bettingGames[_gameId].oddsOverUnder.awayOdds = _awayTeamOddsOverUnder;
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
        returns (int, int, int, int)
    {
        return (bettingGames[_gameId].oddsSpread.homeOdds, bettingGames[_gameId].oddsSpread.awayOdds, bettingGames[_gameId].spread.homeSpread, bettingGames[_gameId].spread.awaySpread);
    }

    // Getter function to get the current over/under (total) odds
    function getGameOverUnderOdds(uint _gameId)
        public
        view
        returns (int, int, uint)
    {
        return (bettingGames[_gameId].oddsOverUnder.homeOdds, bettingGames[_gameId].oddsOverUnder.awayOdds, bettingGames[_gameId].overUnder);
    }

}


