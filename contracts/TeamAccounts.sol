pragma solidity ^0.5.0;

// Container class to hold all the different "Teams" the BlockWager application will support
//    - Will be able to dynamically add new types of teams to be wagered on (e.g. NY Giants, NY Jets, Kansas City Chiefs, etc.)

contract TeamAccounts {
    address payable contractOwnerAddr;    // BlockWager contract owner address
    uint currTeamId = 1;                  // Free running counter used to generate a unique teamId for every new unique team being created.

    mapping(uint => bool) teamExists;     // Mapping the teamId to a boolean to protect that once a team has been created, it cannot be created again
    mapping(uint => string) teamNames;    // Mapping of the teamId to a the team (will be used as a reference id to the team - instead of passing the more expensive string name through the code)
    mapping(string => uint) teamIds;      // If needed, providing a rever map look-up to get the team the reference id (teamId) is pointing to

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

    // Create the team to be wagered on (e.g. _teamName = Giants, NY Jets, Kansas City Chiefs, etc.)
    function createTeam(string memory _teamName)
        public
        onlyOwner
        returns (uint)
    {
        require(teamIds[_teamName] == 0, "This team already exists!");
        uint teamId = currTeamId++;    // increment the sportId for "next" team creation

        teamNames[teamId] = _teamName;
        teamIds[_teamName] = teamId;

        teamExists[teamId] = true;
        return teamId;
    }

    // Getter function to get the generated teamId given the team
    function getTeamId(string memory _teamName)
        public
        view
        returns (uint)
    {
        require(teamIds[_teamName] > 0, "This team does not exist, please create it first (using createTeam)!");
        return teamIds[_teamName];
    }

    // Getter function to get the retrieve the team given the teamId (if needed, for reverse lookup)
    function getTeamName(uint _teamId)
        public
        view
        returns (string memory)
    {
        require(teamExists[_teamId] == true, "This team ID does not exist!");
        return teamNames[_teamId];
    }

}


