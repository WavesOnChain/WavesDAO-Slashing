import math

# Variables
total_proposals = 77
quorum_percentage = 30

# Calculate the exact fractional value of proposals required for quorum
exact_quorum_value = (quorum_percentage / 100) * total_proposals
print(f"Exact quorum value (fractional): {exact_quorum_value}")  # Show the raw fractional value for reference

# Round down the fractional value to the nearest whole number to get the minimum required proposals
required_votes = math.floor(exact_quorum_value)
print(f"Minimum required votes to meet the quorum: {required_votes}\n")  # Show the final rounded-down requirement

# Person's participation
person_1_votes = 2  # Number of proposals Person 1 has voted on

# Check if Person 1 meets the quorum
if person_1_votes >= required_votes:
    print(f"Person 1 has voted on {person_1_votes} proposals and meets the quorum requirement")
else:
    print(f"Person 1 has voted on {person_1_votes} proposals and does NOT meet the quorum requirement")
    print(f"They need to vote on at least {required_votes - person_1_votes} more proposal(s)") 