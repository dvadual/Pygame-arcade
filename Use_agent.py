import torch
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
class DQN(nn.Module):
    def __init__(self,n_observations,n_actions,hidden_size):
        super().__init__()
        self.layer1= nn.Linear(n_observations,hidden_size)
        self.layer2 =nn.Linear(hidden_size,hidden_size)
        self.layer3= nn.Linear(hidden_size,n_actions)
    def forward(self,observations):
        x = F.relu(self.layer1(observations))
        x = F.relu(self.layer2(x))
        return self.layer3(x)



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

 
n_actions = 8
checkpoint = torch.load(
    "dqn_checkpoint_1.pth",
    map_location=device
)
agent = DQN(
    n_observations=checkpoint["n_observations"],
    n_actions=n_actions,
    hidden_size=checkpoint["hidden_size"]
).to(device)



agent.load_state_dict(
    checkpoint["policy_net"]
)
# -------------------------
# Action dictionary
# -------------------------

action_dict = {
    0: [1, 0, 0, 0],
    1: [0, 1, 0, 0],
    2: [0, 0, 1, 0],
    3: [0, 0, 0, 1],
    4: [1, 0, 1, 0],
    5: [1, 0, 0, 1],
    6: [0, 1, 1, 0],
    7: [0, 1, 0, 1]
}


# -------------------------
# Load trained network
# -------------------------


agent.eval()



def choose_action(observation):
    
    observation_list=[]

    if observation:
        for key,value in observation.items():
            observation_list+=list(value)

    state = torch.tensor(
        observation_list,
        dtype=torch.float32,
        device=device
    ).unsqueeze(0)

    with torch.no_grad():

        q_values = agent(state)

        action_index = q_values.argmax(dim=1).item()

    return action_dict[action_index]