# Y2 CEP Final Project - _Surveyinator_
### Description
Surveyinator is a survey analyser for anyone and everyone to use. 
It analyses survey responses through a variety of analysis methods,
such as mean, median and mode. It allows surveyors to get an general idea of what
the survey responses are like.

Surveyinator was originally developed to help our [Computing teacher](https://github.com/lorrainewang)
to find out about the demand of Y2 CEP (i.e how many of them are 
interested to choose CEP in Year 2), and get a consolidated 
picture of how they perceive the 9 weeks CS course based on student 
feedback on their Year 1 CS experience.

Surveyinator is written fully in [Python 3.7](https://python.org).

### Features
+ Able to analyse **_all_** exported google forms data with obvious exceptions
+ Analyse numerical, categorical and openended data
+ Able to give a consolidated picture of responses
+ Beautiful aesthetics
+ Intuitive interface
+ User-friendly
+ Able to export analysis

### Usage
Usage is quick and simple!  
Head to [surveyinator.ml](surveyinator.ml) to use the hosted version.

Alternatively, you can simply click on this [link](https://google.com) to download the latest version. 
Make sure you have python>=3.7. Head to the project root and then run main.py.
 
#### Dependencies
Refer to [requirements.txt](requirements.txt)

For more information on installation, refer to these websites:
+ [Numpy](https://www.numpy.org/#getting-started)
+ [Scipy](https://scipy.org/install.html)
+ [Textblob](https://textblob.readthedocs.io/en/dev/#get-it-now)
+ [word_cloud](https://github.com/amueller/word_cloud#installation)
+ [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/)
+ [openpyxl](https://openpyxl.readthedocs.io/en/stable/#installation)
+ [Plotly](https://plot.ly/python/getting-started/#installation)
+ [matplotlib](https://matplotlib.org/users/installing.html)
+ [python-docx](https://python-docx.readthedocs.io/en/latest/user/install.html)

### Work distribution
- main.py (Mainly Yu Chen, Junxiang helped out in certain places):page_with_curl:
- analyse.py (Junxiang) :computer:
- utils.py (Both) :wrench:
- templates/index.html (Mainly Yu Chen, Junxiang did some) :page_with_curl:
- static/favicon.ico (Drawn by Yu Chen :sparkles:)
- model.pickle (Trained by Junxiang) :computer:
- README.md (Written by Junxiang):pencil2:
- Deployment to [website](https://surveyinator.ml) by Yu Chen :computer:
### Licence
Surveyinator is licenced under the [MIT Licence](LICENCE.txt)
