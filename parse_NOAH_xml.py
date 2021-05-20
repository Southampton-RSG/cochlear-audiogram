"""
Script to read in patients from NOAH Patients Export XML files,
and iterate through their actions.
"""

import xmltodict
from typing import List


def list_patients(root: dict) -> List[dict]:
    """
    Given an input file, returns the list of patients within it.

    :param root: A dictionary that's the root of the patient file.
    :raises TypeError: If the file doesn't contain a single patient dictionary or a list of them.
    :raises KeyError: If the file isn't correctly structured.
    :return: A list of patients.
    """
    try:
        patients = root['pt:NOAH_Patients_Export']['pt:Patient']['pt:Patient']
    except KeyError:
        raise KeyError(
            "Patient file is malformed! It must have a root <NOAH_Patients_Export>, "
            "followed by a  <pt:Patient> entry containing one or more "
            "<pt:Patient> entries."
        )

    if isinstance(patients, list):
        return patients
    elif isinstance(patients, dict):
        return [patients]
    else:
        raise TypeError("Patient file is malformed! Patients are not stored in a list or dictionary.")


def list_actions(patient: dict) -> List[dict]:
    """
    Given a dictionary representing a patient, returns the actions they have had performed.

    :param patient: The patient to check.
    :raises TypeError: If the patient has actions, but they aren't a list or dictionary.
    :return: A list of actions (may be empty!).
    """
    try:
        actions = patient['pt:Actions']['pt:Action']
    except KeyError:
        return []  # The patient has had no actions. This may or may not be an error?

    if isinstance(actions, list):
        return actions
    elif isinstance(actions, dict):
        return [actions]
    else:
        raise TypeError("Patient file is malformed! Actions are not stored in a list or dictionary.")


def list_items(entry: dict, key: str) -> List:
    """
    Pulls a list of sub-entries from an entry in the dictionary tree.
    Required as xmltodict can't tell the difference between a single dict and an array dicts of size 1.

    :param entry: The dictionary to extract a list from.
    :param key: The key the sub-entries should be under.
    :return: A list of sub-entries.
    """
    try:
        items = entry[key]
    except KeyError:
        return []

    if isinstance(items, list):
        return items
    else:
        return [items]


# Go over our input files, printing out the patients and actions
for input_file_name in ['helentest.xml', 'pta_combined_test.xml']:
    with open(input_file_name) as input_file:
        export = xmltodict.parse(input_file.read())
        patients = list_patients(export)

        print(f'\n### Patients in {input_file_name} ###')
        for patient in patients:
            print(f'\nNumber: {patient["pt:NOAHPatientNumber"]}')

            for action in list_actions(patient):
                print(f'- Action: {action["pt:TypeOfData"]}')

                if action['pt:TypeOfData'] == 'Audiogram':
                    tone_thresholds = list_items(
                            action['pt:PublicData']['HIMSAAudiometricStandard'], 'ToneThresholdAudiogram'
                    )

                    for tone_threshold in tone_thresholds:
                        print(
                            f"  - {tone_threshold['AudMeasurementConditions']['StimulusSignalType']} with"
                            f" {len(list_items(tone_threshold, 'TonePoints'))} tone points"
                        )

                    if not tone_thresholds:
                        print("  - Audiogram has no tone threshold entries")
