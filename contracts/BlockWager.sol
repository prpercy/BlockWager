pragma solidity ^0.5.0;

import "./SportAccounts.sol";
import "./TeamAccounts.sol";
import "./CbetAccount.sol";
import "./BettorAccounts.sol";
import "./BettingGames.sol";

contract BetContract is SportAccounts, TeamAccounts, CbetAccount, BettorAccounts, BettingGames {
    address betContractOwner;

    constructor()
        SportAccounts(msg.sender)
        TeamAccounts(msg.sender)
        CbetAccount(msg.sender)
        BettorAccounts(msg.sender)
        BettingGames(msg.sender)
        public 
    {
        betContractOwner = msg.sender;
    }

}
