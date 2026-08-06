
# snake_ai.py
# FULL Snake AI using generic neural network

import pygame
import random
import math
import time

# =========================================================
# AI
# =========================================================

class Brain:
    def __init__(
        self,
        input_size,
        hidden_layers=[32, 32],
        output_size=4
    ):
        self.input_size = input_size
        self.hidden_layers = hidden_layers
        self.output_size = output_size

        layer_sizes = [input_size] + hidden_layers + [output_size]

        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):
            current = layer_sizes[i]
            nxt = layer_sizes[i + 1]

            layer_weights = [
                [random.uniform(-1, 1) for _ in range(nxt)]
                for _ in range(current)
            ]

            layer_biases = [
                random.uniform(-1, 1)
                for _ in range(nxt)
            ]

            self.weights.append(layer_weights)
            self.biases.append(layer_biases)

    def relu(self, x):
        return max(0, x)

    def predict(self, inputs):
        self.activations = [inputs]

        current = inputs

        for layer_i in range(len(self.weights)):
            next_vals = []

            for neuron_i in range(len(self.biases[layer_i])):
                total = self.biases[layer_i][neuron_i]

                for prev_i in range(len(current)):
                    total += (
                        current[prev_i]
                        * self.weights[layer_i][prev_i][neuron_i]
                    )

                if layer_i < len(self.weights) - 1:
                    val = self.relu(total)
                else:
                    val = total

                next_vals.append(val)

            current = next_vals
            self.activations.append(current)

        return current

    def train(
        self,
        inputs,
        targets,
        learning_rate=0.001
    ):
        outputs = self.predict(inputs)

        errors = [
            targets[i] - outputs[i]
            for i in range(self.output_size)
        ]

        layer_errors = [errors]

        for layer_i in reversed(range(len(self.weights) - 1)):
            current_errors = []

            for neuron_i in range(len(self.activations[layer_i + 1])):
                error = 0

                for next_i in range(len(layer_errors[0])):
                    error += (
                        layer_errors[0][next_i]
                        * self.weights[layer_i + 1][neuron_i][next_i]
                    )

                if self.activations[layer_i + 1][neuron_i] > 0:
                    error *= 1
                else:
                    error *= 0

                current_errors.append(error)

            layer_errors.insert(0, current_errors)

        for layer_i in range(len(self.weights)):
            inputs_to_layer = self.activations[layer_i]

            for input_i in range(len(inputs_to_layer)):
                for neuron_i in range(len(layer_errors[layer_i])):
                    self.weights[layer_i][input_i][neuron_i] += (
                        learning_rate
                        * layer_errors[layer_i][neuron_i]
                        * inputs_to_layer[input_i]
                    )

            for neuron_i in range(len(self.biases[layer_i])):
                self.biases[layer_i][neuron_i] += (
                    learning_rate
                    * layer_errors[layer_i][neuron_i]
                )

# =========================================================
# GAME
# =========================================================

GRID_SIZE = 20
CELL_SIZE = 25

WIDTH = GRID_SIZE * CELL_SIZE+500
HEIGHT = GRID_SIZE * CELL_SIZE+100

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI")

clock = pygame.time.Clock()

BLACK = (20, 20, 20)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
WHITE = (240, 240, 240)

font = pygame.font.SysFont(None, 30)


