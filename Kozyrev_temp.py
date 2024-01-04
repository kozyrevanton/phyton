# -*- coding: utf-8 -*-
"""Финальный проект_Козырев_Антон.ipynb"

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c9bX7CiehXfNyfmVNEVMahrRYlADeGiH
"""


import streamlit as st

import os
import numpy as np
import seaborn as sns

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb


from imblearn.over_sampling import SMOTE


import warnings
warnings.filterwarnings(action="ignore")

from catboost import CatBoostClassifier
import pickle

def Learning_model(KNN_check=True,LR_check=True,AB_check=True,RF_check=True,XGB_check=True,CB_check=True, kNN=13,lr_max_iter=100,max_estimators=150,rf_n_estimators=500,xgb_estimators=100,cb_iterations=1000):
    # Считываем данные
    print("Начинаем считывать файл с данными")
    df = pd.read_csv('data.csv')
    # df.head()
    print("Данные прочитаны")
    # len(df)
    
    # """удаляем дубликаты"""
    
    df.drop_duplicates(inplace=True)
    
    # len(df)
    
    # """Количество строк не изменилось - значит дубликатов не было
    
    # Просмотрим первые 15 записей
    # """
    
    # df.head(15)
    
    # """Посмотрим данные - максимальные минимальные значения, и т.д."""
    
    # df.describe()
    
    # """Проверяем на наличие пропусков. количество нулевых, смотрим типы данных
    
    # """
    
    # df.info()
    
    # """Выделим X и y - данные для входы, и результирующие данные"""
    
    X = np.array(df[df._get_numeric_data().drop(columns=['Bankrupt?']).columns])
    y = df['Bankrupt?'].values
    
    # X
    
    # y
    
    # """посмотрим сколько в нашем датасете строк, относящихся к банкротству"""
    
    # df['Bankrupt?'].value_counts()
    
    # """визуализируем распределение значений всех параметров:"""
    
    # df.hist(figsize = (35,30), bins = 50)
    # plt.show()
    
    # """посмотрим карту корреляций между параметрами:"""
    
    # f, ax = plt.subplots(figsize=(30, 25))
    # mat = df.corr('spearman')
    # mask = np.triu(np.ones_like(mat, dtype=bool))
    # cmap = sns.diverging_palette(230, 20, as_cmap=True)
    # sns.heatmap(mat, mask=mask, cmap=cmap, vmax=1, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    # plt.show()
    best_f1 = 0
    best_s_f1 = 0
    # """Для начала используем модель k ближайших соседей"""
    smt = SMOTE()
    X_smote, y_smote = smt.fit_resample(X, y)
    # разбиваем матрицу признаков и ответы на обучающую и тестовую выборки (80 / 20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    X_s_train, X_s_test, y_s_train, y_s_test = train_test_split(X_smote, y_smote, test_size=0.2)
    print("Данные для обучения и тесты расширены")
    best_Model = 0
    
    if KNN_check:
        # инициализируем алгоритм
        knn = KNeighborsClassifier()
        # обучаем алгоритм на train
        knn.fit(X_train, y_train)
        # получаем прогнозы на основе признаков test
        preds = knn.predict(X_test)
        # сравниваем полученные прогнозы с реальными ответами test с помощью метрик качества
        
        # accuracy_score(y_test, preds)
        
        # """Учитывая дисбаланс классов, данный показатель не показателен
        
        # Для получения более точной оценки нашего алгоритма будем использовать кросс-валидацию
        
        # Результаты тестов на каждом проходе (fold) усредним
        
        # ![alt text](http://scott.fortmann-roe.com/docs/docs/MeasuringError/crossvalidation.png)
        # """
        
        # значение, которое будет принимать наше число соседей
        # np.array(np.linspace(1, 100, 10), dtype='int')
        
        # В sklearn есть специальный модуль для работы с кросс-валидацией
        
        
        # Зададим сетку - среди каких значений выбирать наилучший параметр.
        # knn_grid = {'n_neighbors': np.array(np.linspace(15, 30, 15), dtype='int'),}
                    #'metric': ['minkowski', 'euclidean']} # перебираем по параметру <<n_neighbors>>, по сетке заданной np.linspace(2, 100, 10)
        
        # Создаем объект кросс-валидации
        # gs = GridSearchCV(knn, knn_grid, cv=5, n_jobs=-1)
        
        # Обучаем его
        # gs.fit(X, y)
        
        # pd.DataFrame(gs.cv_results_)
        
        # gs.best_params_
        
        # gs.best_estimator_
        
        # Функция отрисовки графиков
        
        # def grid_plot(x, y, x_label, title, y_label='cross_val'):
        #     plt.figure(figsize=(12, 6))
        #     plt.grid(True)
        #     plt.plot(x, y, 'go-')
        #     plt.xlabel(x_label)
        #     plt.ylabel(y_label)
        #     plt.title(title)
        
        # Строим график зависимости качества от числа соседей
        # замечание: результаты обучения хранятся в атрибуте cv_results_ объекта gs
        
        # grid_plot(knn_grid['n_neighbors'], gs.cv_results_['mean_test_score'], 'n_neighbors', 'KNeighborsClassifier')
        
        # по аналогии поменяем количество точек для проверки разных значений параметра k - 11 точек в диапазоне от 15 до 35 (равные промежутки, int)
        # knn_grid = {'n_neighbors': np.array(np.linspace(15, 35, 11), dtype='int')}
        # gs = GridSearchCV(knn, knn_grid, cv=10)
        # gs.fit(X, y)
        
        # # best_params_ содержит в себе лучшие подобранные параметры, best_score_ лучшее качество
        # gs.best_params_, gs.best_score_
        
        # # отобразим результат по аналогии
        # grid_plot(knn_grid['n_neighbors'], gs.cv_results_['mean_test_score'], 'n_neighbors', 'KNeighborsClassifier')
        
        # """Масштабирование признаков можно выполнить, например, одним из следующих способов способами:
        #  - $x_{new} = \dfrac{x - \mu}{\sigma}$, где $\mu, \sigma$ — среднее и стандартное отклонение значения признака по всей выборке (см. функцию [scale](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.scale.html))
        #  - $x_{new} = \dfrac{x - x_{min}}{x_{max} - x_{min}}$, где $[x_{min}, x_{max}]$ — минимальный интервал значений признака
        # """
        
        # X.T.std(axis=1)
        
        X_ = (X - X.T.mean())/X.T.std()
        
        # X.mean(axis=0)
        
        # X.std(axis=0)
        
        X_ = (X_ - X_.mean(axis=0))/X_.std(axis=0)
        # X
        
        X_scaled = scale(np.array(X_, dtype='float'), with_std=True, with_mean=True)
        
        # минимакс шкалирование
        scaler = MinMaxScaler()
        # инициализируем на основе данных X
        scaler.fit(X_)
        # трансформируем X (потом этим же объектом scaler трансформируем test)
        scaler.transform(X_)
        
        # (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
        
        # """Подборка параметра n_neighbors для KNeighborsClassifier при нормированных признаках. Перебираем все значения от 1 до 100."""
        
        # обучение идентично предыдущим, но в этот раз нормированные значения
        grid = {'n_neighbors': np.array(np.linspace(1, 100, 100), dtype='int')}
        gs = GridSearchCV(knn, grid, cv=10)
        gs.fit(X_scaled, y)
        
        # print(gs.best_params_, gs.best_score_)
        
        # grid_plot(grid['n_neighbors'], gs.cv_results_['mean_test_score'], 'n_neighbors', 'KNeighborsClassifier')
        
        # """Получается самое лучшее значение 13 - его и подставим дальше"""
        
        # Используем классификатор умный kNN
        
        # импортируем и создаем knn классификатор по аналогии
        knn = KNeighborsClassifier(n_neighbors=kNN)
        # тренируем для knn
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        clf_knn = knn.fit(X_train, y_train)
        
        # получаем от них предикты
        y_knn = clf_knn.predict(X_test)
        
        # смотрим какой процент правильных предсказаний для каждой из двух моделей
        
        # $$Accuracy = \frac{\sum_{x_i, y_i \in (X, Y)} I(y(x_i) = y_i)}{|(X, Y)|} = \frac{num~right~classified~obj}{num~all~obj}$$
        # 
        
        # print ('knn =', metrics.accuracy_score(y_test, y_knn))
        
        # для каждого из класса смотрим количество правильных и неправильных предсказаний, визуализируем данные"""
        
        # нужно получить кол-во правильных и неправильых предсказаний по каждому классу от knn
        
        
        # fig = plt.figure(figsize=(8,8))
        # nn_mtx = metrics.confusion_matrix(y_test, y_knn)
        # print(nn_mtx)
        # font = {'weight' : 'bold', 'size'   :22}
        
        # matplotlib.rc('xtick', labelsize=20)
        # matplotlib.rc('ytick', labelsize=20)
        # sns.heatmap(nn_mtx, annot=True, fmt="d",
        #             xticklabels=['1', '0'],
        #             yticklabels=['1', '0'])
        # plt.ylabel("Real value")
        # plt.xlabel("Predicted value")
        
        # 
        
        # $$Recall = \frac{TP}{TP + FN}$$
        
        # с помощью Recall проверим способность алгоритма обнаруживать данный класс вообще"""
        
        # print(metrics.classification_report(y_test, y_knn))
        
        #F1 - метрика, по котой мы можем определить качество модели вцелом - агрегированный показатель
        
        # $$F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$$
        # 
        
        # print ('knn =', metrics.f1_score(y_test, y_knn))
        
        # ![](https://img.grepmed.com/uploads/8345/specificity-table-confusionmatrix-biostatistics-contingency-original.jpeg)
        
        # Основная причина в таких плохих показателях - в несбалансированности выборки. дополним наши данные для сбалансированности выборки
        # 
        
        
        clf_knn = knn.fit(X_s_train, y_s_train)
        
        # # получаем от них предикты
        y_s_knn = clf_knn.predict(X_s_test)
        y_knn = clf_knn.predict(X_test)
        
        # fig = plt.figure(figsize=(8,8))
        # nn_mtx = metrics.confusion_matrix(y_test, y_knn)
        # print(nn_mtx)
        # font = {'weight' : 'bold', 'size'   :22}
        
        # matplotlib.rc('xtick', labelsize=20)
        # matplotlib.rc('ytick', labelsize=20)
        # sns.heatmap(nn_mtx, annot=True, fmt="d",
        #             xticklabels=['1', '0'],
        #             yticklabels=['1', '0'])
        # plt.ylabel("Real value")
        # plt.xlabel("Predicted value")
        
        # Способность обнаруживать класс выросла. Посмотрим общие метрики модели:
        
        # print(metrics.classification_report(y_test, y_knn))
        
        # print(metrics.classification_report(y_s_test, y_s_knn))
        
        # Получается что качество модели, на сбалансированных данных чущественно лучше. Но даже проверка на исходных данных показывает, что результат работы модели стал лучше
        # Сохраним эти метрики в переменной best_metrics, best_metrics_s
        # 
        
        if metrics.f1_score(y_test, y_knn) > best_f1:
          best_f1 = metrics.f1_score(y_test, y_knn)
          best_metrics = metrics.classification_report(y_test, y_knn)
          print('best_f1:',best_f1)
          best_Model = clf_knn
          
        
        if metrics.f1_score(y_s_test, y_s_knn) > best_s_f1:
          best_s_f1 = metrics.f1_score(y_s_test, y_s_knn)
          best_metrics_s = metrics.classification_report(y_s_test, y_s_knn)
          print('best_s_f1:',best_s_f1)

        print("KNN модель обучена")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # рассмотрим ещё несколько моделей, которые можно использовать для обучения на нашей выборке. И выберем самую лучшую по показателю F1.
    
    # 1. Logistic Regression

    if LR_check:    
        clf = LogisticRegression(class_weight = 'balanced', max_iter=lr_max_iter)
        
        clf.fit(X_train, y_train)
        
        predictions = clf.predict(X_test)
        
        print(metrics.classification_report(y_test, predictions))
        
        clf = LogisticRegression(class_weight = 'balanced', max_iter=lr_max_iter)
        
        clf.fit(X_s_train, y_s_train)
        
        LR = clf.predict(X_test)
        LR_s = clf.predict(X_s_test)
        
        
        # print(metrics.classification_report(y_test, LR))
        
        # print(metrics.classification_report(y_s_test, LR_s))
        
        if metrics.f1_score(y_test, LR) > best_f1:
          best_f1 = metrics.f1_score(y_test, LR)
          best_metrics = metrics.classification_report(y_test, LR)
          print('best_f1:',best_f1)
          best_Model = clf
          
        
        if metrics.f1_score(y_s_test, LR_s) > best_s_f1:
          best_s_f1 = metrics.f1_score(y_s_test, LR_s)
          best_metrics_s = metrics.classification_report(y_s_test, LR_s)
          print('best_s_f1:',best_s_f1)
        print("LR модель обучена")
    # Рассмотрим следующую модель:
    # 2. AdaBoostClassifier
    
    if AB_check:
        # Обучим на обычной выборке, и на расширенной
        # 
        
        clf_sklearn = AdaBoostClassifier(n_estimators=max_estimators) # If None, then the base estimator is DecisionTreeClassifier initialized with max_depth=1.
        clf_sklearn.fit(X_train, y_train)
        y_pred_sklearn = clf_sklearn.predict(X_test)
        
        if metrics.f1_score(y_test, y_pred_sklearn) > best_f1:
          best_f1 = metrics.f1_score(y_test, y_pred_sklearn)
          best_metrics = metrics.classification_report(y_test, y_pred_sklearn)
          print('best_f1:',best_f1)
        
        # Обучим на расширенных данных. Также изменим параметр n_estimators на 150.
        
        # 
        
        clf_sklearn_s = AdaBoostClassifier(n_estimators=max_estimators) # If None, then the base estimator is DecisionTreeClassifier initialized with max_depth=1.
        clf_sklearn_s.fit(X_s_train, y_s_train)
        y_pred_sklearn_s = clf_sklearn_s.predict(X_s_test)
        y_pred_sklearn = clf_sklearn_s.predict(X_test)
        
        if metrics.f1_score(y_test, y_pred_sklearn) > best_f1:
          best_f1 = metrics.f1_score(y_test, y_pred_sklearn)
          best_metrics = metrics.classification_report(y_test, y_pred_sklearn)
          print('best_f1:',best_f1)
          best_Model = clf_sklearn_s
        
        if metrics.f1_score(y_s_test, y_pred_sklearn_s) > best_s_f1:
          best_s_f1 = metrics.f1_score(y_s_test, y_pred_sklearn_s)
          best_metrics_s = metrics.classification_report(y_s_test, y_pred_sklearn_s)
          print('best_s_f1:',best_s_f1)
        print("AB модель обучена")
    
    # Дальше используем следующую модель:
    # 3. RandomForestClassifier
    # 
    if RF_check: 
        rf = RandomForestClassifier(n_estimators=rf_n_estimators)
        rf.fit(X_train, y_train)
        rfc = rf.predict(X_test)
        
        if metrics.f1_score(y_test, rfc) > best_f1:
          best_f1 = metrics.f1_score(y_test, rfc)
          best_metrics = metrics.classification_report(y_test, rfc)
          print('best_f1:',best_f1)
        
        # Модель не стала лучше. Обученим на расширенных данных:
        
        rf = RandomForestClassifier(n_estimators=rf_n_estimators)
        rf.fit(X_s_train, y_s_train)
        rfc = rf.predict(X_test)
        rfc_s = rf.predict(X_s_test)
        
        if metrics.f1_score(y_test, rfc) > best_f1:
          best_f1 = metrics.f1_score(y_test, rfc)
          best_metrics = metrics.classification_report(y_test, rfc)
          print('best_f1:',best_f1)
          best_Model = rf
          
        
        if metrics.f1_score(y_s_test, rfc_s) > best_s_f1:
          best_s_f1 = metrics.f1_score(y_s_test, rfc_s)
          best_metrics_s = metrics.classification_report(y_s_test, rfc_s)
          print('best_s_f1:',best_s_f1)
        
        print("RF модель обучена")
    
    # модель получилась существенно лучше прежней
    
    # Попробуем следующую модель:
    # 4. Градиентный бустринг
    # 
    if XGB_check:
        param_dist = {'objective':'binary:logistic', 'n_estimators':xgb_estimators}
        
        clf = xgb.XGBClassifier(**param_dist)
        
        clf.fit(X_train, y_train)
                # ,
                # eval_set=[(X_test, y_test)],
                # eval_metric='mae')
        clf_r = clf.predict(X_test)
        
        if metrics.f1_score(y_test, clf_r) > best_f1:
          best_f1 = metrics.f1_score(y_test, clf_r)
          best_metrics = metrics.classification_report(y_test, clf_r)
          print('best_f1:',best_f1)
        
        # опять результаты не лучше стали. Обучим на расширенных данных:
        
        clf.fit(X_s_train, y_s_train)
        #         ,
        #         eval_set=[(X_s_test, y_s_test)],
        #         eval_metric='mae')
        clf_r = clf.predict(X_test)
        clf_r_s = clf.predict(X_s_test)
        
        if metrics.f1_score(y_test, clf_r) > best_f1:
          best_f1 = metrics.f1_score(y_test, clf_r)
          best_metrics = metrics.classification_report(y_test, clf_r)
          print('best_f1:',best_f1)
          best_Model = clf
        
        if metrics.f1_score(y_s_test, clf_r_s) > best_s_f1:
          best_s_f1 = metrics.f1_score(y_s_test, clf_r_s)
          best_metrics_s = metrics.classification_report(y_s_test, clf_r_s)
          print('best_s_f1:',best_s_f1)
        
        # Оба параметра стали ещё лучше. посмотрим расширенные значения метрик:
        print("модель Градиентного бустинга обучена")
    
    
    # И попробуем последнюю, пятую модель:
    # 5. CatBoostClassifier
    # 
    if CB_check:
        model_CB = CatBoostClassifier(iterations=cb_iterations,
                                   task_type="CPU",
                                   devices='0:1',
                                     use_best_model=True,)
        
        model_CB.fit(X_train, y_train, verbose=True, eval_set=[(X_test, y_test)])
        
        preds = model_CB.predict(X_test)
        
        if metrics.f1_score(y_test, preds) > best_f1:
          best_f1 = metrics.f1_score(y_test, preds)
          best_metrics = metrics.classification_report(y_test, preds)
          print('best_f1:',best_f1) 
          best_Model = model_CB
        
          
        
        # результаты модели не улучшились. Обучим на расширенных данныхх, как и ранее:
        
        model_CB.fit(X_s_train, y_s_train, verbose=True, eval_set=[(X_s_test, y_s_test)])
        preds = model_CB.predict(X_test)
        preds_s = model_CB.predict(X_s_test)
        
        if metrics.f1_score(y_test, preds) > best_f1:
          best_f1 = metrics.f1_score(y_test, preds)
          best_metrics = metrics.classification_report(y_test, preds)
          print('best_f1:',best_f1)
          best_Model = model_CB
         
        
        if metrics.f1_score(y_s_test, preds_s) > best_s_f1:
          best_s_f1 = metrics.f1_score(y_s_test, preds_s)
          best_metrics_s = metrics.classification_report(y_s_test, preds_s)
          print('best_s_f1:',best_s_f1)
        
        # Выведем в итоге самые лучшие метрики.
        
        # Первая - для тестовой выборки из исходных данных,
        # Вторая - для тестовой выборки из расширенных данных.
        # 
        
        print("CB модель обучена")
    return best_Model

