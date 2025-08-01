


import string
from prettytable import PrettyTable
import time
import sys
import hashlib
import math
import random
from collections import Counter
from typing import Dict, List, Tuple
from collections import Counter
import math
import string
import random
from prettytable import PrettyTable
import time
import numpy as np
from scipy.stats import entropy as scipy_entropy
from itertools import combinations
     

class Scoring:
    """
    The Scoring class is responsible for evaluating the effectiveness of the encryption
    method used in the Cipher class. It applies a series of metrics to the encrypted string
    and assigns a score based on these metrics.
    """

    def __init__(self, cipher: 'Cipher', running_time: float, weights: Dict[str, float], max_length_multiplier: float = 2.0) -> None:
        """
        The constructor for the Scoring class.
        Parameters:
            cipher (Cipher): An instance of the Cipher class.
            running_time (float): The time taken to run the encryption.
            weights (Dict[str, float]): A dictionary containing the weights for each metric.
            max_length_multiplier (float): The maximum allowed ratio of the length of the encrypted string
                                           to the length of the original string.
        """
        self.cipher = cipher
        self.weights = weights
        self.max_length_multiplier = max_length_multiplier
        self.running_time = running_time
        self.frequency = Counter(self.cipher.encrypted_string)
        self.score = self.calculate_score()
        self.summary = self.generate_summary()


    # Define metrics
    def unique_chars_metric(self) -> float:
        """
        Evaluates the number of unique characters in the encrypted string.
        Returns:
            float: The number of unique characters.
        """
        return len(set(self.cipher.encrypted_string)) / len(set(string.printable))

    def distinct_sequences_metric(self) -> float:
        """
        Evaluates the number of distinct character sequences in the encrypted string.
        Returns:
            float: The number of distinct character sequences.
        """
        # Updated to count sequences of two characters
        sequences = [''.join(seq) for seq in zip(self.cipher.encrypted_string, self.cipher.encrypted_string[1:])]
        return len(set(sequences)) / max(1, len(set(combinations(string.printable, 2))))

    def entropy_metric(self) -> float:
        """
        Evaluates the entropy of the encrypted string.
        Returns:
            float: The entropy of the encrypted string.
        """
        # Updated to use scipy's entropy function for better precision
        probabilities = [count / len(self.cipher.encrypted_string) for count in self.frequency.values()]
        return scipy_entropy(probabilities, base=2) / math.log2(len(set(string.printable)))

    def frequency_analysis_metric(self) -> float:
        """
        Evaluates the result of a frequency analysis on the encrypted string.
        Returns:
            float: The result of a frequency analysis on the encrypted string.
        """
        most_common_char_frequency = self.frequency.most_common(1)[0][1] / len(self.cipher.encrypted_string)
        return 1 - most_common_char_frequency

    def length_consistency_metric(self) -> float:
        """
        Evaluates how the length of the string changes after encryption.
        Returns:
            float: The absolute difference between the length of the original and encrypted strings.
        """
        return abs(len(self.cipher.encrypted_string) - len(self.cipher.original_string)) / len(self.cipher.original_string)

    def evenness_metric(self) -> float:
        """
        Evaluates how evenly distributed the characters in the encrypted string are.
        Returns:
            float: The standard deviation of the character frequencies.
        """
        frequencies = list(self.frequency.values())
        mean_freq = sum(frequencies) / len(frequencies)
        variance = sum((freq - mean_freq) ** 2 for freq in frequencies) / len(frequencies)
        return 1 - (math.sqrt(variance) / len(self.cipher.encrypted_string))

    def reversibility_metric(self) -> float:
        """
        Evaluates whether the original string can be correctly retrieved by decryption.
        Returns:
            float: 1.0 if the decrypted string matches the original string, 0.0 otherwise.
        """
        decrypted_string = self.cipher.decrypt()
        return float(decrypted_string == self.cipher.original_string)

    def change_propagation_metric(self) -> float:
        """
        Evaluates how much the encrypted string changes when a small change
        is made to the original string.
        Returns:
            float: The measure of change propagation.
        """
        # Change the original string
        changed_string = 'a' + self.cipher.original_string[1:]

        # Create a new Cipher instance with the changed string and encrypt it
        cipher_changed = Cipher(changed_string)
        cipher_changed.encrypt()
        changed_encrypted_string = cipher_changed.encrypted_string

        # Calculate the Levenshtein distance
        levenshtein_distance = self._levenshtein_distance(self.cipher.encrypted_string, changed_encrypted_string)

        return levenshtein_distance / len(self.cipher.encrypted_string)

    def pattern_analysis_metric(self) -> float:
        """
        Evaluates how patterns from the original string are unrecognizable in the encrypted string.
        Returns:
            float: The measure of pattern preservation.
        """
        pattern_instances_orig = sum(1 for a, b in zip(self.cipher.original_string, self.cipher.original_string[1:]) if a == b)
        pattern_instances_enc = sum(1 for a, b in zip(self.cipher.encrypted_string, self.cipher.encrypted_string[1:]) if a == b)

        if pattern_instances_orig == 0:
            return 1.0  # No repeated patterns in the original string
        elif pattern_instances_enc == 0:
            return 1.0  # No repeated patterns in the encrypted string
        else:
            return 1 - (pattern_instances_enc / pattern_instances_orig)


    def correlation_analysis_metric(self) -> float:
        """
        Calculates the correlation of the character at each position with the character
        at the same position in the encrypted string.
        Returns:
            float: The average correlation for all positions.
        """
        correlations = sum(1 for a, b in zip(self.cipher.original_string, self.cipher.encrypted_string) if a == b)
        correlation_metric = correlations / len(self.cipher.original_string)
        return 1 - correlation_metric

    def complexity_metric(self) -> float:
        """
        Evaluates the complexity of the encryption by measuring the length of the encrypted string.
        Returns:
            float: The length of the encrypted string divided by the length of the original string.
        """
        return len(self.cipher.encrypted_string) / len(self.cipher.original_string)

    def randomness_metric(self) -> float:
        """
        Evaluates how random the encrypted string appears.
        Returns:
            float: The standard deviation of the character frequencies in the encrypted string of a random string.
        """
        random_string = ''.join(random.choice(string.printable) for _ in range(len(self.cipher.original_string)))
        cipher = Cipher(random_string)
        cipher.encrypt()
        random_encrypted_string = cipher.encrypted_string
        random_encrypted_frequency = Counter(random_encrypted_string)
        frequencies = list(random_encrypted_frequency.values())
        mean_freq = sum(frequencies) / len(frequencies)
        variance = sum((freq - mean_freq) ** 2 for freq in frequencies) / len(frequencies)
        return math.sqrt(variance) / len(string.printable)

    def normalized_levenshtein_metric(self) -> float:
        """
        Evaluates the normalized Levenshtein distance between the original string and the decrypted string.
        Returns:
            float: The normalized Levenshtein distance.
        """
        decrypted_string = self.cipher.decrypt()
        distance = self._levenshtein_distance(self.cipher.original_string, decrypted_string)
        return 1 - distance / max(len(self.cipher.original_string), len(decrypted_string))

    def encryption_consistency_metric(self) -> float:
        """
        Evaluates the consistency of the encryption method.
        Returns:
            float: The consistency of the encryption method.
        """
        original_string = self.cipher.original_string
        original_encrypted_string = self.cipher.encrypted_string

        self.cipher.original_string = original_string
        self.cipher.encrypted_string = ""
        self.cipher.encrypt()
        second_encryption = self.cipher.encrypted_string

        # Reset the encrypted_string back to its original value
        self.cipher.encrypted_string = original_encrypted_string

        return float(original_encrypted_string == second_encryption)

    def running_time_metric(self) -> float:
        """
        Evaluates the time taken for the encryption process.
        Returns:
            float: The time taken for the encryption process.
        """
        # Use numpy's clip function to ensure the returned value is between 0 and 1
        return np.clip(1 - self.running_time, 0, 1)  # Updated to use the new attribute


    def calculate_score(self) -> float:
        """
        Calculates the total score based on the defined metrics.

        Returns:
            float: The total score.
        """
        total_score = 0
        try:
            if len(self.cipher.encrypted_string) > len(self.cipher.original_string) * self.max_length_multiplier:
                raise Exception("The length of the encrypted string exceeds the allowed limit. This entry is disqualified.")

            total_score += self.weights["unique_chars"] * self.unique_chars_metric()
            total_score += self.weights["distinct_sequences"] * self.distinct_sequences_metric()
            total_score += self.weights["entropy"] * self.entropy_metric()
            total_score += self.weights["frequency_analysis"] * self.frequency_analysis_metric()
            total_score += self.weights["length_consistency"] * self.length_consistency_metric()
            total_score += self.weights["evenness"] * self.evenness_metric()
            total_score += self.weights["reversibility"] * self.reversibility_metric()
            total_score += self.weights["change_propagation"] * self.change_propagation_metric()
            total_score += self.weights["pattern_analysis"] * self.pattern_analysis_metric()
            total_score += self.weights["correlation_analysis"] * self.correlation_analysis_metric()
            total_score += self.weights["complexity"] * self.complexity_metric()
            total_score += self.weights["randomness"] * self.randomness_metric()
            total_score += self.weights["normalized_levenshtein"] * self.normalized_levenshtein_metric()
            total_score += self.weights["encryption_consistency"] * self.encryption_consistency_metric()
            total_score += self.weights["running_time"] * self.running_time_metric()
        except Exception as e:
            print(f"An error occurred while calculating the score: {e}")
            return 0

        return total_score

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculates the Levenshtein distance between two strings.

        Parameters:
            s1 (str): The first string.
            s2 (str): The second string.

        Returns:
            int: The Levenshtein distance between the two strings.
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]


    def generate_summary(self) -> Dict[str, float]:
        """
        Generates a summary of the metrics used to calculate the score.
        Returns:
            Dict[str, float]: A dictionary containing the metric names and their values.
        """
        summary = {
            "unique_chars": self.unique_chars_metric(),
            "distinct_sequences": self.distinct_sequences_metric(),
            "entropy": self.entropy_metric(),
            "frequency_analysis": self.frequency_analysis_metric(),
            "length_consistency": self.length_consistency_metric(),
            "evenness": self.evenness_metric(),
            "reversibility": self.reversibility_metric(),
            "change_propagation": self.change_propagation_metric(),
            "pattern_analysis": self.pattern_analysis_metric(),
            "correlation_analysis": self.correlation_analysis_metric(),
            "complexity": self.complexity_metric(),
            "randomness": self.randomness_metric(),
            "normalized_levenshtein": self.normalized_levenshtein_metric(),
            "encryption_consistency": self.encryption_consistency_metric(),
            "running_time": self.running_time_metric()  # New metric
        }
        return summary

    @staticmethod
    def print_results(table_data: List[List[str]], scores: List[float]) -> None:
        """
        Prints the results of the encryption tests in a table format.

        Parameters:
            table_data (list): A list of lists where each sublist contains the test number, original string,
                              encrypted string, decrypted string, decryption success, score, and running time.
            scores (list): A list of all scores.
        """
        try:
            # Create a PrettyTable instance
            table = PrettyTable()

            # Set the column names
            table.field_names = ["Test No.", "Original String", "Encrypted String",
                                "Decrypted String", "Decryption Success", "Score", "Running Time"]

            # Add each test's results to the table
            for data in table_data:
                table.add_row(data)

            # Print the table
            print(table)

            # Print the average score
            print(f"\nAverage score: {sum(scores) / len(scores)}")
        except Exception as e:
            print(f"An error occurred while printing the results: {e}")

     


