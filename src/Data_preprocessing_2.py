# импортируем библиотеки
# from tkinter import Button
from matplotlib import image
from nbformat import write
import streamlit as st
import pandas as pd 
import numpy as np 
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


# Заголовок


st.markdown('''<h1 style='text-align: center; color: black;'
            >Влияние обработки данных на точность прогноза </h1>''', 
            unsafe_allow_html=True)

st.image(image='../images/preprocessing.png', use_column_width='auto')

st.write("""
Предварительная обработка важный этап в машинном обучении. Для того, чтобы обучать модель, ей необходимо предоставить очищенные данные в понятном виде. Ни одну модель не обучают на данных, которые до этого 
не обработали. Именно предварительная обработка, на равне с разведочным анализом данных, обычно занимает большую часть проекта. Все те же этапы (и не только они), которые применяются здесь, применимы ко всем наборам данных. 
Именно поэтому данная лабораторная работа будет актуальна для специалистов из любых сфер, которые хотят познакомиться и освоить возможности машинного обучения.
\n **Полезно почитать:** [1](https://habr.com/ru/post/511132/), [2](https://pythobyte.com/data-preprocessing-0cb9135c/)

\nВ этой лабораторной работе мы предобработаем данные, обучим модель и замерим ее качество. Затем мы попробуем по другому предобработать те же данные, обучим ту же модель и снова замерим качество.
В конце мы сравним, как предварительная обработка повлияла на точность предсказания модели.

\nМодель, которую мы будем применять - линейная регрессия. Она относится к разделу задач, которая называется обучение с учителем. Более подробную информацию вы найдете в самой лабораторной работе.  

\nЛабораторная работа состоит из 4 блоков:
\n* **Анализ данных**: познакомимся с исходным набором данных
\n* **Предобработка данных 1 вариант**: предобработаем данные и обучим модель
\n* **Выбор студента**: дадим возможность студенту самому выбрать варианты предобработки
\n* **Предобработка данных 2 вариант**: посмотрим за счет чего еще можно улучшить качество модели
""")


#-------------------------Информация о проекте-------------------------

st.header('Этапы разработки лабораторной работы', anchor='pipeline') 

st.image(image='../images/Pipeline_2.png', use_column_width='auto', caption='Схема (пайплайн) лабораторной работы')

expander_bar = st.expander("Описание пайплана стримлита:")
expander_bar.markdown(
    """
\nЗелёным обозначены этапы, корректировка которых доступна студенту, красным - этапы, которые предобработаны и скорректированы сотрудником лаборатории.
\n**1. Сбор данных:** был использован датасет из соревнований на платформе kaggle ([ссылка](https://www.kaggle.com/competitions/nyc-taxi-trip-duration/overview))
\n**2. Предобработка данных:** изменения типов данных, создание новых столбцов (feature engineering), кодировка категориальных переменных, отсечение ненужных признаков (feature selection).
\n**3. Обучение и валидация модели**
\n**4. Сравнение результатов** 
\n**5. Выводы:** подведение итогов и краткое описание проделанной работы, ссылки на другие методы предобработки данных.
\n**6. Веб-приложения Streamlit:** работа с данными
\n**Используемые библиотеки:** [streamlit](https://docs.streamlit.io/library/get-started), [pandas](https://pandas.pydata.org/docs/user_guide/index.html), [sklearn](https://matplotlib.org/stable/api/index.html), 
[numpy](https://numpy.org/doc/stable/), [plotly](https://pillow.readthedocs.io/en/stable/)
""")

df_expander = st.expander("Информация о данных:")
df_expander.markdown(
"""
\n**taxi_dataset.csv** - набор данных, о поездках такси в Нью Йорке, который включает в себя время поездки, координаты, количество пассажиров и другие параметры.
Целевая переменная - продолжительность поездки.
\n**[Ссылка на данные](https://www.kaggle.com/competitions/nyc-taxi-trip-duration/overview)**
""")
 
col_expander = st.expander('Описание столбцов:')
col_expander.markdown("""
\n**id** - ID поездки
\n**id_компании** - ID компании, осуществляющей перевозку 
\n**начало_поездки** - Таймкод начала поездки
\n**окончание_поездки** - Таймкод конца поездки 
\n**количество_пассажиров** - Количество пассажиров 
\n**долгота_начала** - Долгота точки, в которой началась поездка 
\n**широта_начала** - Широта точки, в которой началась поездка
\n**долгота_окончания** - Долгота точки, в которой закончилась поездка
\n**широта_окончания** - Широта точки, в которой закончилась поездка
\n**информация_сохранена** - Yes/No: Была ли информация сохранена в памяти транспортного средства из-за потери соединения с сервером
""")

