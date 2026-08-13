# Add imports here (machine, time, etc.)

# Add variables here (temperature_control, moisture_control, led_control, buzzer_control, etc.)
temperature_control = True
moisture_control = True
led_control = True
buzzer_control = True

def main():
    while True:
        if temperature_control == True:
            print("Temperature control is currently ON.")
        else:
            print("Temperature control is currently OFF.")

        if moisture_control == True:
            print("Moisture control is currently ON.")
        else:
            print("Moisture control is currently OFF.")

        if led_control == True:
            print("LEDs are currently ON.")
        else:
            print("LEDs are currently OFF.")

        if buzzer_control == True:
            print("Buzzer is currently ON.")
        else:
            print("Buzzer is currently OFF.")

        screen = [
                "___________________________________________________________",
                "|                                                         |",
                "|                    === Main Menu ===                    |",
                "|                                                         |",
                "|            1. Turn on/off temperature control           |",
                "|            2. Turn on/off moisture control              |",
                "|            3. Turn on/off LEDs                          |",
                "|            4. Turn on/off buzzer                        |",
                "|            5. View current temperature and moisture     |",
                "|            6. Return to system                          |",
                "|_________________________________________________________|"
                ]
        for row in screen:
            print(row)
        main_choice = input("Enter your choice (1-6): ")
        if main_choice == "1":
            if temperature_control == True:
                print("Temperature control is now OFF.")
                temperature_control = False
            else:
                print("Temperature control is now ON.")
                temperature_control = True

        elif main_choice == "2":
            if moisture_control == True:
                print("Moisture control is currently ON.")
                moisture_control = False
            else:
                print("Moisture control is now ON.")
                moisture_control = True

        elif main_choice == "3":
            if led_control == True:
                print("LEDs are currently ON.")
                led_control = False
            else:
                print("LEDs are now ON.")
                led_control = True

        elif main_choice == "4":
            if buzzer_control == True:
                print("Buzzer is currently ON.")
                buzzer_control = False
            else:
                print("Buzzer is now ON.")
                buzzer_control = True
