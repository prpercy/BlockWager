pragma solidity ^0.5.0;

contract BettingGames {
    address payable contractOwnerAddr;
    uint currGameId = 1;
    uint lastGameId;

    enum GameStatus { PRE_GAME_START, GAME_IN_PROGRESS, POST_GAME_END }

    struct Odds {
        int homeOdds;
        int awayOdds;
    }

    struct BettingGameParams {
        GameStatus gameStatus;

        uint homeTeamId;
        uint awayTeamId;

        Odds oddsMoneyline;
        Odds oddsSpread;
        Odds oddsOverUnder;
    
        bool isHomeFavorite;
        uint spread;
        uint overUnder;
    }

    mapping(uint => BettingGameParams) bettingGames;

    modifier onlyOwner {
        require(msg.sender == contractOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    constructor (address payable _contractOwnerAddr) 
        public 
    {
        contractOwnerAddr = _contractOwnerAddr;
    }

    function createGame(uint _homeTeamId, uint _awayTeamId, 
                        int _homeTeamOddsMoneyline, int _awayTeamOddsMoneyline,
                        int _homeTeamOddsSpread, int _awayTeamOddsSpread, bool _isHomeFavorite, uint _spread,
                        int _homeTeamOddsOverUnder, int _awayTeamOddsOverUnder, uint _overUnder)
        public
        onlyOwner
        returns (uint)
    {
        BettingGameParams memory bettingGameParams;

        bettingGameParams.gameStatus = GameStatus.PRE_GAME_START;

        bettingGameParams.homeTeamId = _homeTeamId;
        bettingGameParams.awayTeamId = _awayTeamId;

        bettingGameParams.oddsMoneyline.homeOdds = _homeTeamOddsMoneyline;
        bettingGameParams.oddsMoneyline.awayOdds = _awayTeamOddsMoneyline;

        bettingGameParams.oddsSpread.homeOdds = _homeTeamOddsSpread;
        bettingGameParams.oddsSpread.awayOdds = _awayTeamOddsSpread;
        bettingGameParams.isHomeFavorite = _isHomeFavorite;
        bettingGameParams.spread = _spread;

        bettingGameParams.oddsOverUnder.homeOdds = _homeTeamOddsOverUnder;
        bettingGameParams.oddsOverUnder.awayOdds = _awayTeamOddsOverUnder;
        bettingGameParams.overUnder = _overUnder;

        uint gameId = currGameId++;
        
        bettingGames[gameId] = bettingGameParams;

        lastGameId = gameId;
        return gameId;
    }    

    function getLastGameId()
        public
        view
        onlyOwner
        returns (uint)
    {
        return lastGameId;
    }

    function updateGameOddsMoneyline(uint _gameId, int _homeTeamOddsMoneyline, int _awayTeamOddsMoneyline)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Only accepting updated odds for games that have not yet started");

        bettingGames[_gameId].oddsMoneyline.homeOdds = _homeTeamOddsMoneyline;
        bettingGames[_gameId].oddsMoneyline.awayOdds = _awayTeamOddsMoneyline;
    }

    function updateGameOddsSpread(uint _gameId, int _homeTeamOddsSpread, int _awayTeamOddsSpread, bool _isHomeFavorite, uint _spread)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Only accepting updated odds for games that have not yet started");

        bettingGames[_gameId].oddsSpread.homeOdds = _homeTeamOddsSpread;
        bettingGames[_gameId].oddsSpread.awayOdds = _awayTeamOddsSpread;
        bettingGames[_gameId].isHomeFavorite = _isHomeFavorite;
        bettingGames[_gameId].spread = _spread;
    }

    function updateGameOddsOverUnder(uint _gameId, int _homeTeamOddsOverUnder, int _awayTeamOddsOverUnder, uint _overUnder)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Only accepting updated odds for games that have not yet started");

        bettingGames[_gameId].oddsOverUnder.homeOdds = _homeTeamOddsOverUnder;
        bettingGames[_gameId].oddsOverUnder.awayOdds = _awayTeamOddsOverUnder;
        bettingGames[_gameId].overUnder = _overUnder;
    }

    function setGameStart(uint _gameId)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Can only change status to games to start for games that have not yet started");
        bettingGames[_gameId].gameStatus = GameStatus.GAME_IN_PROGRESS;
    }

    function setGameOver(uint _gameId)
        public
        onlyOwner
    {
        require (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START, "Can only change status to games over for games that have already started");
        bettingGames[_gameId].gameStatus = GameStatus.POST_GAME_END;
    }

    function isAcceptingBets(uint _gameId)
        public
        view
        returns (bool)
    {
        return (bettingGames[_gameId].gameStatus == GameStatus.PRE_GAME_START);       
    }

    function isGameInProgress(uint _gameId)
        public
        view
        returns (bool)
    {
        return (bettingGames[_gameId].gameStatus == GameStatus.GAME_IN_PROGRESS);       
    }

    function isGameOver(uint _gameId)
        public
        view
        returns (bool)
    {
        return (bettingGames[_gameId].gameStatus == GameStatus.POST_GAME_END);       
    }

    function getGameTeamIds(uint _gameId)
        public
        view
        returns (uint, uint)
    {
        return (bettingGames[_gameId].homeTeamId, bettingGames[_gameId].awayTeamId);
    }

    function getGameMoneylineOdds(uint _gameId)
        public
        view
        returns (int, int)
    {
        return (bettingGames[_gameId].oddsMoneyline.homeOdds, bettingGames[_gameId].oddsMoneyline.awayOdds);
    }

    function getGameSpreadOdds(uint _gameId)
        public
        view
        returns (int, int, bool, uint)
    {
        return (bettingGames[_gameId].oddsSpread.homeOdds, bettingGames[_gameId].oddsSpread.awayOdds, bettingGames[_gameId].isHomeFavorite, bettingGames[_gameId].spread);
    }

    function getGameOverUnderOdds(uint _gameId)
        public
        view
        returns (int, int, uint)
    {
        return (bettingGames[_gameId].oddsOverUnder.homeOdds, bettingGames[_gameId].oddsOverUnder.awayOdds, bettingGames[_gameId].overUnder);
    }

}
