import cv2
import numpy as np
import random
import time
import math


# -----------------------------
# Game Configuration
# -----------------------------

WIDTH = 900
HEIGHT = 600

RED_RADIUS = 40
YELLOW_RADIUS = 45

MAX_SPEED = 8
MAX_ACCELERATION = 0.6

WIN_REQUIRED_SECONDS = 3.0
FPS = 30


# -----------------------------
# Utility Functions
# -----------------------------

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def circle_overlap_area(r1, r2, distance):
    """
    Calculates the overlap area between two circles.

    r1: radius of circle 1
    r2: radius of circle 2
    distance: distance between circle centers
    """

    if distance >= r1 + r2:
        return 0.0

    if distance <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2

    part1 = r1 ** 2 * math.acos(
        clamp((distance ** 2 + r1 ** 2 - r2 ** 2) / (2 * distance * r1), -1, 1)
    )

    part2 = r2 ** 2 * math.acos(
        clamp((distance ** 2 + r2 ** 2 - r1 ** 2) / (2 * distance * r2), -1, 1)
    )

    part3 = 0.5 * math.sqrt(
        max(
            0,
            (-distance + r1 + r2)
            * (distance + r1 - r2)
            * (distance - r1 + r2)
            * (distance + r1 + r2)
        )
    )

    return part1 + part2 - part3


# -----------------------------
# Student Controller
# -----------------------------

def student_controller(frame):

    return 0,0


# -----------------------------
# Game Objects
# -----------------------------

class RandomRedCircle:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)

        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)

        self.change_timer = 0

    def update(self):
        self.change_timer += 1

        if self.change_timer > random.randint(20, 60):
            self.vx += random.uniform(-2, 2)
            self.vy += random.uniform(-2, 2)

            self.vx = clamp(self.vx, -MAX_SPEED, MAX_SPEED)
            self.vy = clamp(self.vy, -MAX_SPEED, MAX_SPEED)

            self.change_timer = 0

        self.x += self.vx
        self.y += self.vy

        if self.x < RED_RADIUS or self.x > WIDTH - RED_RADIUS:
            self.vx *= -1

        if self.y < RED_RADIUS or self.y > HEIGHT - RED_RADIUS:
            self.vy *= -1

        self.x = clamp(self.x, RED_RADIUS, WIDTH - RED_RADIUS)
        self.y = clamp(self.y, RED_RADIUS, HEIGHT - RED_RADIUS)


class YellowCircle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.vx = 0
        self.vy = 0

    def update(self, ax, ay):
        ax = clamp(ax, -MAX_ACCELERATION, MAX_ACCELERATION)
        ay = clamp(ay, -MAX_ACCELERATION, MAX_ACCELERATION)

        self.vx += ax
        self.vy += ay

        self.vx = clamp(self.vx, -MAX_SPEED, MAX_SPEED)
        self.vy = clamp(self.vy, -MAX_SPEED, MAX_SPEED)

        self.x += self.vx
        self.y += self.vy

        if self.x < YELLOW_RADIUS or self.x > WIDTH - YELLOW_RADIUS:
            self.vx *= -0.5

        if self.y < YELLOW_RADIUS or self.y > HEIGHT - YELLOW_RADIUS:
            self.vy *= -0.5

        self.x = clamp(self.x, YELLOW_RADIUS, WIDTH - YELLOW_RADIUS)
        self.y = clamp(self.y, YELLOW_RADIUS, HEIGHT - YELLOW_RADIUS)


# -----------------------------
# Main Game Loop
# -----------------------------

def main():
    red_circle = RandomRedCircle()
    yellow_circle = YellowCircle()

    overlap_start_time = None
    win = False

    previous_time = time.time()

    while True:
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        # Draw circles
        cv2.circle(
            frame,
            (int(red_circle.x), int(red_circle.y)),
            RED_RADIUS,
            (0, 0, 255),
            -1
        )

        cv2.circle(
            frame,
            (int(yellow_circle.x), int(yellow_circle.y)),
            YELLOW_RADIUS,
            (0, 255, 255),
            -1
        )

        # Student algorithm controls the yellow circle
        ax, ay = student_controller(frame)

        # Update game objects
        yellow_circle.update(ax, ay)
        red_circle.update()

        # Calculate overlap
        distance = math.dist(
            (red_circle.x, red_circle.y),
            (yellow_circle.x, yellow_circle.y)
        )

        overlap_area = circle_overlap_area(
            RED_RADIUS,
            YELLOW_RADIUS,
            distance
        )

        red_area = math.pi * RED_RADIUS ** 2
        overlap_ratio = overlap_area / red_area

        if overlap_ratio >= 0.5:
            if overlap_start_time is None:
                overlap_start_time = time.time()

            covered_time = time.time() - overlap_start_time

            if covered_time >= WIN_REQUIRED_SECONDS:
                win = True
        else:
            overlap_start_time = None
            covered_time = 0

        # Interface text
        cv2.putText(
            frame,
            f"Acceleration: ax={ax:.2f}, ay={ay:.2f}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Overlap: {overlap_ratio * 100:.1f}%",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        if overlap_start_time is not None:
            cv2.putText(
                frame,
                f"Keep covering: {covered_time:.2f}s / {WIN_REQUIRED_SECONDS}s",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        if win:
            cv2.putText(
                frame,
                "YOU WIN!",
                (WIDTH // 2 - 120, HEIGHT // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 255, 0),
                4
            )

        cv2.imshow("Circle Chaser - OpenCV Exercise", frame)

        key = cv2.waitKey(int(1000 / FPS)) & 0xFF

        if key == 27:
            break

        if key == ord("r"):
            red_circle = RandomRedCircle()
            yellow_circle = YellowCircle()
            overlap_start_time = None
            win = False

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()