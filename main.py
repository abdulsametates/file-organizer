import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Design and Theme Settings
ctk.set_appearance_mode("System")  # System theme compatibility (Light/Dark)
ctk.set_default_color_theme("blue")  # Modern blue accent

# File type to folder mappings
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "PDF and Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".js", ".html", ".css", ".cpp"],
    "Videos and Music": [".mp4", ".mkv", ".avi", ".mp3", ".wav"],
    "Installation Files": [".exe", ".msi", ".iso"]
}

class ModernFileOrganizer(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("File Organizer & Cleaner")
        self.geometry("460x520")
        self.resizable(False, False)

        self.selected_folder = ""

        # Main Container (Modern rounded card design)
        self.main_frame = ctk.CTkFrame(self, corner_radius=25)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="📁 File Organizer", 
            font=("SF Pro Display", 22, "bold")
        )
        self.title_label.pack(pady=(35, 20))

        # Folder Path Display (Pill-shaped input)
        self.path_entry = ctk.CTkEntry(
            self.main_frame, 
            width=360, 
            height=45, 
            placeholder_text="No folder selected...", 
            corner_radius=22,
            font=("Arial", 12)
        )
        self.path_entry.pack(pady=10)
        self.path_entry.configure(state="disabled") # Read-only

        # Select Folder Button
        self.select_btn = ctk.CTkButton(
            self.main_frame, 
            text="Select Folder", 
            width=240, 
            height=45, 
            corner_radius=22,
            font=("Arial", 13, "bold"),
            command=self.select_folder
        )
        self.select_btn.pack(pady=15)

        # Start Organization Button (Soft, eye-friendly muted green accent)
        self.start_btn = ctk.CTkButton(
            self.main_frame, 
            text="Organize Now", 
            width=240, 
            height=45, 
            corner_radius=22,
            font=("Arial", 13, "bold"),
            fg_color="#4A7C59",        # Tok, göz yormayan adaçayı/orman yeşili
            hover_color="#3A6347",     # Üzerine gelince biraz daha koyulaşan yumuşak geçiş
            command=self.organize_files
        )
        self.start_btn.pack(pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="Ready to clean and organize", 
            font=("Arial", 11),
            text_color="gray"
        )
        self.status_label.pack(pady=(15, 0))

    def select_folder(self):
        target_folder = filedialog.askdirectory(title="Select Folder to Organize")
        if target_folder:
            self.selected_folder = target_folder
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, self.selected_folder)
            self.path_entry.configure(state="disabled")
            self.status_label.configure(text=f"Selected: {os.path.basename(target_folder)}")

    def organize_files(self):
        if not self.selected_folder:
            messagebox.showwarning("Warning", "No folder selected.")
            return

        print(f"\n🧹 Selected Folder: {self.selected_folder}")
        print("Scanning, cleaning file names and organizing...\n")

        try:
            files = os.listdir(self.selected_folder)
            moved_count = 0

            for file in files:
                file_path = os.path.join(self.selected_folder, file)

                # Skip folders
                if os.path.isdir(file_path):
                    continue

                _, extension = os.path.splitext(file)
                extension = extension.lower()

                # Skip files without extensions
                if not extension:
                    continue

                # 1. Clean underscores and hyphens from file names
                clean_name = file.replace("_", " ").replace("-", " ")
                clean_name = " ".join(clean_name.split())

                # 2. Determine the category
                found = False
                target_subfolder = ""

                for folder_name, extensions in FILE_TYPES.items():
                    if extension in extensions:
                        target_subfolder = os.path.join(
                            self.selected_folder,
                            folder_name
                        )
                        found = True
                        break

                # Files that don't match any category
                if not found:
                    target_subfolder = os.path.join(
                        self.selected_folder,
                        "Other Files"
                    )

                # Create category folder if it doesn't exist
                if not os.path.exists(target_subfolder):
                    os.makedirs(target_subfolder)

                # 3. Prevent duplicate file names
                base, ext = os.path.splitext(clean_name)

                counter = 1
                new_name = clean_name

                target_file_path = os.path.join(
                    target_subfolder,
                    new_name
                )

                while os.path.exists(target_file_path):
                    new_name = f"{base} ({counter}){ext}"

                    target_file_path = os.path.join(
                        target_subfolder,
                        new_name
                    )

                    counter += 1

                # 4. Move file with cleaned name
                shutil.move(
                    file_path,
                    target_file_path
                )

                print(
                    f"📦 Moved and Cleaned: "
                    f"{file} ➡️ {new_name}"
                )

                moved_count += 1

            print(
                f"\n✨ Operation completed successfully!"
                f"\nTotal files organized: {moved_count}\n"
            )

            self.status_label.configure(text=f"Successfully organized {moved_count} files!")

            messagebox.showinfo(
                "Success",
                f"Operation completed successfully!\n\n"
                f"Total files organized: {moved_count}"
            )

        except Exception as error:
            print(f"❌ An error occurred: {error}")

            self.status_label.configure(text="An error occurred during organization.")

            messagebox.showerror(
                "Error",
                f"An error occurred:\n\n{error}"
            )


if __name__ == "__main__":
    print("--- File Organizer Started ---")
    app = ModernFileOrganizer()
    app.mainloop()
