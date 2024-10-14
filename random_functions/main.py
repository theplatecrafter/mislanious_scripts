# TODO: make everything complex number input supported
# TODO: finish stock market game

import json
import subprocess
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
import math
import random
import os
import glob
import pandas as pd
import numpy as np
import rawpy as r
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from moviepy.editor import ImageSequenceClip
import shutil
import xlsxwriter as xlsw
import webbrowser
import exifread
import piexif
import ffmpeg
from pymediainfo import MediaInfo
import tempfile
import platform


#### converter
def RAW2JPG(RAWfolderPATH:str,printDeets:bool=False,DetectingExtenstionName:list = [
"3fr",
"ari", "arw",
"bay",
"braw", "crw", "cr2", "cr3",
"cap",
"data", "dcs", "dcr", "dng",
"drf",
"eip", "erf",
"fff",
"gpr",
"iiq",
"k25", "kdc",
"mdc", "mef", "mos", "mrw",
"nef", "nrw",
"obm", "orf",
"pef", "ptx", "pxn",
"r3d", "raf", "raw", "rwl", "rw2", "rwz",
"sr2", "srf", "srw",
"tif",
"x3f"]):
    """Converts all .nef files in the inputted directory into jpg. This will create a new directory inside the inputted directory for the output. glob not supported"""
    files = [file for file in os.listdir(RAWfolderPATH) if os.path.splitext(file.lower())[1][1:] in DetectingExtenstionName]
    printIF(printDeets,f"Imported {len(files)} raw files from {RAWfolderPATH}")
    out = os.path.join(RAWfolderPATH,"RAWtoJPGconversionOUTPUT")
    os.mkdir(out)
    printIF(printDeets,f"Created output folder at {out}")
    n = 0
    for i in files:
        n += 1
        file_path = os.path.join(RAWfolderPATH,i)
        with r.imread(file_path) as raw:
            rgb_iamge = raw.postprocess()
            printIF(printDeets,f"Converted {i} to rgb array")
        img = Image.fromarray(rgb_iamge)
        printIF(printDeets,"Created new jpg image from rgb array")
        outIMGname = os.path.splitext(i)[1][1:]+os.path.splitext(i)[0]+".jpg"
        img.save(os.path.join(out,outIMGname),"JPEG")
        printIF(printDeets,f"saved {i} as {outIMGname} to {out} {n}/{len(files)}")


def Polar2Cart(r: float, theta: float, mode: str = "RAD") -> list:
    """converts polar coordinate <r,theta> to cartigean coordinate (x,y) as a list [x,y]. Optional Argument "mode" can either be "RAD" for if theta is in radians, or "DEG" if it is in degrees. Default is "RAD"."""
    if mode == "DEG":
        theta = math.radians(theta)
    return [r*math.cos(theta), r*math.sin(theta)]


def Cart2Polar(x: float, y: float, mode: str = "RAD") -> list:
    """converts cartigean coordinate (x,y) to polar coordinate <r,theta> as a list [r,theta]. Optional Argument "mode" can either be "RAD" for if you want theta to be in radians, or "DEG" for degrees. Default is "RAD"."""
    if mode == "DEG":
        if y >= 0:
            return [math.sqrt(pow(x, 2)+pow(y, 2)), math.degrees(math.acos(x/(math.sqrt(pow(x, 2)+pow(y, 2)))))]
        else:
            return [math.sqrt(pow(x, 2)+pow(y, 2)), math.degrees(2*math.pi-math.acos(x/(math.sqrt(pow(x, 2)+pow(y, 2)))))]
    else:
        if y >= 0:
            return [math.sqrt(pow(x, 2)+pow(y, 2)), math.acos(x/(math.sqrt(pow(x, 2)+pow(y, 2))))]
        else:
            return [math.sqrt(pow(x, 2)+pow(y, 2)), 2*math.pi-math.acos(x/(math.sqrt(pow(x, 2)+pow(y, 2))))]


def png2mp4(image_folder:str, output_folder:str,filename:str = "movie", fps=None):
    filename += ".mp4"
    image_files = sorted([os.path.join(image_folder, img)
                          for img in os.listdir(image_folder)
                          if img.endswith(".png")])
    
    if fps == None:
        fps = int(math.log(len(image_files)+1,1.3))

    clip = ImageSequenceClip(image_files, fps=fps)
    
    clip.write_videofile(os.path.join(output_folder,filename), codec="libx264")



#### polygons
def polygonDetails(points:list) -> dict:
    """gives details of the givin polygon drawn in order of the points list. points = [(x1,y1),(x2,y2),(x3,y3)...(xn,yn)]"""
    vertices = len(points)
    area = 0
    for i in range(vertices):
        x1, y1 = points[i]
        x2, y2 = points[(i+1)%vertices]
        area += x1*y2
        area -= x2*y1
    area = 0.5*abs(area)

    angles = []
    for i in range(vertices):
        x1, y1 = points[(i-1)%vertices]
        x2, y2 = points[i]
        x3, y3 = points[(i+1)%vertices]

        a = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
        b = math.sqrt(math.pow(x1-x3,2)+math.pow(y1-y3,2))
        c = math.sqrt(math.pow(x3-x2,2)+math.pow(y3-y2,2))
        angles.append(math.acos((math.pow(a,2)+math.pow(c,2)-math.pow(b,2))/(2*a*c)))

    return {
        "area":area,
        "vertices":vertices,
        "angles":angles,
        "anglesDEG":[i*180/math.pi for i in angles]
    }


