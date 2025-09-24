import json
from time import sleep

import requests

WAVES_DAO_ADDRESS = "3PEwRcYNAUtoFvKpBhKoiwajnZfdoDR6h4h"

session = requests.Session()


committers_list = session.get(
    f"https://beta-api.wavesonchain.com/v1/on-chain/power/committers/{WAVES_DAO_ADDRESS}"
).json()["commit_list"]

committer_stats = {}

for committer in committers_list:
    committer_address = committer["committer_address"]
    committed = committer["committed"]

    committer_stats[committer_address] = {
        "child_dao": WAVES_DAO_ADDRESS,
        "committed": committed,
        "committer_address": committer_address,
        "to_be_slashed_amount": int(committed * 0.3),
        "percentage": 0.0,
        "total_votes": 0,
        "voted_count": 0,
    }


all_proposals = session.get(
    "https://beta-api.wavesonchain.com/v1/on-chain/power/child-dao-proposals"
).json()
proposals = []

for proposal in all_proposals:
    if proposal["dao_address"] == WAVES_DAO_ADDRESS:
        proposals.append(proposal)

for proposal in proposals:
    response = session.get(
        f"https://beta-api.wavesonchain.com/v1/on-chain/power/child-dao-proposals/{proposal['_id']}/votes"
    )
    response.raise_for_status()
    data_json = response.json()
    for vote in data_json["votes"]:
        committer = vote["committer_address"]

        if committer not in committer_stats:
            continue

        committer_stats[committer]["total_votes"] += 1
        if vote["vote"] == "Yes" or vote["vote"] == "No":
            committer_stats[committer]["voted_count"] += 1
        elif vote["vote"] == "Didn't cast a vote" or vote["vote"] == "Retract":
            pass
        else:
            raise ValueError(f"Unknown vote type: {vote['vote']}")

        committer_stats[committer]["percentage"] = (
            committer_stats[committer]["voted_count"]
            / committer_stats[committer]["total_votes"]
        )

    sleep(0.3)  # To avoid hitting rate limits

print(committer_stats)

result = list(committer_stats.values())
result.sort(
    key=lambda x: (x["percentage"], x["committed"], x["committer_address"]),
    reverse=True,
)

with open("woc-waves-dao-all-time-vote-percentage.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

to_be_slashed = []

for committer in result:
    if committer["percentage"] < 0.30 and committer["total_votes"] >= 100:
        to_be_slashed.append(committer)

with open("woc-waves-dao-all-time-to-be-slashed.json", "w", encoding="utf-8") as f:
    json.dump(to_be_slashed, f, indent=4)


to_be_slashed_part1 = to_be_slashed[: len(to_be_slashed) // 2]
to_be_slashed_part2 = to_be_slashed[len(to_be_slashed) // 2 :]

part1_total = sum(c["to_be_slashed_amount"] for c in to_be_slashed_part1)
part2_total = sum(c["to_be_slashed_amount"] for c in to_be_slashed_part2)

tx_arg_value_part1 = ",".join(
    [
        f"{c['committer_address']}={c['to_be_slashed_amount']}"
        for c in to_be_slashed_part1
    ]
)
tx_arg_value_part2 = ",".join(
    [
        f"{c['committer_address']}={c['to_be_slashed_amount']}"
        for c in to_be_slashed_part2
    ]
)

tx_args_part1 = {
    "args": [
        {"type": "string", "value": "3PEwRcYNAUtoFvKpBhKoiwajnZfdoDR6h4h"},
        {"type": "string", "value": tx_arg_value_part1},
    ],
    "total_slashed": part1_total,
}
tx_args_part2 = {
    "args": [
        {"type": "string", "value": "3PEwRcYNAUtoFvKpBhKoiwajnZfdoDR6h4h"},
        {"type": "string", "value": tx_arg_value_part2},
    ],
    "total_slashed": part2_total,
}

with open("woc-waves-dao-all-time-tx-arg1.json", "w", encoding="utf-8") as f:
    json.dump(tx_args_part1, f, indent=4)

with open("woc-waves-dao-all-time-tx-arg2.json", "w", encoding="utf-8") as f:
    json.dump(tx_args_part2, f, indent=4)
