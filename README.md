# pyCrypto

**README**

## Presentation

This repository contains the code for our project PyCrypto, developed during our [Data Scientist training](https://datascientest.com/en/data-scientist-course) at [DataScientest](https://datascientest.com/).

The financial and banking world is one of the sectors of activity generating the most data and most often in open access. The field of portfolio allocation is particularly interesting in the sense that it is abundant in data and can be systematized.

The objective of this project is to create a portfolio allocation model that adapts its strategy "online", but also to adapt the machine learning approach to a sector of activity with common points.

This project was developed by the following team :

- Ahmed Ouassou ([GitHub](https://github.com/) / [LinkedIn](http://linkedin.com/))
- Pierre Sarzier ([GitHub](https://github.com/) / [LinkedIn](http://linkedin.com/))
- Sofiane Benabdallah ([GitHub](https://github.com/sofiane34000) / [LinkedIn](https://www.linkedin.com/in/sofiane-benabdallah-66b1a46a/))

You can browse and run the [notebooks](./notebooks). You will need to install the dependencies (in a dedicated environment) :

```
pip install -r requirements.txt
```

### tree view

```
+---analysis
ª   +---.ipynb_checkpoints
+---data
ª   +---cryptos
ª   ª   +---articles
ª   ª   +---tweets
ª   +---nasdaq
ª   ª   +---article
ª   ª   +---tweets
ª   +---other
+---models
+---notebooks
ª   +---.ipynb_checkpoints
+---results
+---src
    +---StreamLitpyCrypto
    ª   +---.idea
    ª   ª   +---inspectionProfiles
    ª   +---assets
    ª   ª   +---cryptos
    ª   ª   +---nasdaq
    ª   ª   +---other
    ª   +---universal
    ª   ª   +---algos
    ª   ª   ª   +---ternary
    ª   ª   +---data
    ª   +---universalPF
```

## Streamlit App

To run the app :

```shell
cd ./src/StreamLitpyCrypto
pip install -r requirements.txt
streamlit run main.py
```

The app should then be available at [localhost:8501](http://localhost:8501).

