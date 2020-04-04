import sys
import os
import random
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description='Recommendation simulator',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Fundamental options
    parser.add_argument('-i', type=int, default=2,
                        help='Simulation rounds for [fair|base] recommender')
    parser.add_argument('-r', type=str, default='base',
                        help='Type of recommender [fair|base]')

    args = parser.parse_args()

    sim_itrs = args.i
    rec_type = args.r

    # set paths needed
    # TODO: need to take care of exp00000 vs exp00001
    root_dir = os.getcwd()
    data_file = f"{root_dir}/{rec_type}_recommender/data/ratings.csv"
    dup_file = f"{root_dir}/{rec_type}_recommender/data/ratings_dup.csv"
    result_path = f"{root_dir}/{rec_type}_recommender/exp00000/result"

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
        
        # training run
        os.system(f"python -m librec_auto run {rec_type}_recommender -q")

        # eval run
        os.system(f"python -m librec_auto eval {rec_type}_recommender -q")

        # "files" include [out-1, out-2, .....]
        # TODO: figure out a way to use all out-*.txt files, if possible
        files = os.listdir(result_path)

        # choose one of the "out-*.txt" file
        result = random.choice(files)

        file_path = f"{result_path}/{result}"

        with open(file_path) as f:
            data = f.read().split("\n")
        f.close()


        user_dict = {}

        # create a dictionary of {user: [(item0, rank), (item1, rank), (item2, rank), ...]}
        for entry in data:
            if entry:
                user, item, rank = entry.split(",")
                if user not in user_dict:
                    user_dict[user] = [(int(item), float(rank))]
                else:
                    user_dict[user].append((int(item), float(rank)))

        sample_users = random.sample(user_dict.keys(), 10)

        ratings = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        
        # random weights assigned to the ratings
        # can be modified based on some scale
        weights = [0.01, 0.03, 0.04, 0.1, 0.12, 0.18, 0.2, 0.13, 0.1, 0.07]

        new_ratings = []

        # write the new ratings into the duplicate ratings.csv for next round of simulation
        with open(f"{os.getcwd()}/{rec_type}_recommender/data/ratings_dup.csv", "a") as f:
            for user in sample_users:
                
                # choose the highest ranked.
                # item = 0
                
                # choose random item for different users.
                # item_number: index of the item for a particular user in the user_dict
                item_number = random.choice(range(10))
                
                # choose rating based on an existing probability distribution
                rating = random.choices(ratings, weights=weights, k=1)
                # print(f"User: {user} \tItem: {user_dict[user][item_number][0]} \tRating: {rating[0]}")
                
                # insert the (user, item_number, rating) tuple into the ratings.csv
                f.write(f"{user},{user_dict[user][0][0]},{rating[0]}")
                f.write("\n")

        itr += 1

    end_time = time.time()

    print(f"Execution time: {end_time - start_time}")
    print(f"Type of recommender: {rec_type} recommender")
    print(f"Number of simulations: {sim_itrs}")

if __name__ == '__main__':
    main()