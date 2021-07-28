import random
import math
from typing import List, Dict



def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
  
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'
    
    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def avoid_my_body(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
  
    if "up" in possible_moves:
      up_cord = {"x":my_head["x"], "y":(my_head["y"]+1)}

      if up_cord in my_body: 
        possible_moves.remove("up") 

    if "down" in possible_moves:
      down_cord = {"x":my_head["x"], "y":(my_head["y"]-1)}
      if down_cord in my_body: 
        possible_moves.remove("down") 

    if "right" in possible_moves:
      right_cord = {"x":(my_head["x"]+1), "y":(my_head["y"])}
      if right_cord in my_body: 
        possible_moves.remove("right") 

    if "left" in possible_moves:
      left_cord = {"x":(my_head["x"]-1), "y":(my_head["y"])}
      if left_cord in my_body: 
        possible_moves.remove("left") 

    return possible_moves

def avoid_other_snakes(my_head: Dict[str, int], data:dict, possible_moves: List[str]) -> List[str]:
    
    if "up" in possible_moves:
      up_cord = {"x":my_head["x"], "y":(my_head["y"]+1)}

      for other_snakes in data["board"]["snakes"]:
        for other_snakes_body in other_snakes["body"]:
          if other_snakes_body["x"] == up_cord["x"] and other_snakes_body["y"] == up_cord["y"]:
            possible_moves.remove("up")

    if "down" in possible_moves:
      down_cord = {"x":my_head["x"], "y":(my_head["y"]-1)}

      for other_snakes in data["board"]["snakes"]:
        for other_snakes_body in other_snakes["body"]:
          if other_snakes_body["x"] == down_cord["x"] and other_snakes_body["y"] == down_cord["y"]:
            possible_moves.remove("down")

    if "right" in possible_moves:
      right_cord = {"x":(my_head["x"]+1), "y":(my_head["y"])}
      for other_snakes in data["board"]["snakes"]:
        for other_snakes_body in other_snakes["body"]:
          if other_snakes_body["x"] == right_cord["x"] and other_snakes_body["y"] == right_cord["y"]:
            possible_moves.remove("right")

    if "left" in possible_moves:
      left_cord = {"x":(my_head["x"]-1), "y":(my_head["y"])}
      for other_snakes in data["board"]["snakes"]:
        for other_snakes_body in other_snakes["body"]:
          if other_snakes_body["x"] == left_cord["x"] and other_snakes_body["y"] == left_cord["y"]:
            possible_moves.remove("left")

    return possible_moves

def avoid_boundaries(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str], data:dict) -> List[str]:
    if "up" in possible_moves and (my_head["y"] + 1)> data["board"]["height"]-1:
      possible_moves.remove("up")

    if "down" in possible_moves and (my_head["y"] - 1) < 0:
      possible_moves.remove("down")

    if "right" in possible_moves and (my_head["x"] + 1) > data["board"]["width"]-1:
      possible_moves.remove("right")

    if "left" in possible_moves and (my_head["x"] - 1) < 0:
      possible_moves.remove("left")

    print ("All Moves Are" + str(possible_moves))

    return possible_moves

def go_for_food(data: dict, my_head: Dict[str, int], possible_moves: List[str]) -> List[str]:
    
    food_distance_list = {}
    foods = data["board"]["food"]

    if "left" in possible_moves and len(possible_moves) > 1:
      if foods[0]["x"] > my_head["x"]:
        possible_moves.remove("left")

    if "right" in possible_moves and len(possible_moves) > 1:
      if foods[0]["x"] <= my_head["x"]:
        possible_moves.remove("right")

    if "down" in possible_moves and len(possible_moves) > 1:
      if foods[0]["y"] > my_head["y"]:
        possible_moves.remove("down")

    if "up" in possible_moves and len(possible_moves) > 1:
      if foods[0]["y"] <= my_head["y"]:
        possible_moves.remove("up")
    
    return possible_moves




def choose_move(data: dict) -> str:
   
    my_head = data["you"]["head"]  

    my_body = data["you"]["body"]  

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    
  
    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    possible_moves = avoid_boundaries(my_head, my_body, possible_moves, data)

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body
    
    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake
    possible_moves = avoid_my_body(my_head, my_body, possible_moves)

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board
    
    possible_moves = avoid_other_snakes( my_head, data, possible_moves)
    possible_moves = go_for_food(data, my_head, possible_moves)

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move