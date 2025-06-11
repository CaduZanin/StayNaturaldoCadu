from cx_Freeze import setup, Executable

build_options = {
    "packages": ["pygame", "speech_recognition", "pyttsx3", "tkinter"],
    "include_files": ["recursos/"]  # Pasta com assets
}

setup(
    name="StayNatural",
    version="1.0",
    description="Jogo do Iron Man adaptado",
    options={"build_exe": build_options},
    executables=[Executable("main.py", base="Win32GUI")]  # Substitua "main.py" pelo nome do seu arquivo principal
)