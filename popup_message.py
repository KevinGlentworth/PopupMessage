from tkinter import Tk, Toplevel, Frame, Label, Button, font as tkfont, CENTER, LEFT, RIGHT, BOTTOM
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Separator

class PopupMessage():
    """
    Author: Kevin Glentworth
    Date: July 2026
    Description: popup message with buttons.
    .show returns the value of the clicked button.
    """

    def __init__(self, master):
        self.master = master
        self._answer: str = ''


    def show(self,
             title: str = 'Popup Message',
             message: str = 'The default message.',
             alignment: str = 'left',
             x_pos: float | str | int = 0.2,
             y_pos: float | str | int = 0.4,
             screen_relative: bool = False,
             buttons: list = ['OK'],
             default_button: int = 0,
             default_button_colour: str = 'green',
             other_button_colour: str = 'red',
             window_colour: str = 'lemonchiffon',
             use_text_box: bool = False,
             multi_line: bool = False,
             m_width: int = 50, # characters
             m_height: int = 30, # lines
             max_width: int = 100, # characters
             max_height: int = 30, # lines
             timeout: int = 0, # seconds, 0 = no timout. Closes window and returns default value after timeout.
             show_timeout: bool = False,
             font: list = ('Code New Roman', 14)) -> str:
        '''Show a message window and waits for user to press a button or wait for timeout.
        
           Button title is returned.

        Args:
            title (str):
            message (str):
            alignment (str): Alignment of message text.
                             Middle, Center, Left, Right, West, East.
            x_pos (float | int | str) x location on screen.
                                      value between 0.0 and 1.0 -  0.0 = Left, 1.0 = Right
                                      Value > 1 is pixels
                                      valid str values l, w, r, e, c, m, nw, ne, sw, se
                                      left west right east center middle ...
            y_pos (float | int | str) y location on screen.
                                      value between 0.0 and 1.0 -  0.0 = Top, 1.0 = Bottom
                                      Value > 1 is pixels
                                      valid str values t, n, b, s, c, m
                                      top north bottom south centre middle
            screen_relative (bool) position relative to current window or screen
            buttons (list): If blank, just have OK button, else show these
            default_button (int): When enter is pressed or window is closed
            use_text_box (bool): Use a textbox rather than a label
            multi_line (bool): Allow multiple lines
            m_width (int): width in characters
            m_height (int): height in lines
            max_width (int): maximum width in characters
            max_height (int): maximum height in characters
            timeout (int): seconds to wait before returning default value, 0 = no timeout.
            show_timeout (bool): show timeout countdown in window
            font (list): (Family: str, size: int):

        Returns:
            button text
        '''

        self.buttons = buttons
        self.title = title
        self.timeout = timeout
        self.show_timeout = show_timeout
        if multi_line:
            num_lines: int = 0
            lines = message.splitlines()
            width: int = 0
            for line in lines:
                width = max(width, len(line))
                num_lines += 1
            m_width = width + 2
            m_height = min(num_lines, m_height) - 1
        m_height = min(m_height, max_height)
        m_width = min(m_width, max_width)
        if isinstance(x_pos, str):
            match x_pos:
                case 'l' | 'w': # left, west
                    x_pos = 0.0
                case 'c' | 'm': # centre, middle
                    x_pos = 0.5
                case 'r' | 'e': # right, east
                    x_pos = 1.0
                case 'nw':
                    x_pos, y_pos = 0.0, 0.0
                case 'ne':
                    x_pos, y_pos = 0.0, 1.0
                case 'sw':
                    x_pos, y_pos = 1.0, 0.0
                case 'se':
                    x_pos, y_pos = 1.0, 1.0
                case _:
                    x_pos = 0.2
        if isinstance(y_pos, str):
            match y_pos:
                case 't' | 'n': # top, north
                    y_pos = 0.0
                case 'c' | 'm': # centre, middle
                    y_pos = 0.5
                case 'b' | 's': # bottom, south
                    y_pos = 1.0
                case _:
                    y_pos = 0.4
        x_pos = abs(x_pos)
        y_pos = abs(y_pos)
        self.message_window: Toplevel = Toplevel(background=window_colour)
        self.message_window.title('')
        self.message_window.attributes('-topmost', True)
        if alignment == '':
            alignment = LEFT
        # get alignment based upon first character of alignment, default is 'left'.
        # options are middle, centre, left, west, right, east
        alignment = {'m':CENTER, 'c':CENTER, 'l':LEFT, 'r':RIGHT, 'w':LEFT, 'e':RIGHT}.get(alignment[:1].lower(), LEFT)
        if title != None or title == '':
            Label(master=self.message_window,
                  text = title,
                  background=window_colour,
                  font=font,
                  justify=alignment).pack()
            Separator(self.message_window, orient='horizontal').pack(fill='x')
        msg_box = None
        if use_text_box:
            msg_box = ScrolledText(master=self.message_window,
                                        fg='blue',
                                        bg=window_colour,
                                        width=m_width,
                                        height=m_height,
                                        wrap='word',
                                        font=font)
            msg_box.pack()
            msg_box.insert('0.0', message)
            msg_box.configure(state='disabled')
        else:
            Label(master=self.message_window,
                  text=message,
                  fg='navy',
                  bg=window_colour,
                  justify=alignment,
                  font=font).pack(side='top', pady=10, padx=10)
        max_len = 0
        if len(buttons) == 0:
            buttons=['OK']
        for b in buttons:
            max_len = max(max_len, len(b))
        max_len += 2 # Allow for space at each end
        max_len = max(max_len, 8) # Button is at least 8 characters
        new_buttons: list = []
        if default_button < 0:
            default_button = 0
        if default_button >= len(buttons):
            default_button = len(buttons) - 1
        # Centre the button text in the button.
        for index, button in enumerate(buttons):
            leading_chars = int((max_len - len(button)) / 2)
            trailing_chars = max_len - len(button) - leading_chars
            new_button: str = ' ' * (leading_chars-1) + button + ' ' * (trailing_chars-1)
            new_buttons.append(new_button)
        my_frame = Frame(master=self.message_window, bg=window_colour)
        for index, button in enumerate(new_buttons):
            if index == default_button:
                b_colour = default_button_colour
            else:
                b_colour = other_button_colour
            b = Button(master=my_frame, text=button, width=max_len, font=font, fg=b_colour)
            b.configure(command=lambda x=button: self.popup_answer(x))
            b.grid(row=0, column=index, padx=6, pady=2)
        if self.show_timeout:
            self.timer_label = Label(master=my_frame, bg=window_colour, font=(font[0], font[1]-1))
            self.timer_label.grid(row=1, column=0, columnspan=index+1)
        my_frame.pack()
        self.message_window.update_idletasks()
        if screen_relative:
            master_width = self.master.winfo_screenwidth()
            master_height = self.master.winfo_screenheight()
            master_left = 0
            master_top = 0
        else:
            geo = self.master.winfo_geometry().replace('+', 'x').split('x')
            master_width = int(geo[0])
            master_height = int(geo[1])
            master_left = int(geo[2])
            master_top = int(geo[3])
        geo = self.message_window.winfo_geometry().replace('+', 'x').split('x')
        width = int(geo[0])
        height = int(geo[1])
        if 0 < x_pos <= 1:
            new_left = int(master_left + master_width * x_pos)
        else:
            new_left = int(x_pos)
        if 0 < y_pos <= 1:
            new_top = int(master_top + master_height * y_pos)
        else:
            new_top = int(y_pos)
        if new_left + width > self.master.winfo_screenwidth():
            new_left = self.master.winfo_screenwidth() - width - 10
        if new_top + height > self.master.winfo_screenheight():
            new_top = self.master.winfo_screenheight() - height - 30 # Use 30 for visible taskbar.
        self.message_window.geometry(f'+{new_left}+{new_top}')
        self.message_window.protocol('WM_DELETE_WINDOW', lambda: self.popup_answer(new_buttons[default_button]))
        self.message_window.bind('<Return>', lambda event: self.popup_answer(new_buttons[default_button]))
        self.message_window.bind('<space>', lambda event: self.popup_answer(new_buttons[default_button]))
        self.message_window.bind('<Escape>', lambda event: self.popup_answer(new_buttons[default_button]))
        self.message_window.focus_force()
        if timeout > 0 and timeout <= 60:
            self.message_window.after(timeout * 1000, lambda: self.popup_answer(''))
            if self.show_timeout:
                self.time_left: int = self.timeout
                self.update_timer()
        self.message_window.grab_set()
        self.master.wait_window(self.message_window)
        return self._answer

    def popup_answer(self, answer:str='') -> None:
        if answer == '':
            answer=self.buttons[0]
        self._answer = answer.strip(' ')
        self.message_window.destroy()

    def update_timer(self):
        '''Update text colour, gradually change from green (0, 127, 0) to red (255, 0, 0)
        '''
        diff = int(255 * self.time_left / self.timeout)
        s = f'#{(255-diff):02X}{int(diff/2):02X}{0:02X}'
        self.timer_label.configure(fg = s)
        l = '' if self.time_left == 1 else 's'
        self.timer_label.configure(text=f'{str(self.time_left)} second{l} left')
        self.time_left -= 1
        if self.time_left > 0:
            self.message_window.after(1000, lambda:self.update_timer())

        
def _test():
    tk = Tk()
    tk.geometry('1x1+100+100')
    tk.overrideredirect(True)

    print('** PopupMessage **')
    pm = PopupMessage(tk)
    return_value = pm.show(timeout=10, show_timeout=True)
    print(f'return_value={return_value}')
    return_value = pm.show(
            title='Testing PopupMessage',
            message='Multiple Options, default = 2nd button',
            x_pos=0.25, y_pos=0.25,
            use_text_box=True,
            max_height=5,
            buttons=['Accept', 'Cancel', 'Dismiss', 'Ignore', 'Fail'],
            default_button=1)
    print(f'return_value={return_value}')
    return_value = pm.show(
            title='Testing PopupMessage',
            message='One Button, bottom right',
            x_pos='se',
            use_text_box=True,
            max_height=5,
            buttons=['No way'],
            screen_relative=True)
    print(f'return_value={return_value}')
    return_value = pm.show(
            title='Testing PopupMessage',
            message='Default Buttons',
            x_pos=350, y_pos=300,
            max_height=5)
    print(f'return_value={return_value}')
    exit()

if __name__ == '__main__':
    _test()
