import random
import util_functions
import math,time
BOARD=[
["🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪"]]
class snake:
    def __init__(self,board):
        self.board=board
        self.direction="right"
        self.snake_poses=[]
        while True:
            val1=random.randint(0,14)
            val2=random.randint(0,14)
            if not self.board[val1][val2] in ["🟪","🟩","🟥"]:
                self.board[val1][val2]="🟥"
                self.head_pos=[val1,val2]
                break
        self.score=0
        self.snake_len=5
        self.frut=[7,11]
        while True:
            val1=random.randint(0,14)
            val2=random.randint(0,14)
            if not self.board[val1][val2] in ["🟪","🟩","🟥"]:
                self.board[val1][val2]="🟨"
                self.furt=[val1,val2]
                break
    def left(self):
        if self.direction!="right":
            self.direction="left"
    def right(self):
        if self.direction!="left":
            self.direction="right"
    def up(self):
        if self.direction!="down":
            self.direction="up"
    def down(self):
        if self.direction!="up":
            self.direction="down"
    def tic(self):
        if self.direction=="up":
            self.head_pos=[self.head_pos[0]-1,self.head_pos[1]]
        if self.direction=="down":
            self.head_pos=[self.head_pos[0]+1,self.head_pos[1]]
        if self.direction=="left":
            self.head_pos=[self.head_pos[0],self.head_pos[1]-1]
        if self.direction=="right":
            self.head_pos=[self.head_pos[0],self.head_pos[1]+1]
        for num1,x in enumerate(self.board):
            for num2,y in enumerate(x):
                if [num1,num2]in self.snake_poses:
                    self.board[num1][num2]="🟩"
                else:
                    if not self.board[num1][num2] in ["🟪","🟨","🟩"]:
                        self.board[num1][num2]="⬛"
        self.snake_poses.append(self.head_pos)
        if len(self.snake_poses)>self.snake_len:
            setit=self.snake_poses.pop(0)
            self.board[setit[0]][setit[1]]="⬛"
        if self.board[self.head_pos[0]][self.head_pos[1]] in ["🟪","🟩"]:
            return "game over"
        if self.board[self.head_pos[0]][self.head_pos[1]] in ["🟨"]:
            self.score+=1
            self.snake_len+=1
            while True:
                val1=random.randint(0,14)
                val2=random.randint(0,14)
                if not self.board[val1][val2] in ["🟪","🟩","🟥"]:
                    self.board[val1][val2]="🟨"
                    self.furt=[val1,val2]
                    break
        self.board[self.head_pos[0]][self.head_pos[1]]="🟥"

        #🟥 🟧 🟨 🟩 🟦 🟪 🟫 ⬛ ⬛
    def reset(self):
        self.board=[["🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛","🟪"],
["🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪","🟪"]]
        self.score=0
        self.snake_len=5
        self.direction="right"
        self.snake_poses=[]
        while True:
            val1=random.randint(0,14)
            val2=random.randint(0,14)
            if not self.board[val1][val2] in ["🟪","🟩","🟥"]:
                self.board[val1][val2]="🟥"
                self.head_pos=[val1,val2]
                break
        while True:
            val1=random.randint(0,14)
            val2=random.randint(0,14)
            if not self.board[val1][val2] in ["🟪","🟩","🟥"]:
                self.board[val1][val2]="🟨"
                self.furt=[val1,val2]
                break
game=snake(BOARD)
from ai import *
import sys
brain = nural_net([8, 8], 4, 4)


def mesh(iterations):
    eaten = 0
    epsilon = 0.3  # Chance of random move
    
    for x in range(iterations):
        # 1. FIX TYPOS & GET STATE
        # Note: Ensure snake class uses 'food_pos' consistently
        head_r, head_c = game.head_pos
        food_r, food_c = game.frut # Matches your snake class 'frut'
        
        # Calculate distance before move
        dist_before = math.dist([head_r, head_c], [food_r, food_c])
        
        # Normalize inputs for the neural net
        state = [
            head_r / 15.0,
            head_c / 15.0,
            food_r / 15.0,
            food_c / 15.0
        ]

        # 2. AI DECISION
        predictions = brain.predict(state)
        
        if random.random() < epsilon:
            move_idx = random.randint(0, 3)
        else:
            move_idx = predictions.index(max(predictions))

        # 3. EXECUTE MOVE
        moves = [game.up, game.left, game.down, game.right]
        moves[move_idx]()
        
        scored_before = game.score
        result = game.tic()

        # 4. REWARD CALCULATION
        if result == "game over":
            reward = -10.0
            game.reset()
        elif game.score > scored_before:
            reward = 20.0  # Big reward for food
            eaten += 1
        else:
            # Distance-based reward: Did we get closer?
            dist_after = math.dist(game.head_pos, game.frut)
            if dist_after < dist_before:
                reward = 1.0  # Moving toward food
            else:
                reward = -1.5 # Moving away or wasting time

        # 5. RE-TRAIN (Q-Learning Update)
        # We tell the brain: "In that state, choosing that move should result in this reward"
        targets = game.furt
        print(targets)
        print(move_idx)
        targets[move_idx-1] = reward
        brain.train(state, targets, lr=0.01)

        # 6. DECAY EXPLORATION
        # Slowly stop being random as we learn (minimum 5%)
        if epsilon > 0.05:
            epsilon -= 0.00005

        # 7. RENDER
        if x % 10 == 0: # Render every 10 steps to speed up training
            util_functions.clear_term()
            for row in game.board:
                sys.stdout.write("".join(row) + "\n")
            sys.stdout.write(f"Step: {x} | Eaten: {eaten} | Target: {game.frut}\n")

# Run the training
mesh(200000)