def randomPolygon(sides:int,maxCord:tuple=(10,10),minCord:tuple=(-10,-10)) -> list:
    """returns a random polygon with points = [(x1,y1),(x2,y2),(x3,y3)...(xn,yn)]"""
    return [(randFloat(minCord[0],maxCord[0]),randFloat(minCord[1],maxCord[1])) for i in range(sides)]



#### programming tools
def randFloat(start:float,stop:float) -> float:
    """returns a random float between start and stop (both ends included)"""
    return random.random()*(stop-start)+start


def printIF(boolean:bool,printString:str):
    """prints printString if boolean == True"""
    if boolean:
        print(printString)


def rmSame(x: list) -> list:
    """removes any duplicated values"""
    y = []
    for i in x:
        if i not in y:
            y.append(i)
    return y


def rangePick(list: list, min: float, max: float = "inf") -> list:
    """returns numbers in list that are bigger than min (included), smaller than max (included). leave max blank for infinity"""
    output = []
    if max == "inf":
        for i in list:
            if i >= min:
                output.append(i)
    else:
        for i in list:
            if (i >= min) and (i <= max):
                output.append(i)
    return output


def printTable(table: list):
    try:
        print(table)
    except:
        print("array must be a 2 dimensional array")
        raise


def controledNumInput(type: str = "float", prompt: str = "Enter a number (blank to cancel)", rePrompt: bool = True, cancelAns:str = "",invalidTXT: str = "Invalid input") -> str:
    """"
    this only supports float and int controled input. When rePrompt is set to true, it will keep on prompting for the correct answer. invalidTXT is the text that appears when rePrompt is true, and the user inputed a wrong value. numMin <= <userinput> <= numMax This will return "" when rePrompt is False and the user inputs an invalid input.
    when the prompt was canceled, the function will give back None
    """
    if rePrompt:
        while True:
            user_input = input(prompt + ": ")
            if user_input == cancelAns:
                return None
            try:
                if type == "float":
                    user_input = float(user_input)
                    return user_input
                elif type == "int":
                    user_input = int(user_input)
                    return user_input
            except ValueError:
                print(invalidTXT)
    else:
        user_input = input(prompt)
        if user_input == cancelAns:
            return None
        try:
            if type == "float":
                user_input = float(user_input)
                return user_input
            elif type == "int":
                user_input = int(user_input)
                return user_input
        except ValueError:
            return ""


def controledStrInput(whiteList:list,blackList:list = None,prompt:str = "Enter string (blank to cancel)",UseWhiteList:bool = True,reprompt:bool = True,cancelAns:str = ""):
    """
    strings in whitelist are the only ones that can be entered. if the answer has one or more blacklisted characters of string, then that answer is not valid.
    if the prompt has been canceled, then the function gives back None
    """
    if reprompt:
        while True:
            ans = input(prompt + ": ")
            if ans == cancelAns:
                return None
            if UseWhiteList:
                if ans in whiteList:
                    return ans
            else:
                good = True
                for i in blackList:
                    if i in ans:
                        good = False
                        break
                if good:
                    return ans
    else:
        ans = input(prompt + ": ")
        if ans == cancelAns:
            return None
        if UseWhiteList:
            if ans in whiteList:
                return ans
        else:
            good = True
            for i in blackList:
                if i in ans:
                    good = False
                    break
            if good:
                return ans
        return ""


def ranList(length: int, min: float = 0, max: float = 1) -> list:
    """returns a list with length length, each element being a random value between min and max"""
    output = []
    for i in range(length):
        output.append(random.random()*(abs(max)+abs(min))-abs(min))
    return output


def choose_random_objects(array, num_objects):
    if num_objects > len(array):
        raise ValueError("Number of objects to choose cannot be greater than the array length")
    
    return random.sample(array, num_objects)


def count_elements(list:list):
    out = {}
    types = rmSame(list)
    for i in types:
        out[i] = 0
    
    for i in list:
        out[i] += 1
    return out
    


## text handlers
def list_to_string(lst:list, separator:str=None) -> str:
    """creates a string that has all the elements in lst, but seperated with separator. when sperator left blank, the program will automatically find an ascii charactor for seperation
    outputs combined string, and seperator
    """
    # Convert all elements in the list to strings
    if len(lst) == 1:
        return lst[0], separator
    lst = [str(item) for item in lst]
    
    # If no separator is given, find one that isn't used in the list
    if separator is None:
        all_chars = set(''.join(lst))
        available_separators = set(chr(i) for i in range(33, 127)) - all_chars  # ASCII printable characters
        if available_separators:
            separator = available_separators.pop()
        else:
            raise ValueError("No available separator character found.")

    # Join the list elements with the chosen or given separator
    return separator.join(lst),separator


