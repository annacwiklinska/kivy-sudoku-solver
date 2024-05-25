import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics, svm
from sklearn.model_selection import train_test_split


class DigitRecognizeModel:
    def __init__(self):
        self.clf = svm.SVC(gamma=0.001)

    def load_train_data(self):
        print("Loading training data...")
        csv_file_path = os.path.join(os.path.dirname(__file__), "data-newer.csv")

        data = pd.read_csv(csv_file_path, header=None)
        target = data.iloc[:, 0]
        data = data.drop(data.columns[0], axis=1)
        # normalize
        # data = data / 255.0

        return data, target

    # def display_image(self, data):
    #     image = data.values.reshape(28, 28)
    #     plt.imshow(image, cmap=plt.cm.gray_r, interpolation="nearest")
    #     plt.axis("off")
    #     plt.show()

    def load_test_data(self):
        print("Loading test data...")
        csv_file_path = os.path.join(os.path.dirname(__file__), "data-new.csv")
        data = pd.read_csv(csv_file_path, header=None)
        # print(pd.DataFrame(data).head())
        target = data.iloc[:, 0]
        # print(target)
        data = data.drop(data.columns[0], axis=1)
        # print(pd.DataFrame(data).head())

        return data, target

    def load_data(self):
        print("Loading data...")
        csv_file_path = os.path.join(os.path.dirname(__file__), "data_2.csv")
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
        def batched_data(data, target, batches_amount):
            batch_size = len(data) // batches_amount
            for i in range(0, len(data), batch_size):
                yield data[i : i + batch_size], target[i : i + batch_size]

        for epoch in range(5):
            batches = batched_data(x_train, y_train, 1)
            batch_number = 0
            for x_batch, y_batch in batches:
                batch_number += 1
                print(f"Training with batch {batch_number}/50")
                self.clf.fit(x_batch, y_batch)
            print(f"Epoch {epoch + 1} completed.")

    def predict(self, x_test):
        print(f"Predicting with {x_test.shape}")
        return self.clf.predict(x_test)

    def evaluate(self, y_test, predicted):
        print(
            f"Classification report for classifier {self.clf}:\n"
            f"{metrics.classification_report(y_test, predicted)}\n"
        )
        disp = metrics.ConfusionMatrixDisplay.from_predictions(y_test, predicted)
        disp.figure_.suptitle("Confusion Matrix")
        print(f"Confusion matrix:\n{disp.confusion_matrix}")

    def visualize(self, images, predictions):
        _, axes = plt.subplots(nrows=1, ncols=4, figsize=(10, 3))
        for ax, image, prediction in zip(axes, images, predictions):
            ax.set_axis_off()
            image = image.reshape(8, 8)
            ax.imshow(image, cmap=plt.cm.gray_r, interpolation="nearest")
            ax.set_title(f"Prediction: {prediction}")

        plt.show()

    def save_model(self, filename):
        joblib.dump(self, filename)
        print("Model saved successfully.")


if __name__ == "__main__":
    digit_recognizer = DigitRecognizeModel()
    # data, target = digit_recognizer.load_train_data()
    # test_data, test_target = digit_recognizer.load_test_data()
    data, target = digit_recognizer.load_data()

    # split
    train_data, test_data, train_target, test_target = digit_recognizer.split_data(
        data, target
    )

    digit_recognizer.train(data, target)
    predicted = digit_recognizer.predict(test_data)
    digit_recognizer.evaluate(test_target, predicted)

    # digit_recognizer.visualize(test_data, predicted)

    digit_recognizer.save_model("model_2.pkl")
    # data_train, target_train = digit_recognizer.load_train_data()
    # first row of the data
    # digit_recognizer.train(data_train, target_train)

    # data_test, target_test = digit_recognizer.load_test_data()
    # predicted = digit_recognizer.predict(data_test)

    # digit_recognizer.evaluate(target_test, predicted)
    # # digit_recognizer.visualize(data_test, predicted)
    # digit_recognizer.save_model("model_fix.pkl")