class Cipher:
    """
    The Cipher class handles the encryption and decryption of strings using a custom
    cipher.

    Attributes:
        original_string (str): The original string that will be encrypted.
        encrypted_string (str): The encrypted string after encryption.
    """

    def __init__(self, original_string: str) -> None:
        """
        The constructor for the Cipher class.

        Parameters:
            original_string (str): The original string that will be encrypted.
        """
        self.original_string = original_string
        self.encrypted_string = ""

    def encrypt(self) -> None:
        """
        Encrypts the original string by swapping each character with a character a fixed
        number of places down the alphabet.
        """
        # Encrypt the string
        # self.encrypted_string = self.original_string[::-1]

        word=self.original_string

        word=word[::-1]
        ascii_word=""
        r1=random.randint(0,7)
        add_ascii_word=""
        for i in word:
          ascii_word+=chr((ord(i))-r1)
        add_ascii_word=ascii_word[0]
        for i in ascii_word[1:]:
          # r=chr(random.randint(ord("!"),ord("~")))
          add_ascii_word =add_ascii_word + i+ chr(random.randint(ord("!"),ord("য")))

        t=(str(r1+2)+add_ascii_word)
        if len(t)==((len(word))*2)-1:
                  self.encrypted_string=t+"A"
        else:
          self.encrypted_string=t
    import random
    def decrypt(self) -> str:
        """
        Decrypts the encrypted string by swapping each character with a character a fixed
        number of places up the alphabet.

        Returns:
            str: The decrypted string.
        """
        # Decrypt the string
        # return self.encrypted_string[::-1]

        encrypted_text = self.encrypted_string
        if len(encrypted_text)%2==0:
          encrypted_text = encrypted_text [0:len(encrypted_text)-1]
        else:
          encrypted_text=encrypted_text

        r1 = (int(encrypted_text[:1]))-2

        ex=encrypted_text[1:2]
        encrypted_pairs = encrypted_text[2:]
        a=""
        b=""
        encrypted_pair=list(encrypted_pairs)
        for i in range(0,len(encrypted_pair),2):
            a=a+encrypted_pair[i]
        c=ex+a
        for i in c:
          b+=chr((ord(i))+r1)
        b=b[::-1]
        return b

     


