#!/usr/bin/env python3
"""
This module defines a hard-coded database of exercises.
Each exercise contains ideal joint angles (using Mediapipe joints) and multiple optional error cases.
Raw strings (using the r"" notation) are used exclusively for the long and short messages.
All data is encapsulated in enums or objects, with ample functions to access different data
and proper error handling to ensure no None values are ever served.
"""

import mediapipe as mp
from mediapipe.solutions.pose import PoseLandmark
from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum, auto

# Improved ErrorType with a built-in comparison method.
class ErrorType(Enum):
    GREATER_THAN = auto()
    LESS_THAN = auto()

    def compare(self, value: float, threshold: float) -> bool:
        """
        Compare the given value with the threshold using the error type.
        """
        if self == ErrorType.GREATER_THAN:
            return value > threshold
        elif self == ErrorType.LESS_THAN:
            return value < threshold
        return False

    def label(self) -> str:
        """
        Generates a descriptive label from the enum member.
        """
        return self.name.replace("_", " ").lower()


# Dataclass representing an error case for a joint angle.
@dataclass
class ErrorCase:
    error_type: ErrorType         # Type of error condition (an enum)
    threshold: float              # Threshold value (in degrees)
    long_message: str             # Raw string: detailed explanation message
    short_message: str            # Raw string: concise explanation message
    severity: float               # Severity (scale 0-10)


# Dataclass representing a joint angle with a list of optional error cases.
@dataclass
class JointAngle:
    value: float                           # Ideal angle value (in degrees)
    error_cases: List[ErrorCase] = field(default_factory=list)  # List of error cases


# Dataclass representing an exercise with a set of ideal joint angles.
@dataclass
class Exercise:
    name: str
    # Use Mediapipe's PoseLandmark as keys, not raw strings.
    ideal_joint_values: Dict[PoseLandmark, JointAngle] = field(default_factory=dict)


# Default error case used when no data exists for a query.
DEFAULT_ERROR_CASE = ErrorCase(
    error_type=ErrorType.LESS_THAN,  # Default error type (its comparison is not used here)
    threshold=0.0,
    long_message=r"Data not found.",
    short_message=r"Not found",
    severity=0.0
)


# Hard-coded database of exercises.
EXERCISES: List[Exercise] = [
    Exercise(
        name="Slow Squats",
        ideal_joint_values={
            # For demonstration, using PoseLandmark values that best approximate the example.
            PoseLandmark.RIGHT_KNEE: JointAngle(
                value=77.5,
                error_cases=[
                    ErrorCase(
                        error_type=ErrorType.GREATER_THAN,
                        threshold=82.5,
                        long_message=r"Your squat needs to be lower",
                        short_message=r"Squat lower",
                        severity=4.0
                    ),
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=72.5,
                        long_message=r"Your squat is too low; you risk falling backward.",
                        short_message=r"Squat less",
                        severity=7.0
                    )
                ]
            ),
            PoseLandmark.LEFT_KNEE: JointAngle(
                value=77.5,
                error_cases=[
                    ErrorCase(
                        error_type=ErrorType.GREATER_THAN,
                        threshold=82.5,
                        long_message=r"Your squat needs to be lower",
                        short_message=r"Squat lower",
                        severity=4.1
                    ),
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=72.5,
                        long_message=r"Your squat is too low; you risk falling backward.",
                        short_message=r"Squat less",
                        severity=7.1
                    )
                ]
            ),
            PoseLandmark.LEFT_ELBOW: JointAngle(value=47.0),
            PoseLandmark.RIGHT_WRIST: JointAngle(value=51.0)
        }
    ),
    Exercise(
        name="Hamstring Stretch",
        ideal_joint_values={
            # For demonstration, using PoseLandmark values that best approximate the example.
            PoseLandmark.RIGHT_KNEE: JointAngle(
                value=180,
                error_cases=[
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=160,
                        long_message=r"Your knees should be touching the floor.",
                        short_message=r"Lower knees",
                        severity=4.0
                    ),
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=140,
                        long_message=r"Your knees should be touching the floor.",
                        short_message=r"Lower knees",
                        severity=8.0
                    ),
                ]
            ),
            PoseLandmark.LEFT_KNEE: JointAngle(
                value=180,
                error_cases=[
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=160,
                        long_message=r"Your knees should be touching the floor.",
                        short_message=r"Lower knees",
                        severity=4.1
                    ),
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=140,
                        long_message=r"Your knees should be touching the floor.",
                        short_message=r"Lower knees",
                        severity=8.1
                    ),
                ]
            ),
            PoseLandmark.LEFT_ARM: JointAngle(
                value=45,
                error_cases=[
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=30,
                        long_message=r"You need to extend your arms as far as possible.",
                        short_message=r"Extend arms",
                        severity=6.0
                    ),
                    ErrorCase(
                        error_type=ErrorType.GREATER_THAN,
                        threshold=60,
                        long_message=r"Your arms should be grasping your feet",
                        short_message=r"Arms to feet",
                        severity=5.5
                    ),
                ]
            ),
            PoseLandmark.RIGHT_ARM: JointAngle(
                value=45,
                error_cases=[
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=30,
                        long_message=r"You need to extend your arms as far as possible.",
                        short_message=r"Extend arms",
                        severity=6.0
                    ),
                    ErrorCase(
                        error_type=ErrorType.GREATER_THAN,
                        threshold=60,
                        long_message=r"Your arms should be grasping your feet",
                        short_message=r"Arms to feet",
                        severity=5.5
                    ),
                ]
            ),
        }
    ),
    Exercise(
        name="Wrist Flexion",
        ideal_joint_values={
            # For demonstration, using PoseLandmark values that best approximate the example.
            PoseLandmark.RIGHT_WRIST: JointAngle(
                value=90,
                error_cases=[
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=70,
                        long_message=r"Do not overstretch your wrist. You could damage it.",
                        short_message=r"Relax your wrist",
                        severity=9.1
                    ),
                    ErrorCase(
                        error_type=ErrorType.GREATER_THAN,
                        threshold=110,
                        long_message=r"To get a good stretch, you need to stretch your wrist more.",
                        short_message=r"Stretch more.",
                        severity=7.9
                    ),
                ]
            ),
            PoseLandmark.LEFT_WRIST: JointAngle(
                value=90,
                error_cases=[
                    ErrorCase(
                        error_type=ErrorType.LESS_THAN,
                        threshold=70,
                        long_message=r"Do not overstretch your wrist. You could damage it.",
                        short_message=r"Relax your wrist",
                        severity=9.2
                    ),
                    ErrorCase(
                        error_type=ErrorType.GREATER_THAN,
                        threshold=110,
                        long_message=r"To get a good stretch, you need to stretch your wrist more.",
                        short_message=r"Stretch more.",
                        severity=7.8
                    ),
                ]
            ),
        }
    ),
    # Additional exercises can be added following the same structure.
]


