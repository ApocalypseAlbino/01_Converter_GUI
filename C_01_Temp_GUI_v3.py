from tkinter import *
import all_constants as c


class Converter:
    """
    Temperature conversion tool (°C to °F or °F to °C)
    """

    def __init__(self):
        """
        Temperature converter GUI
        """

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Converter",
                                  font=("Arial", "16", "bold"))
        self.temp_heading.grid(row=0)

        instructions = "Please enter a temperature below and press a button " \
                       "to convert from Celsius to Fahrenheit."
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wraplength=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "11"))
        self.temp_entry.grid(row=2, pady=10)

        error = "Please enter a number"
        self.answer_error = Label(self.temp_frame, text=error,
                                  fg="#004c99")
        self.answer_error.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["To Celsius", "#990099", lambda:self.check_temp(c.ABS_ZERO_FAHRENHEIT), 0, 0],
            ["To Fahrenheit", "#009900", lambda:self.check_temp(c.ABS_ZERO_CELSIUS), 0, 1],
            ["Help / Info", "#cc6600", "", 1, 0],
            ["History / Export", "#004c99", "", 1, 1]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#ffffff", font=("Arial", "12", "bold"),
                                      width=12, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)

            self.button_ref_list.append(self.make_button)

        # retrieve 'history / export' button and disable it at the start
        self.to_history_button = self.button_ref_list[3].config(state=DISABLED)

    def check_temp(self,min_temp):
        """
        Checks temperature is valid and either invokes calculation
        function or shows a custom error
        """

        # Retrieve temperature to be converted
        to_convert = self.temp_entry.get()

        try:
            to_convert = float(to_convert)
            if to_convert >= min_temp:
                error = ""
            else:
                error = "Temperature entered below absolute zero"

        except ValueError:
            error = "Enter a number"

        # display the error if necessary
        if error != "":
            self.answer_error.config(text=error, fg="#9c0000")
            self.temp_entry.config(bg="#f4cccc")


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
