pragma solidity ^0.5.0;

// Container class to hold all the different "Sports" the BlockWager application will support
//    - Will be able to dynamically add new types of sports to be wagered on (e.g. Football, Baseball, Basketball, etc.)

contract SportAccounts {
    address payable contractOwnerAddr;    // BlockWager contract owner address
    uint currSportId = 1;                 // Free running counter used to generate a unique sportId for every new unique sport being created.

    mapping(uint => bool) sportExists;    // Mapping the sportId to a boolean to protect that once a sport has been created, it cannot be created again
    mapping(uint => string) sportNames;   // Mapping of the sportId to a the sport (will be used as a reference id to the sport - instead of passing the more expensive string name through the code)
    mapping(string => uint) sportIds;     // If needed, providing a rever map look-up to get the sport the reference id (sportId) is pointing to

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

    // Create the sport to be wagered on (e.g. _sportName = Football, Baseball, Basketball, etc.)
    function createSport(string memory _sportName)
        public
        onlyOwner
        returns (uint)
    {
        require(sportIds[_sportName] == 0, "This sport already exists!");
        uint sportId = currSportId++;  // increment the sportId for "next" sport creation

        sportNames[sportId] = _sportName;
        sportIds[_sportName] = sportId;

        sportExists[sportId] = true;
        return sportId;
    }

    // Getter function to get the generated sportId given the sport
    function getSportId(string memory _sportName)
        public
        view
        returns (uint)
    {
        require(sportIds[_sportName] > 0, "This sport does not exist, please create it first (using createSport)!");
        return sportIds[_sportName];
    }

    // Getter function to get the retrieve the sport given the sportId (if needed, for reverse lookup)
    function getSportName(uint _sportId)
        public
        view
        returns (string memory)
    {
        require(sportExists[_sportId] == true, "This sport ID does not exist!");
        return sportNames[_sportId];
    }

}


