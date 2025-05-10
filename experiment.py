import os
import pandas as pd

PATH = os.path.dirname(__file__)
# path_trials = PATH + "/trials_test.csv" # 4 trials
path_trials = PATH + "/trials.csv"  # 24 trials


class Experiment:
    """
    Class to manage the experiment. It contains the trial dataset and the
    sequence dataset."""

    trials = pd.read_csv(path_trials, sep=";")
    # seqs = pd.read_csv(PATH+"/matrix.csv", sep=",") # for tests
    seqs = pd.read_csv(PATH + "/matrix16.csv", sep=",")  # full matrix

    def __init__(self):
        self.data = self.generate_trial_dataset()
        self.group = None

    def set_group(self, key):
        """
        Set the group based on the key. The key is an integer that is
        provided by the user. The group is determined by the parity of
        the key. If the key is even, the group is "CAA". If the key is
        odd, the group is "DA". The group is stored in the instance
        variable self.group. The method returns the group as a string.
        """
        if key % 2 == 0:
            self.group = "CAA"
        else:
            self.group = "DA"

        return self.group

    def get_order(self):
        """
        Get the order of the trials based on the key.
        """
        self.trials_iter = list(self.seqs.iloc[self.key, :])[1:3]
        self.seqs = self.seqs.iloc[:, 1:3]
        return self.trials_iter

    def get_group(self):
        if self.group != None:
            return self.group

    def generate_trial_dataset(self, trials_iter=pd.Series()):
        """
        Generate the trial dataset. The dataset is generated based on the
        trials_iter. The trials_iter is a list of integers that represent
        the trials that are selected for the experiment.
        """
        col = [
            "seq",
            "audio_play_time",
            "opinion_before",
            "r_time1",
            "confidence_before",
            "play_time",
            "opinion_after",
            "r_time2",
            "confidence_after",
            "trust_system",
            "difficulty_level",
            "y_pred",
            "case",
        ]
        cols = []
        if len(trials_iter) != 0:
            for i in trials_iter:
                for j in col:
                    cols.append(str(i) + "_" + j)
            col = cols
        return pd.DataFrame(columns=col)
