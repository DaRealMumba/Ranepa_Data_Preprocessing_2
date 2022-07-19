from nbformat import write
import streamlit as st
import pandas as pd 
import numpy as np 
from PIL import Image
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split



st.markdown('''<h1 style='text-align: center; color: black;'
            >Предварительная обработка данных часть 2: Оценка возможностей </h1>''', 
            unsafe_allow_html=True)

st.write("""
Предварительная обработка данных (Data Preprocessing) - важный этап в науке о данных. Для того, чтобы обучать модель, ей необходимо предоставить очищенные данные в понятном ей виде. 
Предварительная обработка данных, на равне с разведочным анализом данных, обычно занимает большую часть проекта.
\n **Полезно почитать:** [1](https://ru.wikipedia.org/wiki/Предварительная_обработка_данных), [2](https://habr.com/ru/post/511132/), [3](https://pythobyte.com/data-preprocessing-0cb9135c/)

\nЛабораторная работа "Предварительная обработка данных" состоит из 2 частей:
\n**Первая часть:** посмотрим, какие есть способы и возможности обработки данных **([ссылка](https://darealmumba-ranepa-data-preprocessing-data-preprocessing-2knprb.streamlitapp.com/))**.
\n**Вторая часть:** обработаем одни и те же данные двумя разными способами, обучим модель и сравним результаты. 
""")
#-------------------------О проекте-------------------------

pipeline = Image.open('images/Pipeline_2.png')
st.image(pipeline)

expander_bar = st.expander("Описание пайплана стримлита:")
expander_bar.markdown(
    """
\nЗелёным обозначены этапы, корректировка которых доступна студенту, красным - этапы, которые предобработаны и скорректированы сотрудником лаборатории.
\n**1. Сбор данных:** был использован датасет из соревнований на платформе kaggle ([ссылка](https://www.kaggle.com/competitions/nyc-taxi-trip-duration/overview))
\n**2. Предобработка данных:** изменения типов данных, создание новых столбцов (feature engineering), кодировка категориальных переменных, отсечение ненужных признаков (feature selection).
\n**3. Обучение и валидация модели**
\n**4. Сравнение результатов** 
\n**5. Выводы:** подведение итогов и краткое описание проделанной работы, ссылки на другие методы предобработки данных.
\n**6. Создание веб-приложения Streamlit:** оформление и выгрузка на сервер
\n**Используемые библиотеки:** [streamlit](https://docs.streamlit.io/library/get-started), [pandas](https://pandas.pydata.org/docs/user_guide/index.html), [sklearn](https://matplotlib.org/stable/api/index.html), 
[numpy](https://numpy.org/doc/stable/), [pillow](https://pillow.readthedocs.io/en/stable/)
""")

df_expander = st.expander("Информация о датасете:")
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

df = pd.read_csv('ny_taxi.csv')

st.subheader('Анализ данных')

if st.checkbox('Показать Датасет'):
  number = st.number_input('Сколько строк показать', min_value=1, max_value=df.shape[1])
  st.dataframe(df.head(number))
  # st.dataframe(df)

if st.checkbox('Размер Датасета'):
  shape = st.radio(
    "Выбор данных",
     ('Строки', 'Колонки'))
  if shape == 'Строки':
    st.write('Количество строк:', df.shape[0])
  elif shape == 'Колонки':
    st.write('Количество столбцов:', df.shape[1])

