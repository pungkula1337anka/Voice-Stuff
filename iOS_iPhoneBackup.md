
<h1 align="center">
<br>

__iPhone Backup to 🦆duckCloud☁️__

</h1><br>
<br><br>

This is an iOS Shortcut that backups your iPhone and stores the data on your personal cloud. <br> 
The backup includes:

- 🦆☁️  Photos <br>

- 🦆☁️  Videos <br>

- 🦆☁️  Contact vCard <br>

- 🦆☁️  Contact Photo <br>

- 🦆☁️  Notes <br>

- 🦆☁️  Documents <br>

- 🦆☁️  Shortcuts <br> 
 
<br>


__This is not a copy paste project__ <br>

<br>
Additional configurations has to be made. <br>

I'll post the code and try to break it down as simple as possible so you can edit for your needs.

You'll have to edit the shortcut to define your NAS IP and authentication.  

Also since Apple wont let you do advanced scripting inside the Shortcut app, to be able to auto save files from automations ti external storage like we do here, you'll have to download probably one of the most powerfull apps on the App Store, called [Scriptable](https://scriptable.app/)
Dont worry, its free and i'll guide you through the process.    
<br><br>

Dont be scared by the number of Shortcuts this requires. <br>
I just found its more simple to edit when the backup process is split into diffrent pieces. 
Its also the preffered way to be able to know when the screen can be locked again.
When the backup process of your Videos has begun, its possible to lcok your iPhone again without any issues.
The Shortcuts has Text to Speech actions, which will let you know how the backup is progressing.

The Video backup is often the largest one in size and thus requires the most time, thats why its the last one so you can lock your screen as soon as possible.
If you do regular backups and have an automation to delete Photos & videos from your phone this process should be fairly short and you can still actually view all your content even if theyre not stored on your phone, with the built in Files app.<br>

[🦆☁️ Part 1 - Base]() _(iCloud link)_ <br>  

[🦆☁️ Part 2 - ]() _(iCloud link)_ <br>  

[🦆☁️ Part 3 - ]() _(iCloud link)_ <br>  

[🦆☁️ Part 4 - ]() _(iCloud link)_ <br>  

[🦆☁️ Part 5 - ]() _(iCloud link)_ <br>  

[🦆☁️ Part 6 - ]() _(iCloud link)_ <br>  


<br><br>

- **1: Download Scriptable from App Store** <br>

Download `Scriptable` from the App Store.

- **2: Create a new script** <br>

Open the SCriptable app and create a new script.  _(try finding a + icon)_  
Name your script `Auto Save` and paste in the code below and save it.

```
/*-------------General Note-------------*
*This script written with Scriptable and it is intended to be used with Siri Shortcuts.
*To run this script you will need to downlaod Scriptable & Siri Shortcuts on you iOS
*To be Able to use this script, please follow instruction in the README


*Follow Exmple below on how the text should be Written
*local and cloud should be in small letters following by :
*Folder Path are case senstive
*Folder Path Should start with / and end with /
*Exmaple 1 local:/Photos/Events/
*Exmaple 2 cloud:/Photos/Events/
*/
const inputText = args.plainTexts

//Get Input File from Shortcuts app
const inputFile = args.fileURLs

//variables values created from Bookmark
//the Values should be same as written in the Scriptable bookmark
const local = "Local Drive"
const cloud = "iCloud Drive"

//Check if the Input received from Shortcuts exist or not
if (inputFile != "" && inputText !=""){
               
        const split = inputText[0].split(':');
               
        const storageType = split[0];
               
    const folderURL = split[1];

        if (storageType == 'local'){
                const fm = FileManager.local()
                const bm = fm.bookmarkedPath(local);
                saveFile(fm, bm, folderURL, inputFile)
               
        } else if (storageType == 'cloud'){
                const fm = FileManager.iCloud()
                const bm = fm.bookmarkedPath(cloud)
                saveFile(fm, bm, folderURL, inputFile)
        } else {
               
                Script.setShortcutOutput("Invalid input")
        }

} else {
       
        Script.setShortcutOutput("no valid File or Text")
}


//*-------------Save FIle to the Specified Folder-------------*

function saveFile(filemanager, bookmark, folder, files){
   
    //Create folder if not exisit
        filemanager.createDirectory(bookmark + folder, true);
        //Getting the Name of the file which received from Shortcuts input
        const filename = files[0].substring(files[0].lastIndexOf('/')+1);
        //Create Address of the file to be saved
        const path = bookmark + folder + filename;
        //Converting to file URL to data so that file manager can read it
        const content = Data.fromFile(files[0])
       
        try {
                // Saving the file
                filemanager.write(path, content)
                Script.setShortcutOutput("Saved")
               
        } catch(err) {
               
                Script.setShortcutOutput("Error: Could not save")
               
        }
}

//*-------------End of the Script-------------*
Script.complete();
```

