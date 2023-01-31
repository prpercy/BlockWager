pragma solidity ^0.5.0;

contract SportAccounts {
    address payable contractOwnerAddr;
    uint currSportId = 1;

    mapping(uint => bool) sportExists;
    mapping(uint => string) sportNames;
    mapping(string => uint) sportIds;

    modifier onlyOwner {
        require(msg.sender == contractOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    constructor (address payable _contractOwnerAddr) 
        public 
    {
        contractOwnerAddr = _contractOwnerAddr;
    }

    function createSport(string memory _sportName)
        public
        onlyOwner
        returns (uint)
    {
        require(sportIds[_sportName] == 0, "This sport already exists!");
        uint sportId = currSportId++;
        
        sportNames[sportId] = _sportName;
        sportIds[_sportName] = sportId;

        sportExists[sportId] = true;
        return sportId;
    }

    function getSportName(uint _sportId)
        public
        view
        returns (string memory)
    {
        require(sportExists[_sportId] == true, "This sport ID does not exist!");
        return sportNames[_sportId];
    }

    function getSportId(string memory _sportName)
        public
        view
        returns (uint)
    {
        require(sportIds[_sportName] > 0, "This sport does not exist, please create it first (createSport)!");
        return sportIds[_sportName];
    }    
}