if st.checkbox('Уникальные значения переменной'):
  cols = st.multiselect('Выбрать колонку', 
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

if st.checkbox('Описательная статистика по всем числовым колонкам'):
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

step_one = st.checkbox('Шаг первый')
if step_one:
  st.write("""
  Для начала добавим нашу целевую переменную (ее еще называют таргетом), по которой будем делать вычисления. Напомню, что наша целевая переменная - время поездки. Чтобы его получить, нам нужно вычесть время начала поездки и о ее окончания.
  Но прежде, чем это сделать, давайте посмотрим, какой тип данных у этих столбцов. Мы видим "object". Чтобы нам было удобней работать, поменяем тип данных этих столбцов на datetime. 
  """)
  type_expander = st.expander('Зачем мы меняем тип данных?')
  type_expander.markdown("""
  В библиотеке pandas, которая нужна нам для работы с табличными данными, есть специальный модуль **[datetime](https://pythonworld.ru/moduli/modul-datetime.html)**. С помощью него легко доставать необходимую информацию
  (год, месяц, день, час, минута, секунда), а также делать вычисления между датами.
  """)
  target_expander  = st.expander('Что такое целевая переменная?')
  target_expander.markdown("""
  Целевая переменная или таргет - признак датасета, который предстоит предсказывать. **[Ссылка на статью](https://www.helenkapatsa.ru/tsielievaia-pieriemiennaia/)**
  """)
  change_type = st.checkbox('Поменять тип данных')
  if change_type:
    df['начало_поездки'] = pd.to_datetime(df['начало_поездки'])
    df['конец_поездки'] = pd.to_datetime(df['конец_поездки'])
    st.write(pd.DataFrame(df.dtypes.astype('str'), columns=['тип данных']))

    st.write('Теперь мы можем получить целевую переменную. Будем считать время в минутах')

    get_target = st.checkbox('Получить целевую переменную')
    if get_target:
      df['длительность_поездки'] = df['конец_поездки'] - df['начало_поездки']
      df['длительность_поездки'] = df['длительность_поездки'].dt.total_seconds().div(60).astype(int)
      st.write('Чтобы не выводить все 1,5 миллиона значений посмотрим на первые 20')
      st.write(df['длительность_поездки'].head(20))

step_two = st.checkbox('Шаг второй')
if step_two:
  st.write("""
Отлично, мы получили нашу целевую переменную. Теперь можно избавиться от столбцов начало и конец поездки, так как эта информация есть в нашем таргете (если мы их оставим, то можем столкнуться с проблемой **[мультиколлениарноcти](http://www.machinelearning.ru/wiki/index.php?title=Мультиколлинеарность)**). 
\n Обратите внимание на столбец "информация_сохранена" - это категориальная переменная. Мы можем ее закодировать, а можем удалить. Давайте попробуем удалить.
\n Мы можем сделать еще одно маленькое преобразование: у нас есть индексы и колонка id. По сути, это одно и то же, так как у каждой поездки уникальный id. Давайте сделаем так, чтобы колонка id стала нашим индексом.
""")    
  drop_time = st.checkbox('Удалить ненужные столбцы')
  if drop_time:
    df = df.drop(['начало_поездки', 'конец_поездки', 'информация_сохранена'], axis=1)

  change_id = st.checkbox('Задать новый индекс')
  if change_id:
    df = df.set_index('id')
    st.write(df.head())  

step_three = st.checkbox('Шаг третий')
if step_three:
  st.write("""
  Прежде, чем начать обучние, нам нужно разделить наши данные на тренировочную часть и тестовую (разделим в пропорции 80/20). Делить будем с помощью встроенного метода train_test_split из библиотеки sklearn 
  """)
  training_info = st.expander('Зачем мы делим наши данные?')
  training_info.markdown("""
  Процедура разделения на тренировочную и тестовую часть нужна для оценки производительности алгоритмов машинного обучения. На тренировочных данных мы учим нашу модель находить и выявлять законномерности,
  а на тестовых данных мы проверяем способность нашей модели предсказывать на новых данных, которые она ранее не видела. Во время обучения мы подаем все данные нашей модели, включая таргетную переменную.
  Во время теста мы делаем предсказание по новым данным без таргета, а уже после сравниваем полученные предсказания с нашим таргетом.  
  """)
  split_train_test = st.checkbox('Разделить данные')
  if split_train_test:
    X_1 = df.drop('длительность_поездки', axis=1)
    y_1 = df['длительность_поездки']
    X_train, X_test, y_train, y_test = train_test_split(X_1, y_1, 
                                                    test_size=0.2, 
                                                    random_state=42)
    st.write("Размер тренировочного датасета:", X_train.shape, 
    "Размер тестового датасета:" , X_test.shape)
    #st.write("обратите внимание, что у нас теперь всего 6 колонок в ", X_test.head())
step_four = st.checkbox('Шаг четвертый')
if step_four:
  st.write("""
  Теперь мы можем обучить нашу модель и оценить ее производительность, посчитав метрику. Обучать мы будем с помощью обычной линейной регрессии. Метрика - MAE
  """)
  lin_reg = st.expander('Что такое линейная регрессия?')
  lin_reg.markdown("""
  **[Линейная регрессия](https://neurohive.io/ru/osnovy-data-science/linejnaja-regressija/)** - это модель зависимости переменной(таргета) от одной или нескольких других переменных(столбцов).
  Линейная регрессия относится к задаче определения «линии наилучшего соответствия» через набор точек данных. Это задача из раздела обучения с учителем.
  Таким образом можно прогнозировать цену недвижимости, капитализацию компании, стоимость акций или, как в нашем случае, время поездки такси.
  """)
  mae = st.expander('Что за метрика MAE?')
  mae.markdown("""
  MAE (mean absolute error)  - это средняя абсолютная разность между предсказанием модели и целевым значением 
  """)

  lin_reg_img = Image.open('images/lin_reg.png')
  st.image(lin_reg_img)

  train_model = st.checkbox('Обучить модель')
  if train_model:
    model_1 = LinearRegression()
    model_1.fit(X_train, y_train)
    losses = mean_absolute_error(y_test,model_1.predict(X_test))
    st.write('Функция ошибки:', round(losses,2))
    explanation = st.expander('Как это можно трактовать?')
    explanation.markdown('Наша функция ошибки составила 10.17. MAE довольно удобная метрика, так как она считает абсолютные значения. Следовательно, можно сказать, что наша модель в среднем ошибается на 10 минут по сравнению с реальными значениями')
step_five = st.checkbox('Промежуточные выводы')
if step_five:
  st.write("""
  Мы с вами научились делать предсказания и даже получили какой-то результат. Но кажется, что ошибка в 10 минут в предсказании времени поездки такси - довольно большая ошибка. 
  Возможно, если мы по другому обработаем данные, у нас получится минимизировать нашу ошибку и делать более точные предсказания.
  """)


#-------------------Student try---------------------------

df_2 = pd.read_csv('ny_taxi.csv')

st.subheader('Выбор студента')

st.write("""
Теперь попробуйте сами выбрать способы предобработки данных, обучите модель и посмотрите на результат. Таргет нам в любом случае надо получить, чтобы мы могли делать предсказание, поэтому оставим этот пункт без изменений.
""")
get_target = st.checkbox('Изменить тип данных и получить таргетную переменную')
drop_trip = st.multiselect('Удалить столбцы "начало_поездки" и "конец_поездки"?', ['Да', 'Нет'])
save_info = st.multiselect('Удалим или закодируем данные в столбце "информация_сохранена"?', ['Удалить', 'Закодировать'])
new_idx = st.multiselect('Зададим новый индекс?', ['Да','Нет'])
company_id = st.multiselect('Перевести в бинарный признак столбец "id_компании', ['Да','Нет'])
get_distance = st.multiselect('Получить новую переменную "расстояние"?', ['Да','Нет'])
drop_long_lat = st.multiselect('Удалить столбцы с долготой и шириной?',['Да','Нет'])

if not get_target or not drop_trip or not save_info or not new_idx or not company_id or not get_distance or not drop_long_lat:
  st.write('*Выбраны не все варианты предобработки*')
else:
  df_2['начало_поездки'] = pd.to_datetime(df_2['начало_поездки'])
  df_2['конец_поездки'] = pd.to_datetime(df_2['конец_поездки'])
  df_2['длительность_поездки'] = df_2['конец_поездки'] - df_2['начало_поездки']
  df_2['длительность_поездки'] = df_2['длительность_поездки'].dt.total_seconds().div(60).astype(int)

show_df = st.checkbox('Показать результат предобратоки')
st.write(show_df)
if show_df:
  if drop_trip[0] =='Да':
    df_2 = df_2.drop(['начало_поездки', 'конец_поездки'], axis=1)
  else:        #нельзя запустить обучение линейной регрессии, если есть тип данных datetime64. Поэтому, если студент решит оставить столбцы начало и конец поездки, нам нужно перевести их в другой формат. 
    df_2['начало_поездки'] = df_2['начало_поездки'].map(dt.datetime.toordinal)  
    df_2['конец_поездки'] = df_2['конец_поездки'].map(dt.datetime.toordinal)

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
  st.write(df_2.shape)
  # st.write(pd.DataFrame(df_2.dtypes.astype('str'), columns=['тип данных']))
  # st.write(df_2['начало_поездки'].dtypes)

# show_df = st.checkbox('Показать результат предобратоки')
# if show_df:
#   st.write(df_2.head())

get_preds = st.checkbox('Обучаем модель')
if get_preds:

  X_2 = df_2.drop('длительность_поездки', axis=1)
  y_2 = df_2['длительность_поездки']

  # X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(X_2, y_2, 
  #                                                 test_size=0.2, 
  #                                                 random_state=42)

  test_indexes = X_test.index
  train_indexes = X_train.index

  X_train_2 = X_2[X_2.index.isin(train_indexes)]
  y_train_2 = y_2[y_2.index.isin(train_indexes)]

  X_test_2 = X_2[X_2.index.isin(test_indexes)]
  y_test_2 = y_2[y_2.index.isin(test_indexes)]

  # st.write(X_2)
  # st.write(y_2)
  
  # st.write(test_indexes)
  # st.write(train_indexes)

  # st.write('Размер Х теста', X_test_2.shape)
  # st.dataframe(X_train_2.info()) 
  #type(y_train_2))
  # st.dataframe(pd.DataFrame(X_train_2.dtypes.astype('str'), columns=['тип данных']))
  #st.write(df_2.dtypes())
  # st.write("Размер У теста", y_test_2.shape)
  # st.write("Размер У трейна", y_train_2.shape)

  model_2 = LinearRegression()
  model_2.fit(X_train_2, y_train_2)
  losses_2 = mean_absolute_error(y_test_2,model_2.predict(X_test_2))
  st.write('Функция ошибки:', round(losses_2,2))




#-------------------Preprocessing: Second_try-----------------

st.subheader('Предобработка данных: 2 вариант')
st.write("""Мы с вами предполагаем, что, если по-другому обработаем наши данные, то сможем улучшить обобщающую способность нашей модели. Давайте проверим нашу гипотезу. 
Возьмем исходный датасет.
""")
termin = st.expander('Что такое обобщающая способность?')
termin.markdown("""
**[Обобщающая способность](https://wiki.loginom.ru/articles/generalization-ability.html)** - это способность модели машинного обучения выдавать правильные результаты не только для примеров, 
участвовавших в процессе обучения, но и для любых новых, которые не участвовали в нем.
""")

df_3 = pd.read_csv('ny_taxi.csv')

step_six = st.checkbox('Шаг первый')
if step_six:
  st.write("""
  Кажется, что некоторые преобразования, которые мы делали в первом варианте, имеют место быть. Давайте восстановим все предыдущие изменения, кроме удаление колонки "информация_сохранена".
  То есть, мы добавим тагрет в наши данные, удалим колонки "начало_поездки", "конец_поездки" и зададим новый индекс.
  """)
  old_preproc = st.checkbox('Сделать изменения')
  if old_preproc:
    df_3['начало_поездки'] = pd.to_datetime(df_3['начало_поездки'])
    df_3['конец_поездки'] = pd.to_datetime(df_3['конец_поездки'])
    df_3['длительность_поездки'] = df_3['конец_поездки'] - df_3['начало_поездки']
    df_3['длительность_поездки'] = df_3['длительность_поездки'].dt.total_seconds().div(60).astype(int) #длительность поездки в минутах
    df_3 = df_3.drop(['начало_поездки', 'конец_поездки'], axis=1)
    df_3 = df_3.set_index('id')
    st.write(df_3.head())  

step_seven = st.checkbox('Шаг второй')
if step_seven:
  st.write("""
  Давайте внимательно посмотрим на уникальные значения столбцов "информация_сохранена" и "id_компании". Они похожи на бинарные признаки. Тогда нам стоит сделать преобразования: 
  в столбце "инфомарция_сохранена" True и False заменить на 1 и 0, а в стоблце "id_компании" переведем значения из {1,2} в {0,1}
  """)
  binary = st.expander('Что такое бинарный признак?')
  binary.markdown('Признаки, которые могут принимать только одно из двух значений (0, 1) называют бинарными. Например, пол - это бинарный признак (мужчина = 0, женщина - 1)')
  binary_cols = st.checkbox('Обработать бинарные признаки')
  if binary_cols:
    df_3['id_компании'] = df_3['id_компании'] - 1
    df_3.информация_сохранена[df_3.информация_сохранена == 'N'] = 0
    df_3.информация_сохранена[df_3.информация_сохранена == 'Y'] = 1
    st.write(df_3.head())

step_eight = st.checkbox('Шаг третий')
if step_eight:
  st.write("""
  Посмотрите на столбцы с долготой и широтой. Мы можем использовать долготу и широту точек начала и окончания поездки, чтобы примерно оценить расстояние между 2 точками. Сами по себе они, 
  как самостоятельные признаки, вряд ли способны хорошо объяснять длительность поездки. Идея заключается в том, чтобы посчитать разность долго и широт, а потом вычислить расстояние
  между двумя точками по теореме Пифагора. Но для начала нам нужно правильно перевести долготу и широту в километры, так как их градусная мера имеет неодинаковую шкалу перевода.
  **[Статья](https://www.datafix.com.au/BASHing/2018-11-07.html)** про перевод разницы градусов долгот и широт в километры.
  """)
  make_km = st.checkbox('Получить новый признак - расстояние_км')
  if make_km:
    latMultiplier  = 111.32
    longMultiplier = np.cos(df_3['широта_окончания']*(np.pi/180.0)) * 111.32
    lat = (latMultiplier  * (df_3['широта_окончания'] - df_3['широта_начала'])) **2
    long = (longMultiplier * (df_3['долгота_окончания'] - df_3['долгота_начала'])) **2
    distance = (lat + long) ** 0.5
    df_3['расстояние_км'] = round(distance,3)
    #st.write(df_3.head())
    # df_dis = pd.DataFrame(distance)
    # st.write(df_dis)
    #st.dataframe(df_dis.Styler.set_precision(2),height=500)
    # st.dataframe(distance.style.format("{:.2}"))
    st.write('Теперь удалим информацию о координатах начала и конца поездки, так как эти данные мы уже имеем в столбце "расстояние_км".')
    drop_coords = st.checkbox('Удалить столбцы с координатами')
    if drop_coords:
      df_3 = df_3.drop(['широта_начала', 'широта_окончания','долгота_начала', 'долгота_окончания'], axis=1)
      st.write(df_3.head())
      st.write(df_3.shape)

step_nine = st.checkbox('Шаг четвертый')
if step_nine:
  st.write("""
  Кажется, мы сделали все необходимые преобразования. Попробуем обучить модель и посмотрим на результат. Использовать мы будем все ту же линейную регрессию, метрика - MAE.
  """)
  X_3 = df_3.drop('длительность_поездки', axis=1)
  y_3 = df_3['длительность_поездки']
  test_indexes_2 = X_test.index
  train_indexes_2 = X_train.index

  X_train_3 = X_3[X_3.index.isin(train_indexes_2)]
  y_train_3 = y_3[y_3.index.isin(train_indexes_2)]

  X_test_3 = X_3[X_3.index.isin(test_indexes_2)]
  y_test_3 = y_3[y_3.index.isin(test_indexes_2)]

  st.write(test_indexes_2)
  st.write(train_indexes_2)
  st.write('X train', X_train_3.shape)
  st.write('X test',X_test_3.shape)
  st.write('Y train', y_train_3.shape)
  st.write('Y test', y_test_3.shape)

  model_3 = LinearRegression()
  model_3.fit(X_train_3, y_train_3)
  losses_3 = mean_absolute_error(y_test_3,model_3.predict(X_test_3))
  st.write('Функция ошибки:', round(losses_3,2))

st.subheader('Подведем итоги')
summary = st.expander('Какие выводы можно сделать?')
summary.markdown("""
Предобработка данных - важный и долгий процесс в машинном обучении. Результаты моделей напрямую зависят от того, какие преобразования будут произведены перед обучением модели.
На примере предсказания длительности поездки такси, мы увидели, как предобработка может влиять на точность предсказаний. Но предобработка не ограничивается теми возможностями, которые были показаны в этом стримлите.
Например, мы можем столкнуться с пропущенными значениями в наших строках (**[как можно обработать пропущенные значения](https://pythobyte.com/python-how-to-handle-missing-dataframe-values-in-pandas-d56af629/)**), 
или же нам нужно будет обработать категориальные признаки, то есть все нечисловые значения, например слова (**[самый простой способ](https://www.helenkapatsa.ru/bystroie-kodirovaniie/)**, 
**[статья про разные виды кодировок](https://dyakonov.org/2016/08/03/python-категориальные-признаки/)**), также, мы можем столкнуться с **[мультиколлениарностью](https://www.bigdataschool.ru/wiki/мультиколлинеарность)** 
и многими другими проблемами, которые решаются только при внимательном анализе и обработке первичных данных.
""")
