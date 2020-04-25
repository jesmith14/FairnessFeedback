import sys
import os
import collections
import numpy as np
import time
import argparse
from scripts import utils

def main():
    parser = argparse.ArgumentParser(description='Recommendation simulator',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Fundamental options
    parser.add_argument('-i', type=int, default=2,
                        help='Simulation rounds for running the recommender')
    parser.add_argument('-r', type=str, default='base',
                        help='Type of recommender [fair|base]')

    # "best" chooses the top ranked item for a user
    # "explore" uses softmax of recommended items as probability distribution for selection
    parser.add_argument('-s', type=str, default='explore',
                        help='Type of user selection [best|explore|random]')

    args = parser.parse_args()

    sim_itrs = args.i
    rec_type = args.r
    sel_type = args.s

    # set paths needed
    # [AZ] For now we will just go with exp00001
    root_dir = os.getcwd()
    data_file = f"{root_dir}/{rec_type}_recommender/data/ratings.csv"
    dup_file = f"{root_dir}/{rec_type}_recommender/data/ratings_dup.csv"
    result_path = f"{root_dir}/{rec_type}_recommender/exp00001/result"
    scripts_path = f"{root_dir}/scripts"
    log_path = f"{root_dir}/{rec_type}_recommender/exp00001/log"

    # delete the existing duplicate ratings file if exists
    if os.path.exists(data_file):
        print("Duplicate file exists.")
        os.system(f"rm -rf {dup_file}")
        print("Duplicate File deleted")

    # create new duplicate ratings file for new simulation cycles
    os.system(f"cp {data_file} {dup_file}")

    start_time = time.time()

    itr = 0
    while itr < sim_itrs:
        utils.load_ratings(dup_file)
        print(f"***********************Running simulation {itr+1}***********************")

        print("----------------------Train Run----------------------")

        # training run
        os.system(f"python -m librec_auto run {rec_type}_recommender -q")

        os.system(f"python3 scripts/extract_log_info.py {log_path} librec.log simulation_log_data.csv {itr} 1")

        print("----------------------Eval Run----------------------")

        # eval run
        os.system(f"python -m librec_auto eval {rec_type}_recommender -q")

        os.system(f"python3 scripts/extract_log_info.py {log_path} librec.log simulation_log_data_reranked.csv {itr} 1")

        # "files" include [out-1, out-2, .....]
        # TODO: figure out a way to use all out-*.txt files, if possible
        files = os.listdir(result_path)

        # choose one of the "out-*.txt" file
        result = np.random.choice(files)

        file_path = f"{result_path}/{result}"

        with open(file_path) as f:
            data = f.read().split("\n")
        f.close()

        cf = False

        if (cf) :
            predictions = utils.surprise_cf(dup_file)
            print("Length of predictions: " + str(len(predictions)))
            print("Taking 5500 random predictions.")
            user_sample = np.random.choice(predictions, 5500)
            with open(f"{os.getcwd()}/{rec_type}_recommender/data/ratings_dup.csv", "a") as f:
                for prediction in user_sample:
                    user = prediction.uid
                    print(user)
                    selection = prediction.iid
                    rating = prediction.r_ui
                    # r_ui(float): The true rating :math:`r_{ui}`.
                    # est(float): The estimated rating :math:`\\hat{r}_{ui}`.

                    f.write(f"{user},{selection},{rating}")
                    f.write("\n")
        else :
            user_dict = collections.OrderedDict()

            # create a dictionary of
            # {user1: [(item0, rank), (item1, rank), (item2, rank), ...],
            # user2: [...], user3:[...],...}
            for entry in data:
                if entry:
                    user, item, score = entry.split(',')
                    if user not in user_dict:
                        user_dict[user] = [(int(item), float(score))]
                    else:
                        user_dict[user].append((int(item), float(score)))

            user_sample = np.random.choice(list(user_dict), 5500)

            # write the new ratings into the duplicate ratings.csv for next round of simulation
            with open(f"{os.getcwd()}/{rec_type}_recommender/data/ratings_dup.csv", "a") as f:
                for user in user_sample:

                    # choose rating based on an existing probability distribution
                    selection, rating = utils.rate_item(user, user_dict[user], sel_type)

                    # insert the (user, item, rating) tuple into the ratings.csv
                    f.write(f"{user},{selection},{rating}")
                    f.write("\n")

            itr += 1



    end_time = time.time()

    print(f"Execution time: {end_time - start_time}")
    print(f"Type of recommender: {rec_type} recommender")
    print(f"Number of simulations: {sim_itrs}")

if __name__ == '__main__':
    main()