df = pd.read_csv('short_taxi.csv')

st.subheader('Анализ данных')

if st.checkbox('Показать набор данных'):
  number = st.number_input('Сколько строк показать', min_value=1, max_value=df.shape[0])
  st.dataframe(df.head(number))
  # st.dataframe(df)

if st.checkbox('Размер набора данных'):
  shape = st.radio(
    "Выбор данных",
     ('Строки', 'Столбцы'))
  if shape == 'Строки':
    st.write('Количество строк:', df.shape[0])
  elif shape == 'Столбцы':
    st.write('Количество столбцов:', df.shape[1]) 

if st.checkbox('Уникальные значения столбцоы'):
  cols = st.multiselect('Выбрать столбец', 
  df.columns.tolist())
  if cols:
    st.write(pd.DataFrame(df[cols].value_counts(), columns=['количество уникальных значений']))

if st.checkbox('Типы данных'):
  st.write('**Тип данных** - внутреннее представление, которое язык программирования использует для понимания того, как данные хранить и как ими оперировать')
  expander_bar = st.expander('Информация об основных типах данных')
  expander_bar.info('''Object - текстовые или смешанные числовые и нечисловые значения 
  \nINT - целые числа 
  \nFLOAT - дробные числа 
  \nBOOL - значения True/False
  \nDATETIME - значения даты и времени
  ''')

  st.write(pd.DataFrame(df.dtypes.astype('str'), columns=['тип данных']))

if st.checkbox('Описательная статистика по всем числовым столбцам'):
  describe_expander_ = st.expander('Информация о данных, которые входят в описательную статистику')
  describe_expander_.info('''Count - сколько всего было записей 
  \nMean - средняя велечина 
  \nStd - стандартное отклонение
  \nMin - минимальное значение
  \n25%/50%/70% - перцентили (показывают значение, ниже которого падает определенный процент наблюдений. Например, если число 5 - это 25% перцентиль, значит в наших данных 25% значений ниже 5)
  \nMax - максимальное значение
  ''')
  st.dataframe(df.describe())


non_val = st.checkbox('Пропущенные значения')
if non_val:
  st.write(pd.DataFrame(df.isnull().sum().sort_values(ascending=False), columns=['количество пропущенных значений']))

#-----------------Preprocessing: first try---------------

st.subheader('Предобработка данных: 1 вариант')
st.write('Попробуем сделать предобработку и обучим нашу первую модель')

df_1 = df.copy()
step_one = st.checkbox('Шаг первый')
if step_one:
  st.write("""
  Для начала добавим нашу целевую переменную (ее еще называют таргетом), по которой будем делать предсказания. Наша целевая переменная - время поездки. Чтобы ее получить, нам нужно вычесть время начала поездки и ее окончания.
  Но прежде, чем это сделать, давайте посмотрим, какой тип данных у этих столбцов. Мы видим "object". Чтобы нам было удобней работать, поменяем тип данных этих столбцов на datetime. 
  """)
  type_expander = st.expander('Зачем мы меняем тип данных?')
  type_expander.markdown("""
  В библиотеке pandas, которая нужна нам для работы с табличными данными, есть специальный модуль **[datetime](https://pythonworld.ru/moduli/modul-datetime.html)**. С помощью него легко доставать необходимую информацию
  (год, месяц, день, час, минута, секунда), а также делать вычисления между датами.
  """)
  target_expander  = st.expander('Что такое целевая переменная?')
  target_expander.markdown("""
  Целевая переменная или таргет - признак пакета данных, который предстоит предсказывать. **[Ссылка на статью](https://www.helenkapatsa.ru/tsielievaia-pieriemiennaia/)**
  """)
  change_type = st.checkbox('Поменять тип данных')
  if change_type:
    df_1['начало_поездки'] = pd.to_datetime(df_1['начало_поездки'])
    df_1['конец_поездки'] = pd.to_datetime(df_1['конец_поездки'])
    st.write(pd.DataFrame(df_1.dtypes.astype('str'), columns=['тип данных']))

    st.write('Теперь мы можем получить целевую переменную. Будем считать время в секундах')

    get_target = st.checkbox('Получить целевую переменную')
    if get_target:
      df_1['длительность_поездки'] = df_1['конец_поездки'] - df_1['начало_поездки']
      df_1['длительность_поездки'] = df_1['длительность_поездки'].dt.total_seconds().astype(int)
      st.write('Чтобы не выводить все 500 тысяч значений, посмотрим на первые 20')
      st.write(df_1['длительность_поездки'].head(20))

