pragma solidity ^0.5.0;
import './BettingGames.sol';
import './CbetAccounts.sol' ;
import './SafeMath.sol';
contract SettleBets is BettingGames,  CbetAccount {
    using SafeMath for uint; 
function _payOutwinnings (CbetAcountAdrr, _user, uint _amount) private {
 _user.transfer(_amount);

}
function _transfertoHouse() private { 
    owner.transfer(address(this.balance));

}
function _isWinningBet(BettingGames.GameOutcome _outcome, uint8, _chosenWinner, int8 _actualWinner) 
private pure returns(bool) {
    return _outcome == BettingGames.GameOutcome.Decided && _chosenWinner >= 0 
    && (_chosenWinner ==uint8(_actualWinner)) 
}
_calculatePayout() {}


function _payoutForGame(bytes32, BettingGames.gameId, BettingGames.GameOutcome _outcome, int8, _winner) private {
    Bet[] storage bets = BettingGames.[_gameId];
    uint losingTotal = 0;
    uint winningTotal = 0; 
    uint totalsPot = 0;
    uint[] memory payuts = new uinr[](bets.length);

    uint n; 
    for (n = 0; n < bets.length; n++) {; {
        if (_outcome == BettingGames.GameOutcome.Draw) { 
            payouts[n] = bets[n].amount; 
        } else { 
            if (_isWinningBet(_outcome, bets[n].chosenWinner,_winner)) { 
                payouts[n] = 0; 
            }
        }
    } 
for (n = 0; n < payouts.length; n++) {
    _payOutWinnings(bets[n].user, payouts[n]);
}
    _transferToHouse();
}
function checkOutcome(bytes32 _gameId) public notDisabled returns (BettingGames.GameOutcome) {
    BettingGames.GameOutcome outcome; 
    int8 winner = -1 

    (,,,,,outcome, winner) = BettingGames.getGame(_gameId);

    if (outcome == BettingGames.GameOutcome.Decided) { 
        if ()
    }
}

}