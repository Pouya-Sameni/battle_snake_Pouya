import random
import math
from typing import List, Dict

danger_map: List[List[int]] = [];
DEATH_BODY = -2;
DEATH_HEAD = -1;
EMPTY = 0;

eat_map: List[List[int]] = [];
FOOD = 10;
KILL_HEAD = 11;


# initialize all to 2d array of 0s
def init_matrices(data: dict):
  global danger_map;
  global eat_map;

  danger_map = [[0]*data['board']['height'] for i in range(data['board']['width'])];
  eat_map = [[0]*data['board']['height'] for i in range(data['board']['width'])];


def wipe(matrix: List[List[int]]):
  for col in range(len(matrix)):
    for cell in range(len(matrix)):
      matrix[col][cell] = 0;


def update_matrices_immediate(data: Dict):
  global danger_map;
  global eat_map;

  wipe(danger_map);
  wipe(eat_map);

  for me_piece in data['you']['body'][:-1]:
    danger_map[me_piece['x']][me_piece['y']] = DEATH_BODY;

  for s in data['board']['snakes']:
    if s['id'] == data['you']['id']:
      continue;
    longer_than_you = s['length'] >= data['you']['length'];
    head_moves = neighbors(s['head'], data['board']['width'], data['board']['height']);
    for head in head_moves:
      if longer_than_you:
        danger_map[head['x']][head['y']] = DEATH_HEAD;
      else:
        eat_map[head['x']][head['y']] = KILL_HEAD;
  # snake body will override a head move (good)
    for body_piece in s['body'][:-1]:
      danger_map[body_piece['x']][body_piece['y']] = DEATH_BODY;

  for f in data['board']['food']:
    eat_map[f['x']][f['y']] = FOOD;
  
  for x in danger_map:
    print(x)



def neighbors(coordinate: dict, board_width: int, board_height: int) -> List[dict]:
  x = coordinate['x'];
  y = coordinate['y'];
  up = y + 1;
  down = y - 1;
  left = x - 1;
  right = x + 1;

  out = [];
  if up < board_height:
    out.append({ 'x': x, 'y': up });
  if down >= 0:
    out.append({ 'x': x, 'y': down });
  if left >= 0:
    out.append({ 'x': left, 'y': y });
  if right < board_width:
    out.append({ 'x': right, 'y': y });
  
  return out;

def remove_death_moves(my_head, possible_moves, death_type) -> List[str]:
  x = my_head['x'];
  y = my_head['y'];
  up = y + 1;
  down = y - 1;
  left = x - 1;
  right = x + 1;

  if 'up' in possible_moves and danger_map[x][up] <= death_type:
    possible_moves.remove('up');
  if 'down' in possible_moves and danger_map[x][down] <= death_type:
    possible_moves.remove('down');
  if 'left' in possible_moves and danger_map[left][y] <= death_type:
    possible_moves.remove('left');
  if 'right' in possible_moves and danger_map[right][y] <= death_type:
    possible_moves.remove('right');

  return possible_moves;


def avoid_boundaries(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str], data:dict) -> List[str]:
  if "up" in possible_moves and (my_head["y"] + 1) > data["board"]["height"]-1:
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
  update_matrices_immediate(data);

  my_head = data["you"]["head"]  

  my_body = data["you"]["body"]  

  possible_moves = ["up", "down", "left", "right"]

  # lol i hate myself
  consider = avoid_boundaries(my_head, my_body, possible_moves, data)
  if len(consider): possible_moves = consider;
  consider = remove_death_moves(my_head, possible_moves, DEATH_BODY)
  if len(consider): possible_moves = consider;
  consider = remove_death_moves(my_head, possible_moves, DEATH_HEAD)
  if len(consider): possible_moves = consider;
  
  # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board
  
  possible_moves = go_for_food(data, my_head, possible_moves)

  # Choose a random direction from the remaining possible_moves to move in, and then return that move
  move = random.choice(possible_moves)
  # TODO: Explore new strategies for picking a move that are better than random

  print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

  return move

