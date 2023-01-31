pragma solidity ^0.5.0;

contract TeamAccounts {
    address payable contractOwnerAddr;
    uint currTeamId = 1;

    mapping(uint => bool) teamExists;
    mapping(uint => string) teamNames;
    mapping(string => uint) teamIds;

    modifier onlyOwner {
        require(msg.sender == contractOwnerAddr, "Only the contracts owner has permissions for this action!");
        _;
    }

    constructor (address payable _contractOwnerAddr) 
        public 
    {
        contractOwnerAddr = _contractOwnerAddr;
    }

    function createTeam(string memory _teamName)
        public
        onlyOwner
        returns (uint)
    {
        require(teamIds[_teamName] == 0, "This team already exists!");
        uint teamId = currTeamId++;
        
        teamNames[teamId] = _teamName;
        teamIds[_teamName] = teamId;

        teamExists[teamId] = true;
        return teamId;
    }

    function getTeamName(uint _teamId)
        public
        view
        returns (string memory)
    {
        require(teamExists[_teamId] == true, "This team ID does not exist!");
        return teamNames[_teamId];
    }

    function getTeamId(string memory _teamName)
        public
        view
        returns (uint)
    {
        require(teamIds[_teamName] > 0, "This team does not exist, please create it first (createTeam)!");
        return teamIds[_teamName];
    }    
}
