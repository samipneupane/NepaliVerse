# NEPALIVERSE: English-to-Nepali Translation and Pronunciation Analysis

This project aims to make working with Nepali language simple and accessible. It helps translate English to Nepali, and translated Nepali font to Unicode, and generate natural Nepali speech. It also evaluates speech similarity for pronunciation learning. Perfect for language learning, communication, and accessibility.
The project is divided into three main components: **Model Training**, **Frontend**, and **Backend**.

---

## Dataset Description

For both Translation and Transliteration we used dataset from huggingface

- The **English-Nepali** translation dataset consists of **1,989,088** pairs.
- The **Nepali-Roman** transliteration dataset consistos of **2,400,218** pairs.


[🔗 eng2nep Dataset](https://huggingface.co/datasets/momo22/eng2nep)

[🔗 Nepali-Roman-Transliteration Dataset](https://huggingface.co/datasets/Saugatkafley/Nepali-Roman-Transliteration)

---

## Model Training

The model training for **Translation** involves:
- **Tokenization**
- **Model Configuration**
- **Data Preparation**
- **Training**
- **Model Evaluation and Saving**

The model training for **Transliteration** involves:
- **Data Cleaning and Preprocessing**: Convert to string, Remove whitespace, Convert to lowercase, Removes rows where the English word contains a period (.) and comma(,), Special tokens ^ (start) and $ (end) are added to the Romanized English text
- **Tokenization**
- **Encoder Decoder Defining**
- **Training**
- **Model Evaluation and Saving**

### Training Notebook

The complete training process can be viewed on the following Notebooks:

1. [🔗 Translation Training Notebook](https://github.com/samipneupane/NepaliVerse/blob/main/backend/logic/translation/En_Ne_train_kaggle.ipynb)

2. [🔗 Transliteration Training Notebook](https://github.com/samipneupane/NepaliVerse/blob/main/backend/logic/unicode/transliteration.ipynb)

*Note:* For running these notebooks, **Python version 3.9** is *recommended* to avoid version incompatibility issues.

---

## Models

You can access the model files through the following links:

1. [Translation Model](https://drive.google.com/drive/u/0/folders/1WA6xnnE-DNnxwCLanGzPug5vpZrLeEBm)
2. [Transliteration Model](https://drive.google.com/drive/u/0/folders/1_hIsBvYeymVj0EbO_RbDb2n4D_KDC5mA)

### Instructions for Placement

- **Translation Model**  
  Download the `model_kag3/` folder from the provided link and place it in the project path:  
  `backend/logic/translation/models/model_kag3/`

- **Transliteration Model**  
  Download the `model_all.h5` file from the provided link and place it in the project path:  
  `backend/logic/unicode/models/model_all.h5`

## Frontend

The frontend is built with **React.js**. It serves as the user interface for interacting with the system.

### Steps to Run the Frontend:

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the production server:
   ```bash
   npm start
   ```

---

## Backend

The backend is built with **Django** and handles the model inference and API requests.

### Steps to Run the Backend:

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment and install dependencies:
   ```bash
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
5. Start the Django server:
   ```bash
   python manage.py runserver
   ```
*Note:* To use `AudioSegment` from **pydub**, **FFmpeg** must be installed on your system.

---

## Project Structure

```plaintext
.
├── backend/
│   ├── core/
|        ├── <Django App>
│   ├── nepaliverse/
|        ├── <Django Project>
│   ├── manage.py
│   └── logic/
|        ├── translation/
|             ├── <Training and Evaluation for translation>
|        ├── unicode/
|             ├── <Training and Evaluation for transliteration>
|        └── similarity/
|             ├── <similarity calculaton>
├── frontend/
│   ├── public/
│   └──src/
|        ├── components/

```

---

Feel free to explore the Notebook and clone this repository to run the system locally.