def string_to_list(s:str, separator:str) -> list:
    """convertes a string to a list, wheras the string is seperated by an ascii charactor"""
    if not separator:
        raise ValueError("Separator must be a non-empty character.")
    
    return s.split(separator)


def list_to_file(lst:list, destination_path:str,file_name:str = "text.txt"):
    """creates a file (file extension can be changed) with each line being an element in lst"""
    with open(os.path.join(destination_path,file_name), 'w') as file:
        for item in lst:
            file.write(f"{item}\n")



#### image handlers
def compare_image(photoOne: str, photoTwo: str, downSamplePercentage: float = 1) -> float:
    A = Image.open(photoOne)
    A = A.resize((int(A.width * downSamplePercentage),
                 int(A.height * downSamplePercentage)))
    A = np.array(A).flatten().astype(np.float64)
    A -= A.mean()

    B = Image.open(photoTwo)
    B = B.resize((int(B.width * downSamplePercentage),
                 int(B.height * downSamplePercentage)))
    B = np.array(B).flatten().astype(np.float64)
    B -= B.mean()

    bottom = math.sqrt(np.dot(A, A))*math.sqrt(np.dot(B, B))
    similarity = np.dot(A, B)/(bottom)

    return similarity


def pick_images_cleverly(FilesToPickFrom: str, DestinationDir: str, fileType: str = ".jpg", downsamplePercent: float = 0.03, threshold: float = 0.78, printDeets: bool = False):
    n = 0
    k = 1
    key = None
    for folder in glob(FilesToPickFrom):
        for root, dirs, files in os.walk(folder):
            files.sort()
            files = [file for file in files if file.lower().endswith(fileType)]
            for i in range(len(files)-1):
                # Process each file
                if key == None:
                    key = os.path.join(root, files[i])
                    if not printDeets:
                        print(f"new keyframe at {key} (#{n})")
                    else:
                        print(f"created #{k} keyframe at image {key}")
                    copy_file(key, os.path.join(DestinationDir, files[i]))
                image = os.path.join(root, files[i+1])
                try:
                    n += 1
                    score = compare_image(key, image, downsamplePercent)
                except Exception as e:
                    if printDeets:
                        print(
                            f"unsuccesful compareing process  at #{n} when comparing:\n{key} and {image}\nErrorCode:\n{e}")
                    else:
                        print(e)
                    continue
                if score < threshold:
                    key = image
                    name = files[i+1]
                    tmp = 0
                    while check_file_existence(DestinationDir, name):
                        tmp += 1
                        name = f"({tmp})_{name}"
                    copy_file(key, os.path.join(DestinationDir, name))
                    if printDeets:
                        print(f"created #{k} keyframe at image {key} (#{n})")
                    else:
                        print(f"new keyframe at {key}")
                    k += 1
                else:
                    if printDeets:
                        print(f"skipped {image} (#{n}) Score: {score}")
                    else:
                        print(f"skipped {image}")

    print(f"processed: {n}    kept: {k/n*100} % ({k}/{n} files)")


def get_image_metadata(filepath):
    metadata = {}
    raw_tags = {}
    
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f)
            raw_tags['exifread'] = {str(k): str(v) for k, v in tags.items()}
            metadata['Date Taken'] = tags.get('EXIF DateTimeOriginal')
            metadata['Camera Make'] = tags.get('Image Make')
            metadata['Camera Model'] = tags.get('Image Model')
            metadata['Orientation'] = tags.get('Image Orientation')
            metadata['Width'] = tags.get('EXIF ExifImageWidth')
            metadata['Height'] = tags.get('EXIF ExifImageLength')
            
            # Check for GPS data
            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat = tags['GPS GPSLatitude'].values
                lon = tags['GPS GPSLongitude'].values
                lat_ref = tags.get('GPS GPSLatitudeRef')
                lon_ref = tags.get('GPS GPSLongitudeRef')
                
                lat = (float(lat[0].num) / lat[0].den +
                       float(lat[1].num) / lat[1].den / 60 +
                       float(lat[2].num) / lat[2].den / 3600)
                lon = (float(lon[0].num) / lon[0].den +
                       float(lon[1].num) / lon[1].den / 60 +
                       float(lon[2].num) / lon[2].den / 3600)
                
                if lat_ref.values == 'S':
                    lat = -lat
                if lon_ref.values == 'W':
                    lon = -lon
                
                metadata['GPS Latitude'] = lat
                metadata['GPS Longitude'] = lon
            
    except Exception as e:
        print(f"Error reading EXIF data with exifread: {e}")

    try:
        img = Image.open(filepath)
        exif_data = img._getexif()
        if exif_data:
            raw_tags['pillow'] = {piexif.TAGS[k]: str(v) for k, v in exif_data.items() if k in piexif.TAGS}
            exif_dict = piexif.load(img.info['exif'])
            metadata['Date Taken'] = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal, metadata.get('Date Taken'))
            metadata['Camera Make'] = exif_dict['0th'].get(piexif.ImageIFD.Make, metadata.get('Camera Make'))
            metadata['Camera Model'] = exif_dict['0th'].get(piexif.ImageIFD.Model, metadata.get('Camera Model'))
            metadata['Orientation'] = exif_dict['0th'].get(piexif.ImageIFD.Orientation, metadata.get('Orientation'))
            metadata['Width'] = exif_dict['Exif'].get(piexif.ExifIFD.PixelXDimension, metadata.get('Width'))
            metadata['Height'] = exif_dict['Exif'].get(piexif.ExifIFD.PixelYDimension, metadata.get('Height'))
            
            # Check for GPS data
            if piexif.GPSIFD.GPSLatitude in exif_dict['GPS'] and piexif.GPSIFD.GPSLongitude in exif_dict['GPS']:
                lat = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]
                lon = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]
                lat_ref = exif_dict['GPS'].get(piexif.GPSIFD.GPSLatitudeRef)
                lon_ref = exif_dict['GPS'].get(piexif.GPSIFD.GPSLongitudeRef)
                
                lat = float(lat[0][0]) / lat[0][1] + float(lat[1][0]) / lat[1][1] / 60 + float(lat[2][0]) / lat[2][1] / 3600
                lon = float(lon[0][0]) / lon[0][1] + float(lon[1][0]) / lon[1][1] / 60 + float(lon[2][0]) / lon[2][1] / 3600
                
                if lat_ref == b'S':
                    lat = -lat
                if lon_ref == b'W':
                    lon = -lon
                
                metadata['GPS Latitude'] = metadata.get('GPS Latitude', lat)
                metadata['GPS Longitude'] = metadata.get('GPS Longitude', lon)
            
    except Exception as e:
        print(f"Error reading EXIF data with Pillow and piexif: {e}")

    metadata['Raw Tags'] = raw_tags
    return {k: (v.decode('utf-8') if isinstance(v, bytes) else v) for k, v in metadata.items()}



