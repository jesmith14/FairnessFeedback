Welcome to the Fairness vs Feedback repository! This houses the code for an ongoing project to test the relationship between fairness-aware re-ranking in recommendation systems and unwanted feedback loops/echo chambers for users. Below you will find the instructions for utilizing this code in the best way.

# How To Run The Experiment
To get the code downloaded and running on your machine or server, you will need to run these commands:

```
python3 -m venv {folder_name}
cd {folder_name}
git clone https://github.com/jesmith14/FairnessFeedback.git
pip install -r requirements.txt
cd FairnessFeedback
```

### How to run the fair recommender:
In order to run the fair recommender, you must run both of these commands. The `run` command will run the base recommender and the `eval` command will run the re-ranking process and produce the visuals for the re-ranker.

`python -m librec_auto run fair_recommender`

`python -m librec_auto eval fair_recommender`

The second step is necessary to get the evaluation result for the html page from the re-ranked results, this will override the result pngs of the base recommender as of now, but we're working to fix this. The base recommender results are in the "original" folder, the re-ranker are in the "results" folder

### How to run the base recommender alone:

`python -m librec_auto run base_recommender`

### How to run the simulation:
In order to run the simulation, you will need to use the following commands. You can run the simulation on just the base recommender or on the fair recommender, with different options for simulation-type and number of simulations.

For example, in the following command we are specifying to run the base recommender with the "best" simulation on 5 rounds. The following command is running the fair re-ranker with the "explore" simulation for 5 rounds.

`python run_simulation.py -i 5 -r base -s best`

`python run_simulation.py -i 5 -r fair -s explore`

For help
`python run_simulation.py -h`

All of the results of the experiments are in the `\logs` folder. The `simulation_log.csv` holds the evaluation metrics for the base recommender, while the `simulation_log_reranked.csv` holds the evaluation metrics for the re-ranker. If you would like to test other metrics like popularity bias, you can utilize the `ratings.csv` (the original user-item ratings) and the `ratings_dup.csv` (the final user-item ratings after simulations have been ran).

Every simulation will add 5500 user-item ratings to the training dataset before completing a new round of training and recommendations.

If you would like to change the items that are considered "protected", you will need to modify the `item-features.csv` files (there are several version available in this repository). As well, you can make any changes to the recommendation algorithm, evaluation metrics, and re-ranker in the `conf/config.xml` file.

If you have any questions, or troubles feel free to refer to these examples for how to use librec-auto:
[librec-auto-tutorial](https://github.com/that-recsys-lab/librec-auto-tutorial)
For extra guidance: [tutorial handout](https://docs.google.com/document/d/1ybazjee50e41pVwoN4CrEuRvcKfmDwQ-ZiGLrwmEUcM/edit?usp=sharing)
[librec-auto repo](https://github.com/that-recsys-lab/librec-auto)
