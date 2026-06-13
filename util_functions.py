# util_functions.py
from collections.abc import Iterable
import random
import time
import os
import threading
import inspect
import socket
import uuid
import platform
import shutil
import queue
import sys
import select
import inspect
#credit for this function is wjandrea and juan Isaza from stack overflow here is the source: https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string?page=1&tab=scoredesc#tab-top:~:text=14%20more%20comments-,56,On,-python3%2C%20this%20function
def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]
# -------------------------
# Input / typing utilities
# -------------------------
def debug(*variables,title="None"):
    # 1. Get the caller's line number
    line = inspect.currentframe().f_back.f_lineno
    title if title else ""
    print(f"--- {title if title else f"DEBUG: as of line {line}"} ---")
    for x in variables:
        name = retrieve_name(x)
        v_type = type(x).__name__
        v_size = sys.getsizeof(x)
        v_id = id(x)
        v_dict = getattr(x, '__dict__','N/A')
        v_doc = str(getattr(x, '__doc__','N/A')).strip().split('\n')[0]
        v_methods = [m for m in dir(x) if not m.startswith('_')][:5]
        print(f"------ VARIABLE NAME: {name}")
        print(f"Value: {x} | Type: {v_type}")
        print(f"Size: {v_size} bytes | ID: {v_id}")
        print(f"Doc: {v_doc}")
        print(f"Dict: {v_dict}")
        print(f"Methods: {v_methods}")
        print("-" * 30)
import math
import csv

class csv_file:
    def __init__(self,path_to_csv):
        self.path_to_csv=path_to_csv
        self.sync()
    def sync(self):
        try:
            with open(self.path_to_csv,mode="r") as file:
                reader=csv.DictReader(file)
                self.headers=[]
                self.headers=reader.fieldnames
                self.rows=[]
                self.rows=list(reader)
        except FileNotFoundError:
            print(f"Error: {self.path_to_csv} dose not exist")
        except Exception as e:
            print(f"An error occurred: {e}")
    def __getitem__(self,index):
        return self.rows[index]
    
    def __str__(self):
        output=""
        for row in self.rows:
            line=",".join([f"{k}:{v}"for k,v in row.items()])
            output+=line+"\n"
        return output
    def return_list_of_dict(self):
        return self.rows
    def add(self,content):
        if len(content)!=len(self.headers):
            raise IndexError(f"len(content)({len(content)})!=len(hedder)({len(self.headers)})")
        try:
            with open(self.path_to_csv,mode="a",newline='\n') as file:
                writer=csv.writer(file)
                writer.writerow(content)
        except FileNotFoundError:
            print(f"Error: {self.path_to_csv} dose not exist")
        except Exception as e:
            print(f"An error occurred: {e}")
        self.sync()
    def __len__(self):
        return len(self.headers)
    def __delitem__(self,line):
        arow=[]
        with open(self.path_to_csv,"r") as source:
            arow=list(csv.reader(source))
        if 0<=line<len(self.rows):
            del arow[line+1]
            try:
                with open(self.path_to_csv,"w",newline='\n') as file:
                    writer=csv.writer(file)
                    writer.writerows(arow)
            except FileNotFoundError:
                print(f"Error: {self.path_to_csv} dose not exist")
            except Exception as e:
                print(f"An error occurred: {e}")
            self.sync()
    def to_dict(self):
        return self.rows
    def update_data(self,username,updated_row):
        for x,row in enumerate(self.rows):
            if row['username']==username:
                self.rows[x]=updated_row
                break
        with open(self.path_to_csv,mode="w",newline='\n') as file:
            writer=csv.DictWriter(file,fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.rows)
        self.sync()
def type_text(text,end="\n",typing=True,random_bounds=(0,.1)):
    """Print text optionally with a typing effect."""
    try:
        if not typing:
            print(text,end=end)
            return
        for ch in text:
            time.sleep(random.uniform(*random_bounds))
            print(ch,end="",flush=True)
        print("",end=end)
    except Exception as e:
        raise RuntimeError("error 003 occurred in type_text") from e

def clear_term():
    """Clear the terminal screen."""
    try:
        if os.name=='nt':
            os.system('cls')
        elif os.name=='posix':
            os.system('clear')
        else:
            print("\n" * 500)
    except Exception as e:
        raise RuntimeError("error 004 occurred in clear_term") from e
