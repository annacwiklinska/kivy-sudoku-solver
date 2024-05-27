import operator

import cv2
import joblib
import numpy as np

from model.model import DigitRecognizeModel  # noqa


class ImagePreprocessor:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def preprocess(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(img_gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        inverted = cv2.bitwise_not(thresh, 0)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph = cv2.morphologyEx(inverted, cv2.MORPH_OPEN, kernel)
        result = cv2.dilate(morph, kernel, iterations=1)
        return result

    def find_extreme_corners(self, polygon, limit_fn, compare_fn):
        section, _ = limit_fn(
            enumerate([compare_fn(pt[0][0], pt[0][1]) for pt in polygon]),
            key=operator.itemgetter(1),
        )
        return polygon[section][0][0], polygon[section][0][1]

    def draw_extreme_corners(self, pts, original):
        cv2.circle(original, pts, 7, (0, 255, 0), cv2.FILLED)

    def find_contours(self, img, original):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        polygon = None

        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, closed=True)
            approx = cv2.approxPolyDP(cnt, 0.01 * perimeter, closed=True)
            num_corners = len(approx)

            if num_corners == 4 and area > 1000:
                polygon = cnt
                break

        if polygon is not None:
            top_left = self.find_extreme_corners(polygon, min, np.add)
            top_right = self.find_extreme_corners(polygon, max, np.subtract)
            bot_left = self.find_extreme_corners(polygon, min, np.subtract)
            bot_right = self.find_extreme_corners(polygon, max, np.add)

            if bot_right[1] - top_right[1] == 0:
                return []
            if not (
                0.95
                < ((top_right[0] - top_left[0]) / (bot_right[1] - top_right[1]))
                < 1.05
            ):
                return []

            cv2.drawContours(original, [polygon], 0, (0, 0, 255), 3)
            [
                self.draw_extreme_corners(x, original)
                for x in [top_left, top_right, bot_right, bot_left]
            ]
            return [top_left, top_right, bot_right, bot_left]

        return []

    def warp_image(self, corners, original):
        corners = np.array(corners, dtype="float32")
        top_left, top_right, bot_right, bot_left = corners

        width = int(
            max(
                [
                    np.linalg.norm(top_right - bot_right),
                    np.linalg.norm(top_left - bot_left),
                    np.linalg.norm(bot_right - bot_left),
                    np.linalg.norm(top_left - top_right),
                ]
            )
        )

        mapping = np.array(
            [[0, 0], [width - 1, 0], [width - 1, width - 1], [0, width - 1]],
            dtype="float32",
        )

        matrix = cv2.getPerspectiveTransform(corners, mapping)
        return cv2.warpPerspective(original, matrix, (width, width)), matrix

    def remove_small_white_spots(self, cell, min_area=100):
        # Find all white spots using connected components labeling
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            cell, connectivity=8
        )

        # Iterate through each labeled white spot
        for label in range(
            1, num_labels
        ):  # Skip the first label because it is the background
            # Check if the area of the white spot is smaller than the minimum area
            if stats[label, cv2.CC_STAT_AREA] < min_area:
                # Turn the small white spot black
                cell[labels == label] = 0  # Set all pixels of this spot to black (0)

    def split_into_cells(self, warped_processed, width, height):
        cells = []

        for i in range(9):
            for j in range(9):
                x = i * width
                y = j * height
                cell = warped_processed[x : x + width, y : y + height]
                cell = cell[10:-10, 10:-10]
                # for _ in range(2):
                self.remove_small_white_spots(cell)
                cell = cv2.medianBlur(cell, 9)
                _, cell = cv2.threshold(
                    cell, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )
                cells.append(cell)

        cells_image = np.array(cells)
        img = np.vstack([np.hstack(cells_image[i * 9 : (i + 1) * 9]) for i in range(9)])
        cv2.imwrite("cells.png", img)
        return cells, img

    def is_mostly_black(self, cell, threshold=0.99):
        # Check if there are white pixels at the border
        if (
            np.count_nonzero(cell[0, :]) > 0
            or np.count_nonzero(cell[-1, :]) > 0
            or np.count_nonzero(cell[:, 0]) > 0
            or np.count_nonzero(cell[:, -1]) > 0
        ):
            # Find all white spots using connected components labeling
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                cell, connectivity=8
            )

            # Calculate the size of the image
            image_size = cell.shape[0] * cell.shape[1]

            # Define the threshold for the white spot size
            white_spot_threshold = image_size * 0.15

            largest_white_spot_size = 0
            for stat in stats[1:]:  # Skip the first stat because it is the background
                if stat[cv2.CC_STAT_AREA] > largest_white_spot_size:
                    largest_white_spot_size = stat[cv2.CC_STAT_AREA]

            # If the largest white spot is smaller than the threshold, turn it black
            if largest_white_spot_size < white_spot_threshold:
                for label in range(1, num_labels):
                    if stats[label, cv2.CC_STAT_AREA] == largest_white_spot_size:
                        cell[labels == label] = 0  # Turn the white spot black

        total_pixels = cell.size
        black_pixels = np.count_nonzero(cell == 0)
        black_ratio = black_pixels / total_pixels
        return black_ratio > threshold

    def recognize_digit(self, cell):
        cell = cv2.resize(cell, (28, 28))
        cell = cv2.dilate(cell, (3, 3))
        # cv2.imwrite("cell_d.png", cell)
        cell = cell.reshape(1, -1)
        cell = cell / 255.0  # normalize
        return self.model.predict(cell)

    def process_image(self, image_path):
        img = cv2.imread(image_path)
        img_corners = img.copy()
        processed_img = self.preprocess(img)
        cv2.imwrite("preprocessed.png", processed_img)

        corners = self.find_contours(processed_img, img_corners)
        cv2.imwrite("corners.png", img_corners)

        if corners:
            warped, matrix = self.warp_image(corners, img)
            warped_processed = self.preprocess(warped)
            cv2.imwrite("warped.png", warped)
            cv2.imwrite("warped_processed.png", warped_processed)

            width = warped_processed.shape[0] // 9
            height = warped_processed.shape[1] // 9

            cells, img = self.split_into_cells(warped_processed, width, height)

            non_empty_cells = []
            for cell in cells:
                if not self.is_mostly_black(cell):
                    non_empty_cells.append(cell)
                    # save cell to file
                    # cv2.imwrite(f"non_empty_cell_{len(non_empty_cells)}.png", cell)

            print(f"Found {len(non_empty_cells)} non-empty cells.")

            for i, cell in enumerate(non_empty_cells):
                cv2.imwrite("cells/cell_%d.png" % i, cell)
                digit = self.recognize_digit(cell)
                print(f"Recognized digit: {digit}")

        else:
            print("No corners found")


if __name__ == "__main__":
    preprocessor = ImagePreprocessor("model_3.pkl")
    preprocessor.process_image("image.jpg")
