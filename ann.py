import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline


def calculate(dummy):
    # load dataset
    dataframe = pandas.read_csv("root_cause_analysis.csv")

    #Feature Encoding for Target using label Encoding
    dataset = dataframe.values




    X = dataset[:,1:8].astype(float)
    Y = dataset[:,8]
    # encode class values as integers
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)


    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/categorical_crossentropy


    estimator = KerasClassifier(build_fn=baseline_model, epochs=20, batch_size=10, verbose=0)
    kfold = KFold(n_splits=10, shuffle=True)
    baseline_model()
    #results = cross_val_score(estimator, X, dummy_y, cv=kfold)


    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(X, encoded_Y, test_size=0.3, random_state=42)
    estimator.fit(X_train, Y_train)
    predictions = estimator.predict(X_test)


    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    #print("Accuracy (Test Set): %.2f" % accuracy_score(Y_test, predictions))
    akur = accuracy_score(Y_test, predictions)

    y_pred_ori = estimator.predict(dummy)
    return y_pred_ori, akur



def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(14, input_dim=7, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model




dummy = pandas.DataFrame({'CPU_LOAD': [0],
                     'MEMORY_LOAD': [1],
                     'DELAY': [0],
                     'ERROR_1000':[1],
                     'ERROR_1001 ':[0],
                     'ERROR_1002 ':[1],
                     'ERROR_1003 ':[0]})

print(calculate(dummy))