def debugger(func):
    def before_and_after():
        print(f"before func {func.__name__}")
        func()
        print(f"affter func{func.__name__}")
    return before_and_after
def menu(options,descriptions,prompt="Select an option: "):
    """
    Displays a menu of options,prompts the user for a selection,and executes
    the corresponding function.

    Parameters:
    - options (list of callables): A list of functions to execute for each menu item.
    - descriptions (list of str): A list of descriptions or labels for each option.
                                    Must be the same length as options.
    - prompt (str): The prompt message displayed to the user for input.

    Behavior:
    - Displays numbered options based on descriptions.
    - Includes an option '0' to quit the menu.
    - Validates user input to ensure it is an integer within the valid range.
    - Calls the selected function from options based on user choice.
    - Loops until the user chooses to quit (inputs 0).
    """
    while True:
        print("\nPlease choose an option:")
        for idx,desc in enumerate(descriptions):
            print(f"{idx + 1}. {desc}")
        print("0. Quit")
        choice=get_valid_type(int,prompt,valid=(0,len(options)))
        if choice==0:
            break
        else:
            options[choice - 1]()

def get_valid_type(type_return: type,prompt,invalid_prompt="Invalid input. Please try again.",valid=None,typing=False,end="",type_speed=False,random_bounds=(0,.1),min_max=None):
    """
    Prompt the user until they provide a value that can be converted to type_return
    and (optionally) is within valid constraints.
    - valid can be None,a tuple (min,max) or a list of allowed values.
    - If typing=True,the prompt is shown via type_text and input() is read on the next line.
    Returns the converted value.
    Raises ValueError on repeated invalid input if interrupted by KeyboardInterrupt.
    """
    try:
        while True:
            try:
                if typing:
                    type_text(prompt,end="",typing=True,random_bounds=random_bounds)
                    raw=input()
                else:
                    raw=input(prompt)
                to_return=type_return(raw)
            except KeyboardInterrupt:
                raise
            except Exception:
                # conversion failed
                if typing:
                    type_text(f"Invalid Input\n{invalid_prompt}{end}","\n",True,random_bounds)
                else:
                    print(f"Invalid Input\n{invalid_prompt}")
                continue
            # validate range or membership
            if valid is None:
                return to_return
            if isinstance(valid,tuple) and len(valid)==2:
                if valid[0] <=to_return <=valid[1]:
                    return to_return
                else:
                    if typing:
                        type_text(f"Invalid Amount\nInput must be between {valid[0]} and {valid[1]}{end}","\n",True,random_bounds)
                    else:
                        print(f"Invalid Amount\nInput must be between {valid[0]} and {valid[1]}")
                    continue
            if isinstance(valid,list):
                if to_return in valid:
                    return to_return
                else:
                    if typing:
                        type_text(f"Invalid Input\nInput must be one of: {valid}{end}","\n",True,random_bounds)
                    else:
                        print(f"Invalid Input\nInput must be one of: {valid}")
                    continue
            if min_max!=None:
                if min_max[0]!=None:
                    min(to_return,min_max[0])
                if min_max[1]!=None:
                    max(to_return,min_max[1])
            return to_return
    except Exception as e:
        raise RuntimeError("error 001 occurred in get_valid_type") from e


#def menu(*options,curser="⁍"):
#    while True:
#        if getch()=="w":
#            item-=1
# -------------------------
# Error helper
# -------------------------
def get_error_type(error_number):
    """Return a human-readable error string for a given error number."""
    errors=[
        None,
        "error 001 is error in get_valid_type function",
        "error 002 is error in get_error_type function",
        "error 003 is error in type_text function",
        "error 004 is error in clear_term function",
        "error 005 is error in alternate_random function",
        "error 006 is error in threads class __init__ function",
        "error 007 is error in threads class start function",
        "error 008 is error in threads class join function",
        "error 009 is error in threads class is_alive function",
        "error 010 is error in threads class repeat_function function",
        "error 011 is error in threads class repeat_function_until_stop function",
        "error 012 is error in threads class get_data function",
        "error 013 is error in threads class set_data function",
        "error 014 is error in factorial function",
        "error 015 is error in fibonacci function",
        "error 016 is error in is_prime function",
        "error 017 is error in get_ip_adress function",
        "error 018 is error in get_mac_address function",
        "error 019 is error in get_system_info function",
        "error 020 is error in read_file function",
        "error 021 is error in write_file function",
        "error 022 is error in append_file function",
        "error 023 is error in delete_file function",
        "error 024 is error in file_exists function",
        "error 025 is error in list_files function",
        "error 026 is error in create_directory function",
        "error 027 is error in delete_directory function",
        "error 028 is error in directory_exists function",
        "error 029 is error in get_file_size function",
        "error 030 is error in get_current_working_directory function",
        "error 031 is error in change_working_directory function",
        "error 032 is your fault whoever is sitting at the computer",
        "error 033 is error in join_paths function",
        "error 034 is error in split_path function",
        "error 035 is error in get_file_extension function",
        "error 036 is error in get_file_name function",
        "error 037 is error in copy_file function",
        "error 038 is error in move_file function",
        "error 039 is error in rename_file function",
    ]
    try:
        return errors[error_number]
    except Exception as e:
        raise RuntimeError("error 002 occurred in get_error_type") from e

