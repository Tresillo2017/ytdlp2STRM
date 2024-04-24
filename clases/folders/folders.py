import os
import glob
import time
import platform
from clases.config import config as c

class folders:
    ytdlp2strm_config = c.config(
        './config/config.json'
    ).get_config()

    keep_downloaded = 86400
    temp_aria2_ffmpeg_files = 600
    if 'ytdlp2strm_temp_file_duration' in ytdlp2strm_config:
        keep_downloaded = int(ytdlp2strm_config['ytdlp2strm_temp_file_duration'])
    

    def make_clean_folder(self, folder_path, forceclean, config):
        # Verificar si el directorio existe
        if os.path.exists(folder_path):
            # Verificar si se debe realizar una limpieza forzada
            if forceclean or not config.get("ytdlp2strm_keep_old_strm", True):
                # Obtener la lista de archivos en el directorio
                file_list = glob.glob(os.path.join(folder_path, "*"))

                # Eliminar los archivos en el directorio
                for file_path in file_list:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")

                print(f"Cleaned direcotry: {folder_path}")
        else:
            # Crear el directorio y subdirectorios
            os.makedirs(folder_path, exist_ok=True)

            print(f"Created directory: {folder_path}")

    def write_file(self, file_path, content):
        # Escribir el contenido en el archivo
        try:
            with open(file_path, "w") as file:
                file.write(content.replace('\n',''))

            print(f"File created: {file_path}")
        except:
            pass
        
    def clean_waste(self, files_to_delete):
        """
        Elimina los ficheros especificados en la lista files_to_delete.

        :param files_to_delete: Lista de rutas completas de los ficheros a eliminar.
        """
        for file_path in files_to_delete:
            try:
                # Comprueba si el archivo existe antes de intentar eliminarlo
                if os.path.isfile(file_path):
                    os.remove(file_path)
                else:
                    continue
            except Exception as e:
                pass

    def clean_old_videos(self):
        def creation_date(path_to_file):
            """
            Try to get the date that a file was created, falling back to when it was
            last modified if that isn't possible.
            See http://stackoverflow.com/a/39501288/1709587 for explanation.
            """
            if platform.system() == 'Windows':
                return os.path.getctime(path_to_file)
            else:
                stat = os.stat(path_to_file)
                try:
                    return stat.st_birthtime
                except AttributeError:
                    # We're probably on Linux. No easy way to get creation dates here,
                    # so we'll settle for when its content was last modified.
                    return stat.st_mtime
        def modified_date(path_to_file):
            """
            Returns the time of last modification of a file.
            """
            stat = os.stat(path_to_file)
            return stat.st_mtime
        
        while True:
            try:
                time.sleep(5)  # Espera entre iteraciones para no sobrecargar el sistema
                path = os.getcwd()
                temp_path = os.path.join(path, 'temp')
                now = time.time()
                aria2_ffmpeg_files = ['.part', 'aria2', 'urls', '.temp', 'm4a', '.ytdl']

                for f in os.listdir(temp_path):
                    temp_file = os.path.join(temp_path, f)
                    if not f == "__init__.py":  # Ignora el archivo __init__.py
                        if any(keyword in f for keyword in aria2_ffmpeg_files):
                            if os.path.isfile(temp_file) and modified_date(temp_file) < now - self.temp_aria2_ffmpeg_files:
                                print("Enter keyword: \n files: {} \n creation_date : {} \n delete_time: {} ".format(temp_file, modified_date(temp_file), now - self.temp_aria2_ffmpeg_files))
                                os.remove(temp_file)
                        else:
                            if os.path.isfile(temp_file) and modified_date(temp_file) < now - self.keep_downloaded:
                                print("Enter older: \n files: {} \n creation_date : {} \n delete_time: {} ".format(temp_file, modified_date(temp_file), now - self.temp_aria2_ffmpeg_files))
                                os.remove(temp_file)
            except Exception as e:
                print(e)
                continue