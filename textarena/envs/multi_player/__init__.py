""" Register multi-player environments """

from textarena.envs.registration import register


# Register Individual Games
register(
    id="CharacterConclave-multiplayer-v0",
    entry_point="textarena.envs.multi_player.CharacterConclave.env:CharacterConclaveEnv",
    num_players=5,
    character_budget=1_000,
)

register(
    id="CharacterConclave-multiplayer-v0-long",
    entry_point="textarena.envs.multi_player.CharacterConclave.env:CharacterConclaveEnv",
    num_players=5,
    character_budget=5_000,
)

register(
    id="CharacterConclave-multiplayer-v0-extreme",
    entry_point="textarena.envs.multi_player.CharacterConclave.env:CharacterConclaveEnv",
    num_players=5,
    character_budget=10_000,
)