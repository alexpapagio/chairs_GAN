import os

def save_uploadedfile(upload_directory, uploaded_file):
    if uploaded_file is not None:
        # Construct the file path
        file_path = os.path.join(upload_directory, uploaded_file.name)

        # Write the file to the specified directory
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None