#### video handlers
def get_video_metadata(filepath):
    metadata = {}
    raw_tags = {}
    
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return None

    file_extension = os.path.splitext(filepath)[1].lower()
    if get_file_type(filepath) == "image":
        print(f"Unsupported file type: {file_extension}")
        return None

    try:
        # Run ffprobe command
        command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', filepath]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        probe = json.loads(result.stdout)
        raw_tags['ffprobe'] = probe
        
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        if video_stream:
            metadata['Width'] = video_stream.get('width')
            metadata['Height'] = video_stream.get('height')
            metadata['Duration'] = float(video_stream.get('duration', 0))
            metadata['Codec'] = video_stream.get('codec_name')
            metadata['Frame Rate'] = video_stream.get('avg_frame_rate')
            metadata['Bit Rate'] = video_stream.get('bit_rate')
        
        if 'format' in probe:
            metadata['Format'] = probe['format'].get('format_name')
            metadata['File Size'] = int(probe['format'].get('size', 0))
            metadata['Date Taken'] = probe['format'].get('tags', {}).get('creation_time')
        
        # Check for GPS data
        if 'tags' in probe['format']:
            gps_latitude = probe['format']['tags'].get('location-lat')
            gps_longitude = probe['format']['tags'].get('location-lng')
            if gps_latitude and gps_longitude:
                metadata['GPS Latitude'] = float(gps_latitude)
                metadata['GPS Longitude'] = float(gps_longitude)
        
        # Check for additional metadata
        if 'tags' in probe['format']:
            metadata['Title'] = probe['format']['tags'].get('title')
            metadata['Artist'] = probe['format']['tags'].get('artist')
            metadata['Album'] = probe['format']['tags'].get('album')
            metadata['Year'] = probe['format']['tags'].get('date')
            metadata['Comment'] = probe['format']['tags'].get('comment')
        
        metadata['Raw Tags'] = raw_tags
        
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")
        print(f"ffprobe output: {e.stdout}")
        print(f"ffprobe error: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding ffprobe output: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error reading metadata from video file: {e}")
        return None

    return metadata


def convert_video_format(input_file: str, video_codec="libx264", audio_codec="aac"):
    """
    Converts the input_file video format.
    Video codec types:
    - libx264: H.264 / AVC
    - libx265: H.265 / HEVC
    - libvpx: VP8
    - libvpx-vp9: VP9
    - libaom-av1: AV1
    - mpeg4: MPEG-4 Part 2
    - libxvid: Xvid
    - mjpeg: Motion JPEG
    - libtheora: Theora
    
    Audio codec types:
    - aac: Advanced Audio Coding (AAC)
    - libmp3lame: MP3
    - libvorbis: Vorbis
    - libopus: Opus
    - pcm_s16le: 16-bit PCM (uncompressed)
    - flac: FLAC (lossless)
    - libtwolame: MP2
    - ac3: Dolby Digital (AC-3)
    - copy: Copy audio without re-encoding
    
    
    must have ffmpeg sudo apt installed:
    sudo apt install ffmpeg
    """
    # Create a temporary directory
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate a simple filename for FFmpeg
            temp_input = os.path.join(temp_dir, "temp_input.mp4")
            temp_output = os.path.join(temp_dir, "temp_output.mp4")
            
            # Copy original file to the temporary location
            shutil.copy2(input_file, temp_input)
            
            # Run FFmpeg on the temporary file
            stream = ffmpeg.input(temp_input)
            output_args = {}
            if video_codec:
                output_args['vcodec'] = video_codec
            if audio_codec:
                output_args['acodec'] = audio_codec

            # Output the converted file to another temporary location
            stream = ffmpeg.output(stream, temp_output, **output_args, map_metadata='0')
            stream = ffmpeg.overwrite_output(stream)
            ffmpeg.run(stream)
            
            # Move the converted file back to the original location, replacing the original
            shutil.move(temp_output, input_file)
            
            print(f"Conversion complete and original file updated: {input_file}")
            return True
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as ex:
        print(f"An unexpected error occurred: {str(ex)}")
        return False



