"""
Capture the Flag team: TurkiyeIsTheBest

Offensive agent focuses on efficient food collection and strategic returns.
Defensive agent maintains position and intercepts invaders.
"""

from __future__ import annotations

import typing

import pacai.core.agentinfo
import pacai.capture.agents


def create_team() -> list[pacai.core.agentinfo.AgentInfo]:
    """
    Returns agent configuration for the capture team.
    """
    return [
        pacai.core.agentinfo.AgentInfo(name = f"{__name__}.OptimizedOffense"),
        pacai.core.agentinfo.AgentInfo(name = f"{__name__}.OptimizedDefense"),
    ]


class OptimizedOffense(pacai.capture.agents.OffensiveAgent):
    """
    Optimized offensive agent - fast execution with smart decisions.
    """

    def __init__(self, **kwargs: typing.Any) -> None:
        # Tuned weights for best performance
        base_weights = {
            'score': 110.0,
            'distance_to_food': -3.5,
            'stopped': -150.0,
            'reverse': -5.0,
            'on_home_side': -18.0,
            'distance_to_ghost': 2.5,
            'distance_to_ghost_squared': 0.12,
        }
        
        super().__init__(override_weights = base_weights, **kwargs)
        
    def get_features(self, state, action):
        """
        Fast feature extraction with smart return logic.
        """
        # Use parent's optimized features
        features = super().get_features(state, action)
        
        # Extract state information
        food_carrying = state.get_agent_state(self.get_index()).get_num_carrying()
        successor = self.get_successor(state, action)
        my_state = successor.get_agent_state(self.get_index())
        my_pos = my_state.get_position()
        
        # Get game state
        time_left = state.get_data().get_timeleft()
        score = self.get_score(state)
        
        # Quick ghost distance check
        enemies = [successor.get_agent_state(i) for i in self.get_opponents(successor)]
        ghosts = [e for e in enemies if not e.is_pacman() and e.get_position() is not None]
        
        min_ghost_dist = 999
        for ghost in ghosts:
            if ghost.get_scared_timer() < 3:  # Only dangerous ghosts
                g_dist = self.get_maze_distance(my_pos, ghost.get_position())
                min_ghost_dist = min(min_ghost_dist, g_dist)
        
        # Smart return logic - simple but effective
        should_return = (
            food_carrying >= 4 or
            (food_carrying >= 3 and score > 1) or
            (food_carrying >= 3 and min_ghost_dist < 5) or
            (food_carrying >= 2 and score > 6) or
            (food_carrying > 0 and time_left < 120)
        )
        
        if should_return:
            # Prioritize getting home
            if 'on_home_side' in features:
                features['on_home_side'] = features['on_home_side'] * 6.5
            if 'distance_to_food' in features:
                features['distance_to_food'] = 0.0
        
        # Chase scared ghosts (simple check)
        for enemy in enemies:
            if enemy.is_pacman() or enemy.get_position() is None:
                continue
            if enemy.get_scared_timer() > 5:
                dist = self.get_maze_distance(my_pos, enemy.get_position())
                if dist < 5:
                    features['chase_scared'] = -dist * 8.0  # Aggressive chase
                    break
        
        return features
    
    def is_red(self):
        """Returns true if agent is on red team."""
        return self.get_index() < 2


class OptimizedDefense(pacai.capture.agents.DefensiveAgent):
    """
    Optimized defensive agent - aggressive interception.
    """

    def __init__(self, **kwargs: typing.Any) -> None:
        # Aggressive defensive weights
        override_weights = {
            'on_home_side': 120.0,
            'stopped': -200.0,
            'reverse': -3.0,
            'num_invaders': -2000.0,
            'distance_to_invader': -30.0,
        }
        
        super().__init__(override_weights = override_weights, **kwargs)

    def get_features(self, state, action):
        """
        Fast defensive features with smart prioritization.
        """
        # Use parent's features (already optimized)
        features = super().get_features(state, action)
        
        successor = self.get_successor(state, action)
        my_state = successor.get_agent_state(self.get_index())
        my_pos = my_state.get_position()
        
        # Smart invader prioritization
        enemies = [successor.get_agent_state(i) for i in self.get_opponents(successor)]
        invaders = [e for e in enemies if e.is_pacman() and e.get_position() is not None]
        
        if invaders and len(invaders) > 1:
            # Multiple invaders - prioritize the one closest to our food
            food_list = self.get_food_you_are_defending(state).as_list()
            
            if food_list:
                best_threat = 999999
                for invader in invaders:
                    inv_pos = invader.get_position()
                    my_dist = self.get_maze_distance(my_pos, inv_pos)
                    
                    # Quick check - only look at first 3 food pieces for speed
                    min_food_dist = min([
                        self.get_maze_distance(inv_pos, food) 
                        for food in food_list[:3]
                    ])
                    
                    # Threat score: prioritize invaders near food
                    threat = my_dist - (min_food_dist * 2)
                    best_threat = min(best_threat, threat)
                
                # Override with threat-based distance
                features['distance_to_invader'] = best_threat * -35.0
        
        return features
    
    def is_red(self):
        """Returns true if agent is on red team."""
        return self.get_index() < 2