# -------------------------
# Random / math / misc
# -------------------------
def alternate_random(bounds,type_of_random=int,seed=None):
    """
    Deterministic-ish alternate random using system values.
    bounds: (min,max) where max > min
    type_of_random: int or float
    """
    try:
        if not (isinstance(bounds,(tuple,list)) and len(bounds)==2):
            raise ValueError("bounds must be a tuple/list of length 2")
        a,b=bounds
        # build a seed from available system values
        nums=[]
        try:
            nums.append(os.getpid())
            nums.append(os.getppid())
        except Exception:
            nums.append(int(time.time()) & 0xFFFF)
            nums.append((int(time.time()) >> 8) & 0xFFFF)
        nums.append(os.cpu_count() or 1)
        try:
            size=os.path.getsize(__file__)
        except Exception:
            size=int(time.time() * 1000) & 0xFFFF
        nums.append(size)
        nums.append(int(time.time() * 1000) & 0xFFFFFFFF)
        if seed is None:
            seed_val=sum(nums)
        else:
            seed_val=seed + sum(nums)
        # simple mixing
        random_number=(seed_val * 1103515245 + 12345) & 0x7FFFFFFF
        # scale into range
        span=max(1,b - a)
        scaled=a + (random_number % span)
        if type_of_random==int:
            return int(scaled)
        return float(a + (random_number / 0x7FFFFFFF) * span)
    except Exception as e:
        raise RuntimeError("error 005 occurred in alternate_random") from e

def factorial(n):
    try:
        n=int(n)
        if n < 0:
            raise ValueError("n must be non-negative")
        if n in (0,1):
            return 1
        result=1
        for i in range(2,n + 1):
            result *=i
        return result
    except Exception as e:
        raise RuntimeError("error 014 occurred in factorial") from e

def fibonacci(n):
    try:
        n=int(n)
        if n <=0:
            return 0
        if n==1:
            return 1
        a,b=0,1
        for _ in range(2,n + 1):
            a,b=b,a + b
        return b
    except Exception as e:
        raise RuntimeError("error 015 occurred in fibonacci") from e

def is_prime(n):
    try:
        n=int(n)
        if n <=1:
            return False
        if n <=3:
            return True
        if n % 2==0:
            return False
        i=3
        while i * i <=n:
            if n % i==0:
                return False
            i +=2
        return True
    except Exception as e:
        raise RuntimeError("error 016 occurred in is_prime") from e

# -------------------------
# Networking / system info
# -------------------------
def get_ip_adress():
    try:
        hostname=socket.gethostname()
        return socket.gethostbyname(hostname)
    except Exception as e:
        raise RuntimeError("error 017 occurred in get_ip_adress") from e

def get_mac_address():
    try:
        mac=uuid.getnode()
        return ':'.join(("%012X" % mac)[i:i+2] for i in range(0,12,2))
    except Exception as e:
        raise RuntimeError("error 018 occurred in get_mac_address") from e

def get_system_info():
    try:
        return {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor()
        }
    except Exception as e:
        raise RuntimeError("error 019 occurred in get_system_info") from e

# -------------------------
# File / directory helpers
# -------------------------
def read_file(file_path):
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError("error 020 occurred in read_file") from e

def write_file(file_path,contents):
    try:
        with open(file_path,'w',encoding='utf-8') as f:
            f.write(contents)
    except Exception as e:
        raise RuntimeError("error 021 occurred in write_file") from e

