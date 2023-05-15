import pandas as pd
from collections import Counter

def extract_temperature(temperature_str):
    # Split the temperature string on the "-" character
    temperature_range = temperature_str.split("-")

    # Convert the temperature values to floats
    temperature_values = [float(temp) for temp in temperature_range]

    # Take the average of the temperature values
    temperature = sum(temperature_values) / len(temperature_values)

    return temperature



def find_most_probable_organisms(attributes, bacteria,inverted_counts, vaccination=None, gram = None, travelling=None, n=1):
    # Convert the organism data to a dictionary
    organism_dict = dict(zip(bacteria['organism'], bacteria.iloc[:, 1:].values.tolist()))

    # Define a function to calculate the similarity between a set of attributes and an organism's characteristics
    def similarity(attributes, organism):
        score = 0

        for i in range(1, len(attributes)):
            for j in range(len(organism)):
                try:
                    if attributes[i] in organism[j]:
                        try:
                            factor = inverted_counts[attributes[i]]
                            score += factor * 1
                        except:
                            score += 1
                except:
                    pass

            if "Temperature:" in attributes[i]:
                split_string = attributes[i].split()
                temperature = float(int(split_string[1]))

                try:
                    organism_temp_range = organism[11].split("-")
                except:
                    organism_temp_range = organism[11]

                try:
                    organism_min_temp = float(int(organism_temp_range[0]))
                    organism_max_temp = float(int(organism_temp_range[1]))
                    if organism_min_temp <= temperature <= organism_max_temp:
                        score += 1
                except:
                    if temperature ==organism_temp_range:
                        score += 1



        if travelling is not None and organism[20] == travelling:
            score += 1
        if vaccination is not None and organism[21] == vaccination:
            score += 1
        if gram not in attributes and gram != None:
            score = 0
        return score

    # Calculate the similarity score for each organism
    scores = {organism: similarity(attributes, organism_dict[organism]) for organism in organism_dict}

    # Sort the organisms by their similarity score, in descending order
    sorted_organisms = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    tuples = sorted_organisms[:n]

    found_scores = []
    found_organisms = []
    for i in tuples:
        found_scores.append(i[1])
        found_organisms.append(i[0])
    # Return the top N organisms with the highest similarity score
    return found_scores, found_organisms



# create a sample dataframe
def count_frequency(df):
    word_counts = {}

    # iterate over each column in the dataframe
    for col in df.columns:
        # convert the column to a string
        text = ' '.join(df[col].astype(str).tolist())

        # split the string into words
        words = text.split()

        # count the frequency of each word in the column
        word_counts[col] = Counter(words)

    # create a new dictionary to store the total word counts across all columns
    total_counts = {}

    # iterate over each column in the word_counts dictionary
    for col, count_dict in word_counts.items():
        # iterate over each word in the count_dict
        for word, count in count_dict.items():
            # add the count to the total_counts dictionary
            if word in total_counts:
                total_counts[word] += count
            else:
                total_counts[word] = count

    # sort the words by their count
    sorted_words = sorted(total_counts.items(), key=lambda x: x[1], reverse=True)
    max_count = 15
    inverted_counts = {word: max_count / count for word, count in total_counts.items()}
    # print the total count for e
    return inverted_counts