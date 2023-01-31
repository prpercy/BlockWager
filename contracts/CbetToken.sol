pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

contract CbetToken is ERC20, ERC20Detailed, ERC20Mintable {
    address payable owner;

    // Generic modifier that can be applied to any function (as if this code is copy/pasted into function itself)
    modifier onlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _;
    }

    // Parameters passed into the constructor must be provided at deployment time
    // When deploy, token name, symbol, and decimals are automatically passed through
    constructor(uint initial_supply) 
        ERC20Detailed("CbetToken", "CBET", 18) 
        public 
    {
        // owner will be wallet/address who hit the deploy button
        owner = msg.sender;
        // At deploytment time, min arcade tokens with the initial_supply provided in this constructor
        // Note, this does not require any ether to be paid, just minted from scratch
        mint(msg.sender, initial_supply);
    }

}

