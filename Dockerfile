FROM python:3.9.13

#EXPOSE 8501

WORKDIR /ranepa_data_prerocessing_2

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt


COPY . ./

CMD streamlit run src/Data_preprocessing_2.py

