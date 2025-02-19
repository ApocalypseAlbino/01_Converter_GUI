from tkinter import *
from functools import partial  # To prevent unwanted windows
import all_constants as c
import conversion_rounding as cr
from datetime import date


class Converter:
    """
    Temperature conversion tool (°C to °F or °F to °C)
    """

    def __init__(self):
        """
        Temperature converter GUI
        """

        self.all_calculations_list = ["This is a test"]

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
                                  fg="#004c99", font=("Arial", "11", "bold"))
        self.answer_error.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["To Celsius", "#990099", lambda:self.check_temp(c.ABS_ZERO_FAHRENHEIT), 0, 0],
            ["To Fahrenheit", "#009900", lambda:self.check_temp(c.ABS_ZERO_CELSIUS), 0, 1],
            ["Help / Info", "#cc6600", self.to_help, 1, 0],
            ["History / Export", "#004c99", self.to_history, 1, 1]
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
        self.to_history_button = self.button_ref_list[3]
        self.to_history_button.config(state=DISABLED)

        self.to_help_button = self.button_ref_list[2]

    def check_temp(self, min_temp):
        """
        Checks temperature is valid and either invokes calculation
        function or shows a custom error
        """

        # Retrieve temperature to be converted
        to_convert = self.temp_entry.get()

        # Reset label and entry box (after previous error)
        self.answer_error.config(fg="#004C99", font=("Arial", "11", "bold"))
        self.temp_entry.config(bg="#fff")

        error = f"Enter a number more than / equal to {min_temp}"
        has_errors = "no"

        # checks that amount to be converted is above absolute zero
        try:
            to_convert = float(to_convert)
            if to_convert >= min_temp:
                error = ""
                self.convert(min_temp, to_convert)
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if error != "":
            self.answer_error.config(text=error, fg="#9c0000", font=("Arial", "9", "bold"))
            self.temp_entry.config(bg="#f4cccc")
            self.temp_entry.delete(0, END)

    def convert(self, min_temp, to_convert):

        if min_temp == c.ABS_ZERO_CELSIUS:
            answer = cr.to_fahrenheit(to_convert)
            answer_statement = f"{to_convert}°C is {answer}°F"
        else:
            answer = cr.to_celsius(to_convert)
            answer_statement = f"{to_convert}°F is {answer}°C"

        # enable 'history / export' button as soon as we have a valid calculation
        self.to_history_button.config(state=NORMAL)

        self.answer_error.config(text=answer_statement)
        self.all_calculations_list.append(answer_statement)

    def to_help(self):
        DisplayHelp(self)

    def to_history(self):
        DisplayHistory(self, self.all_calculations_list)


class DisplayHelp:

    def __init__(self, partner):

        # set up dialogue box and background color
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable button
        partner.to_help_button.config(state=DISABLED)

        # If users press 'X' instead of dismiss, unblocks help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "To se the program, simply enter the temperature " \
                    "you wish to convert and then choose to convert " \
                    "to either degrees Celsius (centigrade) or " \
                    "Fahrenheit... \n \n"\
                    "Note that -273 degrees C " \
                    "(-459 F) is absolute zero (the coldest possible " \
                    "temperature). If you try to convert a " \
                    "temperature that is less than -273 degrees C, " \
                    "you will see an error message. \n \n" \
                    "To see your " \
                    "calculation history and export it to a text " \
                    "file, please click the 'History / Export' button."

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#cc6600",
                                     fg="#fff",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List of everything to put background colour on
        recolour_list = (self.help_frame, self.help_heading_label,
                         self.help_text_label)

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)  # Re-enable the button
        self.help_box.destroy()


class DisplayHistory:
    """
    Displays history dialogue box
    """
    def __init__(self, partner, calculations):
        # set up dialogue box and background color
        background = "#fff"
        self.history_box = Toplevel()

        # disable button
        partner.to_history_button.config(state=DISABLED)

        # If users press 'X' instead of dismiss, unblocks history button
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=300,
                                   height=200)
        self.history_frame.grid()

        # background colour and text for the calculation area
        if len(calculations) <= c.MAX_CALCS:
            calc_back = "#d5e8d4"
            calc_amount = "all your calculations."
        else:
            calc_back = "#ffe6cc"
            calc_amount = (f"your recent calculations - "
                           f"showing {c.MAX_CALCS} / {len(calculations)}.")

        history_text = f"Below are {calc_amount} " \
                       f"All calculations are shown to the nearest degree"

        # Create string from calculations list (newest calculations first)
        newest_first_string = ""
        newest_first_list = list(reversed(calculations))

        if len(newest_first_list) <= c.MAX_CALCS:

            for item in newest_first_list[:-1]:
                newest_first_string += item + "\n"

            newest_first_string += newest_first_list[-1]

        else:
            for item in newest_first_list[:c.MAX_CALCS-1]:
                newest_first_string += item + "\n"

            newest_first_string += newest_first_list[c.MAX_CALCS-1]

        export_text = "Please push <Export> to save your calculations in a text file. " \
                      "If the filename already exists, it will be overwritten."

        # Labels

        self.history_heading_label = Label(self.history_frame,
                                           text="History / Export",
                                           font=("Arial", "14", "bold"))
        self.history_heading_label.grid(row=0)

        self.history_text_label = Label(self.history_frame,
                                        text=history_text, wraplength=240,
                                        justify="left")
        self.history_text_label.grid(row=1, padx=10, pady=10)

        self.history = Label(self.history_frame, text=newest_first_string, bg=calc_back, justify="left",
                             font=("Arial", "14"), padx=15, pady=5)
        self.history.grid(row=2)

        self.export_text_label = Label(self.history_frame,
                                       text=export_text, wraplength=240,
                                       justify="left")
        self.export_text_label.grid(row=3, padx=10, pady=10)

        # Label to display export success message
        self.export_filename_label = Label(self.history_frame, text="", wraplength=240, justify="left",
                                           font=("Arial", "10", "bold"))
        self.export_filename_label.grid(row=5)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["Export", "#004c99", lambda: self.export_data(calculations), 0],
            ["Close", "#666666", partial(self.close_history, partner), 1],
        ]

        self.hist_button_frame = Frame(self.history_frame)
        self.hist_button_frame.grid(row=5)

        for btn in button_details_list:
            self.make_button = Button(self.hist_button_frame,
                                      font=("Arial", "12", "bold"),
                                      text=btn[0], bg=btn[1],
                                      fg="#ffffff", width=12,
                                      command=btn[2])
            self.make_button.grid(row=0, column=btn[3], padx=10, pady=10)

        # List of everything to put background colour on
        recolour_list = (self.history_frame, self.history_heading_label,
                         self.history_text_label, self.export_text_label,
                         self.hist_button_frame, self.export_filename_label)

        for item in recolour_list:
            item.config(bg=background)

    def export_data(self, calculations):
        # **** Get current date for heading and filename
        today = date.today()

        # Get day, month and year as individual strings
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        file_name = f"temperatures_{year}_{month}_{day}"

        success_string = ("Export Successful! The file is called "
                          f"{file_name}.txt")
        self.export_filename_label.config(fg="#009900", text=success_string)
        self.export_filename_label.grid(row=4)

        write_to = f"{file_name}.txt"

        with open(write_to, "w") as text_file:
            text_file.write("***** Temperature Calculations *****\n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")
            text_file.write("Here is your calculation history (oldest to newest)...\n")

            # Write the calculations in file
            for item in calculations:
                text_file.write(item)
                text_file.write("\n")

    def close_history(self, partner):
        partner.to_history_button.config(state=NORMAL)  # Re-enable the button
        self.history_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
