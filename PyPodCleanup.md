
<h1 align="center">
<br>
PyPodCleanup
</h1><br>
<br><br>

Counts the number of files inside each subfolder of your specified directory.  
If there are more files in a subfolder than the allowed number set when running the script, they are deleted, in order of creation date (oldest first).      
  
I use the container based service [Podgrab](https://github.com/akhilrex/podgrab) to automatically download new episodes.  
And my [PyPlayPodcast](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PyPlayPodcast.md) script to start playback by voice.    
   

<br>



<br><br>

- **1: Create the shell command.** <br>

Create the file 'shell_command.yaml' file in your /config dir and paste in the code below. 
_(dont forget to include it in `configuration.yaml` like `shell_command: !include shell_command.yaml`.)_ 
This will allow you to call the script easily later from for example an automation. <br>
Here we specify all the information that the python script needs to be run. <br>
Chose your folder where your podcasts lies, the maximum number of files, and the fileextension. <br>

- **2: Python script** <br>

This is where the magic happends. <br>
Within your /config dir, create a file called `pypodcleanup.py` <br>
Paste in the code from below. <br>
It has commented sections so you can more easy understand how it is being run.  


- **3: Example automation** <br>

This is an example of an automation to run the script each day.  
I would suggest that you edit or make your own after you specifc needs.  


<br>
Your all set, try it out!<br><br>


## **⚠️⚠️ __IMPORTANT__ ⚠️⚠️** <br>

This script is written for a folder structure like:
`/media/Podcasts/PodcastName/PodcastFiles.mp3`

    
<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  py_podcleanup: "python pypodcleanup.py '/media/Podcasts' 10 mp3"
```

<br><br>




## 🦆 /config/play_fuzzy_podcast.py <br>


<br>

```
import os
import sys
import glob
import time

def cleanup_subfolders(folder_path, max_files, file_extension):
    # Iterate through each subfolder in the specified folder
    for subdir, _, _ in os.walk(folder_path):
        # Filter files by extension
        files = glob.glob(os.path.join(subdir, f"*.{file_extension}"))
        
        # Check if the number of files exceeds the maximum allowed
        if len(files) > max_files:
            # Sort files by creation time (oldest first)
            files.sort(key=lambda x: os.path.getctime(x))
            
            # Calculate the number of files to delete
            files_to_delete_count = len(files) - max_files
            
            # Delete the oldest files
            for i in range(files_to_delete_count):
                os.remove(files[i])
                print(f"Deleted: {files[i]}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py folder_path max_files file_extension")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    max_files = int(sys.argv[2])
    file_extension = sys.argv[3]
    
    cleanup_subfolders(folder_path, max_files, file_extension)

```


<br><br>


## 🦆 /config/automation.yaml <br>


<br>

```

```

<br><br>