# --- Data Access Functions with Error Handling --- #

def get_exercise_by_name(name: str) -> Exercise:
    """
    Retrieves an exercise by its name.
    If the exercise is not found, returns a default Exercise with the given name and empty joint data.
    """
    for exercise in EXERCISES:
        if exercise.name == name:
            return exercise
    return Exercise(name=name, ideal_joint_values={})


def get_joint_angle_from_exercise(exercise: Exercise, joint: PoseLandmark) -> JointAngle:
    """
    Retrieves the JointAngle for a given joint from an exercise.
    If the joint data does not exist, returns a JointAngle with a value of 0.0 and a default error case.
    """
    return exercise.ideal_joint_values.get(joint, JointAngle(value=0.0, error_cases=[DEFAULT_ERROR_CASE]))


def get_joint_value_from_exercise(exercise: Exercise, joint: PoseLandmark) -> float:
    """
    Retrieves the ideal joint value for the specified joint in the exercise.
    Returns 0.0 if the joint value is not found.
    """
    joint_angle = get_joint_angle_from_exercise(exercise, joint)
    return joint_angle.value


def get_error_cases_from_exercise(exercise: Exercise, joint: PoseLandmark) -> List[ErrorCase]:
    """
    Retrieves the list of error cases for the specified joint in the exercise.
    Returns a default error case in a list if none is found.
    """
    joint_angle = get_joint_angle_from_exercise(exercise, joint)
    if joint_angle.error_cases:
        return joint_angle.error_cases
    return [DEFAULT_ERROR_CASE]


def list_all_exercises() -> List[str]:
    """
    Returns a list of all exercise names in the database.
    """
    return [exercise.name for exercise in EXERCISES]


def list_joints_in_exercise(exercise: Exercise) -> List[str]:
    """
    Returns a list of joint names (using PoseLandmark names) that have defined data in the exercise.
    """
    return [joint.name for joint in exercise.ideal_joint_values.keys()]


# --- Example Usage Demonstration --- #

def print_exercise_details(exercise: Exercise) -> None:
    """
    Prints details of the exercise including joint angles and all associated error cases.
    """
    print(f"Exercise: {exercise.name}")
    if not exercise.ideal_joint_values:
        print("  No joint data available.")
    for joint, joint_angle in exercise.ideal_joint_values.items():
        print(f"  {joint.name}: {joint_angle.value}º")
        if joint_angle.error_cases:
            for idx, ec in enumerate(joint_angle.error_cases, start=1):
                print(f"    Error Case {idx}:")
                print(f"      Type: {ec.error_type.label()}")
                print(f"      Threshold: {ec.threshold}º")
                print(f"      Long Message: {ec.long_message}")
                print(f"      Short Message: {ec.short_message}")
                print(f"      Severity: {ec.severity}/10")
    print()


if __name__ == "__main__":
    # Demonstrate accessing exercise data safely.
    exercise_name = "Exercise A"
    exercise = get_exercise_by_name(exercise_name)
    print_exercise_details(exercise)

    # Example: Access joint angle and error cases for a specific joint.
    joint = PoseLandmark.RIGHT_KNEE
    joint_angle = get_joint_angle_from_exercise(exercise, joint)
    print(f"Accessed {joint.name}: {joint_angle.value}º")
    error_cases = get_error_cases_from_exercise(exercise, joint)
    for idx, ec in enumerate(error_cases, start=1):
        print(f"Error Info {idx} -> Type: {ec.error_type.label()}, "
              f"Long Message: {ec.long_message}, "
              f"Short Message: {ec.short_message}")