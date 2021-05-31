from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from playsound import playsound
from functions import translate
from dictonary_data import MyDictionary


def translate_action():
    text = to_translate_window.get("1.0", END)
    to_lang = from_lang_combo.get()
    from_lang = to_lang_combo.get()

    try:
        translated_text = translate(text, language_codes_translator[to_lang], language_codes_translator[from_lang])
    except:
        if from_lang_combo.get() == "English/Englisch":
            messagebox.showerror("Error", "Something went wrong, you could reached daily limit or email is invalid")
        else:
            messagebox.showerror("Fehler", "Sie konnten das Tageslimit erreichen oder die E-Mail ist ungültig")
        return
    translated_window.delete("1.0", END)
    translated_window.insert("1.0", translated_text.replace("&#10; ", "\n"))


def prepare_dictionary_data():
    word = word_entry.get()
    if word == "":
        if dict_lang_combo.get() == "English":
            messagebox.showwarning("Warning", "Please enter a word to explore")
        else:
            messagebox.showwarning("Achtung", "Bitte geben Sie ein Wort ein, um es zu erkunden")
        return
    try:
        if dict_lang_combo.get() == "English":
            object_dictonary_res.search(word, "en_US")
        else:
            object_dictonary_res.search(word, "de")
    except:
        if dict_lang_combo.get() == "English":
            messagebox.showwarning("Warning", "The word you entered is incorrect!")
        else:
            messagebox.showwarning("Achtung", "Das eingegebene Wort ist falsch!")
        return

    combo_part_of_speech['values'] = tuple(object_dictonary_res.parts_of_speech.keys())
    combo_part_of_speech.current(0)
    phonetic_label.place(x=40, y=320, width=179, height=30)
    phonetic_var.set(object_dictonary_res.phonetics)
    sound_button.place(x=250, y=320, width=30, height=30)
    object_dictonary_res.view = 0


def sound():
    if dict_lang_combo.get() == "Deutsch":
        messagebox.showinfo("Message", "Der Ton ist im Moment leider nicht verfügbar")
    else:
        playsound(object_dictonary_res.sound)


def show_selected_results():
    dict_output_window.config(state=NORMAL)
    dict_output_window.delete("1.0", END)

    try:
        if radio_var.get() == 'def':
            dict_output_window.insert("1.0", object_dictonary_res.parts_of_speech[combo_part_of_speech.get()][
                object_dictonary_res.view]["definition"].capitalize())
        if radio_var.get() == 'examp':
            dict_output_window.insert("1.0", object_dictonary_res.parts_of_speech[combo_part_of_speech.get()][
                object_dictonary_res.view]["example"].capitalize())
        if radio_var.get() == 'synon':
            for elem in object_dictonary_res.parts_of_speech[combo_part_of_speech.get()][object_dictonary_res.view][
                "synonyms"]:
                dict_output_window.insert("1.0", elem + '\n')
            if dict_lang_combo.get() == "Deutsch":
                for elem in object_dictonary_res.optional_germ_synonyms:
                    dict_output_window.insert("1.0", elem + '\n')
        dict_output_window.config(state=DISABLED)


    except:
        dict_output_window.config(state=NORMAL)
        dict_output_window.insert("1.0", "")
        dict_output_window.config(state=DISABLED)


def next_meaning_view():
    if not object_dictonary_res.view == len(object_dictonary_res.parts_of_speech[combo_part_of_speech.get()]) - 1:
        object_dictonary_res.view += 1
        radio_var.set("def")
        show_selected_results()
    else:
        if dict_lang_combo.get() == "English":
            messagebox.showinfo("Message", "No more meanings")
        else:
            messagebox.showinfo("Nachricht", "Keine Bedeutungen mehr")
    # TODO


def prev_meaning_view():
    if object_dictonary_res.view > 0:
        object_dictonary_res.view -= 1
        radio_var.set("def")
        show_selected_results()