#### os handlers
def copy_file(CopyThisFile: str, ToBecomeThisFile: str):
    src = CopyThisFile
    dst = ToBecomeThisFile
    if os.name == 'nt':  # Windows
        cmd = f'copy "{src}" "{dst}"'
    else:  # Unix/Linux
        cmd = f'cp "{src}" "{dst}"'
    os.system(cmd)


def copy_file_path_generative(from_here, to_here):
    """copies a file, but will make the neccessary directories to get it on the correct path"""
    try:
        os.makedirs(os.path.dirname(to_here), exist_ok=True)
    except:
        print(f"error creating folders {to_here}")
    try:
        shutil.copy2(from_here, to_here)
    except:
        print(f"error copying {to_here} from {from_here} possibly duplicate files")


def check_file_existence(directory, filename):
    file_path = os.path.join(directory, filename)
    return os.path.exists(file_path)


def slightly_change_names(dir: str, whatToAddInFrontOfName: str):
    for file in os.listdir(dir):
        os.rename(f"{dir}/{file}", f"{dir}/{whatToAddInFrontOfName}_{file}")


def copy_random_files(FileOriginDir: str, DestinationDir: str, whatToAddInFrontOfName: str, percentage: int = 0.5):
    for file in os.listdir(FileOriginDir):
        if random.random() <= percentage:
            src = f'{FileOriginDir}\{file}'
            dst = f'{DestinationDir}\{whatToAddInFrontOfName}_{file}'
            if os.name == 'nt':  # Windows
                cmd = f'copy "{src}" "{dst}"'
            else:  # Unix/Linux
                cmd = f'cp "{src}" "{dst}"'
            os.system(cmd)


def force_remove_all(directory_path):
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        except Exception as e:
            print(f"Failed to remove {item_path}: {e}")

    print(f"All files and directories in {directory_path} have been removed.")


def get_all_file_paths(pattern):
    file_paths = []
    
    # If the pattern is a directory, process it as before
    if os.path.isdir(pattern):
        for root, _, files in os.walk(pattern):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    else:
        # Use glob to handle patterns
        for path in glob.glob(pattern, recursive=True):
            if os.path.isfile(path):
                file_paths.append(path)
            elif os.path.isdir(path):
                # If a directory matches the pattern, walk through it
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_paths.append(file_path)
    
    return file_paths


def open_on_web(file_path):
    # Make sure the file path is absolute
    abs_path = os.path.abspath(file_path)
    webbrowser.open(abs_path)


def get_file_type(path):
    """
    returns:
    image, video, audio, document, archive, code, markdown, e-book, spreadsheet, presentation, database, configuration, log, script, font

    last updated:
    2024/7/21
    """


    file_extensions = {
        "image": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".heif", ".ico", ".svg"],
        "video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".3gp", ".rm", ".ts"],
        "audio": [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a", ".wma", ".alac", ".opus", ".aiff"],
        "document": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf", ".odt", ".csv"],
        "archive": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"],
        "code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".rb", ".php", ".swift", ".go", ".rs"],
        "markdown": [".md"],
        "e-book": [".epub", ".mobi", ".azw"],
        "spreadsheet": [".xls", ".xlsx", ".ods"],
        "presentation": [".ppt", ".pptx", ".key"],
        "database": [".sql", ".db", ".sqlite", ".mdb", ".accdb"],
        "configuration": [".json", ".yaml", ".yml", ".xml", ".ini", ".cfg"],
        "log": [".log"],
        "script": [".sh", ".bat", ".ps1"],
        "font": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    }

    _, ext = os.path.splitext(path.lower())

    for file_type, extensions in file_extensions.items():
        if ext in extensions:
            return file_type

    return "unknown"


def getRandomFiles(paths:list,type,count:int):
    """
    type variable must be:
    image, video, audio, document, archive, code, markdown, e-book, spreadsheet, presentation, database, configuration, log, script, font
    
    if None, it will pick from everything

    path is a list of paths to get stuff from
    """

    all_paths = []
    for path in paths:
        for i in get_all_file_paths(path):
            all_paths.append(i)
    
    
    if type:
      files = [file for file in all_paths if get_file_type(file) in type]
    else:
      files = all_paths
    return choose_random_objects(files,count)


