import os

import joblib
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import metrics, svm
from sklearn.model_selection import train_test_split


class DigitRecognizeModel:
    def __init__(self):
        self.clf = svm.SVC(gamma=0.001)

    def load_data(self):
        print("Loading data...")
        csv_file_path = os.path.join(os.path.dirname(__file__), "data.csv")
        data = pd.read_csv(csv_file_path, header=None)
        target = data.iloc[:, 0]
        data = data.drop(data.columns[0], axis=1)

        data = data / 255.0

        return data, target

    def split_data(self, data, target):
        print("Splitting data...")
        x_train, x_test, y_train, y_test = train_test_split(
            data, target, test_size=0.2, shuffle=True, random_state=42
        )
        return x_train, x_test, y_train, y_test

    def train(self, x_train, y_train):
        for epoch in range(5):
            self.clf.fit(x_train, y_train)
            print(f"Epoch {epoch + 1} completed.")

    def predict(self, x_test):
        print("Predicting...")
        return self.clf.predict(x_test)

    def evaluate(self, y_test, predicted):
        print(
            f"Classification report for classifier {self.clf}:\n"
            f"{metrics.classification_report(y_test, predicted)}\n"
        )
        disp = metrics.ConfusionMatrixDisplay.from_predictions(y_test, predicted)
        disp.figure_.suptitle("Confusion Matrix")
        print(f"Confusion matrix:\n{disp.confusion_matrix}")

    def visualize(self, x_test, y_test):
        print("Visualizing...")
        plt.figure(figsize=(10, 10))
        for i in range(25):
            plt.subplot(5, 5, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(x_test.iloc[i].values.reshape(28, 28), cmap=plt.cm.binary)
            plt.xlabel(y_test.iloc[i])
        plt.show()

    def save_model(self, filename):
        joblib.dump(self, filename)
        print("Model saved successfully.")


if __name__ == "__main__":
    digit_recognizer = DigitRecognizeModel()

    data, target = digit_recognizer.load_data()

    train_data, test_data, train_target, test_target = digit_recognizer.split_data(
        data, target
    )

    digit_recognizer.train(data, target)
    predicted = digit_recognizer.predict(test_data)
    digit_recognizer.evaluate(test_target, predicted)

    digit_recognizer.visualize(test_data, test_target)

    digit_recognizer.save_model("model.pkl")
