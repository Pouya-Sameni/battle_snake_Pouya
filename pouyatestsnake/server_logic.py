import random
import math
from typing import List, Dict



def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
  
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'
    
    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves["left"] = possible_moves["left"]+1
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves["right"] = possible_moves["right"]+1
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves["down"] = possible_moves["down"]+1
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves["up"] = possible_moves["up"]+1

    return possible_moves

def avoid_my_body(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
  
    if "up" in possible_moves:
      up_cord = {"x":my_head["x"], "y":(my_head["y"]+1)}

      if up_cord in my_body: 
        possible_moves["up"] = possible_moves["up"]+1 

    if "down" in possible_moves:
      down_cord = {"x":my_head["x"], "y":(my_head["y"]-1)}
      if down_cord in my_body: 
        possible_moves["down"] = possible_moves["down"]+1 

    if "right" in possible_moves:
      right_cord = {"x":(my_head["x"]+1), "y":(my_head["y"])}
      if right_cord in my_body: 
        possible_moves["right"] = possible_moves["right"]+1 

    if "left" in possible_moves:
      left_cord = {"x":(my_head["x"]-1), "y":(my_head["y"])}
      if left_cord in my_body: 
        possible_moves["left"] = possible_moves["left"]+1 

    return possible_moves

def avoid_other_snakes(my_head: Dict[str, int], data:dict, possible_moves: List[str]) -> List[str]:
    
    if "up" in possible_moves:
      up_cord = {"x":my_head["x"], "y":(my_head["y"]+1)}

      for other_snakes in data["board"]["snakes"]:
        for other_snakes_body in other_snakes["body"]:
          if other_snakes_body["x"] == up_cord["x"] and other_snakes_body["y"] == up_cord["y"]:
            possible_moves["up"] = possible_moves["up"]+1

    if "down" in possible_moves:
      down_cord = {"x":my_head["x"], "y":(my_head["y"]-1)}
      for other_snakes in data["board"]["snakes"]:
        for other_snakes_body in other_snakes["body"]:
          if other_snakes_body["x"] == down_cord["x"] and other_snakes_body["y"] == down_cord["y"]:
            possible_moves["down"] = possible_moves["down"]+1

    if "right" in possible_moves:
      right_cord = {"x":(my_head["x"]+1), "y":(my_head["y"])}
      for other_snakes in data["board"]["snakes"]:
        for other_snakes_body in other_snakes["body"]:
          if other_snakes_body["x"] == right_cord["x"] and other_snakes_body["y"] == right_cord["y"]:
            possible_moves["right"] = possible_moves["right"]+1

    if "left" in possible_moves:
      left_cord = {"x":(my_head["x"]-1), "y":(my_head["y"])}
      for other_snakes in data["board"]["snakes"]:
        for other_snakes_body in other_snakes["body"]:
          if other_snakes_body["x"] == left_cord["x"] and other_snakes_body["y"] == left_cord["y"]:
            possible_moves["left"] = possible_moves["left"]+1

    return possible_moves

def avoid_boundaries(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str], data:dict) -> List[str]:
    if "up" in possible_moves and (my_head["y"] + 1)> data["board"]["height"]-1:
      possible_moves["up"] = possible_moves["up"]+1

    if "down" in possible_moves and (my_head["y"] - 1) < 0:
      possible_moves["down"] = possible_moves["down"]+1

    if "right" in possible_moves and (my_head["x"] + 1) > data["board"]["width"]-1:
      possible_moves["right"] = possible_moves["right"]+1

    if "left" in possible_moves and (my_head["x"] - 1) < 0:
      possible_moves["left"] = possible_moves["left"]+1

    print ("All Moves Are" + str(possible_moves))

    return possible_moves

def go_for_food(data: dict, my_head: Dict[str, int], possible_moves: List[str]) -> List[str]:
    
  
    foods = data["board"]["food"]

    if "left" in possible_moves and len(possible_moves) > 1:
      if foods[0]["x"] > my_head["x"]:
        possible_moves["left"] = possible_moves["left"]+1

    if "right" in possible_moves and len(possible_moves) > 1:
      if foods[0]["x"] <= my_head["x"]:
        possible_moves["right"] = possible_moves["right"]+1

    if "down" in possible_moves and len(possible_moves) > 1:
      if foods[0]["y"] > my_head["y"]:
        possible_moves["down"] = possible_moves["down"]+1

    if "up" in possible_moves and len(possible_moves) > 1:
      if foods[0]["y"] <= my_head["y"]:
        possible_moves["up"] = possible_moves["up"]+1
    
    return possible_moves