step_two = st.checkbox('Шаг второй')
if step_two:
  st.write("""
  Отлично, мы получили нашу целевую переменную. Теперь нужно подумать, что сделать со столбцами начало и конец поездки. Есть 2 нюанса: во-первых, алгоритм машинного обучения линейная регрессия (о нем поговорим чуть ниже), который мы будем использовать при обучении, не работает с данными типа datetime, поэтому нам нужно будет снова менять тип данных; 
  во-вторых, если мы оставим эти столбцы, то можем столкнуться с проблемой **[мультиколлиниарноcти](https://www.bigdataschool.ru/wiki/мультиколлинеарность)**, так как часть этой информации уже есть в целевой переменной. 
  Мультиколлинеарность - наличие линейной зависимости между признаками, т.е. когда можно выразить один признак через другие, что зачастую приводит к переобучению модели. Это происходит потому, что у нас переизбыток информации. Проверять наличие линейной зависимости будем при помощи определителя матрицы. **[Определитель матрицы](https://ru.onlinemschool.com/math/library/matrix/determinant/)** - это понятие из высшей математики. Нам не очень важно само понятие, нас интересует одно из его свойств:
  \n*определитель матрицы равен нулю, если две или несколько строк или столбцов матрицы линейно зависимы*. 
  \nСледовательно, чем определитель матрицы ближе к нулю, тем сильнее мультиколлиниарность и ненадежнее результаты. Чем ближе определитель к единице, тем меньше мультиколлиниарность.
  Скорее всего, вы не получите просто цифру 0, когда будете делать вычисления определителя матрицы, но получите [экспоненциальную запись числа](https://allcalc.ru/node/1103), как на фото ниже. Это и будет подтверждением наличия мультиколлиниарности.
  """)
 
  st.image('../images/scientific_notation.png', use_column_width=True)
  st.write("""
  \nЕсть несколько вариантов предобработки. Мы можем просто удалить эти данные, можем изменить тип данных на int64 и оставить (не лучший вариант из-за возможной мультиколлиниарности), а можем вытащить дополнительную информация, например, месяц, день недели и время поездки (datetime дает нам такую возможность), а затем уже удалить столбцы начало и конец поездки.
  Давайте попробуем первый вариант и просто удалим их.
  \n Обратите также внимание на столбец "информация_сохранена" - это категориальная переменная. Мы можем ее закодировать, а можем удалить. Сегодня мы с вами решили, что будем от всего избавляться. Давайте удалим и ее.
  """)    
  drop_time = st.checkbox('Удалить ненужные столбцы')
  if drop_time:
    df_1 = df_1.drop(['начало_поездки', 'конец_поездки', 'информация_сохранена'], axis=1)
    st.write(df_1.head())  

step_three = st.checkbox('Шаг третий')
if step_three:
  st.write("""
  \n Мы можем сделать еще одно маленькое преобразование: у нас есть индексы и столбец id. Посмотрите на уникальные значения переменной "id". У каждой поездки он свой. По сути, это то же самое, что и индекс. Давайте сделаем так, чтобы столбец id стала нашим индексом.
  """)
  change_id = st.checkbox('Задать новый индекс')
  if change_id:
    df_1 = df_1.set_index('id')
    st.write(df_1.head())  

step_four = st.checkbox('Шаг четвертый')
if step_four:
  st.write("""
  Прежде, чем начать обучение, нам нужно разделить наши данные на тренировочную часть и тестовую (разделим в пропорции 80/20). Делить будем с помощью встроенного метода train_test_split из библиотеки sklearn 
  """)
  training_info = st.expander('Зачем мы делим наши данные?')
  training_info.markdown("""
  Процедура разделения на тренировочную и тестовую часть нужна для оценки производительности алгоритмов машинного обучения. На тренировочных данных мы учим нашу модель находить и выявлять закономерности,
  а на тестовых данных мы проверяем способность нашей модели предсказывать на новых данных, которые она ранее не видела. Во время обучения мы подаем все данные нашей модели, включая целевую переменную.
  Во время теста мы делаем предсказание по новым данным без целевой переменной, а уже после сравниваем полученные предсказания с целевой переменной.  
  """)
  split_train_test = st.checkbox('Разделить данные')
  if split_train_test:
    X_1 = df_1.drop('длительность_поездки', axis=1)
    y_1 = df_1['длительность_поездки']
    X_train, X_test, y_train, y_test = train_test_split(X_1, y_1, 
                                                    test_size=0.2, 
                                                    random_state=42)
    st.write("Размер тренировочного датасета:", X_train.shape, 
    "Размер тестового датасета:" , X_test.shape)
