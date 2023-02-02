pragma solidity ^0.5.0;

import "./SportAccounts.sol";
import "./TeamAccounts.sol";
import "./CbetAccount.sol";
import "./UserAccounts.sol";
import "./BettingGames.sol";

contract BlockWager is SportAccounts, TeamAccounts, CbetAccount, UserAccounts, BettingGames {
    address betContractOwner;

    constructor()
        SportAccounts(msg.sender)
        TeamAccounts(msg.sender)
        CbetAccount(msg.sender)
        UserAccounts(msg.sender)
        BettingGames(msg.sender)
        public 
    {
        betContractOwner = msg.sender;
    }

}