def copy_multiple_files(file_paths, target_directory):
    # Ensure the target directory exists
    os.makedirs(target_directory, exist_ok=True)

    for file_path in file_paths:
        # Extract the file name and extension
        file_name = os.path.basename(file_path)
        file_name_without_ext, file_ext = os.path.splitext(file_name)
        
        # Determine the target file path
        target_file_path = os.path.join(target_directory, file_name)
        
        # Handle file name conflicts
        counter = 1
        while os.path.exists(target_file_path):
            new_file_name = f"{file_name_without_ext}_{counter}{file_ext}"
            target_file_path = os.path.join(target_directory, new_file_name)
            counter += 1
        
        # Copy the file to the target directory
        shutil.copy(file_path, target_file_path)
        print(f"Copied {file_path} to {target_file_path}")


def combinePATH(list:list):
    out = ""
    for i in list:
        out = os.path.join(out,i)
    return out


def checkStrValidicityOnPath(text:str):
    try:
        open(os.path.join(text+".txt"),"w")
        os.remove(os.path.join(text+".txt"))
        return True
    except:
        return False


def split_path(path: str,noFile:bool = False) -> list:
    # Normalize the path (to handle different slashes on different OS)
    normalized_path = os.path.normpath(path)
    
    # Split the normalized path into directories and file
    parts = []
    
    # Loop while there is still something to split
    while True:
        # Split the path into head (directory) and tail (last component)
        head, tail = os.path.split(normalized_path)
        
        # If there's no more head (root directory), break
        if tail:
            parts.insert(0, tail)  # Insert at the beginning to keep order
        if head == normalized_path:  # When head == normalized_path, it's root
            parts.insert(0, head)
            break
        normalized_path = head
    
    if noFile and "." in parts[-1]:
        parts.pop()
    
    return parts

def normalize_path(path: str) -> str:
    """
    Converts a file path with spaces or special characters into a format
    that can be recognized globally by programs without using quotes,
    by escaping special characters (especially on Linux).
    
    Args:
        path (str): The original file path.
    
    Returns:
        str: The normalized file path with escaped characters for Linux.
    """
    # Check the current operating system
    current_os = platform.system()

    if current_os == 'Windows':
        # On Windows, no need to escape anything, return as is
        return path
    else:
        # On Linux, escape spaces and other special characters
        special_chars = r' !"#$&\'()*,:;<=>?@[\\]^`{|}'
        
        escaped_path = ''
        for char in path:
            if char in special_chars:
                escaped_path += '\\' + char  # Escape the character with a backslash
            else:
                escaped_path += char

        return escaped_path




