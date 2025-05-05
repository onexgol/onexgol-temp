#import tkinter
from tkinter import *
from tkinter import messagebox;
from tkinter import filedialog;
import tkinter.font as tkFont;

#root
root = Tk();
root.title("Nit - Free Text Editor");
root.geometry("500x500");
print("NIT - Free Text Editor");

#load image
try:
    imgpng = PhotoImage(file="nit.png");
    root.tk.call('wm', 'iconphoto', root._w, imgpng);
    print("Download nit.png...");
except Exception as e:
    print(f"Error setting icon: {e} /nit/nit.png not found");

#create menu
main_menu = Menu(root);
root.config(menu=main_menu);

#open file
def open_file():
    file_path = filedialog.askopenfilename(title='Choose file: ', filetypes=(("TD (*.cpp)", "*.cpp"), ("All Files", "*.*")));
    if (file_path):
        text_fild.delete("1.0", END);
        text_fild.insert("1.0", open(file_path, encoding="utf-8").read());

#save file
def save_file(event=None):
    file_path = filedialog.asksaveasfilename(filetypes=(("TD (*.cpp)", "*.cpp"), ("All Files", "*.*")));
    f = open(file_path, 'w', encoding='utf-8');
    text = text_fild.get('1.0', END);
    f.write(text);
    f.close();

#tab
def insert_tab(event):
    text_fild.insert(INSERT, "    ");
    return 'break';

#highlight
def highlight_syntax(event=None):

    #import re
    import re; 

    keyword_colors = {
        'int': 'white', 'float': 'white', 'double': 'white', 'char': 'white',
        'void': 'white', 'if': 'white', 'else': 'white', 'for': 'white',
        'while': 'white', 'return': 'white',
        'using': 'white', 'define': 'white', 'long long': 'white', 'long double': 'white',
        'string': 'cyan', 'll': 'cyan', 'ld': 'cyan', 'str': 'white', 'include': 'white', '#': 'white',
        '<<': 'red', '>>': 'red', 'cout': 'white', 'cin': 'white', 'signed': 'white', 'namespace': 'white',
        'std': 'white', '1': 'red', '2': 'red', '{': 'white', '}': 'white'
    };

    for tag in text_fild.tag_names():
        text_fild.tag_remove(tag, "1.0", END);

    content = text_fild.get("1.0", END);
    for keyword, color in keyword_colors.items():
        tag_name = f"{keyword}_keyword";
        text_fild.tag_configure(tag_name, foreground=color);

        pattern = r'\b' + keyword + r'\b';
        for match in re.finditer(pattern, content):
            start = "1.0 + %dc" % match.start();
            end = "1.0 + %dc" % match.end();
            text_fild.tag_add(tag_name, start, end);

#font size +
def increase_font_size(event=None):
    global font;
    font.config(size=font.actual(option="size") + 1);
    text_fild.config(font=font);
    highlight_syntax();

#font size -
def decrease_font_size(event=None):
    global font;
    font_size = font.actual(option="size");
    if font_size > 1:
       font.config(size=font_size - 1);
       text_fild.config(font=font);
       highlight_syntax();

#paired
def insert_paired(event, char):
    text_fild.insert(INSERT, event.char + char);
    text_fild.mark_set(INSERT, "insert-1c");
    return 'break';

#select all
def select_all(event=None):
    text_fild.tag_add(SEL, "1.0", END);
    text_fild.mark_set(INSERT, "1.0");
    text_fild.see(INSERT);
    return 'break';

#add insert to data
def add_to_data(event=None):
    text_fild.insert(INSERT, '\n');
    return 'break';

#file MENU
file_menu = Menu(main_menu, tearoff=0);
file_menu.add_command(label="Open", command=open_file);
file_menu.add_command(label="Save", command=save_file);
root.config(menu=main_menu);
main_menu.add_cascade(label='File', menu=file_menu);

#font MENU
font_menu = Menu(main_menu, tearoff=0);
font_menu.add_command(label="Zoom In", command=increase_font_size);
font_menu.add_command(label="Zoom Out", command=decrease_font_size);
main_menu.add_cascade(label="Font", menu=font_menu);

#Settings MENU
settings_menu = Menu(main_menu, tearoff=0);
settings_menu.add_command(label="General");
settings_menu.add_command(label="Set Color Theme");
settings_menu.add_command(label="Package Settings");
settings_menu.add_command(label="Auto Save");
settings_menu.add_command(label="About");
main_menu.add_cascade(label="Preferences", menu=settings_menu);

#font
font = tkFont.Font(family="Consolas", size=12);

#text field (MAIN)
text_fild = Text(root, 
                bg='blue', 
                fg='cyan',
                padx=10,
                pady=10,
                insertbackground='#00FFFF',
                selectbackground='#009999',
                width=30,
                font=font,
                undo=True
                );

#scroll
scroll = Scrollbar(root, command=text_fild.yview);
text_fild.config(yscrollcommand=scroll.set);

#bottom_bar
bottom_bar = Frame(root, bg="#009999", height=20);
status_text = Label(bottom_bar, text=f"Nit - Free Text Editor    https://github.com/onexgol/nit", bg="#009999", anchor="w");
status_text.pack(side=LEFT, padx=5);

#transform
root.grid_rowconfigure(0, weight=1);
root.grid_columnconfigure(0, weight=1);
root.grid_columnconfigure(1, weight=0);
text_fild.grid(row=0, column=0, sticky=NSEW);
scroll.grid(row=0, column=1, sticky=NS);
bottom_bar.grid(row=1, column=0, columnspan=2, sticky=EW);

#cntrl++, cntrl+-
text_fild.bind("<Control-plus>", increase_font_size);
text_fild.bind("<Control-minus>", decrease_font_size);
text_fild.bind("<Control-equal>", increase_font_size);

#cntrl+s
text_fild.bind("<Control-s>", save_file);

#keys
text_fild.bind("<Tab>", insert_tab);
text_fild.bind("<KeyRelease>", highlight_syntax);
text_fild.bind("(", lambda event: insert_paired(event, ")"));
text_fild.bind("[", lambda event: insert_paired(event, "]"));
text_fild.bind("{", lambda event: insert_paired(event, "}"));
text_fild.bind("'", lambda event: insert_paired(event, "'"));
text_fild.bind('"', lambda event: insert_paired(event, '"'));
text_fild.bind("<Control-a>", select_all);

#KP - enter (numpad)
text_fild.bind("<KP_Enter>", add_to_data);

#command line (bananuci monkey monkey uchi(.ru))
command = "";

while (command != "--close-terminal-but-not-nit"):
    print("@nit ", end='');
    command = input();
    if (command == "--version"):
        f = open("version.txt", "r");
        print(*f); #output NIT version
    if (command == "stop" or command == "exit"):
        print("OK:)))))");
        try:
            root.destroy();
        except Exception as e:
            print("Error");
        break;

#run
root.mainloop();













# JFJSDFSFSFSMSVMXKFGJDGFLKFDGHJKOPFLDSFJPF[KNJBJKDFL]
# https://github.com/onexgol/nit
# please, liked it :)

# Last Update: 4th May 2025 Sunday 16:34
# Made In Russia, Moscow