def main(max_length_multiplier: float):
    """
    The main function that tests the Cipher and Scoring classes.

    Parameters:
        max_length_multiplier (float): The maximum allowed ratio of the length of the encrypted string
                                       to the length of the original string.
    """
    # Ensure the maximum length multiplier is a positive number
    assert max_length_multiplier > 0, "Maximum length multiplier must be a positive number"

    # Define the sample strings
    sample_strings = [
        "Hello, World!",
        "This is a sample string",
        "Another string for testing",
        "A very very long string that should result in a high score",
        "Short string",
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "1234567890",
        "A string with special characters: !@#$%^&*()",
        "A string with spaces    between     words",
        "A string with a mix of letters, numbers, and special characters: abc123!@#"
    ]


    # Define the weights for each metric
    weights = {
        "unique_chars": 0.1,
        "distinct_sequences": 1.0,
        "entropy": 1.5,
        "frequency_analysis": 0.1,
        "length_consistency": 0.5,
        "evenness": 1.2,
        "reversibility": 2.0,
        "change_propagation": 1.5,
        "pattern_analysis": 1.5,
        "correlation_analysis": 1.5,
        "complexity": 1.0,
        "randomness": 1.5,
        "normalized_levenshtein": 1.0,
        "encryption_consistency": 2.0,  # High weight as this is critical
        "running_time": 0.5
    }


    print("\n********** Cipher Testing **********")
    scores = []
    table_data = []

    for i, original_string in enumerate(sample_strings, start=1):
        # Create a Cipher instance and encrypt the string
        cipher = Cipher(original_string)

        # Start the timer
        start_time = time.time()

        cipher.encrypt()

        # End the timer
        end_time = time.time()

        # Calculate the running time
        running_time = end_time - start_time

        # Create a Scoring instance and calculate the score
        scoring = Scoring(cipher, running_time, weights, max_length_multiplier)
        scores.append(scoring.score)

        # Decrypt the string and verify it's the same as the original
        decrypted_string = cipher.decrypt()
        decryption_success = decrypted_string == original_string

        # Add the results to the table data
        table_data.append([
            i, original_string, cipher.encrypted_string,
            decrypted_string, decryption_success, scoring.score, running_time
        ])

    Scoring.print_results(table_data, scores)
    print("\n********** Testing Complete **********\n")

if __name__ == "__main__":

    main(2.0)  # Maximum length multiplier is set to twice the length of the original string
     
