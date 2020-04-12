import os
import csv
import sys

location = ''#'fair_recommender/exp00001/log/'
log_filename = ''#'librec.log'
out_filename = '' #'simulation_log_data.csv'
simulation_number = '' #-1
out_location = f"{os.getcwd()}/logs/"
float_format = '{0:.10f}'
# need to write code to populate this list
attributes = ['SimulationNumber', 'DiscountedProportionalPFairnessEvaluator','RecallEvaluator', 'StatisticalParityEvaluator','PrecisionEvaluator']
average_text = "Average Evaluation Result of Cross Validation"

def validate_out_file() :
    print("Checking to see whether output file exists...")
    if os.path.isfile(os.path.join(out_location, out_filename)) :
        print("File exists, checking to see whether headers match.")
        headers = ''
        out_file = open(os.path.join(out_location, out_filename), 'r')
        headers = out_file.readline()
        if headers == ",".join(attributes)+ "\n" :
            print("Headers match. Proceed.")
        else :
            print("Headers do not match. Please proceed with a different file name or different headers. Exiting.")
            sys.exit()
        out_file.close();
    else :
        print("File does not exist. Creating file.")
        out_file = open(os.path.join(out_location, out_filename), 'w')
        out_file_writer = csv.DictWriter(out_file, fieldnames=attributes)
        out_file_writer.writeheader()
        out_file.close()

def read_log() :
    lines = []
    new_row = {}
    new_row[attributes[0]] = simulation_number
    with open(os.path.join(location,log_filename), "r") as f :
        file_lines = f.readlines()
        print("Read in " + str(len(file_lines)) + " lines from " + location + log_filename)

        # handle cross validation if present
        avg_index = [x for x in range(len(file_lines)) if average_text in file_lines[x]]
        print("Found average at line: " + str(avg_index))

        #check for cross validation not present
        eval_lines = [] # TODO : case where no cross validation
        if len(avg_index) > 0 :
            ind = avg_index[len(avg_index)-1]
            eval_lines = file_lines[ind:]
            print("Length of eval lines: " + str(len(eval_lines)))
            # now it should be the first instance of each text no matter what, so we just locate it
            for line in eval_lines :
                for exp in attributes[1:] :
                    if exp in line :
                        lines.append(line)
                        input_str = line[(line.index(exp)+len(exp)+4):len(line)-1] #index of name + length + 4 for ' is '
                        new_row[exp] = float_format.format(float(input_str))
    return new_row

def write(new_row) :
    # writing to output file
    print("type" + str(type(float(new_row['PrecisionEvaluator']))))
    with open(os.path.join(out_location, out_filename), 'a+', newline='') as out_file :
        print("Writing fields to file at" + os.path.join(out_location, out_filename))
        print(new_row)
        print(attributes)

        out_file_writer = csv.DictWriter(out_file, fieldnames=attributes)
        out_file_writer.writerow(new_row)
        out_file.close()

if __name__ == "__main__" :
    print("Usage: python3 extract_log_info.py <log_dir> <log_filename> <out_filename> <simulation_number> <evaluation attribute group>")

    location = sys.argv[1]
    log_filename = sys.argv[2]
    out_filename = sys.argv[3]
    simulation_number = sys.argv[4]
    attribute_group = sys.argv[5]

    print("Running with: location: " + location + "; log_filename: " + log_filename + "; out_filename: " + out_filename + "; simulation_number: " + simulation_number)
    print("Attributes...")
    print(attributes)

    validate_out_file()
    extracted_row = read_log()
    write(extracted_row)