class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [[10, 10]]
        self.direction = [1, 0]

        self.length = 5

        self.score = 0

        self.spawn_food()

        self.steps = 0

    def spawn_food(self):
        while True:
            x = random.randint(1, GRID_SIZE - 2)
            y = random.randint(1, GRID_SIZE - 2)

            if [x, y] not in self.snake:
                self.food = [x, y]
                return

    def move(self):
        self.steps += 1

        new_head = [
            self.snake[-1][0] + self.direction[0],
            self.snake[-1][1] + self.direction[1]
        ]

        # wall collision
        if (
            new_head[0] <= 0 or
            new_head[0] >= GRID_SIZE - 1 or
            new_head[1] <= 0 or
            new_head[1] >= GRID_SIZE - 1
        ):
            return "dead"

        # self collision
        if new_head in self.snake:
            return "dead"

        self.snake.append(new_head)

        if len(self.snake) > self.length:
            self.snake.pop(0)

        # food
        if new_head == self.food:
            self.length += 1
            self.score += 1
            self.spawn_food()
            return "food"

        return "alive"

    def draw(self):
        win.fill(BLACK)

        # walls
        for x in range(GRID_SIZE):
            pygame.draw.rect(
                win,
                WHITE,
                (x * CELL_SIZE, 0, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                win,
                WHITE,
                (x * CELL_SIZE,
                 (GRID_SIZE - 1) * CELL_SIZE,
                 CELL_SIZE,
                 CELL_SIZE)
            )

        for y in range(GRID_SIZE):
            pygame.draw.rect(
                win,
                WHITE,
                (0, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                win,
                WHITE,
                ((GRID_SIZE - 1) * CELL_SIZE,
                 y * CELL_SIZE,
                 CELL_SIZE,
                 CELL_SIZE)
            )

        # snake
        for s in self.snake:
            pygame.draw.rect(
                win,
                GREEN,
                (
                    s[0] * CELL_SIZE,
                    s[1] * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
            )

        # food
        pygame.draw.rect(
            win,
            RED,
            (
                self.food[0] * CELL_SIZE,
                self.food[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

        txt = font.render(
            f"""Games: {games} | Score: {game.score} | Best: {best_score} | Total: {score} | Reward: {reward} | Epsilon: {round(epsilon, 3)}""",
            True,
            WHITE
        )

        win.blit(txt, (10, 550))

        pygame.display.update()


# =========================================================
# AI SETUP
# =========================================================

brain = Brain(
    input_size=12,
    hidden_layers=[32, 32],
    output_size=4
)

game = SnakeGame()

epsilon = 1.0

games = 0
best_score = 0

# =========================================================
# MAIN LOOP
# =========================================================

running = True
score=0
reward=0
while running:

    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    head_x, head_y = game.snake[-1]

    food_x, food_y = game.food

    # =====================================================
    # STATE
    # =====================================================

    state = [

        # danger up
        int(
            [head_x, head_y - 1] in game.snake or
            head_y - 1 <= 0
        ),

        # danger down
        int(
            [head_x, head_y + 1] in game.snake or
            head_y + 1 >= GRID_SIZE - 1
        ),

        # danger left
        int(
            [head_x - 1, head_y] in game.snake or
            head_x - 1 <= 0
        ),

        # danger right
        int(
            [head_x + 1, head_y] in game.snake or
            head_x + 1 >= GRID_SIZE - 1
        ),

        # food up
        int(food_y < head_y),

        # food down
        int(food_y > head_y),

        # food left
        int(food_x < head_x),

        # food right
        int(food_x > head_x),

        # moving up
        int(game.direction == [0, -1]),

        # moving down
        int(game.direction == [0, 1]),

        # moving left
        int(game.direction == [-1, 0]),

        # moving right
        int(game.direction == [1, 0]),
    ]

    # =====================================================
    # AI MOVE
    # =====================================================

    outputs = brain.predict(state)

    if random.random() < epsilon:
        move = random.randint(0, 3)
    else:
        move = outputs.index(max(outputs))

    # up
    if move == 0 and game.direction != [0, 1]:
        game.direction = [0, -1]

    # down
    elif move == 1 and game.direction != [0, -1]:
        game.direction = [0, 1]

    # left
    elif move == 2 and game.direction != [1, 0]:
        game.direction = [-1, 0]

    # right
    elif move == 3 and game.direction != [-1, 0]:
        game.direction = [1, 0]

    dist_before = math.dist(
        game.snake[-1],
        game.food
    )

    score_before = game.score

    result = game.move()

    dist_after = math.dist(
        game.snake[-1],
        game.food
    )

    # =====================================================
    # REWARD
    # =====================================================

    if result == "dead":
        reward -=10
        
    elif result == "food":
        reward += 20

    else:
        if dist_after < dist_before:
            reward += 1
        else:
            reward -= 1
    reward+=game.length-4
    # =====================================================
    # TRAIN
    # =====================================================

    targets = outputs[:]

    targets[move] = reward

    brain.train(
        state,
        targets,
        learning_rate=0.001
    )

    # =====================================================
    # RESET
    # =====================================================

    if result == "dead":

        games += 1

        if game.score > best_score:
            best_score = game.score
        score+=game.score
        print(
            "Games:",
            games,
            "| Score:",
            game.score,
            "| Best:",
            best_score,
            "| Total: ",
            score,
            "| Reward",
            reward,
            "| Epsilon:",
            round(epsilon, 3)
        )
        
        if best_score>10:
            print("hasa")
        reward=0
        game.reset()

    # =====================================================
    # EPSILON DECAY
    # =====================================================

    if epsilon > 0.2:
        for x in range(game.score+1):
            epsilon *= 0.99995
        epsilon *= 0.999995
    if epsilon <.5 and best_score<3:
        epsilon=1
    # =====================================================
    # DRAW
    # =====================================================

    game.draw()

pygame.quit()
