from tkinter import Toplevel, Label, Button, StringVar, font as tkfont, CENTER, LEFT, RIGHT
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Separator
from typing import Any
class PopupMessage():
    """
    Author: Kevin Glentworth
    Date: August-2025
    Description: popup message with either yes/no buttons or close button.
    Returns y or n for Yes/No buttons, nothing for Close button.
    If a textbox is used, a reference to it can be retrieved for further actions.
    Used ScrolledText so I don't have to bother with manually adding a vertical scroll bar.
    """
    def __init__(self, master):
        self.master = master
        self.yes_no: str = 'n'
        self.textbox = None


    def colour_button(self, button: Button, Enter: bool, colour:str):
        """
        Colours the button depending upon whether the action is <Enter> or <Leave>.
        """
        if Enter:
            button.configure(bg=colour)
        else:
            button.configure(bg=colour)
        
            
    def show(self,
             title: str = '',
             message: str = '',
             alignment: str = 'center',
             x_pos: float = 0.2,
             y_pos: float = 0.4,
             yesno: bool = False,
             use_text_box: bool = False,
             multi_line: bool = False,
             m_width: int = 50, # characters
             m_height: int = 30, # lines
             max_width: int = 100, # characters
             max_height: int = 30, # lines
             wait: bool = True,
             font: list = ('Code New Roman', 14)):
        '''Shows a message window and waits for user to press OK or Yes/No.
           If wait is True, the message window must be closed before control
           returns to the calling window.

        :param title: str
        :param message: str
        :param alignment: str [LEFT, CENTER, RIGHT]
        :param x_pos: float [value between 0 and 1]
        :param y_pos: float [value bewtween 0 and 1]
        :param yesno: bool [Use Yes and No buttons or just a Close button]
        :param use_text_box: bool [Use a textbox rather than a label]
        :param multi_line: bool [Allow multiple lines]
        :param m_width: int [width in characters]
        :param m_height: int [height in lines]
        :param max_width: int [maximum width in characters]
        :param wait: bool [wait makes returns to calling process only after window is clsoed]
        :param font: list(Family:str, size: int)
        :return:
        '''

        def popup_yes() -> None:
            self.yes_no = 'y'
            self.message_window.destroy()

        def popup_no() -> None:
            self.yes_no = 'n'
            self.message_window.destroy()
            
        geo = self.master.winfo_geometry().replace('+', 'x').split('x')
        width = int(geo[0])
        height = int(geo[1])
        left = int(geo[2])
        top = int(geo[3])
        new_left = int(left + width * x_pos)
        new_top = int(top + height * y_pos)
        if multi_line:
            num_lines: int = 0
            lines = message.splitlines()
            width: int = 0
            for line in lines:
                width = max(width, len(line))
                num_lines += 1
            m_width = width + 2
            m_height = min(num_lines, m_height) - 1
        if m_width > max_width:
            m_width = max_width
        self.message_window: Toplevel = Toplevel()
        self.message_window.title('')
        if alignment == '':
            alignment = CENTER
        self.s1 = StringVar(self.message_window, title)
        if title != None or title == '':
            Label(master=self.message_window,
                  textvariable=self.s1,
                  font=font,
                  justify=alignment).pack()
            Separator(self.message_window, orient='horizontal').pack(fill='x')
        self.textbox = None
        if use_text_box:
            self.textbox = ScrolledText(master=self.message_window,
                                        fg='blue',
                                        bg='lightyellow',
                                        width=m_width,
                                        height=m_height,
                                        wrap='word',
                                        font=font)
            self.textbox.pack()
            self.textbox.insert('0.0', message)
            self.textbox.configure(state='disabled')
        else:
            self.s2 = StringVar(self.message_window, message)
            Label(master=self.message_window,
                  textvariable=self.s2,
                  fg='navy',
                  bg='lightyellow',
                  justify=alignment,
                  font=font).pack(side='top', pady=10, padx=10)
        if yesno:
            self.yes_no = 'n'
            self.b_yes = Button(master=self.message_window,
                                text='Yes',
                                command=popup_yes,
                                width=5,
                                height=1,
                                bd=2,
                                fg='blue',
                                bg='rosybrown1',
                                font=font)
            self.b_yes.pack(side=LEFT)
            self.b_yes.bind('<Enter>', lambda x: self.colour_button(self.b_yes, True, 'lightskyblue2'))
            self.b_yes.bind('<Leave>', lambda x: self.colour_button(self.b_yes, False, 'rosybrown1'))
            self.b_no = Button(master=self.message_window,
                               text='No',
                               command=popup_no,
                               width=5,
                               height=1,
                               bd=2,
                               fg='blue',
                               bg='rosybrown1',
                               font=font)
            self.b_no.pack(side=RIGHT)
            self.b_no.bind('<Enter>', lambda x: self.colour_button(self.b_no, True, 'lightskyblue2'))
            self.b_no.bind('<Leave>', lambda x: self.colour_button(self.b_no, False, 'rosybrown1'))
            self.message_window.bind('<Return>', lambda event: popup_no())
            self.message_window.bind('<space>', lambda event: popup_no())
            self.message_window.bind('<Escape>', lambda event: popup_no())
            self.message_window.bind('y', lambda event: popup_yes())
            self.message_window.bind('n', lambda event: popup_no())
            self.message_window.bind('Y', lambda event: popup_yes())
            self.message_window.bind('N', lambda event: popup_no())
        else:
            self.b_close = Button(master=self.message_window,
                                  text='Close',
                                  command=self.message_window.destroy,
                                  width=7,
                                  height=1,
                                  bd=2,
                                  fg='yellow',
                                  bg='steelblue4',
                                  font=font)
            self.b_close.pack()
            self.b_close.bind('<Enter>', lambda x: self.colour_button(self.b_close, True, 'lightskyblue2'))
            self.b_close.bind('<Leave>', lambda x: self.colour_button(self.b_close, False, 'steelblue4'))
            self.message_window.bind('<Return>', lambda event: self.message_window.destroy())
            self.message_window.bind('<space>', lambda event: self.message_window.destroy())
            self.message_window.bind('<Escape>', lambda event: self.message_window.destroy())
        self.message_window.geometry(f'+{new_left}+{new_top}')
        self.message_window.update_idletasks()
        self.message_window.focus_force()
        if wait:
            self.message_window.grab_set()
            self.master.wait_window(self.message_window)
        
    def get_textbox(self) -> any:
        """
        Returns the textbox created. If no textbox was used, returns None. This allows other operations to be performed
        on the textbox by the calling program.
        """
        return self.textbox
        
    def get(self) -> str:
        """
        Returns the value of self.yes_no
        """
        return self.yes_no
        
    def set(self) -> None:
        """
        Sets the value of self.yes_no to 'y'
        """
        self.yes_no = 'y'