step_five = st.checkbox('Шаг пятый')
if step_five:
  st.write("""
  Теперь мы можем обучить нашу модель и оценить ее производительность, посчитав метрику. Обучать мы будем с помощью обычной линейной регрессии. Метрика - MAE
  """)
  lin_reg = st.expander('Что такое линейная регрессия?')
  lin_reg.markdown("""
  **[Линейная регрессия](https://neurohive.io/ru/osnovy-data-science/linejnaja-regressija/)** - это модель зависимости целевой переменной от одной или нескольких других переменных(столбцов).
  Линейная регрессия относится к задаче определения «линии наилучшего соответствия» через набор точек данных. Это задача из раздела **[обучения с учителем](http://www.machinelearning.ru/wiki/index.php?title=Обучение_с_учителем)**
  (то есть когда у нас в данных есть примеры с ответами, на которых мы учимся. В нашем случае ответы - время поездки такси).
  """)
  
  st.write("""На графике снизу черная линия - линейная регрессия, красные квадратики - предсказания линейной регрессии, зеленые кружки - реальные значения целевой переменной, пунктиром отмечена разница каждого предсказания с реальным значением.
  Затем эта разница считается по метрике: берутся все значения разниц, суммируются друг с другом, а затем мы делим это число на количество наблюдений (на фото их 6).
   """)

  st.image('../images/lin_reg.png', use_column_width=True)

  mae = st.expander('Что за метрика MAE?')
  mae.markdown("""
  Метрика - критерий по которому измеряется качество всей модели. MAE (mean absolute error)  - это средняя абсолютная разность между предсказанием модели и целевым значением. 
  """)

  train_model = st.checkbox('Обучить модель')
  if train_model:
    model = LinearRegression()
    model.fit(X_train, y_train)
    train_losses = mean_absolute_error(y_train, model.predict(X_train))
    test_losses = mean_absolute_error(y_test,model.predict(X_test))
    
    st.write('Посмотрим на график корреляции')
    fig, ax = plt.subplots(1, 1, figsize=(15, 10)) 
    ax = sns.heatmap(df_1.corr().abs(), 
                  vmin=0, vmax=1, annot=True, cmap='magma') 
    st.pyplot(fig)
    #st.write('Ранг матрицы:', np.linalg.matrix_rank(df.corr())) 
    st.write('Определитель:', np.linalg.det(df_1.corr()))
    
    st.write('Показатель метрики на тренировочных данных (в секундах):', round(train_losses,2))
    st.write('Показатель метрики на тестовых данных (в секундах):', round(test_losses,2))
    

    explanation = st.expander('Как это можно трактовать?')
    explanation.markdown("""
    Во-первых, мы видим, что у нас нет линейной зависимости, так как определитель не стремится к нулю. И на графике корреляции видно, что у нас нет сильно зависимых друг от друга столбцов. Самая сильная зависимость у широты начала и широты окончания (0.46), но это приемлимые цифры.
    \n Во-вторых, посмотрим на метрику. *MAE* довольно удобная для интерпретации метрика (именно поэтому мы ее и выбрали), так как она считает абсолютные значения. Следовательно, можно сказать, что наша модель в среднем ошибается на 576 секунд (примерно 9,5 минут) по сравнению с реальными значениями.
    """)
inter_cocnlusion = st.expander('Промежуточные выводы')
inter_cocnlusion.markdown("""
  Мы с вами научились делать предсказания и даже получили какой-то результат. Но кажется, что ошибка в 9,5 минут в предсказании времени поездки такси - довольно большая ошибка. 
  Возможно, если мы по другому обработаем данные, у нас получится улучшить показатель нашей метрики и делать более точные предсказания.
  """)


#-------------------Student try---------------------------

df_2 = df.copy()


st.subheader('Выбор студента')

