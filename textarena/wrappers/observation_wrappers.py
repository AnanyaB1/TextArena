from textarena.core import ObservationWrapper, Env, Wrapper
from typing import Any, Dict, Optional, Tuple, Union

__all__ = [
    "LLMObservationWrapper"
]

class LLMObservationWrapper(ObservationWrapper):
    """ TODO """
    def __init__(self, env:Env):
        """ TODO"""
        super().__init__(env)
        self.full_observations = {}


    def reset(self, seed:Optional[int]=None) -> Tuple[Optional[Dict[int, str]], Dict[str, Any]]:
        """ TODO """
        observations, info = self.env.reset(seed=seed)
        self.full_observations = observations.copy() if observations else {}
        return self.full_observations, info
        # observations, info = self.env.reset(seed=seed)
        # # reset the full observations
        # self.full_observations = observations # inital observations are just copied 

        # return self.full_observations, info 


    def observation(
        self, observations: Optional[Dict[int, str]] # player-wise observations
    ) -> Optional[Dict[int, str]]: # full player-wise observations
        # """ TODO """
        # # check if game provided observations
        # if observations is None:
        #     return None 

        # # extend the full observations with the current observations
        # for player_id in observations.keys():
        #     self.full_observations[player_id] += observations[player_id]

        # # return the full observations
        # # debugging
        # input(self.full_observations)
        # return self.full_observations 
        if observations is None:
            return None 

        # Extend the full observations with the current observations
        for player_id, obs in observations.items():
            if player_id in self.full_observations:
                self.full_observations[player_id] += obs
            else:
                self.full_observations[player_id] = obs

        # Debugging: Display the full observations
        # input(self.full_observations)
        return self.full_observations