#!/usr/bin/env python3
"""
This module defines a hard-coded database of exercises.
Each exercise contains ideal joint angles (using Mediapipe joints) and optional error cases.
Raw strings (using the r"" notation) are used exclusively for the long and short messages.
All data is encapsulated in enums or objects, with ample functions to access different data
and proper error handling to ensure no None values are ever served.
"""

import mediapipe as mp
from mediapipe.solutions.pose import PoseLandmark
from dataclasses import dataclass, field
from typing import Optional, Dict, List
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
        This does not use raw strings; it derives the label from the enum name.
        """
        # Converts 'GREATER_THAN' to 'greater than' etc.
        return self.name.replace("_", " ").lower()


# Dataclass representing an error case for a joint angle.
@dataclass
class ErrorCase:
    error_type: ErrorType            # Type of error condition (an enum)
    threshold: float                 # Threshold value (in degrees)
    long_message: str                # Raw string: detailed explanation message
    short_message: str               # Raw string: concise explanation message
    severity: float                  # Severity (scale 0-10)


# Dataclass representing a joint angle with an optional error case.
@dataclass
class JointAngle:
    value: float                                  # Ideal angle value (in degrees)
    error_case: Optional[ErrorCase] = None        # Optional error case for the joint


# Dataclass representing an exercise with a set of ideal joint angles.
@dataclass
class Exercise:
    name: str
    # Use Mediapipe's PoseLandmark as keys, not raw strings.
    ideal_joint_values: Dict[PoseLandmark, JointAngle] = field(default_factory=dict)


# Default error case used when no data exists for a query.
DEFAULT_ERROR_CASE = ErrorCase(
    error_type=ErrorType.LESS_THAN,  # Default error type; its comparison is not used here.
    threshold=0.0,
    long_message=r"Data not found.",
    short_message=r"Not found",
    severity=0.0
)


# Hard-coded database of exercises.
EXERCISES: List[Exercise] = [
    Exercise(
        name="Exercise A",
        ideal_joint_values={
            # For demonstration, using PoseLandmark values that best approximate the example.
            PoseLandmark.RIGHT_KNEE: JointAngle(
                value=31.0,
                error_case=ErrorCase(
                    error_type=ErrorType.GREATER_THAN,
                    threshold=35.0,
                    long_message=r"you need to increase your angle",
                    short_message=r"increase angle",
                    severity=5.0
                )
            ),
            PoseLandmark.LEFT_KNEE: JointAngle(value=28.0),
            PoseLandmark.LEFT_ELBOW: JointAngle(value=47.0),
            PoseLandmark.RIGHT_WRIST: JointAngle(value=51.0)
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
    return exercise.ideal_joint_values.get(joint, JointAngle(value=0.0, error_case=DEFAULT_ERROR_CASE))


def get_joint_value_from_exercise(exercise: Exercise, joint: PoseLandmark) -> float:
    """
    Retrieves the ideal joint value for the specified joint in the exercise.
    Returns 0.0 if the joint value is not found.
    """
    joint_angle = get_joint_angle_from_exercise(exercise, joint)
    return joint_angle.value


def get_error_case_from_exercise(exercise: Exercise, joint: PoseLandmark) -> ErrorCase:
    """
    Retrieves the error case for the specified joint in the exercise.
    Returns a default error case if none is found.
    """
    joint_angle = get_joint_angle_from_exercise(exercise, joint)
    return joint_angle.error_case if joint_angle.error_case is not None else DEFAULT_ERROR_CASE


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
    Prints details of the exercise including joint angles and error cases.
    """
    print(f"Exercise: {exercise.name}")
    if not exercise.ideal_joint_values:
        print("  No joint data available.")
    for joint, joint_angle in exercise.ideal_joint_values.items():
        print(f"  {joint.name}: {joint_angle.value}º")
        if joint_angle.error_case:
            ec = joint_angle.error_case
            print("    Error Case:")
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

    # Example: Access joint angle and error case for a specific joint.
    joint = PoseLandmark.RIGHT_KNEE
    joint_angle = get_joint_angle_from_exercise(exercise, joint)
    print(f"Accessed {joint.name}: {joint_angle.value}º")
    error_case = get_error_case_from_exercise(exercise, joint)
    print(f"Error Info -> Type: {error_case.error_type.label()}, "
          f"Long Message: {error_case.long_message}, "
          f"Short Message: {error_case.short_message}")