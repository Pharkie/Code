def modify_menu(menu, depth=0):
    """
    Recursively modifies the menu to add ' >' to the end of any items that are submenus
    and adds a '< Back' option to each sub-menu, ensuring it is the last item.

    Args:
        menu (dict): The menu structure.
        depth (int): The current depth of the menu. Used to avoid adding '< Back' to the top-level menu.
    """
    for key, value in list(menu.items()):
        if isinstance(value, dict):
            new_key = f"{key} >"
            menu[new_key] = menu.pop(key)  # Rename the key with ' >' at the end
            modify_menu(menu[new_key], depth + 1)  # Recurse into the submenu
            if depth > 0:  # Ensure it's not the top-level menu
                menu[new_key]["< Back"] = None  # Add '< Back' option at the end


# Example usage
menu = {
    "Main Menu": {
        "Option 1": None,
        "Option 2": {
            "Sub-option 1": None,
            "Sub-option 2": None,
        },
        "Option 3": None,
    }
}

print("Menu before modification:")
print(menu)
modify_menu(menu)
print("Menu after modification:")
print(menu)