st.write("""
В этом блоке вы можете попробовать свои силы: самостоятельно обработать данные и обучить модель. Для того, чтобы лучше понять, как это все работает, попробуйте выполнить данную лабораторную 3 раза, запищите результаты в бланк отчетности и проанализируйте их. Что вы меняли чтобы улучшить модель? А что влияло на ухудшение показателя метрики?
Попробуйте достичь следующих результатов: MAE меньше или равен 470, определитель матрицы больше 0.4.
\nАлгоритм и метрика те же самые - линейная регрессия и MAE.
\nЦелевую переменную нам в любом случае надо получить, чтобы мы могли делать предсказание, поэтому оставим этот пункт без изменений.
""")
with st.form(key='student_choice'):

  st.warning('Обязательно выберите все варианты предобработки иначе алгоритм не заработает')

  get_target = st.checkbox('Изменить тип данных и получить целевую переменную')

  get_more_info = st.multiselect('Получить столбцы месяц, день и час поездки?', ['Да', 'Нет'])

  drop_trip = st.multiselect('Удалить столбцы "начало_поездки" и "конец_поездки"?', ['Да', 'Нет'])

  save_info = st.multiselect('Удалить или закодировать данные в столбце "информация_сохранена"?', ['Удалить', 'Закодировать'])

  new_idx = st.multiselect('Задать новый индекс?', ['Да','Нет'])

  company_id = st.multiselect('Перевести в бинарный признак столбец "id_компании"?', ['Да','Нет'])
  company_exp = st.expander('Пояснение')
  company_exp.markdown("""
  Значения в столбец "id_компании" 1 и 2. Это явно бинарный категориальный признак. Но обычно бинарные признаки обозначаются, как 0 и 1. Приводить их к общепринятому виду или нет - ваш личный выбор.
  """)

  get_distance = st.multiselect('Получить новую переменную "расстояние"?', ['Да','Нет'])
  dist_exp = st.expander('Пояснение')
  dist_exp.markdown("""
  Мы можем использовать долготу и широту точек начала и окончания поездки для того, чтобы примерно оценить расстояние между 2 точками и получить новую переменную.
  """)

  drop_long_lat = st.multiselect('Удалить столбцы с долготой и широтой?',['Да','Нет'])

  # if not get_target or not get_more_info or not drop_trip or not save_info or not new_idx or not company_id or not get_distance or not drop_long_lat:
  #   st.error('Выбраны не все варианты предобработки') 
  #   # st.write('*Выбраны не все варианты предобработки*')
  # else:
  show_df = st.form_submit_button('Показать результат предобратоки и обучить модель')
  if show_df:
    if get_target:
      df_2['начало_поездки'] = pd.to_datetime(df_2['начало_поездки'])
      df_2['конец_поездки'] = pd.to_datetime(df_2['конец_поездки'])
      df_2['длительность_поездки'] = df_2['конец_поездки'] - df_2['начало_поездки']
      df_2['длительность_поездки'] = df_2['длительность_поездки'].dt.total_seconds().astype(int)

    if get_more_info[0] == 'Да':
      df_2['месяц_поездки'] = df_2['начало_поездки'].dt.month
      df_2['день_недели_поездки'] = df_2['начало_поездки'].dt.dayofweek
      df_2['час_начала_поездки'] = df_2['начало_поездки'].dt.hour

    if drop_trip[0] =='Да':
      df_2 = df_2.drop(['начало_поездки', 'конец_поездки'], axis=1)
    else:        #нельзя запустить обучение линейной регрессии, если есть тип данных datetime64. Поэтому, если студент решит оставить столбцы начало и конец поездки, нам нужно перевести их в другой формат. 
      df_2['начало_поездки'] = df_2['начало_поездки'].map(lambda x: x.timestamp()).astype(int)
      df_2['конец_поездки'] = df_2['конец_поездки'].map(lambda x: x.timestamp()).astype(int)
      comments = st.expander('Что стало со столбцами начало и конец поездки?')
      comments.markdown("""
      Внимательные из вас могли заметить, что столбцы начало поездки и конец поездки выглядят довольно странно. Мы уже отмечали, что алгоритм линейной регрессии не может обучаться, когда в данных есть тип datetime64. 
      Мы применили метод, который называется timestamp(). Он возвращает время в секундах от 01-01-1970 до даты, которая указана в переменной. Благодаря этому преобразованию тип данных стал float и мы можем обучать нашу модель.
      """)

    if save_info[0] == 'Удалить':  
      df_2 = df_2.drop('информация_сохранена', axis=1)
    else: 
      df_2.информация_сохранена = df_2.информация_сохранена.map(dict(Y=1, N=0))

    if new_idx[0] == 'Да':
      df_2 = df_2.set_index('id')

    if company_id[0] == 'Да':
      df_2['id_компании'] = df_2['id_компании'] - 1

    if get_distance[0] == 'Да':
      latMultiplier  = 111.32
      longMultiplier = np.cos(df_2['широта_окончания']*(np.pi/180.0)) * 111.32
      lat = (latMultiplier  * (df_2['широта_окончания'] - df_2['широта_начала'])) **2
      long = (longMultiplier * (df_2['долгота_окончания'] - df_2['долгота_начала'])) **2
      distance = (lat + long) ** 0.5
      df_2['расстояние_км'] = round(distance,3)

    if drop_long_lat[0] == 'Да':
      df_2 = df_2.drop(['широта_начала', 'широта_окончания','долгота_начала', 'долгота_окончания'], axis=1)

    st.write(df_2.head())
    # st.write(df_2.shape)

    fig, ax = plt.subplots(1, 1, figsize=(15, 10)) 
    ax = sns.heatmap(df_2.corr().abs(), 
                    vmin=0, vmax=1, annot=True, cmap='magma') 
    st.pyplot(fig)
    #st.write('Ранг матрицы:', np.linalg.matrix_rank(df_2.corr())) 
    st.write('Определитель:', np.linalg.det(df_2.corr()))

    X_2 = df_2.drop('длительность_поездки', axis=1)
    y_2 = df_2['длительность_поездки']

    # не будем повторно мешать данные, потому что нам нужно сравнить точность с предыдущим вариантом предобработки
    test_indexes = X_test.index
    train_indexes = X_train.index

    X_train_2 = X_2[X_2.index.isin(train_indexes)]
    y_train_2 = y_2[y_2.index.isin(train_indexes)]

    X_test_2 = X_2[X_2.index.isin(test_indexes)]
    y_test_2 = y_2[y_2.index.isin(test_indexes)]

    model.fit(X_train_2, y_train_2)
    train_losses_2 = mean_absolute_error(y_train_2, model.predict(X_train_2))
    test_losses_2 = mean_absolute_error(y_test_2,model.predict(X_test_2))
    st.write('Показатель метрики на тренировочных данных (в секундах):', round(train_losses_2,2))
    st.write('Показатель метрики на тестовых данных (в секундах):', round(test_losses_2,2))

    get_results = st.expander('Интерпретация результатов')
    get_results.markdown("""
    Если ваша метрика варьируется от 470 до 460 - это значит, что вы правильно предобработали данные и смогли улучшить нашу метрику. Если посмотреть на определитель и график корреляции, можно увидеть отсутствие мультиколлиниарности.
    \n Если ваша метрика на тестовых данных варьируется от 590 и выше - это значит, что ваша модель недообучилась. Скорее всего, график корреляции и определитель матрицы будут выглядеть нормально, но метрика все равно будет слишком высокой. Это может быть связано с тем, что вы потеряли важную информацию о данных, удалив какие-то из столбцов.  
    Подумайте, как можно обработать данные, чтобы улучшить результат и попробуйте снова.
    \n Если метрика удивительным образом равна 0, не спешите радоваться. В задачах машинного обучения всегда стремятся улучшить показатель метрики, то есть минимизировать ошибку предсказания. Тем не менее, не бывает ситуаций, когда мы совершенно не ошибаемся, это просто невозможно. Поэтому, если вы видите цифру 0 - это значит, что ваша модель нерабочая. Во-первых, внимательно посмотрите на график корреляции. Если вы увидите там значения между разными переменными, которые стремятся к единице, это признак линейной зависимости, то есть мультиколлиниарности. 
    Во-вторых, проверьте значение определителя матрицы. Если вы увидите экспоненциальную запись числа - это тоже показатель наличия мультиколлиниарности. Это значит, что модель она переобучилась и нужно избавляться от избыточных данных.
    """)

