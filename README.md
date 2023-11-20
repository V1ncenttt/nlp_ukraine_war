<p align="center">
  <a href="" rel="noopener">
 <img width=100px height=100px src="src/assets/ukr_flag.png" alt="Project logo"></a>
</p>
<div align="center">

![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

</div>

# Ukrainian War: A Global Opinion Analysis Using Twitter Data 🌍🐦

## Overview 📜

This project focuses on conducting a comprehensive sentiment analysis on the War in Ukraine, utilizing a vast dataset of tweets published throughout the year 2022. Our aim is to extract, analyze, and interpret the sentiments, opinions, and emerging trends expressed on Twitter regarding the ongoing conflict. This analysis will provide valuable insights into public perception and the global discourse surrounding the conflict.

## Contributors 👥

- **Claudia Agromayor**
- **Malo Langourieux**
- **Arthur Fournon**
- **Vincent Lefeuve**
- **Gauthier Riquier**
- **Nicolas Brandel**

## Dataset 📊

The primary dataset for this project is the "Ukraine Russian Crisis Twitter Dataset," which comprises over 1.2 million tweets. This extensive collection has been meticulously gathered to represent a wide array of perspectives and voices discussing the conflict. The dataset is publicly available on Kaggle and can be accessed through the following link: [Ukraine Russian Crisis Twitter Dataset](https://www.kaggle.com/datasets/bwandowando/ukraine-russian-crisis-twitter-dataset-1-2-m-rows).

## Project Structure 🏗️

1. **Data:**
   - The `data` directory contains tweets related to the War in Ukraine found on an online database in csv format.

2. **Src:**
   - The `src` directory includes code for running the web-application and all of the code.

3. **Tests:**
   - The `tests` directory houses the code corresponding to the unit and coverage tests.

4. **ML:**
   - The `ml` directory focuses on the code needed to construct the text classification models, including the Shallow learning and Transformer-based approaches.

## How to Use 🛠️

1. **Clone the Repository:**
   ```bash
   git clone https://gitlab-cw4.centralesupelec.fr/groupe-7-les-bg/war_ukraine.git


2. **Install the necessary packages:**
   ```bash
   make init

**If you have Python3 installed:**
3. **Run the project:**
   ```bash
   make build3

4. **Run unit tests:**
   ```bash
   make test3

**If you only have Python installed:**
3. **Run the project:**
   ```bash
   make build

4. **Run unit tests:**
   ```bash
   make test

## Requirements ✅
| Req № | Description                                            | Importance | Current state |
|--------|--------------------------------------------------------|------------|---------------|
| 1      | Pre-process the datasets and extract knowledge         | Crucial    | Done          |
| 2      | Create data visualisations from the dataset            | Crucial    | WIP           |
| 3      | Perform sentiment analysis from the dataset            | Crucial    | WIP           |
| 4      | Create a transformer/shallow learning-based tweet classifier (pro Russian/Ukrainian) | Important | WIP |
| 5      | Make a web-application using dash                      | Important  | WIP           |
| 6      | Create wordclouds                                      | Important  | Done          |
| 7      | Implement a cloropleth using geographical data and the classification of the tweets | Important | WIP |
| 8      | Provide a way for users to easily run the project (Makefile) | Important  | Done      |
| 9      | Add other plots to the web application                | Medium     | Not started   |
| 10     | Add unit and coverage testing                          | Medium     | Not started   |
| 11     | Provide documentation with docstrings and a sphynx wiki | Medium   | Not started   |
| 12     | Compare other methods of classifiers (rule-based, LSTMs...) | Low     | Not started |
| 13     | Put the repository in a docker container to run it easily | Low      | Not started   |
| 14     | Write a project report                                 | Low        | Not started   |
| 15     | Analyse the datasets as time-series                    | Very Low   | Will not do   |

## Contributing 👫
If you'd like to contribute to this project, feel free to fork the repository, create a new branch, make your changes, and submit a pull request. Make sure to follow the project's coding standards and guidelines.

## Contact 📪
For any questions or concerns, please contact the project maintainers:
- Claudia Agromayor: [claudia.agromayor@student-cs.fr]
- Malo Langourieux: [malo.langourieux@student-cs.fr]
- Arthur Fournon: [arthur.fournon@student-cs.fr]
- Vincent Lefeuve: [vincent.lefeuve@student-cs.fr]
- Gauthier Riquier: [gauthier.riquier@student-cs.fr]
- Nicolas Brandel: [nicolas.brandel@student-cs.fr]