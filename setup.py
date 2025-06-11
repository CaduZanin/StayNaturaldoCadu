import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="recursos/imagens/icone.webp") ]
cx_Freeze.setup(
    name = "Stay Natural",
    options={
        "build_exe":{
            "packages":["pygame", "pyttsx3", "tkinter"],
            "include_files":["recursos"]
        }
    }, executables = executaveis
)
