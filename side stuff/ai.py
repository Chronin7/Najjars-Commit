import json,math,random,time
class node:
    def __init__(self,inputs: list,operation: str,name: str = "node"):
        self.inputs = inputs
        self.operation = operation
        self.name = name
        self.value = random.uniform(-5,5)
        self.gradient = 0.0 # dLoss / dNode
    def to_dict(self):
        return {
            "name": self.name,
            "operation": self.operation,
            "value": self.value,
            "inputs": [n.name for n in self.inputs] # Store names,not objects
        }

    def compute(self):
        if not self.inputs: return self.value
        
        vals = [n.value for n in self.inputs]
        if self.operation == "+":    
            self.value = sum(vals)
        elif self.operation == "*":  
            self.value = vals[0] * vals[1] if len(vals) > 1 else vals[0]
        elif self.operation == "sig": # Sigmoid for boolean-like output
            self.value = 1 / (1 + math.exp(-vals[0]))
        elif self.operation == ">":   # Comparison
            self.value = 1.0 if vals[0] > vals[1] else 0.0
            
        return self.value

    def backward(self):
        if not self.inputs: return
        
        # Simple Chain Rule implementations
        if self.operation == "+":
            for n in self.inputs: n.gradient += 1.0 * self.gradient
        elif self.operation == "*":
            self.inputs[0].gradient += self.inputs[1].value * self.gradient
            self.inputs[1].gradient += self.inputs[0].value * self.gradient
        elif self.operation == "sig":
            # dSigmoid = s * (1 - s)
            s = self.value
            self.inputs[0].gradient += (s * (1 - s)) * self.gradient
class NodeManager:
    def __init__(self):
        self.nodes = []

    def train_step(self,target,learning_rate=0.01):
        # 1. Forward Pass
        for n in self.nodes:
            n.compute()
        
        # 2. Calculate Loss Gradient (assuming last node is output)
        output_node = self.nodes[-1]
        # Loss = (output - target)^2 -> Derivative = 2 * (output - target)
        output_node.gradient = 2 * (output_node.value - target)

        # 3. Backward Pass (Reverse order)
        for n in reversed(self.nodes):
            if n.inputs: # Only nodes with parents have a backward pass
                n.backward()

        # 4. Update Weights (Nodes with no inputs act as weights/parameters)
        for n in self.nodes:
            if not n.inputs:
                n.value -= learning_rate * n.gradient
            n.gradient = 0 # Reset for next step
        
    def add_node(self,n: node):
        self.nodes.append(n)
        return n

    def run(self):
        """Executes all nodes in the order they were added."""
        results = {}
        for n in self.nodes:
            val = n.compute()
            results[n.name] = val
        return results

    def set_input(self,name: str,value):
        """Manually set value for an input node."""
        for n in self.nodes:
            if n.name == name:
                n.value = value
    
    def save(self,filename: str):
        data = [n.to_dict() for n in self.nodes]
        with open(filename,'w') as f:
            json.dump(data,f,indent=4)
        print(f"Graph saved to {filename}")

    def load(self,filename: str):
        with open(filename,'r') as f:
            data = json.load(f)
        
        self.nodes = []
        node_map = {}

        # 1. Recreate all node objects first
        for d in data:
            new_node = node([],d['operation'],d['name'])
            new_node.value = d['value']
            node_map[d['name']] = new_node
            self.nodes.append(new_node)

        # 2. Re-link the inputs based on stored names
        for d in data:
            current_node = node_map[d['name']]
            current_node.inputs = [node_map[input_name] for input_name in d['inputs']]
    def run_and_learn(self,input_vals: list,targets: list,lr=0.1):
        # 1. Load Inputs (Convert Bool to Float)
        for i,val in enumerate(input_vals):
            self.inputs[i].value = float(val)

        # 2. Forward Pass
        for n in self.nodes:
            n.compute()

        # 3. Calculate Loss & Backward Pass
        # We calculate gradients for all outputs provided in targets
        for i,target in enumerate(targets):
            target_f = float(target)
            out_node = self.outputs[i]
            # Mean Squared Error Gradient
            out_node.gradient = 2 * (out_node.value - target_f)

        # 4. Backward Pass (Reverse)
        for n in reversed(self.nodes):
            n.backward()

        # 5. Update Weights (Nodes with no inputs and no name in 'inputs')
        for n in self.nodes:
            if not n.inputs and n not in self.inputs:
                n.value -= lr * n.gradient
            n.gradient = 0 # Reset

        return [n.value for n in self.outputs]
class nural_net:
    def __init__(self, layer_sizes, input_count, output_count):
        self.mgr = NodeManager()
        self.inputs = []
        self.outputs = []
        
        # 1. Create Input Nodes
        for i in range(input_count):
            n = self.mgr.add_node(node([], "", f"in_{i}"))
            self.inputs.append(n)
            
        prev_layer = self.inputs
        
        # 2. Create Hidden Layers
        # layer_sizes example: [8, 8]
        for l_idx, size in enumerate(layer_sizes):
            current_layer = []
            for n_idx in range(size):
                # Weight nodes (parameters with no inputs)
                weights = [self.mgr.add_node(node([], "", f"w_l{l_idx}_n{n_idx}_i{i}")) 
                           for i in range(len(prev_layer))]
                
                # Multiply inputs by weights and sum them
                # For simplicity, we'll sum (input * weight) pairs
                mult_nodes = []
                for i, p_node in enumerate(prev_layer):
                    m = self.mgr.add_node(node([p_node, weights[i]], "*", f"m_l{l_idx}_n{n_idx}_i{i}"))
                    mult_nodes.append(m)
                
                # Sum the results and pass through Sigmoid activation
                sum_node = self.mgr.add_node(node(mult_nodes, "+", f"sum_l{l_idx}_n{n_idx}"))
                sig_node = self.mgr.add_node(node([sum_node], "sig", f"sig_l{l_idx}_n{n_idx}"))
                
                current_layer.append(sig_node)
            prev_layer = current_layer

        # 3. Create Output Nodes
        for i in range(output_count):
            # Final output layer (connected to last hidden layer)
            out_weights = [self.mgr.add_node(node([], "", f"out_w_{i}_{j}")) 
                           for j in range(len(prev_layer))]
            out_mults = [self.mgr.add_node(node([prev_layer[j], out_weights[j]], "*", f"out_m_{i}_{j}"))
                         for j in range(len(prev_layer))]
            
            out_final = self.mgr.add_node(node(out_mults, "+", f"out_{i}"))
            self.outputs.append(out_final)
            
        # Attach to manager for the run_and_learn method
        self.mgr.inputs = self.inputs
        self.mgr.outputs = self.outputs

    def predict(self, input_vals):
        return self.mgr.run_and_learn(input_vals, [0]*len(self.outputs), lr=0)

    def train(self, input_vals, targets, lr=0.1):
        return self.mgr.run_and_learn(input_vals, targets, lr=lr)