def on_speech_part_change(*a):
    radio_var.set("def")
    object_dictonary_res.view = 0
    show_selected_results()


def on_left_lang_change(*a):
    if from_lang_combo.get() == "German/Deutsch":
        right_flag.place(x=225, y=20, width=52, height=35)
        left_flag.place(x=520, y=20, width=52, height=35)
        translate_button.configure(text="Übersetzen")
        to_lang_combo.set("English/Englisch")

    if from_lang_combo.get() == "English/Englisch":
        left_flag.place(x=225, y=20, width=52, height=35)
        right_flag.place(x=520, y=20, width=52, height=35)
        translate_button.configure(text="Translate")
        to_lang_combo.set("German/Deutsch")


def on_right_lang_change(*a):
    if to_lang_combo.get() == "German/Deutsch":
        right_flag.place(x=520, y=20, width=52, height=35)
        left_flag.place(x=225, y=20, width=52, height=35)
        from_lang_combo.set("English/Englisch")

    if to_lang_combo.get() == "English/Englisch":
        left_flag.place(x=520, y=20, width=52, height=35)
        right_flag.place(x=225, y=20, width=52, height=35)
        from_lang_combo.set("German/Deutsch")


def swap_translation():
    tmp_lang = from_lang_combo.get()
    from_lang_combo.set(to_lang_combo.get())
    to_lang_combo.set(tmp_lang)

    to_translate_window.delete("1.0", END)
    to_translate_window.insert("1.0", translated_window.get("1.0", END))
    translated_window.delete("1.0", END)


def on_language_change(*a):
    object_dictonary_res.view = 0
    phonetic_var.set("")
    combo_part_of_speech.set("")
    if dict_lang_combo.get() == "English":
        explore_button.configure(text="Explore")
        r1.configure(text="Definitions")
        r2.configure(text="Examples of usage")
        r3.configure(text="Synonyms")
        dict_info_label.configure(text="Switch between meanings")
        root.title("Welcome in English-German translator and english dictionary!")

    else:
        explore_button.configure(text="Erkunden")
        r1.configure(text="Definitionen")
        r2.configure(text="Anwendungsbeispiele")
        r3.configure(text="Synonyme")
        root.title("Willkommen im englisch-deutschen Übersetzer und Deutsch-Wörterbuch!")
        dict_info_label.configure(text="Zwischen Bedeutungen wechseln")
    dict_output_window.config(state=NORMAL)
    dict_output_window.delete("1.0", END)
    dict_output_window.config(state=DISABLED)
    word_entry.delete(0, END)


