pragma solidity >=0.4.22 <0.7.0;

contract Ballot {
  // This declares a new complex type which will
  // be used for variables later.
  // It will represent a single voter.
  struct Voter {
	bool allowed_to_vote;
	bool voted;  // if true, that person already voted
	uint vote;   // index of the voted proposal
  }

  // This is a type for a single proposal.
  struct Proposal {
	bytes32 name;   // short name (up to 32 bytes)
	uint voteCount; // number of accumulated votes
  }

  address public chairperson;

  // This declares a state variable that
  // stores a `Voter` struct for each possible address.
  mapping(address => Voter) public voters;

  // A dynamically-sized array of `Proposal` structs.
  Proposal[] public proposals;

  /// Create a new ballot to choose one of `proposalNames`.
  constructor(bytes32[] memory proposalNames) public {
	chairperson = msg.sender;
	voters[chairperson].allowed_to_vote = true;

	// For each of the provided proposal names,
	// create a new proposal object and add it
	// to the end of the array.
	for (uint i = 0; i < proposalNames.length; i++) {
	  // `Proposal({...})` creates a temporary
	  // Proposal object and `proposals.push(...)`
	  // appends it to the end of `proposals`.
	  proposals.push(Proposal({
		  name: proposalNames[i],
			  voteCount: 0
			  }));
	}
  }

  // Give `voter` the right to vote on this ballot.
  // May only be called by `chairperson`.
  function giveRightToVote(address voter) public {
	require(
			msg.sender == chairperson,
			"Only chairperson can give right to vote."
			);
	require(
			!voters[voter].voted,
			"The voter already voted."
			);
	voters[voter].allowed_to_vote = true;
  }

  function vote(uint proposal) public {
	Voter storage sender = voters[msg.sender];
	require(sender.allowed_to_vote, "Not allowed to vote");
	require(!sender.voted, "Already voted.");
	sender.voted = true;
	sender.vote = proposal;

	// If `proposal` is out of the range of the array,
	// this will throw automatically and revert all
	// changes.
	proposals[proposal].voteCount += 1;
  }

  /// @dev Computes the winning proposal taking all
  /// previous votes into account.
  function winningProposal() public view
	returns (uint winningProposal_)
  {
	uint winningVoteCount = 0;
	for (uint p = 0; p < proposals.length; p++) {
	  if (proposals[p].voteCount > winningVoteCount) {
		winningVoteCount = proposals[p].voteCount;
		winningProposal_ = p;
	  }
	}
  }

  // Calls winningProposal() function to get the index
  // of the winner contained in the proposals array and then
  // returns the name of the winner
  function winnerName() public view
	returns (bytes32 winnerName_)
  {
	winnerName_ = proposals[winningProposal()].name;
  }
}