#### number theory
def checkPrime(n: int) -> bool:
    """Checks if n is a prime number or not"""

    if n <= 1:
        return False

    if n == 2 or n == 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    for i in range(5, int(math.sqrt(n))+1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False

    return True


def factorTree(n: int) -> list:
    """returns the factor tree in a list form (smallest to largest)"""
    tree = []
    while n > 1:
        for i in range(2, int(n)+1):
            if n % i == 0:
                tree.append(i)
                n /= i
                break
    return tree


def factors(n: int) -> list:
    """returns all factors of n in a list (smallest to largest)"""
    list = factorTree(n)
    list.insert(0, 1)
    factorD = []
    for i in list:
        for j in list:
            factorD.append(i*j)
    return rangePick(rmSame(factorD), 1, n)



#### mathmatics
def root(base: float, root: float) -> float:
    """takes the root of base"""
    return math.pow(base, 1/root)


def Qroots(a: float, b: float, c: float) -> list:
    """returns the roots of ax^2 + bx + c as a list. If there is only one root, returns it as a float. If the roots are imaginary, returns [[a,b],[c,d]] where as the first root is a + b*i, and the second is c + d*i"""
    if math.pow(b, 2) - 4*a*c > 0:
        return [(-1*b+math.sqrt(math.pow(b, 2) - 4*a*c))/(2*a), (-1*b-math.sqrt(math.pow(b, 2) - 4*a*c))/(2*a)]
    elif math.pow(b, 2) - 4*a*c == 0:
        return (-1*b+math.sqrt(math.pow(b, 2) - 4*a*c))/(2*a)
    else:
        return [[(-1*b)/(a*2), math.sqrt(abs(math.pow(b, 2) - 4*a*c))], [(-1*b)/(a*2), math.sqrt(abs(math.pow(b, 2) - 4*a*c))*-1]]


def rootsDK(poly: list, Iter: int = 100) -> list:
    """returns the roots of poly[0]*x^n + poly[1]*x^(n-1) + ... + poly[n-1]*x^1 + poly[n]*x^0 down to the imaginary numbers using the Durand-Kerner method. set the Iter to any natural value. The higher this value, the more accurate. Default value is 100. Return syntax: [root1:[(real part),(imaginary part)],root2:[(Re),(Im)], ... ,rootN[(Re),(Im)]]"""
    for i in range(1, len(poly)-1):
        poly[i] /= poly[0]
    poly[0] = 1

    points = []
    for i in range(len(poly)-1):
        points.append(Polar2Cart(root(abs(
            1/poly[len(poly)-1]), len(poly)-1), 2*math.pi/(len(poly)-1)*i+(math.pi/(2*(len(poly)-1)))))

    for g in range(Iter):
        for i in range(len(points)):
            deno = [1, 0]
            for j in range(len(points)):
                if j != i:
                    deno = CompMul(deno, CompSub(points[i], points[j]))
            points[i] = CompSub(points[i], CompDiv(
                CompPoly(points[i], poly), (deno)))
    return points


def poly(input: float, eq: list) -> float:
    """for a polynominal equation f(x) = eq[0]*x^n + eq[1]*x^(n-1) + ... + eq[n-1]*x^1 + eq[n]*x^0 returns f(input)"""
    s = []
    for i in range(len(eq)):
        s.append(eq[i]*math.pow(input, len(eq)-1-i))
    return sum(s)


def Dpoly(eq: list) -> list:
    """returns the first derivative of f(x) = eq[0]*x^n + eq[1]*x^(n-1) + ... + eq[n-1]*x^1 + eq[n]*x^0"""
    for i in range(len(eq)):
        eq[i] *= len(eq)-1-i
    eq.pop()
    return eq


def polyFPIter(input: float, eq: list, iter: int) -> float:
    """Returns the input calculated through eq using fixed point iteration, iter times"""
    for i in range(iter):
        input = poly(input, eq)
    return input


def CompPolyFPIter(input: list, eq: list, iter: int) -> list:
    """Returns the input calculated through eq using fixed point iteration, iter times. outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    for i in range(iter):
        input = CompPoly(input, eq)
    return input


def CompPoly(input: list, eq: list) -> list:
    """for a polynominal equation f(x) = eq[0]*x^n + eq[1]*x^(n-1) + ... + eq[n-1]*x^1 + eq[n]*x^0 returns f(input[0] + input[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    s = []
    for i in range(len(eq)):
        if type(eq[i]) == list:
            s.append(CompMul(eq[i], CompPow(input, len(eq)-1-i)))
        else:
            s.append(CompMul([eq[i], 0], CompPow(input, len(eq)-1-i)))
    return CompSum(s)


def CompAdd(A: list, B: list) -> list:
    """does (A[0] + A[1]*i) + (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    return [A[0] + B[0], A[1] + B[1]]


def CompSum(A: list) -> list:
    """returns the sum of all complex numbers [(real part),(imaginary part)] in 2D array A outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    RealP = []
    ImagP = []
    for i in A:
        RealP.append(i[0])
        ImagP.append(i[1])
    return [sum(RealP), sum(ImagP)]


def CompSub(A: list, B: list) -> list:
    """does (A[0] + A[1]*i) - (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    return [A[0] - B[0], A[1] - B[1]]


def CompMul(A: list, B: list) -> list:
    """does (A[0] + A[1]*i) * (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    return [A[0]*B[0]-A[1]*B[1], A[1]*B[0]+A[0]*B[1]]


def CompDiv(A: list, B: list) -> list:
    """does (A[0] + A[1]*i) / (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    BDash = math.pow(B[0], 2) + math.pow(B[1], 2)
    ADash = CompMul(A, [B[0], -1*B[1]])
    return [ADash[0]/BDash, ADash[1]/BDash]


def CompConj(A: list) -> list:
    """returns the conjugate of A[0] + A[1]*i outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    return [A[0], -1*A[1]]


def Re(A: list) -> float:
    """returns the real part of the complex number A[0] + A[1]*i"""
    return A[0]


def Im(A: list) -> float:
    """returns the imaginary part of the complex number A[0] + A[1]*i"""
    return A[1]


def CompPow(base: list, power: float):
    """returns the complex number base[0] + base[1]*i raised to the power of "power"(real number) as [(Real part),(imaginary part)]. All values must be float or int"""
    base = Cart2Polar(base[0], base[1])
    return Polar2Cart(math.pow(base[0], power), base[1]*power)


def polyPrint(eq: list) -> str:
    """returns a string that shows the polynominal equation in standard form"""
    output = ""
    for i in range(len(eq)):
        if type(eq[i]) != list:
            if i == 0:
                if eq[i] < 0:
                    if eq[i] == -1:
                        output += "-"
                    else:
                        output += str(eq[i])
                elif eq[i] > 0:
                    if eq[i] != 1:
                        output += str(eq[i])
            else:
                if eq[i] < 0:
                    if eq[i] == -1:
                        output += " - "
                    else:
                        if output == "":
                            output += str(eq[i])
                        else:
                            output += " - " + str(abs(eq[i]))
                elif eq[i] > 0:
                    if eq[i] == 1:
                        output += " + "
                    else:
                        if output == "":
                            output += str(eq[i])
                        else:
                            output += " + " + str(eq[i])
        else:
            if i == 0:
                output += "(" + compPrint(eq[i]) + ")"
            else:
                output += " + (" + compPrint(eq[i]) + ")"
        if eq[i] != 0:
            if len(eq)-1-i == 0:
                if eq[i] == 1 or eq[i] == -1:
                    output += "1"
            elif len(eq)-1-i == 1:
                output += "x"
            else:
                output += "x^" + str(len(eq)-1-i)
    return output


def compPrint(comp: list, precision: int = 2) -> str:
    """returns a string that shows the complex equation in standard form"""
    comp = [round(y, precision) for y in comp]
    if comp[0] == 0:
        if comp[1] == -1:
            return "-i"
        elif comp[1] == 1:
            return "i"
        elif comp[1] == 0:
            return str(comp[1])
        else:
            return str(comp[1]) + "i"
    else:
        if comp[1] < 0:
            if comp[1] == -1:
                return str(comp[0]) + "  - i"
            else:
                return str(comp[0]) + " - " + str(abs(comp[1])) + "i"
        elif comp[1] == 0:
            return str(comp[0])
        else:
            if comp[1] == 1:
                return str(comp[0]) + " + i"
            else:
                return str(comp[0]) + " + " + str(comp[1]) + "i"


def polyExpand(roots: list):
    """complex roots should be [(real part),(imaginary part)] and real numbers should be float"""
    poly = []
    for i in range(len(roots)):
        subMulti = []
        for j in range(math.factorial(len(roots))/math.factorial(len(roots)-(i+1))/math.factorial(i+1)):
            pass  # TODO


def calculateAreaOfTriangle(points:list):
    if len(points) != 3:
        raise ValueError("Input must be a list of three tuples representing the vertices of a triangle.")
    
    (x1, y1), (x2, y2), (x3, y3) = points[0],points[1],points[2]

    # Calculate the area using the determinant method
    area = 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
    return area



#### generators
def genRandomWord(length: int = 5, pronouncible: bool = True):
    if not pronouncible:
        word = ""
        for i in range(length):
            word += "qwertyuiopasdfghjklzxcvbnm"[random.randint(0,)]
    else:
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        word = ''
        
        for i in range(length):
            if i % 2 == 0:
                # Even positions: prefer consonants, but allow some vowels
                if random.random() < 0.8:
                    word += random.choice(consonants)
                else:
                    word += random.choice(vowels)
            else:
                # Odd positions: prefer vowels, but allow some consonants
                if random.random() < 0.8:
                    word += random.choice(vowels)
                else:
                    word += random.choice(consonants)
    
    return word


def print_styled(text, color_code, style_code="0",end="\n"):
    print(f"\033[{style_code};{color_code}m{text}\033[0m",end=end)


def createSimpleXLSX(collumNames:list,collumContent:list,output_folder:str,output_name:str="xls"):
    workbook = xlsw.Workbook(os.path.join(output_folder,output_name+".xlsx"))
    worksheet = workbook.add_worksheet()
    for i in range(len(collumNames)):
        worksheet.write(0,i,collumNames[i])
    for i in range(len(collumContent)):
        for j in range(len(collumContent[i])):
            worksheet.write(j+1,i,collumContent[i][j])
    
    workbook.close()


#### other
def startStockGame():
    print("\n\n\nStock Market Minigame")
    print("\nEnter at least 1 player names. leave blank to go to next")
    userinput = input("Player 1 name... ")
    players = []
    while userinput == "":
        userinput = input("Player 1 name... ")
    players.append(userinput)
    userinput = input("Player 2 name... ")
    n = 2
    while userinput != "":
        if userinput not in players:
            n += 1
            players.append(userinput)
        else:
            print("That player name already exist. Please enter another one.")
        userinput = input(f"Player {n} name... ")

    printTable([["Players"]+players])
    print("")
    userinput = input(
        "Would you like to add custom companies or randomly? [y/N]... ")
    if userinput != "":
        while not (userinput.lower() == "y" or userinput.lower() == "n"):
            userinput = input(
                "Would you like to add custom companies or randomly? [y/N]... ")
            if userinput == "":
                break

    sharesName = []
    sharesPrice = []
    sharesStrength = []
    if userinput.lower() == "y":
        print("\nEnter at least 1 company.")

        userinput = input("Company 1 name... ")
        while userinput == "":
            userinput = input("Company 1 name... ")
        sharesName.append(userinput)
        sharesPrice.append(controledNumInput(
            "float", f"  {sharesName[-1]} starting price... "))
        sharesStrength.append(controledNumInput(
            "float", f"  {sharesName[-1]} aggresiveness... "))
        n = 2
        print("")
        while True:
            userinput = input(f"Company {n} name... ")
            if userinput not in sharesName:
                n += 1
                if userinput == "":
                    break
                sharesName.append(userinput)
                sharesPrice.append(controledNumInput(
                    "float", f"  {sharesName[-1]} starting price... "))
                sharesStrength.append(controledNumInput(
                    "float", f"  {sharesName[-1]} aggresiveness... "))
                print("")
            else:
                print("That company name already exist. Please enter another one.")
    else:
        print("")
        userinput = int(controledNumInput(
            "int", "How many companies woudl you like... "))
        while not (userinput >= 1):
            userinput = int(controledNumInput(
                "int", "How many companies woudl you like... "))
        for i in range(userinput):
            sharesName.append()
            sharesPrice.append()
            sharesStrength.append()
        print("")

    printTable([["Companies"]+sharesName, ["Starting price"] +
               sharesPrice, ["aggresiveness"]+sharesStrength])

