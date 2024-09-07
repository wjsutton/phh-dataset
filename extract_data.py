from pokerkit import HandHistory
import polars as pl

def extract_hand_info(file_path):
    with open(file_path, 'rb') as file:
        hh = HandHistory.load(file)
    
    info = {
        'actions': hh.actions,
        'starting_stacks': hh.starting_stacks,
        'players': hh.players,
        'finishing_stacks': hh.finishing_stacks,
        'blinds_or_straddles': hh.blinds_or_straddles,
        'antes': hh.antes,
        'variant': hh.variant
    }
    
    return info

# Usage
#file_path = 'data/wsop/2023/43/5/00-02-07.phh'
file_path = 'data/wsop/2023/43/5/00-08-38.phh'
hand_info = extract_hand_info(file_path)

# Print extracted information
for key, value in hand_info.items():
    print(f"{key}: {value}")


def parse_actions(actions):
    parsed_actions = []
    for action in actions:
        parts = action.split()
        if parts[0] == 'd':
            if parts[1] == 'dh':
                parsed_actions.append(f"Deal hole cards to {parts[2]}: {parts[3]}")
            elif parts[1] == 'db':
                parsed_actions.append(f"Deal board cards: {' '.join(parts[2:])}")
        elif parts[1] in ['f', 'cc', 'cbr', 'sm']:
            action_type = {'f': 'folds', 'cc': 'calls', 'cbr': 'raises', 'sm': 'shows'}[parts[1]]
            parsed_actions.append(f"{parts[0]} {action_type} {' '.join(parts[2:])}")
    return parsed_actions

# Example usage
actions = hand_info['actions']
parsed = parse_actions(actions)

# for action in parsed:
#     print(action)

print(parsed)

dealt_cards = [action for action in parsed if action.startswith('Deal hole cards')]

print(dealt_cards)

# Filter for "Deal hole cards" actions and extract player and cards
dealt_cards = [action.split(': ') for action in dealt_cards if action.startswith('Deal hole cards')]
dealt_cards = [(player.split()[-1], cards) for player, cards in dealt_cards]

# Create a DataFrame from the dealt cards
df = pl.DataFrame({
    'player': [player for player, _ in dealt_cards],
    'player_name': hand_info['players'],
    'dealt_cards': [cards for _, cards in dealt_cards],
    'starting_stacks': hand_info['starting_stacks'],
    'blinds_or_straddles': hand_info['blinds_or_straddles'],
    'antes': hand_info['antes']
})

# Find the index of the last 'd dh' action
last_dh_index = max(i for i, action in enumerate(actions) if action.startswith('d dh'))

# Find the index of the first 'd db' action
first_db_index = next(i for i, action in enumerate(actions) if action.startswith('d db'))

# Extract the actions between these two points
preflop_actions = actions[last_dh_index + 1:first_db_index]
preflop_actions = parse_actions(preflop_actions)


# Create a DataFrame with a single column
preflop_df = pl.DataFrame({'preflop_action': preflop_actions})
print(preflop_df)

# Split the 'action' column into multiple columns
preflop_df = preflop_df.with_columns([
    pl.col('preflop_action').str.split(' ').alias('split_action')
])

# Extract player, move, and amount from the split_action list
preflop_df = preflop_df.with_columns([
    pl.col('split_action').list.get(0).alias('player'),
    pl.col('split_action').list.get(1).alias('preflop_move'),
    pl.col('split_action').list.get(2).cast(pl.Float64, strict=False).alias('preflop_raise_amount')
])

# Drop the intermediate columns
preflop_df = preflop_df.drop(['preflop_action', 'split_action'])

df = df.join(preflop_df, on='player', how='inner')
print(df)

