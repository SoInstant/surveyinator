from numpy import mean, median
from scipy.stats import mode
from utils import parse_config, parse_excel
from textblob import TextBlob
from wordcloud import WordCloud
import os
from string import ascii_letters, digits
import random


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
            For example: ["Yes","No","Yes"] or ("Yes","No","Yes")

    Returns:
        A dictionary containing the sorted percentages of each response
        and the mode(s). For example:
        {'Percentages': {'Yes': 0.6666666666666666, 'No': 0.3333333333333333},
         'Modes': ('Yes')}
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
    sorting = sorted(categories.items(), key=lambda x: x[1])
    output = {}
    for category, freq in sorting:
        output[category] = freq
    return {"Percentages": output, "Modes": tuple(modes)}


def openended(responses, directory):
    """Analyses openended responses

    Args:
        responses(list/tuple): List/tuple of responses
            For example: ["Nil","The duration","Microbit"] or
            ("Nil","The duration","Microbit")
        directory(str): path to the folder containing the excel file and config file
            For example: "./uploads/responses.xlsx"

    Returns:
        A string that is the path to the wordcloud generated from the responses
            For example: "./uploads/responses.xlsx/qJLTOIDesAlqxRakLkFt7Qoz0xGDdXpl2HcPxcKMwNn9KShKYVuOXku0yqT0didc"
    """
    text = " ".join(responses)
    cloud = WordCloud(background_color="white").generate(text)
    image = cloud.to_image()
    filename = "".join([random.choice(ascii_letters + digits) for i in range(64)])
    path = os.path.join(directory, f"{filename}.png")
    image.save(path)
    return path


def analyse(file_directory, excel_file, config_file,save_directory):
    categorised_responses = categorise(
        parse_excel(os.path.join(file_directory, excel_file)),
        parse_config(os.path.join(file_directory, config_file)),
    )
    analysis = {}
    analysed = None
    for qn, responses in categorised_responses.items():
        category = responses[0]
        list_of_responses = responses[1]
        if category == "numerical":
            analysed = ("numerical", numerical(list_of_responses))
        elif category == "categorical":
            analysed = ("categorical", categorical(list_of_responses))
        elif category == "openended":
            analysed = ("openended", openended(list_of_responses, save_directory))
        analysis[qn] = analysed
    return analysis


if __name__ == "__main__":
    bruh = analyse("./uploads/responses.xlsx/files", "responses.xlsx", "config_file.txt")
    print(bruh)
