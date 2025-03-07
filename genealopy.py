import yaml
import os
import curses
import uuid

if not os.path.isfile("genealopy.yml"):
    template = {"individuals": [], "relationships": []}
    with open("genealopy.yml", "w") as file:
        yaml.dump(template, file, default_flow_style = False)

def uuid_to_individual(uuid):
    data = yaml.safe_load(open("genealopy.yml", "r"))
    return next((ind for ind in data["individuals"] if ind["uuid"] == uuid), None)

def new_individual(identifier, name, birthplace, birthdate, deathdate, sex):
    individual = {"uuid": identifier, "name": name, "birth": {"place": birthplace, "date": birthdate}, "deathdate": deathdate, "sex": sex}
    data = yaml.safe_load(open("genealopy.yml", "r"))
    data["individuals"].append(individual)
    with open("genealopy.yml", "w") as file:
        yaml.dump(data, file, default_flow_style = False)

def delete_individual(uuid):
    data = yaml.safe_load(open("genealopy.yml", "r"))
    data["individuals"] = [ind for ind in data["individuals"] if ind["uuid"] != uuid]
    data["relationships"] = [rel for rel in data["relationships"] if rel["father"] != uuid and rel["mother"] != uuid and rel["child"] != uuid]
    with open("genealopy.yml", "w") as file:
        yaml.dump(data, file, default_flow_style = False)

def set_father_mother_child_relationship(identifier, father, mother, child):
    relationship = {"uuid": identifier, "father": father, "mother": mother, "child": child}
    data = yaml.safe_load(open("genealopy.yml", "r"))
    data["relationships"].append(relationship)
    with open("genealopy.yml", "w") as file:
        yaml.dump(data, file, default_flow_style = False)

def delete_father_mother_child_relationship(uuid):
    data = yaml.safe_load(open("genealopy.yml", "r"))
    data["relationships"] = [rel for rel in data["relationships"] if rel["uuid"] != uuid]
    with open("genealopy.yml", "w") as file:
        yaml.dump(data, file, default_flow_style = False)