#-------------------Preprocessing: Second_try-----------------

st.subheader('Предобработка данных: 2 вариант')
st.write("""
Теперь посмотрим, как можно еще улучшить обобщающую способность нашей модели.
""")
termin = st.expander('Что такое обобщающая способность?')
termin.markdown("""
**[Обобщающая способность](https://wiki.loginom.ru/articles/generalization-ability.html)** - это способность модели машинного обучения выдавать правильные результаты не только для примеров, 
участвовавших в процессе обучения, но и для любых новых, которые не участвовали в нем.
""")

df_3 = df.copy()

step_six = st.checkbox('Шаг первый ')
if step_six:
  st.write("""
  Кажется, что некоторые преобразования, которые мы делали в первом варианте, имеют место быть. Давайте восстановим все предыдущие изменения, кроме удаление столбца "информация_сохранена".
  То есть, мы добавим целевую переменную в наши данные, удалим столбец "начало_поездки", "конец_поездки" и зададим новый индекс.
  """)
  old_preproc = st.checkbox('Сделать изменения')
  if old_preproc:
    df_3['начало_поездки'] = pd.to_datetime(df_3['начало_поездки'])
    df_3['конец_поездки'] = pd.to_datetime(df_3['конец_поездки'])
    df_3['длительность_поездки'] = df_3['конец_поездки'] - df_3['начало_поездки']
    df_3['длительность_поездки'] = df_3['длительность_поездки'].dt.total_seconds().astype(int) #длительность поездки в минутах
    df_3 = df_3.drop(['начало_поездки', 'конец_поездки'], axis=1)
    df_3 = df_3.set_index('id')
    st.write(df_3.head())  

