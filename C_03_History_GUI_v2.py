from tkinter import *
from functools import partial  # To prevent unwanted windows
import all_constants as c


class Converter:
    """
    Temperature conversion tool (°C to °F or °F to °C)
    """

    def __init__(self):
        """
        Temperature converter GUI
        """

        # self.all_calculations_list = ['10.0°F is -12°C', '20.0°F is -7°C', '30.0°F is -1°C',
        #                               '40.0°F is 4°C', '50.0°F is 10°C', '60.0°F is 16°C']

        self.all_calculations_list = ['10.0°F is -12°C', '20.0°F is -7°C', '30.0°F is -1°C',
                                      '40.0°F is 4°C', '50.0°F is 10°C']

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.to_history_button = Button(self.temp_frame,
                                        text="History / Export",
                                        bg="#004c99",
                                        fg="#fff",
                                        font=("Arial", "14", "bold"),
                                        width=12, command=self.to_history)

        self.to_history_button.grid(row=1, padx=5, pady=5)

    def to_history(self):
        DisplayHistory(self, self.all_calculations_list)


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

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["Export", "#004c99", "", 0],
            ["Close", "#666666", partial(self.close_history, partner), 1],
        ]

        self.hist_button_frame = Frame(self.history_frame)
        self.hist_button_frame.grid(row=4)

        for btn in button_details_list:
            self.make_button = Button(self.hist_button_frame,
                                      font=("Arial", "12", "bold"),
                                      text=btn[0], bg=btn[1],
                                      fg="#ffffff", width=12,
                                      command=btn[2])
            self.make_button.grid(row=0, column=btn[3], padx=10, pady=10)

        # List of everything to put background colour on
        recolour_list = (self.history_frame, self.history_heading_label,
                         self.history_text_label, self.export_text_label, self.hist_button_frame)

        for item in recolour_list:
            item.config(bg=background)

    def close_history(self, partner):
        partner.to_history_button.config(state=NORMAL)  # Re-enable the button
        self.history_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