def create_centered_text_input(screen, height):
    input_text = ""
    underline = "_" * 64
    while True:
        screen.move(height, (screen.getmaxyx()[1] - len(underline)) // 2)
        screen.addstr(input_text + underline[len(input_text):], curses.A_UNDERLINE)
        key = screen.getch()
        if key == curses.KEY_ENTER or key == 10 or key == 13:
            break
        elif (key == curses.KEY_BACKSPACE or key == 127) and len(input_text) > 0:
            input_text = input_text[:-1]
        elif len(input_text) < 64 and 32 <= key <= 126:
            input_text = input_text + chr(key)
        screen.refresh()
    return input_text

def create_individual_list_selection(screen, height):
    individual_list = yaml.safe_load(open("genealopy.yml", "r"))["individuals"]
    selected_index = 0
    while True:
        for i, individual in enumerate(individual_list):
            text = individual["name"] + ", from " + individual["birth"]["place"] + " (" + individual["birth"]["date"] + ")"
            if i == selected_index:
                screen.addstr(height + i, ((screen.getmaxyx()[1] - len(text)) // 2), text, curses.A_REVERSE)
            else:
                screen.addstr(height + i, ((screen.getmaxyx()[1] - len(text)) // 2), text)
        screen.refresh()
        key = screen.getch()
        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(individual_list) - 1:
            selected_index += 1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            return individual_list[selected_index]

def create_relationship_list_selection(screen, height):
    relationship_list = yaml.safe_load(open("genealopy.yml", "r"))["relationships"]
    selected_index = 0
    while True:
        for i, relationship in enumerate(relationship_list):
            text = uuid_to_individual(relationship["father"])["name"] + " + " + uuid_to_individual(relationship["mother"])["name"] + " = " + uuid_to_individual(relationship["child"])["name"]
            if i == selected_index:
                screen.addstr(height + i, ((screen.getmaxyx()[1] - len(text)) // 2), text, curses.A_REVERSE)
            else:
                screen.addstr(height + i, ((screen.getmaxyx()[1] - len(text)) // 2), text)
        screen.refresh()
        key = screen.getch()
        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(relationship_list) - 1:
            selected_index += 1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            return relationship_list[selected_index]

def screen_function(screen):
    curses.curs_set(0)
    screen.keypad(True)
    while True:
        screen.clear()
        o = "================================= GENEALOPY - BY MONT ================================="
        screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
        o = "Please choose the option you want to use and press the key for it:"
        screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
        o = "1 - Add new individual"
        screen.addstr(4, (screen.getmaxyx()[1] - len(o)) // 2, o)
        o = "2 - Add new father-mother-child relationship"
        screen.addstr(5, (screen.getmaxyx()[1] - len(o)) // 2, o)
        o = "3 - Delete individual"
        screen.addstr(6, (screen.getmaxyx()[1] - len(o)) // 2, o)
        o = "4 - Delete father-mother-child relationship"
        screen.addstr(7, (screen.getmaxyx()[1] - len(o)) // 2, o)
        o = "5 - Quit"
        screen.addstr(8, (screen.getmaxyx()[1] - len(o)) // 2, o)
        screen.refresh()
        key = screen.getch()
        if key == ord("1"):
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW INDIVIDUAL >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "What's the name of the individual?"
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            new_individual_name = create_centered_text_input(screen, 4)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW INDIVIDUAL >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Where was he/she born at?"
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            new_individual_birthplace = create_centered_text_input(screen, 4)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW INDIVIDUAL >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "When was he/she born?"
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            new_individual_birthdate = create_centered_text_input(screen, 4)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW INDIVIDUAL >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "When did he/she die? If he/she did not, just write \"Alive\"!"
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            new_individual_deathdate = create_centered_text_input(screen, 4)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW INDIVIDUAL >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Lastly, what's the sex of the individual?"
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            new_individual_sex = create_centered_text_input(screen, 4)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW INDIVIDUAL >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Name: " + new_individual_name
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Date of Birth: " + new_individual_birthdate + ", in " + new_individual_birthplace
            screen.addstr(4, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Date of Death: " + new_individual_deathdate
            screen.addstr(5, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Sex: " + new_individual_sex
            screen.addstr(6, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "If you want to add said individual, press 1. Otherwise, press 2."
            screen.addstr(8, (screen.getmaxyx()[1] - len(o)) // 2, o)
            key = screen.getch()
            new_individual_uuid = str(uuid.uuid4())
            if key == ord("1"):
                new_individual(new_individual_uuid, new_individual_name, new_individual_birthplace, new_individual_birthdate, new_individual_deathdate, new_individual_sex)
            elif key == ord("2"):
                continue
        elif key == ord("2"):
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW FATHER-MOTHER-CHILD RELATIONSHIP >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Choose the father."
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            new_relationship_father = create_individual_list_selection(screen, 5)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW FATHER-MOTHER-CHILD RELATIONSHIP >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Now choose the mother."
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            new_relationship_mother = create_individual_list_selection(screen, 5)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW FATHER-MOTHER-CHILD RELATIONSHIP >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Lastly, choose the child."
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            new_relationship_child = create_individual_list_selection(screen, 5)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< ADD NEW FATHER-MOTHER-CHILD RELATIONSHIP >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Father: " + new_relationship_father["name"] + ", from " + new_relationship_father["birth"]["place"] + " (" + new_relationship_father["birth"]["date"] + ")"
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Mother: " + new_relationship_mother["name"] + ", from " + new_relationship_mother["birth"]["place"] + " (" + new_relationship_mother["birth"]["date"] + ")"
            screen.addstr(4, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Child: " + new_relationship_child["name"] + ", from " + new_relationship_child["birth"]["place"] + " (" + new_relationship_child["birth"]["date"] + ")"
            screen.addstr(5, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "If you want to add said relationship, press 1. Otherwise, press 2."
            screen.addstr(7, (screen.getmaxyx()[1] - len(o)) // 2, o)
            key = screen.getch()
            new_relationship_uuid = str(uuid.uuid4())
            if key == ord("1"):
                set_father_mother_child_relationship(new_relationship_uuid, new_relationship_father["uuid"], new_relationship_mother["uuid"], new_relationship_child["uuid"])
            elif key == ord("2"):
                continue
        elif key == ord("3"):
            if len(yaml.safe_load(open("genealopy.yml", "r"))["individuals"]) == 0:
                continue
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< DELETE INDIVIDUAL >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Choose the individual to delete."
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            deleted_individual = create_individual_list_selection(screen, 5)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< DELETE INDIVIDUAL >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Name: " + deleted_individual["name"]
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Date of Birth: " + deleted_individual["birth"]["date"] + ", in " + deleted_individual["birth"]["place"]
            screen.addstr(4, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Date of Death: " + deleted_individual["deathdate"]
            screen.addstr(5, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Sex: " + deleted_individual["sex"]
            screen.addstr(6, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "If you want to delete said individual and all the relationships he/she are part of, press 1. Otherwise, press 2."
            screen.addstr(8, (screen.getmaxyx()[1] - len(o)) // 2, o)
            key = screen.getch()
            if key == ord("1"):
                delete_individual(deleted_individual["uuid"])
            elif key == ord("2"):
                continue
        elif key == ord("4"):
            if len(yaml.safe_load(open("genealopy.yml", "r"))["relationships"]) == 0:
                continue
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< DELETE FATHER-MOTHER-CHILD RELATIONSHIP >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Choose the relationship to delete."
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            deleted_relationship = create_relationship_list_selection(screen, 5)
            screen.clear()
            o = "================================= GENEALOPY - BY MONT ================================="
            screen.addstr(0, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "<< DELETE FATHER-MOTHER-CHILD RELATIONSHIP >>"
            screen.addstr(2, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Father: " + uuid_to_individual(deleted_relationship["father"])["name"] + ", from " + uuid_to_individual(deleted_relationship["father"])["birth"]["place"] + " (" + uuid_to_individual(deleted_relationship["father"])["birth"]["date"] + ")"
            screen.addstr(3, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Mother: " + uuid_to_individual(deleted_relationship["mother"])["name"] + ", from " + uuid_to_individual(deleted_relationship["mother"])["birth"]["place"] + " (" + uuid_to_individual(deleted_relationship["mother"])["birth"]["date"] + ")"
            screen.addstr(4, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "Child: " + uuid_to_individual(deleted_relationship["child"])["name"] + ", from " + uuid_to_individual(deleted_relationship["child"])["birth"]["place"] + " (" + uuid_to_individual(deleted_relationship["child"])["birth"]["date"] + ")"
            screen.addstr(5, (screen.getmaxyx()[1] - len(o)) // 2, o)
            o = "If you want to delete said relationship, press 1. Otherwise, press 2."
            screen.addstr(7, (screen.getmaxyx()[1] - len(o)) // 2, o)
            key = screen.getch()
            if key == ord("1"):
                delete_father_mother_child_relationship(deleted_relationship["uuid"])
            elif key == ord("2"):
                continue
        elif key == ord("5"):
            break

if __name__ == "__main__":
    curses.wrapper(screen_function)