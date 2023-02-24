import os
import json
import datetime
import streamlit as st
import tkinter as tk
from tkinter import filedialog

# Function to recursively list all mp3 and wav files in a directory and its subdirectories
def list_files(startpath):
    """
    This function uses os.walk to recursively find all mp3 and wav files in a given directory,
    including any subdirectories.
    """
    audio_files = []
    for root, dirs, files in os.walk(startpath):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.wav'):
                audio_files.append(os.path.join(root, file))
        # Append all subdirectories to the dirs list so that they are also searched
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            audio_files += list_files(subfolder_path)
    return audio_files

def Youglish():
    st.components.v1.html(
        """
        <a id="yg-widget-0" class="youglish-widget" data-query=" " data-lang="english" data-zones="all,us,uk,aus" data-components="8415" data-bkg-color="theme_light"  rel="nofollow" href="https://youglish.com">Visit YouGlish.com</a>
        <script async src="https://youglish.com/public/emb/widget.js" charset="utf-8"></script>
        """,
        height=600,
    )


def main():
    st.set_page_config(page_title="Language Leaning")
    # Set up tkinter
    root = tk.Tk()
    root.withdraw()

    # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)

    # Folder picker button
    st.title('Enjoy Learning')
    st.write('Please select an audio folder:')
    if 'folder_path' not in st.session_state:
        st.session_state.folder_path = None
    clicked = st.button('Folder Picker')
    if clicked:
        #folder_path = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
        folder_path= filedialog.askdirectory(master=root)

        # Check if folder path is valid
        if not os.path.isdir(folder_path):
            st.warning("Please enter a valid folder path")
        else:
            # Store the folder path in the session state
            st.session_state.folder_path = folder_path

    if st.session_state.folder_path:
        folder_path = st.session_state.folder_path
        # Display list of available audio files in the selected folder
        audio_files = list_files(folder_path)
        st.write(f"Found {len(audio_files)} audio files in {folder_path}")
        selected_file_index = st.session_state.get('selected_file_index', 0)
        selected_file = st.selectbox("Select an audio file", [os.path.relpath(f, start=folder_path) for f in audio_files], index=selected_file_index)

        # Display audio player for the selected file
        st.audio(os.path.join(folder_path, selected_file))

        # Buttons to play the previous and next file in the list
        with st.container():
            col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Previous"):
                selected_file_index = max(0, selected_file_index - 1)
                st.session_state.selected_file_index = selected_file_index
        with col2:
            if st.button("Next"):
                selected_file_index = min(len(audio_files) - 1, selected_file_index + 1)
                st.session_state.selected_file_index = selected_file_index

    # Text area for saving content to JSON
    st.sidebar.title("Note")
    text_input = st.sidebar.text_area("Say something")
    if st.sidebar.button("Save"):
        # Get current date/time as key for the JSON dictionary
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Load existing data from JSON file
        if os.path.exists("audio listening note.json"):
            with open("audio listening note.json", "r") as f:
                data = json.load(f)
        else:
            data = {}
        # Add new text to JSON dictionary using current date/time as key
        data[current_time] = text_input
        # Write updated data back to JSON file
        with open("audio listening note.json", "w") as f:
            json.dump(data, f)
        # Confirm to the user that the text has been saved
        st.sidebar.success("Text saved to JSON")
    Youglish()

if __name__ == "__main__":
    main()
