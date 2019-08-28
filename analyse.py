"""Analyses survey responses

This module analyses survey responses in an excel .xlsx file through various
data analysis methods.
"""
from numpy import mean, median
from scipy.stats import mode
from utils import parse_config, parse_excel, secure
from textblob import TextBlob
from wordcloud import WordCloud
import os


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
    """
    output = {}
    print([i for i,j in responses.items()])
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
        If there are multiple modes, the smallest mode is given.
        For example:
        {'Mean': 8.0, 'Median': 3.0, 'Mode': [1]}
    """
    central_tendencies = {
        "Mean": mean(responses),
        "Median": median(responses),
        "Mode": mode(responses)[0].tolist(),
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
            For example: "./static/uploads/4SikvVjjqlWV44AW/"

    Returns:
        A string that is the path to the wordcloud generated from the responses
            For example: "./static/uploads/4SikvVjjqlWV44AW/zxmVHMV1QlAvYFq3.png"
    """
    text = " ".join(responses)
    cloud = WordCloud(background_color="white").generate(text)
    image = cloud.to_image()
    path = os.path.join(directory, f"{secure(16)}.png")
    image.save(path)
    return path


def analyse(directory, excel_file, config_file):
    """Analyses survey responses

    Args:
        directory(str): path to the folder containing the excel file and config file
            For example: "./static/uploads/4SikvVjjqlWV44AW/"
        excel_file(str): name of excel file
            For example: "responses.xlsx"
        config_file(str): name of config file
            For example: "config_file.txt"

    Returns:
        A dictionary mapping each survey question to the analysis of its
        responses.
    """
    categorised_responses = categorise(
        parse_excel(os.path.join(directory, excel_file)),
        parse_config(os.path.join(directory, config_file)),
    )
    analysis = {}
    analysed = None
    for qn, responses in categorised_responses.items():
        category = responses[0]
        list_of_responses = responses[1]
        if category == "numerical":
            analysed = ("numerical", numerical(list(map(int,list_of_responses))))
        elif category == "categorical":
            analysed = ("categorical", categorical(list_of_responses))
        elif category == "openended":
            analysed = ("openended", openended(list_of_responses, directory))
        analysis[qn] = analysed
    return analysis


def generate_report(directory,analysis):
    """Generates a report based on analysis

    Generates a .docx report based on the analysis from analysis().

    Args:
        directory(str): path to the folder containing the original excel
            file and config file.
            For example: "./static/uploads/4SikvVjjqlWV44AW/"
        analysis(dict): analysis of the original excel file and config file
            from analysis()

    Returns:
        A string that is the path to the report file
    """
    for qn ,j in analysis:
        pass
if __name__ == "__main__":
    bruh = analyse(r"C:\Users\chi_j\Desktop", "responses.xlsx", "config_file.txt")
    print(bruh)
