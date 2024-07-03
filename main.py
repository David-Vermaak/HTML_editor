
HTML_Welcome_Text = """\
<h1>Welcome to the Live HTML Editor!</h1>
<p>This is a simple live HTML editor. You can modify the HTML and see the changes in real time.</p>
<p><strong>Try editing this text or adding new HTML elements to see the effects instantly.</strong></p>

<p><i>Happy coding!</i></p>

<h3>List of supported tags:</h3>

<table>
    <tr>
        <td>&lt;a&gt;</td>
        <td>Defines a hyperlink</td>
    </tr>
    <tr>
        <td>&lt;b&gt;</td>
        <td>Defines bold text</td>
    </tr>
    <tr>
        <td>&lt;br&gt;</td>
        <td>Inserts a single line break</td>
    </tr>
    <tr>
        <td>&lt;div&gt;</td>
        <td>Defines a division or section</td>
    </tr>
    <tr>
        <td>&lt;em&gt;</td>
        <td>Defines emphasized text</td>
    </tr>
    <tr>
        <td>&lt;h1&gt; to &lt;h6&gt;</td>
        <td>Defines HTML headings</td>
    </tr>
    <tr>
        <td>&lt;hr&gt;</td>
        <td>Defines a thematic change in the content</td>
    </tr>
    <tr>
        <td>&lt;i&gt;</td>
        <td>Defines italic text</td>
    </tr>
    <tr>
        <td>&lt;img&gt;</td>
        <td>Defines an image</td>
    </tr>
    <tr>
        <td>&lt;p&gt;</td>
        <td>Defines a paragraph</td>
    </tr>
    <tr>
        <td>&lt;span&gt;</td>
        <td>Defines a section in a document</td>
    </tr>
    <tr>
        <td>&lt;strong&gt;</td>
        <td>Defines important text</td>
    </tr>
    <tr>
        <td>&lt;table&gt;</td>
        <td>Defines a table</td>
    </tr>
    <tr>
        <td>&lt;td&gt;</td>
        <td>Defines a cell in a table</td>
    </tr>
    <tr>
        <td>&lt;th&gt;</td>
        <td>Defines a header cell in a table</td>
    </tr>
    <tr>
        <td>&lt;tr&gt;</td>
        <td>Defines a row in a table</td>
    </tr>
    <tr>
        <td>&lt;u&gt;</td>
        <td>Defines underlined text</td>
    </tr>
        <tr>
        <td>&lt;ol&gt;</td>
        <td>Defines an ordered list</td>
    </tr>
    <tr>
        <td>&lt;ul&gt;</td>
        <td>Defines an unordered list</td>
    </tr>
    <tr>
        <td>&lt;li&gt;</td>
        <td>Defines a list item</td>
    </tr>
</table>

<h5>For example here is an ordered list:</h5>

<ol>
    <li>Item 1</li>
    <li>Item 2</li>
</ol>

<br/>

<h5>And an unordered list:</h5>

<ul>
    <li>Item 1</li>
    <li>Item 2</li>
</ul>
"""


#GUI Imports
import tkinter as tk
from tkinter import ttk
import sv_ttk
from tkhtmlview import HTMLLabel


#copies the text to clipboard
def copy_to_clipboard(clip):
        root.clipboard_clear()
        root.clipboard_append(clip)
        root.update()



