# Slime Volleyball Gym Environment

## Installation
The program runs on Python 3.7. Install all dependency to do training and evaluation:
```sh
git clone https://github.com/JStrick510/slimevolleygym.git
cd slimevolleygym
pip install -e .
```

## Basic Usage

Train the agents:
```python
# Train agent against PPO
python training_scripts/train_w_best_opponent.py

# Train agent against GA
python training_scripts/train_w_best_ga.py

```

Evaluation the agents:

```python
# Evaluate ppo_new against baseline
python eval_agents.py --left baseline --right ppo_new

# Evaluate ppo_ga against ppo_new
python eval_agents.py --left ppo_new --right ppo_ga 

# Evaluate ppo_ga against ppo_new with render
python eval_agents.py --left ppo_new --right ppo_ga --render

```

## Training Result

Training result are located under folder `best_opponent_vs_ppo1` and `best_opponent_ga`:
1. `final_model.zip`: 
  the final model to evaluate in the game
2. `progress.csv`: the progress of training

Folder Structure:
```
├── best_opponent_ga
│   ├── final_model.zip
│   └── progress.csv
├── best_opponent_vs_ppo1
│   ├── final_model.zip
│   └── progress.csv
├── setup.py
├── training_scripts
└── zoo
```