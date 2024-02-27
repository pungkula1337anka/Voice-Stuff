
<h1 align="center">
<br>

Papercut

</h1><br>
<br><br>

This is an iOS Shortcut that opens the Camera app, you then scan a piece of paper/document with your camera. <br> 
Papercut then tags the document with relative tags found on the paper, renames the file and convert it into PDF and sends it to your NAS for storage.   
Siri will then read you the document out loud, and after she finishes, if any dates was found on the document, she will  ask you if the dates should be entered into your calendar. _Answer Ja/Nej_

You'll have to edit the shortcut to define your NAS IP and authentication.  

Also since Apple wont let you do advanced scripting inside the Shortcut app, to be able to auto save files from automations ti external storage like we do here, you'll have to download probably one of the most powerfull apps on the App Store, called `Scriptable`. 
Dont worry, its free and i'll guide you through the process.    
<br><br>

[Papercut iCloud download](https://www.icloud.com/shortcuts/6cfb96efb80a4cd7beffa65cdb76c66a)

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

- **4: to be on the safe side** <br>

Make sure that the `Run Auto Save` part of the Shortcut is correct, the `text` value should be `local:/TheDirectoryYouChose/`

<br><br><br>

Once you understand how this works, you will realize that its an incredible powerful tool for doing backups from iPhone to external storage. Only sad part is that the automations cannot be triggered from a locked screen..... not yet atleast.  
But as long as the connection has been made its cool to lockdown.
<br><br>