def final_check (data: dict, my_head: Dict[str, int], possible_moves: List[str])-> List[str]:
   

  for other_snakes in data["board"]["snakes"]:
    other_head = other_snakes["head"]
    
    if (my_head["x"] - 1) == other_head["x"] and (my_head["y"] + 1) == other_head["y"] and other_snakes["length"] >= data["you"]["length"]:
      if "up" in possible_moves:
        possible_moves["up"] = possible_moves["up"]+1
      if "left" in possible_moves:
        possible_moves["left"] = possible_moves["left"]+1

    elif (my_head["x"] - 1) == other_head["x"] and (my_head["y"] - 1) == other_head["y"] and other_snakes["length"] >= data["you"]["length"]:
      if "down" in possible_moves:
        possible_moves["down"] = possible_moves["down"]+1
      if "left" in possible_moves:
        possible_moves["left"] = possible_moves["left"]+1

    elif (my_head["x"] + 1) == other_head["x"] and (my_head["y"] + 1) == other_head["y"] and other_snakes["length"] >= data["you"]["length"]:
      if "up" in possible_moves:
        possible_moves["up"] = possible_moves["up"]+1
      if "right" in possible_moves:
        possible_moves["right"] = possible_moves["right"]+1

    elif (my_head["x"] + 1) == other_head["x"] and (my_head["y"] - 1) == other_head["y"] and other_snakes["length"] >= data["you"]["length"]:
      if "down" in possible_moves:
        possible_moves["down"] = possible_moves["down"]+1
      if "right" in possible_moves:
        possible_moves["right"] = possible_moves["right"]+1
    
    elif (my_head["x"]) == other_head["x"] and (my_head["y"] + 2) == other_head["y"] and other_snakes["length"] >= data["you"]["length"]:
     if "up" in possible_moves:
        possible_moves["up"] = possible_moves["up"]+1
    
    elif (my_head["x"]) == other_head["x"] and (my_head["y"] - 2) == other_head["y"] and other_snakes["length"] >= data["you"]["length"]:
     if "down" in possible_moves:
        possible_moves["down"] = possible_moves["down"]+1
    
    elif (my_head["x"]+ 2) == other_head["x"] and (my_head["y"]) == other_head["y"] and other_snakes["length"] >= data["you"]["length"]:
     if "right" in possible_moves:
        possible_moves["right"] = possible_moves["right"]+1
    
    elif (my_head["x"] - 2) == other_head["x"] and (my_head["y"]) == other_head["y"] and other_snakes["length"] >= data["you"]["length"]:
     if "left" in possible_moves:
        possible_moves["left"] = possible_moves["left"]+1


    return possible_moves 

def go_to_corner (data: dict, my_head: Dict[str, int], possible_moves: dict)-> List[str]:
    
    if my_head["x"] <= 5 and my_head["y"] <= 5:
      x_cord = 0
      y_cord = 0
    elif my_head["x"] <= 5 and my_head["y"] >= 5:
      x_cord = 0
      y_cord = 10
    elif my_head["x"] >= 5 and my_head["y"] >= 5:
      x_cord = 10
      y_cord = 10
    else:
      x_cord = 10
      y_cord = 0

    if "left" in possible_moves and len(possible_moves) > 1:
      if x_cord > my_head["x"]:
        possible_moves["left"] = possible_moves["left"]+1

    if "right" in possible_moves and len(possible_moves) > 1:
      if x_cord <= my_head["x"]:
        possible_moves["right"] = possible_moves["right"]+1

    if "down" in possible_moves and len(possible_moves) > 1:
      if y_cord > my_head["y"]:
        possible_moves["down"] = possible_moves["down"]+1

    if "up" in possible_moves and len(possible_moves) > 1:
      if y_cord <= my_head["y"]:
        possible_moves["up"] = possible_moves["up"]+1

    return possible_moves

def move_picker (data:dict, possible_moves:dict):

    my_head = data["you"]["head"]  

    my_body = data["you"]["body"]  

    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
  
    possible_moves = avoid_boundaries(my_head, my_body, possible_moves, data)

    possible_moves = avoid_my_body(my_head, my_body, possible_moves)

    possible_moves = avoid_other_snakes( my_head, data, possible_moves)

    possible_moves = final_check(data, my_head, possible_moves)
    
    if data["you"]["health"] <= 30:
      possible_moves = go_for_food(data, my_head, possible_moves)
    
    return possible_moves
    print ("List: " + str(possible_moves)) 

    

def choose_move(data: dict) -> str:
   
    possible_moves = {"up":0, "down":0, "left":0, "right":0}
    possible_moves = move_picker(data, possible_moves)
    move = min(possible_moves, key=possible_moves.get)

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
