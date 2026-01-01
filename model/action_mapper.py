def action_to_label(action_value):
    if action_value < 4:
        return "Surveillance"
    elif action_value < 7:
        return "Prévention"
    else:
        return "Urgence"