def live_html_editor(Frame, HTML):
    if HTML == HTML_Welcome_Text:
        clear_window()
    
    # Create a frame to hold the editor and preview
    editor_frame = ttk.Frame(Frame)
    editor_frame.pack(fill="both", expand=True)
   
    # Create PanedWindow to allow resizing
    paned_window = ttk.PanedWindow(editor_frame, orient="horizontal")
    paned_window.pack(fill="both", expand=True)
   
    # Create left frame for text input
    left_frame = ttk.Frame(paned_window)
    paned_window.add(left_frame, weight=1)
   
    # Create right frame for HTML preview
    right_frame = ttk.Frame(paned_window)
    paned_window.add(right_frame, weight=1)
   
    # Create text widget for HTML input
    html_input = tk.Text(left_frame, wrap="word", font=menu_font)
    html_input.pack(fill="both", expand=True, padx=10, pady=10)
    # Insert some default HTML
    html_input.insert('1.0', HTML)
   
    # Create scrollbar for HTML input
    input_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=html_input.yview)
    input_scrollbar.pack(side="right", fill="y")
    html_input.config(yscrollcommand=input_scrollbar.set)

    # Create HTML preview widget
    html_preview = HTMLLabel(right_frame, html=HTML)
    html_preview.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create scrollbar for HTML preview
    preview_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=html_preview.yview)
    preview_scrollbar.pack(side="right", fill="y")
    html_preview.config(yscrollcommand=preview_scrollbar.set)
    
    # Function to update preview
    def update_preview(event=None):
        html_content = html_input.get("1.0", "end-1c")
        html_preview.set_html(html_content)
        
    # Function to synchronize scrolling
    def sync_scroll_input(*args):
        html_preview.yview_moveto(html_input.yview()[0])

    def sync_scroll_preview(*args):
        html_input.yview_moveto(html_preview.yview()[0])

    def autocomplete_tag(event):
        if event.char == '>':
            current_pos = html_input.index(tk.INSERT)
            line, col = map(int, current_pos.split('.'))
            line_content = html_input.get(f"{line}.0", f"{line}.{col}")
            
            # Find the last '<' before the current position
            last_open_bracket = line_content.rfind('<')
            if last_open_bracket != -1:
                tag = line_content[last_open_bracket+1:col].strip()
                
                # List of self-closing tags
                self_closing_tags = [
                    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                    'link', 'meta', 'param', 'source', 'track', 'wbr'
                ]
                
                if tag and not tag.startswith('/'):
                    if tag in self_closing_tags:
                        # For self-closing tags, just add the closing '>'
                        if not tag.endswith('/'):
                            html_input.insert(tk.INSERT, '/')
                        return None  # Allow the '>' to be inserted
                    elif not tag.endswith('/'):
                        # For normal tags, add the closing tag
                        closing_tag = f"></{tag}>"
                        html_input.insert(tk.INSERT, closing_tag)
                        html_input.mark_set(tk.INSERT, f"{line}.{col+1}")
                        return "break"  # Prevents the default '>' from being inserted
        
        update_preview()
        return None  # Allows the default '>' to be inserted if not autocompleted

    # Bind the autocomplete function to '>' key press
    html_input.bind('<Key-greater>', autocomplete_tag)

    # Bind the update function to key release event
    html_input.bind("<KeyRelease>", update_preview)
    
    # Bind scrolling events
    html_input.config(yscrollcommand=lambda *args: [input_scrollbar.set(*args), sync_scroll_input(*args)])
    html_preview.config(yscrollcommand=lambda *args: [preview_scrollbar.set(*args), sync_scroll_preview(*args)])
    
    # Initial update
    update_preview()

    # Function to set initial sash position and adjust on window resize
    def set_sash_position(event=None):
        width = paned_window.winfo_width()
        if width > 1:  # Ensure the width is valid
            paned_window.sashpos(0, width // 2)

    # Set initial position of the separator after a short delay
    paned_window.after(100, set_sash_position)
    
    # Bind the resize function to the paned_window
    paned_window.bind("<Configure>", set_sash_position)

    # Function to clear HTML content
    def clear_html():
        html_input.delete('1.0', tk.END)
        update_preview()

    def copy_HTML():
        HTML_contents = html_input.get("1.0", "end-1c")
        copy_to_clipboard(HTML_contents)

    button_frame = ttk.Frame(left_frame)
    button_frame.pack(pady=10)

    copy_button = ttk.Button(button_frame, text="Copy", style="Accent.TButton", command=copy_HTML)
    copy_button.pack(side="left", padx=5)

    clear_button = ttk.Button(button_frame, text="Clear", command=clear_html)
    clear_button.pack(side="left", padx=5)



#information textbox
def info():

    clear_window()

    title = "Program Information"
    info_text = """
        Welcome to the Live HTML Editor
        How to Use:

        Start typing HTML

    """
    
    # Title Label
    textbox_label = ttk.Label(content_frame, text=title)
    textbox_label.pack(pady=15)
    
    frame = ttk.Frame(content_frame)
    frame.pack(fill="both", expand=False)
    
    text_area = tk.Text(frame, wrap="none", font=menu_font)
    text_area.pack(padx=15, pady=15, fill="both", expand=True)
    
    # Inserting Text which is read only
    text_area.insert(tk.INSERT, info_text)


def clear_window():
    # Destroy everything except Menu, content frame, and boolian values
    for widget in content_frame.winfo_children():
        if widget != Menu_button and widget != Info_button and widget != Exit_button and widget != content_frame:
            widget.destroy()


#stops program
def exit_program():
    root.destroy()




#Main program config:

root = tk.Tk()

#window header title
root.title("Live HTML Editor")



#setting tkinter window size (fullscreen windowed)
root.state('zoomed')

# Set the minimum width and height for the window
root.minsize(900, 400)


menu_font = ("Arial", 14)

# Create a style for the Menu button
menu_button_style = ttk.Style()
menu_button_style.configure("Menu.TButton", font=menu_font, foreground='white', background='#2589bd')

# Create a style for the Info button
info_button_style = ttk.Style()
info_button_style.configure("Toggle.TButton", font=menu_font, foreground='white', background='#5C946E')

# Create a style for the Exit button
exit_button_style = ttk.Style()
exit_button_style.configure("Toggle.TButton", font=menu_font, foreground='white', background='#B3001B')


# Create a content frame for the main content area
content_frame = ttk.Frame(root)
content_frame.place(x=175, y=5, relwidth=.8, relheight=.95)  # Use relative dimensions for expansion


# Add Main Menu button at the top left of the window
Menu_button = ttk.Button(root, text="Menu", command=lambda: live_html_editor(content_frame, HTML_Welcome_Text), style="Accent.TButton")
Menu_button.place(x=15, y=12)

# Add an Info button
Info_button = ttk.Button(root, text="Info", command=info, style="Info.TButton")
Info_button.place(x=15, y=66)  # Position below Menu_button


# Add an Exit button
Exit_button = ttk.Button(root, text="Exit", command=exit_program, style="Exit.TButton")
Exit_button.place(x=15, y=120)  # Position below Info_button


# Add a darkmode toggle switch
switch = ttk.Checkbutton(text="Light mode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
switch.place(x=15, y=260)  # Position below toggle switch



# Bind the window close event to the exit_program function
root.protocol("WM_DELETE_WINDOW", exit_program)



import ctypes as ct
#dark titlebar - ONLY WORKS IN WINDOWS 11!!
def dark_title_bar(window):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


dark_title_bar(root)

#trying to get the taskbar icon to work
myappid = 'HTML.Display.V2' # arbitrary string
ct.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


# Theme
sv_ttk.set_theme("dark")

# Initial function
live_html_editor(content_frame, HTML_Welcome_Text)


#this is the loop that keeps the window persistent 
root.mainloop()
