import math

# Variables
total_proposals = 77
quorum_percentage = 30

# Calculate minimum proposals required to meet quorum
required_votes = math.ceil((quorum_percentage / 100) * total_proposals)

# Person's participation
person_1_votes = 2  # Number of proposals Person 1 has voted on

# Check if Person 1 meets the quorum
if person_1_votes >= required_votes:
    print(f"Person 1 has voted on {person_1_votes} proposals and meets the quorum requirement")
else:
    print(f"Person 1 has voted on {person_1_votes} proposals and does NOT meet the quorum requirement")
    print(f"They need to vote on at least {required_votes - person_1_votes} more proposal(s)") 