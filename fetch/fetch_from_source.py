import os
import pandas as pd
import argparse
from pathlib2 import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='fetch data args')
    parser.add_argument('-b', '--base_path',
                        help='directory to base', default='../')
    parser.add_argument(
        '-d', '--data', help='directory to training data', default='train')
    parser.add_argument(
        '-t', '--target', help='target file to hold good data', default='train.csv') 
   
    # parse arguments   
    args = parser.parse_args()
    
    # define paths
    base_path = Path(args.base_path).resolve(strict=False)
    data_path = base_path.joinpath(args.data).resolve(strict=False)
    target_path = Path(data_path).resolve(strict=False).joinpath(args.target)
    print('Train File: {}'.format(target_path))
    
    # read input csv file
    df = pd.read_csv('./userinput.csv')

    # renove the feast specific columns
    df.drop(['id', 'event_timestamp', 'created_timestamp'], axis=1, inplace=True)

    print(df.to_string())

    # create path if it doesn't exist
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    # Save processed input to a new csv file
    df.to_csv(target_path, index=False)

