import os
import pandas as pd

PATH = os.path.dirname(__file__)
#path_trials = PATH + "/trials_test.csv" # 4 trials
path_trials = PATH + "/trials.csv" # 24 trials
class Experiment:
    trials = pd.read_csv(path_trials, sep=";")
    #seqs = pd.read_csv(PATH+"/matrix.csv", sep=",") # for tests
    seqs = pd.read_csv(PATH + "/matrix16.csv", sep=",") # full matrix
    def __init__(self):
        self.data = self.generate_trial_dataset()
        self.group = None

    def set_group(self, key):
        if key % 2 == 0:
            self.group = "CAA"
        else:
            self.group = "DA"

        return self.group

    def get_order(self):
        self.trials_iter = list(self.seqs.iloc[self.key, :])[1:3]
        self.seqs = self.seqs.iloc[:, 1:3]
        return self.trials_iter

    def get_group(self):
        if self.group != None:
            return self.group

    def generate_trial_dataset(self, trials_iter=pd.Series()):
        col = ["seq", 'audio_play_time', "opinion_before", "r_time1", "confidence_before", "play_time", "opinion_after", "r_time2",
               "confidence_after", "trust_system", "difficulty_level", "y_pred", "case"]
        cols = []
        if len(trials_iter) != 0:
            for i in trials_iter:
                for j in col:
                    cols.append(str(i) + "_" + j)
            col = cols
        return pd.DataFrame(columns=col)




