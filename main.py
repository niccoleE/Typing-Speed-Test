from tkinter import *
from tkinter import messagebox
import random

from text import words

new_text = ""
start_char = 0
color_char = 0
typed = []
index = 0
words_error = {}
tried = 0
the_end = False


def play():
    """general function for the program"""
    global color_char
    global start_char
    global typed
    global index
    global words_error
    global new_text
    global tried
    global the_end

    # update start data
    new_text = ""
    for _ in range(10):
        new_word = random.choice(words)
        if new_word not in new_text:
            new_text += f'{new_word} '
    start_char = 0
    color_char = 0
    typed = []
    index = 0
    words_error = {}
    tried = 0
    the_end = False

    root = Tk()
    root.title('Typing Speed Test')
    root.geometry("700x500")
    root.config(padx=50, pady=30)

    start_message = "How fast can you type?"

    canvas = Canvas(width=700, height=500, highlightthickness=0)

    canvas.grid(column=0, row=0, ipadx=30, ipady=30, pady=(10, 100))

    general = Label(canvas, font=('arial', 15, 'bold'), text=start_message, fg='#3E065F')
    good_luck = Label(canvas, font=('arial', 18, 'bold'), text="Check Your Typing Speed in 60 Seconds.", fg='#1A1A40')
    good_luck.config(pady=15)
    general.grid(row=0, column=1)
    good_luck.grid(row=1, column=1)

    text_widget = Text(canvas, height=5, width=45, wrap=WORD, font=('Lucida', 18))
    text_widget.insert(END, new_text)
    text_widget.config(state=DISABLED)
    text_widget.grid(row=3, column=1, pady=(10, 50))

    def restart():
        """restart function"""
        root.destroy()
        play()

    def get_text(*args):
        """get the text typed by user; check for mistakes"""

        def check():
            """check typed words for mistakes"""
            global typed
            global the_end

            errors_message = "Too many mistakes: \n\n"

            def finish(message):
                """disable text entry widget; show message with detailed mistakes"""
                text_entry.config(state='disabled')
                messagebox.showinfo("showinfo", message)
                start_button.config(text="RESTART", command=restart)

            def timer(count):
                """start timer; calculate typing speed"""
                canvas.itemconfig(timer_widget, text=f'00:0{count}')
                if count > 9:
                    canvas.itemconfig(timer_widget, text=f'00:{count}')
                if count > 50:
                    canvas.itemconfig(timer_widget, fill='red')
                if count < 60 and not the_end:
                    root.after(1000, timer, count + 1)
                elif count == 60:
                    canvas.itemconfig(wpm_widget, text=f'Speed: {len(typed)} wpm')
                    finish(f"You've typed {len(typed)} words per minute.")
                # if 5 mistakes or out of words
                elif the_end:
                    used_time = count
                    wpm = len(typed) / used_time * 60
                    canvas.itemconfig(wpm_widget, text=f'Speed: {round(wpm)} wpm')

            def change_to_green():
                """change word color to green"""
                text_widget.tag_add("check", f'1.{start_char}', f'1.{color_char}')
                text_widget.tag_config("check", font=("arial", 18, "bold"), foreground="#10AF6F")
                text_widget.tag_lower("check")

            def change_to_red():
                """change word color to red"""
                text_widget.tag_add("mistake", f'1.{red_start_char}', f'1.{red_end_char}')
                text_widget.tag_config("mistake", font=("arial", 18, "bold"), foreground="red")
                text_widget.tag_raise("mistake")

            def mistakes_check():
                """if len(typed_word) == len(checking_word)) - find mistakes positions in the word"""
                start_index = 0
                mistakes = []
                checked = ""
                for i in range(min(len(typed_word), len(checking_word))):
                    if typed_word[i] == checking_word[i]:
                        checked += "t"
                    else:
                        checked += "f"

                for char in checked:
                    if char == "f":
                        f_index = checked.index(char, start_index, len(checked))
                        mistakes.append(f_index)
                        start_index = f_index + 1
                return mistakes

            # ----------------------get_test start ------------------- #
            global index
            global color_char
            global typed
            global tried

            # start timer with first typed char
            if len(value) == 1 and len(typed) == 0 and tried == 0:
                tried = 1
                timer(0)
            if " " in value:
                typed.append(value[:-1])
                typed_word = typed[index]
                checking_word = text_list[index]
                index += 1
                mistakes_in_word = mistakes_check()

                # if typed word is correct: make it green
                if typed_word == checking_word:
                    color_char += len(checking_word) + 1
                    change_to_green()

                # if len(typed_word) != len(checking_word): change the whole word to red
                elif len(typed_word) != len(checking_word):
                    red_start_char = color_char
                    red_end_char = color_char + len(checking_word)
                    change_to_red()
                    color_char += len(checking_word) + 1
                    error = {checking_word: typed_word}
                    words_error.update(error)

                # if len(typed_word) == len(checking_word): highlight only mistake letters
                elif mistakes_in_word:
                    a = 0
                    for _ in range(len(mistakes_in_word)):
                        red_start_char = color_char + mistakes_in_word[a]
                        red_end_char = red_start_char + 1
                        change_to_red()
                        a += 1
                    color_char += len(checking_word) + 1
                    change_to_green()
                    error = {checking_word: typed_word}
                    words_error.update(error)

                for ch, t in words_error.items():
                    if t == "":
                        t = " "
                    error = f"'{t}' instead of '{ch}';\n"
                    errors_message += error

                canvas.itemconfig(mistakes_widget, text=f"Mistakes: {len(words_error)}")

                text_entry.delete(0, END)

            if len(typed) == len(text_list):
                the_end = True
                finish("You've typed all 120 words from our list! That is a fantastic result!")

            if len(words_error) == 5:
                the_end = True
                canvas.itemconfig(wpm_widget, fill="red")
                canvas.itemconfig(mistakes_widget, fill="red")
                finish(errors_message)

        value = v.get()
        text_list = new_text.split()
        check()

    v = StringVar()
    v.trace("w", get_text)
    text_entry = Entry(canvas, font=('Lucida', 15), width=35, textvariable=v)
    text_entry.grid(row=5, column=0, columnspan=3, pady=40)

    wpm_widget = canvas.create_text(150, 300, text="Speed: ", font=('Lucida', 15, 'bold'), fill="#3E065F")
    mistakes_widget = canvas.create_text(420, 300, text="Mistakes: ", font=('Lucida', 15, 'bold'), fill='#3E065F')

    start_button = Button(canvas, text="START")
    start_button.config(command=restart)
    start_button.grid(row=6, column=1, pady=20, padx=10)

    timer_widget = canvas.create_text(550, 20, text="00:00", fill='#054B07', font=('Lucida', 18))

    root.mainloop()


play()
