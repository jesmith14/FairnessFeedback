# How To Run The Experiment
```
python3 -m venv {folder_name}
cd {folder_name}
git clone https://github.com/jesmith14/FairnessFeedback.git
pip install -r requirements.txt
cd FairnessFeedback
```

### How to run the fair recommender:
(this might take around 5 mins to run)

`python -m librec_auto run fair_recommender`

`python -m librec_auto eval fair_recommender`

The second step is necessary to get the evaluation result for the html page from the re-ranked results, this will override the result pngs of the base recommender as of now, we're working to fix this. The base recommender results are in the "original" folder, the re-ranker are in the "results" folder

### How to run the base recommender alone (this is ran automatically with the fair recommender):
`python -m librec_auto run base_recommender`

### How to run the simulation:
`python run_simulation.py -i 5 -r base -s best`

`python run_simulation.py -i 5 -r fair -s explore`

For help
`python run_simulation.py -h`

Code modified from [librec-auto-tutorial](https://github.com/that-recsys-lab/librec-auto-tutorial)
For extra guidance: [tutorial handout](https://docs.google.com/document/d/1ybazjee50e41pVwoN4CrEuRvcKfmDwQ-ZiGLrwmEUcM/edit?usp=sharing)
[librec-auto repo](https://github.com/that-recsys-lab/librec-auto)