step_seven = st.checkbox('Шаг второй ')
if step_seven:
  st.write("""
  Теперь закодируем столбец "информация_сохранена" и приведем к общепринятому виду бинарный признак "id_компании".
  """)
  binary_cols = st.checkbox('Обработать бинарные признаки')
  if binary_cols:
    df_3['id_компании'] = df_3['id_компании'] - 1
    df_3.информация_сохранена = df_3.информация_сохранена.map(dict(Y=1, N=0))
    st.write(df_3.head())

step_eight = st.checkbox('Шаг третий ')
if step_eight:
  st.write("""
  Посмотрите на столбцы с долготой и широтой. Мы можем использовать долготу и широту точек начала и окончания поездки, чтобы примерно оценить расстояние между 2 точками.
  Идея заключается в том, чтобы посчитать разность долгот и широт, а потом вычислить расстояние между двумя точками по теореме Пифагора. Но для начала нам нужно правильно перевести долготу и широту в километры, так как их градусная мера имеет неодинаковую шкалу перевода.
  **[Статья](https://www.datafix.com.au/BASHing/2018-11-07.html)** про перевод разницы градусов долгот и широт в километры.
  \n В блоке "выбор студента" у вас была возможность убедиться в том, что такая предобработка дает нам дополнительную информацию и улучшает точность модели. 
  Умение вытаскивать нужную информацию из данных и создавать новые переменные на основе старых - тоже важный и ценный навык, который может в значительной степени улучшить вашу модель. 
  """)
  make_km = st.checkbox('Получить новый столбец - расстояние_км')
  if make_km:
    latMultiplier  = 111.32
    longMultiplier = np.cos(df_3['широта_окончания']*(np.pi/180.0)) * 111.32
    lat = (latMultiplier  * (df_3['широта_окончания'] - df_3['широта_начала'])) **2
    long = (longMultiplier * (df_3['долгота_окончания'] - df_3['долгота_начала'])) **2
    distance = (lat + long) ** 0.5
    df_3['расстояние_км'] = round(distance,3)

    st.write('Теперь удалим информацию о координатах начала и конца поездки, так как эти данные мы уже имеем в столбце "расстояние_км".')
    drop_coords = st.checkbox('Удалить столбцы с координатами')
    if drop_coords:
      df_3 = df_3.drop(['широта_начала', 'широта_окончания','долгота_начала', 'долгота_окончания'], axis=1)
      st.write("Вот так теперь выглядит теперь наш датасет", df_3.head())
      st.write("Размер датасета", df_3.shape)