if __name__ == '__main__':
    root = Tk()
    root.title("Welcome in English-German dictionary and translator!")
    root.geometry('944x620')
    Font_tuple = ("Arial", 10)
    root.resizable(0, 0)
    object_dictonary_res = MyDictionary()

    bg_file = PhotoImage(file="bg.png")
    bg_label = Label(root, image=bg_file)
    bg_label.place(x=0, y=0)

    translate_button = Button(root, text='Translate')
    translate_button.place(x=660, y=60, width=84, height=30)
    translate_button["command"] = lambda: translate_action()

    to_translate_window = Text(root, wrap=WORD)
    to_translate_window.place(x=40, y=60, width=279, height=159)
    to_translate_window.configure(font=Font_tuple)

    translated_window = Text(root, wrap=WORD)
    translated_window.place(x=340, y=60, width=279, height=159)
    translated_window.configure(font=Font_tuple)

    dict_info_label = Label(root, text="Switch between meanings")
    dict_info_label.config(anchor=CENTER)
    dict_info_label.place(x=201, y=550, width=185, height=30)

    eng_file = PhotoImage(file="england_flag.png")
    eng_img = eng_file.subsample(10, 9)
    left_flag = Label(root, image=eng_img)
    left_flag.place(x=260, y=20, width=52, height=35)

    germ_file = PhotoImage(file="german_flag.png")
    germ_img = germ_file.subsample(2, 8)
    right_flag = Label(root, image=germ_img)
    right_flag.place(x=520, y=20, width=52, height=35)

    swap_file = PhotoImage(file="swap_icon.png")
    swap_image = swap_file.subsample(5, 5)
    swap_translat_button = Button(root, text="swap", image=swap_image)
    swap_translat_button.place(x=660, y=110, width=40, height=40)
    swap_translat_button["command"] = lambda: swap_translation()

    explore_button = Button(root, text="Explore")
    explore_button.place(x=250, y=270, width=97, height=30)
    explore_button["command"] = lambda: prepare_dictionary_data()

    languages = ("English/Englisch", "German/Deutsch")
    language_codes_translator = {"English/Englisch": "en", "German/Deutsch": "de"}

    lang_var1 = StringVar()
    lang_var1.trace('w', on_left_lang_change)
    from_lang_combo = Combobox(root, text=lang_var1, state="readonly")
    from_lang_combo['values'] = languages
    from_lang_combo.place(x=40, y=30, width=130, height=30)

    lang_var2 = StringVar()
    lang_var2.trace('w', on_right_lang_change)
    to_lang_combo = Combobox(root, text=lang_var2, state="readonly")
    to_lang_combo['values'] = languages
    to_lang_combo.place(x=340, y=30, width=130, height=30)
    from_lang_combo.current(0)
    to_lang_combo.current(1)

    dict_output_window = Text(root, wrap=WORD)
    dict_output_window.place(x=400, y=360, width=279, height=182)
    dict_output_window.configure(font=Font_tuple)

    radio_var = StringVar()
    r1 = Radiobutton(root, text='Definitions', variable=radio_var, value='def', command=show_selected_results)
    r1.place(x=40, y=400, width=145, height=25)
    r2 = Radiobutton(root, text='Examples of usage', variable=radio_var, value='examp', command=show_selected_results)
    r2.place(x=40, y=450, width=145, height=25)
    r3 = Radiobutton(root, text='Synonyms', variable=radio_var, value='synon', command=show_selected_results)
    r3.place(x=40, y=500, width=145, height=25)

    phonetic_var = StringVar()
    word_entry = Entry(root)
    word_entry.place(x=40, y=270, width=179, height=30)
    phonetic_label = Label(root, textvariable=phonetic_var, relief=RAISED)

    speech_var = StringVar()
    speech_var.trace('w', on_speech_part_change)
    combo_part_of_speech = Combobox(root, text=speech_var, state="readonly")
    combo_part_of_speech.place(x=222, y=420, width=140, height=30)

    speaker_file = PhotoImage(file="speaker_icon.svg.png")
    speaker_image = speaker_file.subsample(35, 35)
    sound_button = Button(root, text="playSound", image=speaker_image)
    sound_button["command"] = lambda: sound()

    next_arrow_file = PhotoImage(file="arrow_next.png")
    next_arrow_image = next_arrow_file.subsample(15, 15)
    next_button = Button(root, image=next_arrow_image)
    next_button.place(x=293, y=503, width=48, height=41)
    next_button["command"] = lambda: next_meaning_view()

    prev_arrow_file = PhotoImage(file="arrow_prev.png")
    prev_arrow_image = prev_arrow_file.subsample(15, 15)
    prev_button = Button(root, image=prev_arrow_image)
    prev_button.place(x=243, y=503, width=48, height=41)
    prev_button["command"] = lambda: prev_meaning_view()

    dict_lang_var = StringVar()
    dict_lang_var.trace('w', on_language_change)
    dict_lang_combo = Combobox(root, text=dict_lang_var, state="readonly")
    languages_trans = ("English", "Deutsch")
    dict_lang_combo['values'] = languages_trans
    dict_lang_combo.current(0)
    dict_lang_combo.place(x=598, y=310, width=86, height=30)

    root.mainloop()