- **3: Add file bookmarks** <br>

Still in the Scriptable app, in the top left corner there is an setting icon, click that.  
In the settings browse to File bookmarks. and add an Folder Bookmark.  
It will take you to the File Manager app, and when your in there, double tap the Browse icon in the bottom right, where you will find all your cloud storage and external host storage. (If you dont see your NAS, add its SMB share).
Chose your folder path in your NAS and when prompted for a name, name it `local`.  
Add another folder bookmark, this time your icloud drive, and name it `cloud`.  
And that should be it!  

- **4: Download the Shortcuts** <br>

Download all the 🦆☁️ Shortcuts. _(Links at top)_

Configurations has to be made.  
Make sure that the `Run Auto Save` part of the Shortcut is correct, the `text` value should be `local:/TheDirectoryYouChose/`
Chose your prefered directories for the photos, videos, contacts, notes and shortcuts on your NAS.  
I also strongly recommend editing the Shortcut for your preference, the Shortcut is not specifically made for sharing, its just a copy of mine, so possible modifications might be neccesary.  

<br><br><br>

Once you understand how this works, you will realize that its an incredible powerful tool for doing backups from iPhone to external storage. Only sad part is that the automations cannot be triggered from a locked screen..... not yet atleast.  
But as long as the connection has been made its cool to lock screen  
I send a actionable notification sent from within Home Assistant, when clicking the notification on your iPhone it prompts for lockscreen password and starts the backup process.
Below is a service call example to send the push notification. 
Its important that if you change the Shortcut name, you have to define it as such in the service call.  

```
service: notify.mobile_app_YOUR_iPHONE
      data:
        title: 🦆☁️
        message: Click me to start backup!
        data:
            shortcut:
                name: duckcloud
            push:
                sound:
                    name: default
                    critical: 1
                    volume: 1
            tag: shortcut
```

<br><br>


- **5: Some optional bonus stuff** <br>


<br>


![image](https://github.com/pungkula1337anka/Voice-Stuff/assets/105579081/8f43321c-a209-474e-8725-6a1251dbd627)



__Dashboard__ <br>


This backup moves my data to `NAS:\iPhone_Export\` where I manually process the data before moving it to `NAS:\Personal\`.
On the top left of the dashboard there are command line sensors, at the top the size of everything in `NAS:\Personal\` gets counted. <br>

```
  - sensor:
      name: duck_cloud_size
      command_timeout: 60
      scan_interval: 600
      command: 'du -sh /share/NAS/Personal'
```

Then we have a few sensors that counts all the files for each subdirectory of `NAS:\Personal\`. <br>

```
  - sensor:
      name: files_in_cloud_photos
      command: 'cd ''/share/NAS/Personal/Camera/'' && find . -type f | wc -l'
```

```
  - sensor:
      name: folders_in_cloud_projects
      command: 'cd ''/share/NAS/Personal/Projects/'' && find . -mindepth 1 -maxdepth 1 -type d | wc -l'
```

<br>
Then there a card that takes me to view the `NAS:\Personal` after prompt for a password.<br>
<br>
In the middle sechtion, to the left I count all the different files on my phone. <br>

This is done by automating a [Shortcut](http://#) that for example could be triggered when an alarm finishes.<br>

MIddle section right side I count the size of `NAS:\iPhone_export\` and also how many files in the subdirectories. <br>
Then there is a card to manually trigger the backup process.<br>
As you can see I have network mounted the NAS storage to the HA host in `\share`.



<br><br>

__🦆 Happy Cloudin'! ☁️__



<br><br>