def append_file(file_path,contents):
    try:
        with open(file_path,'a',encoding='utf-8') as f:
            f.write(contents)
    except Exception as e:
        raise RuntimeError("error 022 occurred in append_file") from e

def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        raise RuntimeError("error 023 occurred in delete_file") from e

def file_exists(file_path):
    try:
        return os.path.isfile(file_path)
    except Exception as e:
        raise RuntimeError("error 024 occurred in file_exists") from e

def list_files(directory):
    try:
        return os.listdir(directory)
    except Exception as e:
        raise RuntimeError("error 025 occurred in list_files") from e

def create_directory(directory):
    try:
        os.makedirs(directory,exist_ok=True)
    except Exception as e:
        raise RuntimeError("error 026 occurred in create_directory") from e

def delete_directory(directory):
    try:
        shutil.rmtree(directory)
    except Exception as e:
        raise RuntimeError("error 027 occurred in delete_directory") from e

def directory_exists(directory):
    try:
        return os.path.isdir(directory)
    except Exception as e:
        raise RuntimeError("error 028 occurred in directory_exists") from e

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        raise RuntimeError("error 029 occurred in get_file_size") from e

def get_current_working_directory():
    try:
        return os.getcwd()
    except Exception as e:
        raise RuntimeError("error 030 occurred in get_current_working_directory") from e

def change_working_directory(directory):
    try:
        os.chdir(directory)
    except Exception as e:
        raise RuntimeError("error 031 occurred in change_working_directory") from e

def join_paths(*paths):
    try:
        return os.path.join(*paths)
    except Exception as e:
        raise RuntimeError("error 033 occurred in join_paths") from e

def get_linenumber():
    try:
        return inspect.currentframe().f_back.f_lineno
    except Exception as e:
        raise RuntimeError("error 033 occurred in get_linenumber") from e

# -------------------------
# Thread helper class
# -------------------------
class threads:
    """Lightweight wrapper around threading.Thread with some helpers."""
    def __init__(self,target,args=()):
        try:
            self.thread=threading.Thread(target=target,args=args)
            self.thread.daemon=True
        except Exception as e:
            raise RuntimeError("error 006 occurred in threads.__init__") from e

    def start(self):
        try:
            self.thread.start()
        except Exception as e:
            raise RuntimeError("error 007 occurred in threads.start") from e

    def join(self,timeout=None):
        try:
            self.thread.join(timeout)
        except Exception as e:
            raise RuntimeError("error 008 occurred in threads.join") from e

    def is_alive(self):
        try:
            return self.thread.is_alive()
        except Exception as e:
            raise RuntimeError("error 009 occurred in threads.is_alive") from e

    @staticmethod
    def repeat_function(func,times,delay=0,args=()):
        try:
            for _ in range(times):
                func(*args)
                time.sleep(delay)
        except Exception as e:
            raise RuntimeError("error 010 occurred in threads.repeat_function") from e

    @staticmethod
    def repeat_function_until_stop(func,delay=0,args=()):
        try:
            while True:
                func(*args)
                time.sleep(delay)
        except Exception as e:
            raise RuntimeError("error 011 occurred in threads.repeat_function_until_stop") from e

    def get_data(self):
        try:
            return getattr(self.thread,"data",None)
        except Exception as e:
            raise RuntimeError("error 012 occurred in threads.get_data") from e

    def set_data(self,data):
        try:
            setattr(self.thread,"data",data)
        except Exception as e:
            raise RuntimeError("error 013 occurred in threads.set_data") from e

    def input_thread_setup(self):
        """Start a background input thread that collects stdin lines into a queue."""
        try:
            class InputThread(threading.Thread):
                def __init__(self):
                    super().__init__(daemon=True)
                    self.queue=queue.Queue()

                def run(self):
                    while True:
                        if select.select([sys.stdin],[],[],0.1)[0]:
                            user_input=sys.stdin.readline().rstrip("\n")
                            self.queue.put(user_input)

                def get_input(self):
                    items=[]
                    while not self.queue.empty():
                        items.append(self.queue.get())
                    return items

            self.input_thread=InputThread()
            self.input_thread.start()
            return self.input_thread
        except Exception as e:
            raise RuntimeError("error 013 occurred in threads.input_thread_setup") from e