step_nine = st.checkbox('Шаг четвертый ')
if step_nine:
  st.write("""
  Кажется, что было бы неплохо посмотреть на распределение нашей целевой переменной. В данных бывают **[выбросы](https://www.helenkapatsa.ru/vybros/)** (наблюдения, которые расходятся с общей закономерностью выборки), которые могут влиять на точность модели. 
  Посмотрите на 2 графика снизу. Это предсказания алгоритма линейной регрессии. Красные кружки - реальные показатели, а пунктиром отмечена разница предсказаний с реальными значениями (ошибки). Как вы помните, любая метрика - среднее значение по всем ошибкам. Алгоритм всегда пытается минимизировать эту среднюю ошибку. 
  На графике слева у нас нет выбросов и алгоритм линейной регрессии смог построить хорошую линию. На графике справа - те же самые данные, но с 3 выбросами. Наш алгоритм теперь учитывает и эти экстремальные значения. Во втором случае наши предсказания будут намного сильнее отличаться от реальных, чем в первом, соответственно показатель метрики и функция ошибки будут хуже. Именно поэтому от выбросов стараются избавляться.
  """)

  st.image('../images/outliers.png', use_column_width=True)
  st.write("Давайте построим гистограмму и ящик с усами по целевой переменной, чтобы оценить их наличие.")

  show_plots = st.checkbox('Построить графики')  #очень долго строятся графики. Чтобы не ждать, будем показывать скриншот 
  if show_plots:
    # box = px.box(df_3, y='длительность_поездки')
    # hist = px.histogram(df_3, x='длительность_поездки')
    # st.plotly_chart(box)
    # st.plotly_chart(hist)

    st.image('../images/plots_first.jpg', use_column_width=True)


    st.write("""
    Мы видим, что у нас довольно большие выбросы (настолько большие, что на графике даже не видно сам ящик с усами). Чтобы модель лучше уловила зависимости в данных, от выбросов лучше избавиться. При этом, полностью от выбросов избавляться нельзя. 
    Давайте обозначим границы: отсечем 5 тысычных значений сверху и 5 тысячных значений снизу. Воспользуемся для этого перцентилями. То есть верхний порог у нас будет 0.995 перцентиль, а нижний 0.005 перцентиль.
    """)
    del_outliers = st.checkbox('Обработать выбросы и посмотреть графики')
    if del_outliers:
      q_low = df_3['длительность_поездки'].quantile(0.005)
      q_hihg = df_3['длительность_поездки'].quantile(0.995)
      df_3 = df_3[(df_3['длительность_поездки'] >= q_low) & (df_3['длительность_поездки'] <= q_hihg)]
      st.image('../images/plots_second.jpg', use_column_width=True)


step_ten = st.checkbox('Шаг пятый ')
if step_ten:
  st.write("""
  Кажется, мы сделали все необходимые преобразования. Попробуем обучить модель и посмотрим на результат. Использовать мы будем все ту же линейную регрессию, метрика - MAE.
  """)

  train_model_2 = st.checkbox('Обучить модель ')
  if train_model_2:
    X_3 = df_3.drop('длительность_поездки', axis=1)
    y_3 = df_3['длительность_поездки']
    test_indexes_2 = X_test.index
    train_indexes_2 = X_train.index

    X_train_3 = X_3[X_3.index.isin(train_indexes_2)]
    y_train_3 = y_3[y_3.index.isin(train_indexes_2)]

    X_test_3 = X_3[X_3.index.isin(test_indexes_2)]
    y_test_3 = y_3[y_3.index.isin(test_indexes_2)]


    # model_3 = LinearRegression()
    model.fit(X_train_3, y_train_3)
    train_losses_3 = mean_absolute_error(y_train_3,model.predict(X_train_3))
    test_losses_3 = mean_absolute_error(y_test_3,model.predict(X_test_3))

    fig, ax = plt.subplots(1, 1, figsize=(15, 10)) 
    ax = sns.heatmap(df_3.corr().abs(), 
                    vmin=0, vmax=1, annot=True, cmap='magma') 
    st.pyplot(fig)
    #st.write('Ранг матрицы:', np.linalg.matrix_rank(df_3.corr())) 
    st.write('Определитель:', np.linalg.det(df_3.corr()))

    st.write('Показатель метрики на тренировочных данных (в секундах):', round(train_losses_3,2))
    st.write('Показатель метрики на тестовых данных (в секундах):', round(train_losses_3,2))


st.subheader('Подведем итоги')
summary = st.expander('Какие выводы можно сделать?')
summary.markdown("""
Предобработка данных - важный и долгий процесс в машинном обучении. Результаты моделей напрямую зависят от того, какие преобразования будут произведены перед обучением модели.
На примере предсказания длительности поездки такси, мы увидели, как предобработка может влиять на обобщающую способность модели. Мы улучшили точность предсказаний почти в 2 раза по сравнению с первым вариантом предобработки.
\n Есть много разных способов обработки данных, о которых мы не упомянули. Например, можно приводить данные к одному порядку - **[отмасштабировать](https://www.helenkapatsa.ru/minmaxscaler/)** или применять разные способы отбора столбцов, 
которые мы передаем модели для обучения (**[встроенные методы, методы фильтрации и методы обертки](https://proglib.io/p/postroenie-i-otbor-priznakov-chast-2-feature-selection-2021-09-25)**).
""")