def main():
   page = st.sidebar.selectbox("Выбрать страницу", ["Параметры моделей и выбор лучшей модели", "Выполнение прогноза банкротства"])
   if page == "Параметры моделей и выбор лучшей модели":

       st.header("""Параметры для обучения моделей. Будет выбрана лучшая модель по метрике F-1, из всех ниже перечисленных, по этим параметрам:""")
       KNN_check = st.checkbox('Классификатор умный kNN',value=False)
       KNN = st.slider('Количество ближайших соседей', 1, 25, 13, 1)
       LR_check = st.checkbox('Метод логистической регрессии',value=True)
       LR_max_iter = st.slider('Количество итераций логистической регрессии', 1, 1000, 100, 1)
       AB_check = st.checkbox('Метод AdaBoost',value=False)
       Max_estimators = st.slider('Максимальное количество estimators в модели AdaBoost', 1, 1000, 150, 1)
       RF_check = st.checkbox('Метод Случайного леса',value=False)
       RF_n_estimators = st.slider('Количество деревьев в методе случайного леса', 1, 1000, 500, 1)
       XGB_check = st.checkbox('Метод градиентного бустинга',value=False)
       XGB_estimators = st.slider('Число деревьев в методе градиентного бустинга', 1, 1000, 100, 1)
       CB_check = st.checkbox('Модель CatBoost',value=False)
       CB_iterations = st.slider('Количество итераций в модели CatBoost', 1, 3000, 1000, 1)
       st.write("После обучения модели можно будет проводить анализ данных")    
       if  st.button("Запуск обучения модели"):
           st.write('Идет обучение модели и выбор лучшей')
           model = Learning_model(KNN_check,LR_check,AB_check,RF_check,XGB_check,CB_check, kNN=KNN,lr_max_iter=LR_max_iter, max_estimators=Max_estimators,rf_n_estimators=RF_n_estimators,xgb_estimators=XGB_estimators,cb_iterations=CB_iterations)
           with open('data.pickle', 'wb') as f:
               # Pickle the 'data' dictionary using the highest protocol available.
               pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)
           st.write('Обучение модели закончено. Лучшая модель:')
           st.write(model)

   elif page == "Выполнение прогноза банкротства":
       st.header("Прогноз банкротства на основании финансовых показателей компании")
       with open('data.pickle', 'rb') as f:
           # The protocol version used is detected automatically, so we do not
           # have to specify it.
           try:
               model = pickle.load(f)
           except pickle.UnpicklingError:
               model = 0
       if model == 0:
           st.write("Нет модели для прогноза данных. Перейдите на первую страницу и обучите модель")
       else:
           st.write("Сейчас вам необходимо загрузить данные фирм для анализа на предмет потенциального банкротства")  
           st.write("Формат файла должен быть следующим:") 
           df = pd.read_csv('data_test_head')  
           st.write(df.head())
           file_data = st.file_uploader("Выберите файл для загрузки исходных данных",type=["csv"])           
           if file_data is not None:
               predict_bunkrot(model,file_data)
       
def predict_bunkrot(model,file_data):
    df = pd.read_csv(file_data)
    X = np.array(df[df._get_numeric_data().columns])
    y = model.predict(X)
    st.write("Результат предсказания банкротства:")
    st.write(y)
   
if __name__ == "__main__":

    if ('model' not in locals()) and ('model' not in globals()):
        model = 0
    main()
