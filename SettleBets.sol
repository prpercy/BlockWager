pragma solidity ^0.5.0;
import '.BlockWager.sol';
import './CbetAccounts.sol' ;
import './SafeMath.sol';
contract SettleBets is BlockWager,  CbetAccount {
    using SafeMath for uint; 
function _payOutwinnings_cbet (CbetAcountAdrr, _user, uint _amount) private {
 _user.transfer(_amount);

}
//seperate functions for the paying out in eth versus paying out in Cbet token
function _payoutwinnings_eth(address, _user, _amount) private { 
    _user.transfer(_amount) 
}

//for transfering to house in event of  user losing
function _transfertoHouse() private { 
    owner.transfer(address(this.balance));

}
//needs to be fixed this doesnt work yet
function _isWinningBet(isWin, bool, BlockWager.getBetTotalAddress, uint _amount) private 
private pure returns(bool) {
    return _outcome == BettingGames.GameOutcome.Decided && _chosenWinner >= 0 
    && (_chosenWinner ==uint8(_actualWinner)) 
}
_calculatePayout() {}


function _payoutForGame(bytes32, BlockWager.gameEvent, _winner) private {
    Bet[] storage bets = BettingGames.[_gameId];
    uint losingTotal = 0;
    uint winningTotal = 0; 
    uint totalsPot = 0;
    uint[] memory payuts = new uint[](bets.length);

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

//internal function for checking to see if bets were actually settled. not yet implemented
function checkOutcome(bytes32 _gameId) public notDisabled returns (BlockWager.gameEvent) {
    Blockwager.gameEvent.outcome; 
    int8 winner = -1 

    (,,,,,outcome, winner) = BettingGames.getGame(_gameId);

    if (outcome == BettingGames.GameOutcome.Decided) { 
        if ()
    }
}

}