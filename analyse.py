from numpy import mean, median
from scipy.stats import mode
from parse import open_config, open_excel


def categorise(responses, datatypes):
    """Maps the question to a tuple containing the datatype of
    the responses and the responses

    Args:
        responses(dict): The responses(tuple/list) mapped to their question
        datatypes(tuple/list): The datatypes of the list_of_responses

    Returns:
        A dictionary which maps a tuple of the datatype of the response
        and the responses to their question. For example:
        {"Do you like python?": ("categorical", ("yes", "no", "yes"))}

    Raises:
        IndexError: "Config file does not have same number of questions
            as excel file"
    """
    output = {}
    for i, items in enumerate(responses.items()):
        output[items[0]] = tuple([datatypes[i], items[1]])
    return output


def numerical(responses):
    """Analyses numerical responses

    Args:
        responses(list/tuple): List/tuple of the responses
            For example: [1,2,3,1,2,3,4,58,1,5,8]

    Returns:
        A dict of the Mean, Median and Mode of the data.
        Mode(s) is/are returned in an numpy array.
        For example:
        {'Mean': 8.0, 'Median': 3.0, 'Mode': array([1])}
    """
    central_tendencies = {
        "Mean": mean(responses),
        "Median": median(responses),
        "Mode": mode(responses)[0],
    }
    return central_tendencies


def categorical(responses):
    """Analyses categorical responses

    Args:
        responses(list/tuple): List/tuple of the responses
            For example: ["Yes","No","Yes"]

    Returns:
        A dictionary containing the sorted percentages of each response
        and the mode(s). For example:
        {'Percentages': {'Yes': 0.6666666666666666, 'No': 0.3333333333333333},
         'Modes': ['Yes']}
    """
    categories = {}
    # Count responses per category
    for i in responses:
        if i not in categories.keys():
            categories[i] = 1
        else:
            categories[i] += 1

    # Find mode and percentage
    max_freq = max(categories.values())
    modes = []
    for category, freq in categories.items():
        if freq == max_freq:
            modes.append(category)
        categories[category] = freq / len(responses)
    sorting = sorted(categories.items(), key = lambda x : x[1])
    output = {}
    for category,freq in sorting:
        output[category] = freq
    return {"Percentages": output, "Modes": modes}


def openended(responses):
    pass


def analyse(file, config_file):
    responses = open_excel(file)
    qn_categories = open_config(config_file)

    categorised_responses = categorise(responses, qn_categories)

    analysis = {}
    for qn, responses in categorised_responses.items():
        category = responses[0]
        list_of_responses = responses[1]
        if category == "ignore":
            continue
        elif category == "numerical":
            analysed = numerical(list_of_responses)
        elif category == "categorical":
            analysed = categorical(list_of_responses)
        elif category == "openended":
            analysed = openended(list_of_responses)
        analysis[qn] = analysed
    return analysis


if __name__ == "__main__":
    print(analyse("responses.xlsx", "config_file.txt"))
    print(categorical(["Yes", "No", "Yes"]))
