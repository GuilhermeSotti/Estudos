from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def treinar_modelos(X_train, y_train):
    modelos = {
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "KNN": KNeighborsClassifier(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "SVM": SVC()
    }

    treinados = {}
    for nome, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        treinados[nome] = modelo
    return treinados

def avaliar_modelos(modelos, X_test, y_test):
    resultados = {}

    for nome, modelo in modelos.items():
        y_pred = modelo.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        cr = classification_report(y_test, y_pred, output_dict=True)

        resultados[nome] = {
            'acuracia': acc,
            'matriz_confusao': cm,
            'relatorio_classificacao': cr
        }

    return resultados
