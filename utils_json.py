"""
Author: Adam Knowles
Version: 0.1
Description:

GitHub Repository: https://github.com/Pharkie/
License: GNU General Public License (GPL)
"""

from collections import OrderedDict


def json_loads_ordered(raw_json):
    """
    Manually parse JSON and maintain the order of items.
    """

    def parse_json(data):
        data = data.strip()
        if data.startswith("{"):
            items = []
            data = data[1:-1].strip()
            while data:
                key, data = parse_key(data)
                value, data = parse_value(data)
                items.append((key, parse_json(value)))
                data = data.lstrip(",").strip()
            return OrderedDict(items)
        elif data.startswith("["):
            items = []
            data = data[1:-1].strip()
            while data:
                value, data = parse_value(data)
                items.append(parse_json(value))
                data = data.lstrip(",").strip()
            return items
        elif data.startswith('"'):
            return parse_string(data)
        elif data in ("true", "false"):
            return data == "true"
        elif data == "null":
            return None
        else:
            return parse_number(data)

    def parse_key(data):
        if data.startswith('"'):
            end = data.find('"', 1)
            while data[end - 1] == "\\":
                end = data.find('"', end + 1)
            key = data[1:end]
            return key, data[end + 1 :].lstrip(":").strip()
        raise ValueError("Invalid JSON key")

    def parse_value(data):
        if data.startswith('"'):
            end = data.find('"', 1)
            while data[end - 1] == "\\":
                end = data.find('"', end + 1)
            return data[: end + 1], data[end + 1 :].strip()
        elif data.startswith("{"):
            count = 1
            for i in range(1, len(data)):
                if data[i] == "{":
                    count += 1
                elif data[i] == "}":
                    count -= 1
                if count == 0:
                    return data[: i + 1], data[i + 1 :].strip()
        elif data.startswith("["):
            count = 1
            for i in range(1, len(data)):
                if data[i] == "[":
                    count += 1
                elif data[i] == "]":
                    count -= 1
                if count == 0:
                    return data[: i + 1], data[i + 1 :].strip()
        else:
            end = data.find(",")
            if end == -1:
                return data, ""
            return data[:end], data[end + 1 :].strip()

    def parse_string(data):
        end = data.find('"', 1)
        while data[end - 1] == "\\":
            end = data.find('"', end + 1)
        return data[1:end], data[end + 1 :].strip()

    def parse_number(data):
        end = len(data)
        for i, char in enumerate(data):
            if char in " ,]}":
                end = i
                break
        num_str = data[:end]
        if "." in num_str or "e" in num_str or "E" in num_str:
            return float(num_str)
        return int(num_str)

    return parse_json(raw_json)


def load_menu_from_json(file_path):
    try:
        with open(file_path, "r") as file:
            raw_json = file.read()
            return json_loads_ordered(raw_json)
    except OSError as e:
        print(f"Error reading file {file_path}: {e}")
        return OrderedDict()  # Return an empty OrderedDict in case of error
