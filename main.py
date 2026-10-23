# -*- coding: utf-8 -*-
import time
import serial
import vgamepad as vg

#Arduino Configuration
PORT = "COM9"
BAUDRATE = 115200

# X-axis : left = 0, center = 515, right = 1023
X_GAUCHE = 0
X_CENTRE = 515
X_DROITE = 1023

# Y-axis : top = 0, center = 510, bottom = 1023
Y_HAUT = 0
Y_CENTRE = 515
Y_BAS = 1023

ZONE_MORTE = 0.12


def limiter(valeur, minimum, maximum):
    return max(minimum, min(maximum, valeur))


def normaliser(valeur, minimum, centre, maximum):
    if valeur < centre:
        resultat = (valeur - centre) / (centre - minimum)
    else:
        resultat = (valeur - centre) / (maximum - centre)

    resultat = limiter(resultat, -1.0, 1.0)

    if abs(resultat) < ZONE_MORTE:
        resultat = 0.0

    return resultat


def main():
    gamepad = vg.VX360Gamepad()
    arduino = None

    try:
        print(f"Connecting to the Arduino on {PORT}...")
        arduino = serial.Serial(PORT, BAUDRATE, timeout=1)

        # The Arduino often restarts when the port is opened.
        time.sleep(2)
        arduino.reset_input_buffer()

        print("Virtual controller active!")
        print("Press Ctrl+C to stop.")

        while True:
            ligne = arduino.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            if not ligne:
                continue

            valeurs = ligne.split(",")

            if len(valeurs) != 6:
                continue

            try:
                x, y, bouton_x, bouton_y, bouton_b, bouton_a = (
                    int(v) for v in valeurs
                )
            except ValueError:
                continue

            #X-axis joystick: left is negative, right is positive.
            stick_x = normaliser(
                x, X_GAUCHE, X_CENTRE, X_DROITE
            )

            # Joystick Y: up positive, down negative.
            stick_y = -normaliser(
                y, Y_HAUT, Y_CENTRE, Y_BAS
            )

            gamepad.left_joystick_float(
                x_value_float=stick_x,
                y_value_float=stick_y
            )

            boutons = {
                vg.XUSB_BUTTON.XUSB_GAMEPAD_X: bouton_x,
                vg.XUSB_BUTTON.XUSB_GAMEPAD_Y: bouton_y,
                vg.XUSB_BUTTON.XUSB_GAMEPAD_B: bouton_b,
                vg.XUSB_BUTTON.XUSB_GAMEPAD_A: bouton_a,
            }

            for bouton, appuye in boutons.items():
                if appuye:
                    gamepad.press_button(bouton)
                else:
                    gamepad.release_button(bouton)

            gamepad.update()

    except KeyboardInterrupt:
        print("\nController shutdown...")

    except serial.SerialException as erreur:
        print(f"Error : {erreur}")

    finally:
        #Release all the buttons and recenter the stick.
        try:
            gamepad.reset()
            gamepad.update()
        except Exception:
            pass

	#Close COM9 so that it can be reused.
	#If the Python process is abruptly killed via Task Manager, 
	#or if Windows crashes, the `finally` block cannot guarantee execution
	
	if arduino is not None and arduino.is_open:
            arduino.close()
            print(f"Port {PORT} close.")

        print("Program finished.")


if __name__ == "__main__":
    main()
