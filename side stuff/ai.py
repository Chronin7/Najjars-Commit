
# ai.py
#
# Generic Reinforcement Learning AI System
#
# Features:
# - Works with ANY game
# - Supports:
#     bool
#     float
#     int
#     list
# - Deep neural network
# - Replay memory
# - Q-learning
# - Save/load
# - Exploration
#
# Designed for:
# - Snake
# - Platformers
# - Shooters
# - Emulator AI
# - Eventually retro games like Super Metroid
#
# ================================================

import random
import math
import json
from collections import deque


# ================================================
# ACTIVATIONS
# ================================================

def relu(x):
    return max(0.0, x)


def relu_derivative(x):
    return 1.0 if x > 0 else 0.0


# ================================================
# BRAIN
# ================================================

class Brain:

    def __init__(
        self,
        input_size,
        output_size,
        hidden_layers=[64, 64],
        learning_rate=0.001,
        gamma=0.99,
        epsilon=1.0,
        epsilon_decay=0.99995,
        epsilon_min=0.02,
        memory_size=50000,
        batch_size=64
    ):

        self.input_size = input_size
        self.output_size = output_size

        self.hidden_layers = hidden_layers

        self.learning_rate = learning_rate

        self.gamma = gamma

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        self.batch_size = batch_size

        self.memory = deque(maxlen=memory_size)

        # ========================================
        # BUILD NETWORK
        # ========================================

        layer_sizes = (
            [input_size]
            + hidden_layers
            + [output_size]
        )

        self.weights = []
        self.biases = []

        for i in range(len(layer_sizes) - 1):

            current = layer_sizes[i]
            nxt = layer_sizes[i + 1]

            layer_weights = []

            for _ in range(current):

                row = []

                for _ in range(nxt):
                    row.append(random.uniform(-0.5, 0.5))

                layer_weights.append(row)

            layer_biases = []

            for _ in range(nxt):
                layer_biases.append(
                    random.uniform(-0.5, 0.5)
                )

            self.weights.append(layer_weights)
            self.biases.append(layer_biases)

    # ============================================
    # INPUT FLATTENING
    # ============================================

    def flatten(self, value):

        result = []

        if isinstance(value, bool):
            result.append(float(value))

        elif isinstance(value, (int, float)):
            result.append(float(value))

        elif isinstance(value, list):

            for item in value:
                result.extend(self.flatten(item))

        else:
            raise TypeError(
                f"Unsupported type: {type(value)}"
            )

        return result

    # ============================================
    # FORWARD PASS
    # ============================================

    def predict(self, state):

        x = self.flatten(state)

        if len(x) != self.input_size:
            raise ValueError(
                f"Expected {self.input_size} inputs "
                f"but got {len(x)}"
            )

        self.activations = [x]
        self.z_values = []

        current = x

        for layer_i in range(len(self.weights)):

            z_layer = []
            next_layer = []

            for neuron_i in range(len(self.biases[layer_i])):

                total = self.biases[layer_i][neuron_i]

                for prev_i in range(len(current)):

                    total += (
                        current[prev_i]
                        * self.weights[layer_i][prev_i][neuron_i]
                    )

                z_layer.append(total)

                # hidden layers
                if layer_i < len(self.weights) - 1:
                    next_layer.append(relu(total))

                # output layer
                else:
                    next_layer.append(total)

            self.z_values.append(z_layer)

            current = next_layer

            self.activations.append(current)

        return current

    # ============================================
    # ACTION SELECTION
    # ============================================

    def choose_action(self, state):

        # exploration
        if random.random() < self.epsilon:
            return random.randint(
                0,
                self.output_size - 1
            )

        q_values = self.predict(state)

        return q_values.index(max(q_values))

    # ============================================
    # MEMORY
    # ============================================

    def remember(
        self,
        state,
        action,
        reward,
        next_state,
        done
    ):

        self.memory.append(
            (
                state,
                action,
                reward,
                next_state,
                done
            )
        )

    # ============================================
    # TRAIN SINGLE SAMPLE
    # ============================================

    def train_single(
        self,
        state,
        target_q
    ):

        outputs = self.predict(state)

        # ========================================
        # OUTPUT ERROR
        # ========================================

        errors = []

        for i in range(self.output_size):
            errors.append(
                target_q[i] - outputs[i]
            )

        layer_errors = [errors]

        # ========================================
        # BACKPROPAGATE
        # ========================================

        for layer_i in reversed(
            range(len(self.weights) - 1)
        ):

            current_errors = []

            for neuron_i in range(
                len(self.activations[layer_i + 1])
            ):

                error = 0.0

                for next_i in range(
                    len(layer_errors[0])
                ):

                    error += (
                        layer_errors[0][next_i]
                        * self.weights[layer_i + 1][neuron_i][next_i]
                    )

                error *= relu_derivative(
                    self.z_values[layer_i][neuron_i]
                )

                current_errors.append(error)

            layer_errors.insert(0, current_errors)

        # ========================================
        # UPDATE WEIGHTS
        # ========================================

        for layer_i in range(len(self.weights)):

            inputs_to_layer = self.activations[layer_i]

            for input_i in range(len(inputs_to_layer)):

                for neuron_i in range(
                    len(layer_errors[layer_i])
                ):

                    self.weights[layer_i][input_i][neuron_i] += (
                        self.learning_rate
                        * layer_errors[layer_i][neuron_i]
                        * inputs_to_layer[input_i]
                    )

            # biases
            for neuron_i in range(
                len(self.biases[layer_i])
            ):

                self.biases[layer_i][neuron_i] += (
                    self.learning_rate
                    * layer_errors[layer_i][neuron_i]
                )

    # ============================================
    # EXPERIENCE REPLAY
    # ============================================

    def replay(self):

        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(
            self.memory,
            self.batch_size
        )

        for (
            state,
            action,
            reward,
            next_state,
            done
        ) in batch:

            target = self.predict(state)

            if done:
                target[action] = reward

            else:

                future_q = max(
                    self.predict(next_state)
                )

                target[action] = (
                    reward
                    + self.gamma * future_q
                )

            self.train_single(state, target)

        # decay exploration
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # ============================================
    # HELPERS
    # ============================================

    def output_float(
        self,
        outputs,
        index=0
    ):
        return outputs[index]

    def output_bool(
        self,
        outputs,
        index=0,
        threshold=0
    ):
        return outputs[index] > threshold

    def output_index(self, outputs):
        return outputs.index(max(outputs))

    def output_list(
        self,
        outputs,
        threshold=0
    ):

        result = []

        for i, value in enumerate(outputs):

            if value > threshold:
                result.append(i)

        return result

    # ============================================
    # SAVE
    # ============================================

    def save(self, filename):

        data = {

            "weights": self.weights,
            "biases": self.biases,

            "input_size": self.input_size,
            "output_size": self.output_size,

            "hidden_layers": self.hidden_layers,

            "learning_rate": self.learning_rate,

            "gamma": self.gamma,

            "epsilon": self.epsilon,
            "epsilon_decay": self.epsilon_decay,
            "epsilon_min": self.epsilon_min,

            "batch_size": self.batch_size
        }

        with open(filename, "w") as f:
            json.dump(data, f)

    # ============================================
    # LOAD
    # ============================================

    @classmethod
    def load(cls, filename):

        with open(filename, "r") as f:
            data = json.load(f)

        brain = cls(
            input_size=data["input_size"],
            output_size=data["output_size"],
            hidden_layers=data["hidden_layers"],
            learning_rate=data["learning_rate"],
            gamma=data["gamma"],
            epsilon=data["epsilon"],
            epsilon_decay=data["epsilon_decay"],
            epsilon_min=data["epsilon_min"],
            batch_size=data["batch_size"]
        )

        brain.weights = data["weights"]
        brain.biases = data["biases"]

        return brain
