
#?=== MODULES ===
#?=================================================
import os 
from libs.exiftool import ExifToolHelper
from datetime import datetime
import errno
from shutil import move,copy
from libs.colorama import init
from libs.colorama import Fore,Back,Style
from tkinter.filedialog import askdirectory
from time import sleep
from random import shuffle
#?=================================================


#?=================================================
#? Start of functions

def DateReNamer(source,filelist):
    flag=0 
    sumflag=0
    with ExifToolHelper() as et:
        for item in filelist:
            for d in et.get_tags(str(item), tags=["EXIF:DateTimeOriginal","File:FileTypeExtension"]): #! BE EXTRA CAREFUL with file ext...jpg,JPG and jpeg are diff
                #print(d)
                #et.set_tags([item],tags={"Keywords": str(item)})
                ext=d["File:FileTypeExtension"]
                try:
                    date=d["EXIF:DateTimeOriginal"]
                except:
                    item=item.split("/")
                    print(Style.BRIGHT+Fore.RED+"\nERROR"+Style.RESET_ALL+", its possible that"+Style.BRIGHT+Fore.CYAN+f"'{item[-1]}'"+Style.RESET_ALL+" doesnt have EXIF metadata or the creation date metadata\n")
                    break;  
                better_date=date.split(":")
                better_date='_'.join(better_date)        
            #//print(new_item)                          
                name=(f"{source}/{better_date}.{ext}")    
                try:
                    os.rename(item,name)
                    #print(f"{item} was renamed to {name} successfully :)")
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        flag+=1
                        name=(f"{source}/{better_date}_dup{flag}.{ext}")
                        os.rename(item,name)
                    else:
                        raise
                name=name.split("/")    
                print("photo is renamed to "+Fore.CYAN+name[-1]+Style.RESET_ALL+" successfully :)") 
                sumflag+=1
    print("\n/// Renaming complete, "+Fore.CYAN+f"{sumflag}"+Style.RESET_ALL+" photos renamed succesfully ///")      

def CustomRenamer1(source,filelist,uiMetadata,uiFlag):
    flag=0
    sumflag=0
    nameFlag=1       
    with ExifToolHelper() as et:
        for item in filelist:
            for d in et.get_tags(str(item), tags=[uiMetadata,"File:FileTypeExtension"]): #! BE EXTRA CAREFUL with file ext...jpg,JPG and jpeg are diff
                #et.set_tags([item],tags={"Keywords": str(item)})
                ext=d["File:FileTypeExtension"]
                try:
                    md=d[uiMetadata]
                except:
                    item=item.split("/")
                    print(Style.BRIGHT+Fore.RED+"\nERROR"+Style.RESET_ALL+", its possible that"+Style.BRIGHT+Fore.CYAN+f"'{item[-1]}'"+Style.RESET_ALL+" doesnt have EXIF metadata\nor the metadata you entered is wrong\n")
                    break;  
                md=str(md)
                better_md=md.split(" ")
                better_md=[item for item in better_md if item!=""]
                better_md='_'.join(better_md)
                
                if ":" in uiMetadata:
                        better_uiMetadata=uiMetadata.split(":")
                        better_uiMetadata=better_uiMetadata[-1]
                better_md= better_uiMetadata + "-" + better_md                
            #//print(new_item)                          
                name=(f"{source}/{better_md}_pic{nameFlag}.{ext}")
                try:
                    os.rename(item,name)
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        flag+=1
                        name=(f"{source}/{better_md}_dup{flag}.{ext}")
                        os.rename(item,name)
                    else:
                        raise
                better_name=name.split("/")
                print("photo is renamed to "+Fore.CYAN+better_name[-1]+Style.RESET_ALL+" successfully :)")    
                sumflag+=1
                nameFlag+=1
    print("\n/// Renaming complete, "+Fore.CYAN+f"{sumflag}"+Style.RESET_ALL+" photos renamed succesfully ///")           

def CustomRenamer2(source,filelist,uiName):
    sumflag=0
    flag=1

    for item in filelist:
     ext=item.split(".")
     #print(ext)
     ext=ext[-1]
     name=(f"{source}/{uiName}_{flag}.{ext}")   
     try:
        os.rename(item,name)
     except OSError as e:                
        if e.errno == errno.EEXIST:
                flag+=1
                name=(f"{source}/{uiName}_dup{flag}.{ext}")
                os.rename(item,name)
        else:
            raise
     name=name.split("/")      
     print("photo is renamed to "+Fore.CYAN+name[-1]+Style.RESET_ALL+" successfully :)")        
     flag+=1
     sumflag+=1
    print("\n/// Renaming complete, "+Fore.CYAN+f"{sumflag}"+Style.RESET_ALL+" photos renamed succesfully ///")

def RatingSorting(source,filelist):
    try:
        os.mkdir(f"{source}/5 stars images")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print('5 stars images folder already exists, no changes done')
    try:
        os.mkdir(f"{source}/4 stars images")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print('4 stars images folder already exists, no changes done')    
    try:
        os.mkdir(f"{source}/3 stars images")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print('3 stars images folder already exists, no changes done')    
    try:
        os.mkdir(f"{source}/2 stars images")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print('2 stars images folder already exists, no changes done')  
    try:
        os.mkdir(f"{source}/1 star images")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print('1 star images folder already exists, no changes done')
    try:
        os.mkdir(f"{source}/No stars images")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print('5 stars images folder already exists, no changes done')                                                                          
    sumflag=0
    with ExifToolHelper() as et:
        for item in filelist:
            for d in et.get_tags(str(item), tags=["XMP:Rating","Sourcefile"]): #or XMP:Rating 
                    try:
                        rating=d["XMP:Rating"]
                    except:
                        item=item.split("/")
                        print(Style.BRIGHT+Fore.RED+"\nERROR"+Style.RESET_ALL+", its possible that"+Style.BRIGHT+Fore.CYAN+f"'{item[-1]}'"+Style.RESET_ALL+" doesnt have EXIF metadata or the Rating metadata\n")
                        break;                  
                    
                    
                    name=d["SourceFile"]
                    name=name.split("/")
                    name=name[-1]
                    match str(rating):
                    #? 5 Stars
                        case "5":
                            imagepath=(f"{item}")
                            destination=(f"{source}/5 stars images/{name}")
                            move(imagepath,destination)
                            print(Fore.CYAN+name+Style.RESET_ALL,"moved to the 5 stars folder")
                    
                    #? 4 Stars
                        case "4":
                            imagepath=(f"{item}")
                            destination=(f"{source}/4 stars images/{name}")
                            move(imagepath,destination)
                            print(Fore.CYAN+name+Style.RESET_ALL,"moved to the 4 stars folder")

                    #? 3 Stars
                        case "3":
                            imagepath=(f"{item}")
                            destination=(f"{source}/3 stars images/{name}")
                            move(imagepath,destination)
                            print(Fore.CYAN+name+Style.RESET_ALL,"moved to the 3 stars folder")
                        
                    #? 2 Stars
                        case "2":
                            imagepath=(f"{item}")
                            destination=(f"{source}/2 stars images/{name}")
                            move(imagepath,destination)
                            print(Fore.CYAN+name+Style.RESET_ALL,"moved to the 2 stars folder")
                        
                    #? 1 Star
                        case "1":
                            imagepath=(f"{item}")
                            destination=(f"{source}/1 star images/{name}")
                            move(imagepath,destination)
                            print(Fore.CYAN+name+Style.RESET_ALL,"moved to the 1 stars folder")
                        
                    
                    #? No Stars
                        case "0":
                            imagepath=(f"{item}")
                            destination=(f"{source}/No stars images/{name}")
                            move(imagepath,destination)
                            print(Fore.CYAN+name+Style.RESET_ALL,"moved to the No stars folder")
                    sumflag+=1
    print("\n///Moving complete, "+Fore.CYAN+f"{sumflag}"+Style.RESET_ALL+" photos moved succesfully ///")

def DateSorting(source,filelist,ui):
   sumflag=0
   if ui == "1": 
    with ExifToolHelper() as et:
        
        for item in filelist:
            for d in et.get_tags(str(item), tags=["ModifyDate","SourceFile","FileTypeExtension"]): #! BE EXTRA CAREFUL with file ext...jpg,JPG and jpeg are diff
                try:
                    date=d["EXIF:ModifyDate"]
                except:
                    item=item.split("/")
                    print(Style.BRIGHT+Fore.RED+"\nERROR"+Style.RESET_ALL+", its possible that"+Style.BRIGHT+Fore.CYAN+f"'{item[-1]}'"+Style.RESET_ALL+" doesnt have EXIF metadata or the creation date metadata\n")
                    break;              
                
                #print(d)
                #et.set_tags([item],tags={"Keywords": str(item)})
                name=d["SourceFile"]
                name=name.split("/")
                name=name[-1]
                
                ext=d["File:FileTypeExtension"]
                date=date.split(":")
                better_date=(f"{date[0]}_{date[1]}")
           

                try: 
                    os.mkdir(f"{source}/{better_date}")
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        print(f'Folder "{better_date}" already exists, no changes done')    

                imagepath=(f"{item}")
                destination=(f"{source}/{better_date}/{name}")
                move(imagepath,destination)
                print(Fore.CYAN+name+Style.RESET_ALL,"moved succesfully to "+Fore.CYAN+f"{better_date}"+Style.RESET_ALL+" folder.")
                sumflag+=1
   else:
    with ExifToolHelper() as et:
        
        for item in filelist:
            for d in et.get_tags(str(item), tags=["ModifyDate","SourceFile","FileTypeExtension"]): #! BE EXTRA CAREFUL with file ext...jpg,JPG and jpeg are diff
                try:
                    date=d["EXIF:ModifyDate"]
                except:
                    item=item.split("/")
                    print(Style.BRIGHT+Fore.RED+"\nERROR"+Style.RESET_ALL+", its possible that"+Style.BRIGHT+Fore.CYAN+f"'{item[-1]}'"+Style.RESET_ALL+" doesnt have EXIF metadata or the creation date metadata\n")
                    break;
                #print(d)
                #et.set_tags([item],tags={"Keywords": str(item)})
                name=d["SourceFile"]
                name=name.split("/")
                name=name[-1]
                
                ext=d["File:FileTypeExtension"]
                date=date.split(":")
                day=date[2]
                better_date=(f"{date[0]}_{date[1]}_{day[:2]}")
                #? Instead of this way I can also put an if statement at the better date above so its checks the flag every time, I can try testing it 

                try: 
                    os.mkdir(f"{source}/{better_date}")
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        print(f'Folder "{better_date}" already exists, no changes done')    

                imagepath=(f"{item}")
                destination=(f"{source}/{better_date}/{name}")
                move(imagepath,destination)
                print(Fore.CYAN+name+Style.RESET_ALL,"moved succesfully to "+Fore.CYAN+f"{better_date}"+Style.RESET_ALL+" folder.")
                sumflag+=1                                     
   print("\n///Moving complete, "+Fore.CYAN+f"{sumflag}"+Style.RESET_ALL+" photos moved succesfully ///")

def customSorting1(source, filelist,uiMetadata):
    sumflag=0
    if ":" in uiMetadata:
        better_uiMetadata=uiMetadata.split(":")
        better_uiMetadata=better_uiMetadata[-1]
                
    with ExifToolHelper() as et:
        for item in filelist:
            for d in et.get_tags(str(item), tags=[uiMetadata,"FileTypeExtension"]): #! BE EXTRA CAREFUL with file ext...jpg,JPG and jpeg are diff
    
                #et.set_tags([item],tags={"Keywords": str(item)})
                ext=d["File:FileTypeExtension"]
                try:
                    md=d[uiMetadata]
                except:
                    item=item.split("/")
                    print(Style.BRIGHT+Fore.RED+"\nERROR"+Style.RESET_ALL+", its possible that"+Style.BRIGHT+Fore.CYAN+f"'{item[-1]}'"+Style.RESET_ALL+" doesnt have EXIF metadata\nor the metadata you entered is wrong\n")
                    break;  
                md=str(md)
                better_md=md.split(" ")
                better_md=[item for item in better_md if item!=""]
                better_md='_'.join(better_md)
                better_md= better_uiMetadata + "-" + better_md
                name=item.split("/")
                name=name[-1]
                name=name.split("\\")
                name=name[-1]
                try:
                    os.mkdir(f"{source}/{better_md}")
                except OSError as e:
                   if e.errno == errno.EEXIST:
                     print(f"{better_md} folder exists, no changes done")
                imagepath=(f"{item}")
                destination=(f"{source}/{better_md}/{name}")
                move(imagepath,destination)
                print(Fore.CYAN+name+Style.RESET_ALL,"moved succesfully to "+Fore.CYAN+f"{better_md}"+Style.RESET_ALL+" folder.")
                sumflag+=1
    print("\n///Moving complete, "+Fore.CYAN+f"{sumflag}"+Style.RESET_ALL+" photos moved succesfully ///")

def customsorting2(source,filelist,uiName):
    sumflag=0
    try:
        os.mkdir(f"{source}/{uiName}")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print(f"{uiName} folder exists, no changes done")
            
    
    for item in filelist:
        imagepath=(f"{item}")
        name=item.split("/")
        name=name[-1]
        name=name.split("\\")
        name=name[-1]
        destination=(f"{source}/{uiName}/{name}")
        move(imagepath,destination)
        print(Fore.CYAN+name+Style.RESET_ALL,"moved succesfully to "+Fore.CYAN+f"{uiName}"+Style.RESET_ALL+" folder.")
        sumflag+=1
    print("\n///Moving complete, "+Fore.CYAN+f"{sumflag}"+Style.RESET_ALL+" photos moved succesfully ///")

def Randphrase():
    listed_string=list(phrase)
    shuffle(listed_string)
    randphrase = ''.join(listed_string)
    return randphrase 

def userInput(listofAvailableitems):
    ui=input("--> ")
    ui=ui.lower()
    while ui not in listofAvailableitems:
        print(Fore.RED+Style.BRIGHT+"ERROR!"+Style.RESET_ALL+" Please select one of the above")
        ui=input("--> ")
    return ui 

#? End of functions
#?=================================================

#? Static Data
PopularExif={"1":"EXIF:DateTimeOriginal","2":"EXIF:ISO",
            "3":"MakerNotes:WhiteBalance","4":"EXIF:Model","5":"File:FileType"}
rawtypes=['nef', 'NEF', 'cr2', 'CR2']
masslist=["y","Y","n","N"]
ynlist=["y","Y","n","N"]
phrase="D3nt4!"
#?=== MAIN ===

print("=============================================\n")
print("    Photo organizing now in CLI form :)\n")
print("=============================================\n")
sleep(2)
print(Style.BRIGHT+Fore.BLUE+" _______   __    __  __    __  ________  ______")
sleep(0.2)  
print("/       \\ /  |  /  |/  \\  /  |/        |/      \\")
sleep(0.2) 
print("******   |** |  ** |**  \\ ** |********//******  |")
sleep(0.2)
print("** |  ** |** |__** |***  \\** |   ** |  ** ___**|")
sleep(0.2)
print("** |  ** |**    ** |****  ** |   ** |    /   **< ")
sleep(0.2)
print("** |  ** |******** |** ** ** |   ** |   _*****  |")
sleep(0.2)
print("** |__** |      ** |** |**** |   ** |  /  \\__** |")
sleep(0.2)
print("**    **/       ** |** | *** |   ** |  **    **/ ")
sleep(0.2)
print("*******/        **/ **/   **/    **/    ******/  "+Style.RESET_ALL)

print("\n\nWelcome to "+Style.BRIGHT+Fore.CYAN+"D4NT3"+Style.RESET_ALL+"\n\n(Dante), an organizer for photos (both processed and RAWs)\nthat uses EXIF metadata to do all sort of things like\nrenaming photos based on their date and time of creation,\nmoving photos on folders based on date,rating,white balance,filetype\nand many more you'll see later on :)\n\n")

print("Before starting please select the folder you would like to work with")


source = askdirectory()
flagdir=os.path.isdir(str(source))
while flagdir !=True: 
    print(Fore.RED+"ERROR"+Style.RESET_ALL+f", you either didnt select a directory or the directory doesnt exist")
    source = askdirectory()
    flagdir=os.path.isdir(str(source))

print("Would you like to do a"+Fore.RED+" M4SS "+Style.RESET_ALL+"organize?\n")
print(Fore.RED+"M4SS "+Style.RESET_ALL+"organizing is when the operation you choose will commence on every subfolder of the folder you entered.\nwithout it every subfolder inside will be ignored,but with it \nD4nt3 will do the operation to the contents of every subfolder too")
print("\nSo would you like to"+Fore.RED+" M4SS "+Style.RESET_ALL+"organize?\ny/n")

massui=userInput(masslist)
if massui == "y" or massui == "Y":
    massflag = True
else:
    massflag = False

print("\nWhat would you like to do today?")  

while True:
    print("\n-------|\n     1.| Rename photos\n     2.| Sort photos in folders\n     3.| Select another folder\n  kill.| Kill the program\n-------|\n")
    uiMainList=["1","2","3","kill"]
    uiMain=userInput(uiMainList)
    source = source.rstrip(os.path.sep)
    filelist=os.listdir(source)
    filelist = [os.path.join(source, item) for item in os.listdir(source) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
    dirlist = [os.path.join(source, item) for item in os.listdir(source) if os.path.isdir(os.path.join(source, item))]
    match uiMain:
        #? Rename 
        case "1":
            print("\nWould you like to rename the pics with a custom name or with an exif metadata\n\n-------|\n     1.| Custom name\n     2.| Exif metadata\n break.| To go back\n-------|\n")
            customRenList=["1","2","break"]
            custom_ren=userInput(customRenList)
            match custom_ren:
                #? Custom name
                case "1":
                    randphrase=Randphrase()
                    print(f'Please input the naming pattern of the photos(This will be the name and it will be followed with a number)\n\nIf you want to go back please type"'+Fore.GREEN+randphrase+Style.RESET_ALL+'"')                    
                    uiName=input("--> ")
                    match uiName:
                        case _ if uiName == str(randphrase):
                            print("Going back!")
                            sleep(0.2)
                        case _:
                            if massflag == True:
                                for Dir in dirlist:
                                    better_dir=Dir.split("\\")
                                    better_dir=better_dir[-1]
                                    print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                                    subsource=f"{source}/{better_dir}"
                                    subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]

                                    CustomRenamer2(subsource,subfilelist,uiName)
                            
                            CustomRenamer2(source,filelist,uiName)
                #? EXIF
                case "2":
                    print("Would you like the EXIF metadata title to be in front of a every title?\ny/n")
                    
                    uiFlag=userInput(ynlist)
                    #? Exif
                    print("Before typing an EXIF metadata would you like one of the presets:\n\n-------|\n     1.| Date\n     2.| ISO\n     3.| White Balance\n     4.| Camera Model\n     5.| None\n break.| To go back\n-------|\n")
                    exifRenamelist=["1","2","3","4","5","break"]
                    exif_ren=userInput(exifRenamelist)
                    match exif_ren:
                        #? Date
                        case "1":
                            if massflag == True:
                                for Dir in dirlist:
                                    better_dir=Dir.split("\\")
                                    better_dir=better_dir[-1]
                                    print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                                    subsource=f"{source}/{better_dir}"
                                    subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]

                                    DateReNamer(subsource,subfilelist)
                            
                            DateReNamer(source,filelist)
                        #? ISO
                        case "2":
                            uiMetadata=PopularExif["2"]
                            if massflag == True:
                                for Dir in dirlist:
                                    better_dir=Dir.split("\\")
                                    better_dir=better_dir[-1]
                                    print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                                    subsource=f"{source}/{better_dir}"
                                    subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                                    
                                    CustomRenamer1(subsource,subfilelist,uiMetadata,uiFlag)
                           
                            CustomRenamer1(source,filelist,uiMetadata,uiFlag)                    
                        #? White Balance
                        case "3":
                            uiMetadata=PopularExif["3"]
                            if massflag == True:
                                for Dir in dirlist:
                                    better_dir=Dir.split("\\")
                                    better_dir=better_dir[-1]
                                    print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                                    subsource=f"{source}/{better_dir}"
                                    subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                                     
                                    CustomRenamer1(subsource,subfilelist,uiMetadata,uiFlag)
                            
                            CustomRenamer1(source,filelist,uiMetadata,uiFlag)
                            source = source.rstrip(os.path.sep)
                            filelist=os.listdir(source)

                            filelist = [os.path.join(source, item) for item in os.listdir(source) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                            dirlist = [os.path.join(source, item) for item in os.listdir(source) if os.path.isdir(os.path.join(source, item))]
                        #? Camera Model 
                        case "4":
                            uiMetadata=PopularExif["4"]
                            if massflag == True:
                                for Dir in dirlist:
                                    better_dir=Dir.split("\\")
                                    better_dir=better_dir[-1]
                                    print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                                    subsource=f"{source}/{better_dir}"
                                    subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                                   
                                    CustomRenamer1(subsource,subfilelist,uiMetadata,uiFlag)
                            
                            CustomRenamer1(source,filelist,uiMetadata,uiFlag)
                        #? None (User selects metadata)
                        case "5":
                            print("Input your desired metadata you want to be renamed with (ex. ModifyDate,ImageWidth etc. you can read the EXIF available list)")
                            uiMetadata=input("--> ")
                            if massflag == True:
                                for Dir in dirlist:
                                    better_dir=Dir.split("\\")
                                    better_dir=better_dir[-1]
                                    print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                                    subsource=f"{source}/{better_dir}"
                                    subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                                   
                                    CustomRenamer1(subsource,subfilelist,uiMetadata,uiFlag)
                            
                            CustomRenamer1(source,filelist,uiMetadata,uiFlag)
                        case "break":
                            print("Going back!")
                            sleep(0.2)
                case "break":
                    print("Going back!")
                    sleep(0.2)                          
        #? Sorting             
        case "2":
            print("\nHow would you like to sort your pictures?\n")
            print("-------|\n     1.| In folders based on date of the camera click\n     2.| In folders based on the camera that was taken with\n     3.| In folders based on the White Balance of the picture\n     4.| In folders based on the ISO of the picture\n     5.| In folders based on the Rating of the picture (1-5 stars)\n     6.| In folders based on the type of the image file\n     7.| Custom sorting\n     break.|To go back\n-------|\n")
            customSortList=["1","2","3","4","5","6","7","break"]
            SortInput=userInput(customSortList)
            match SortInput:
                #? Date
                case "1":
                    print("Which preset would you like:")
                    print("1. Year/Month")
                    print("2. Year/Month/Day")  
                    listofavailableitems=["1","2"]
                    ui=userInput(listofavailableitems) 
                    if massflag == True:
                        for Dir in dirlist:
                            better_dir=Dir.split("\\")
                            better_dir=better_dir[-1]
                            print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                            subsource=f"{source}/{better_dir}"
                            subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                            DateSorting(subsource,subfilelist,ui)                            
                    DateSorting(source,filelist,ui)
                #? Camera Model
                case "2":
                    uiMetadata=PopularExif["4"]
                    if massflag == True:
                        for Dir in dirlist:
                            better_dir=Dir.split("\\")
                            better_dir=better_dir[-1]
                            print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                            subsource=f"{source}/{better_dir}"
                            subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                            customSorting1(subsource,subfilelist,uiMetadata)                            
                    customSorting1(source,filelist,uiMetadata)
                #? White Balance
                case "3":
                    uiMetadata=PopularExif["3"]
                    if massflag == True:
                        for Dir in dirlist:
                            better_dir=Dir.split("\\")
                            better_dir=better_dir[-1]
                            print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                            subsource=f"{source}/{better_dir}"
                            subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                            customSorting1(subsource,subfilelist,uiMetadata)                            
                    customSorting1(source,filelist,uiMetadata)
                #? ISO
                case "4":
                    uiMetadata=PopularExif["2"]
                    if massflag == True:
                        for Dir in dirlist:
                            better_dir=Dir.split("\\")
                            better_dir=better_dir[-1]
                            print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                            subsource=f"{source}/{better_dir}"
                            subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                            customSorting1(subsource,subfilelist,uiMetadata)                            
                    customSorting1(source,filelist,uiMetadata)                  
                #? Rating
                case "5":
                    print("Under construction")
                    kill=input("")                       
                #? Extension
                case "6":
                    uiMetadata=PopularExif["5"]
                    if massflag == True:
                        for Dir in dirlist:
                            better_dir=Dir.split("\\")
                            better_dir=better_dir[-1]
                            print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                            subsource=f"{source}/{better_dir}"
                            subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
                            customSorting1(subsource,subfilelist,uiMetadata)                            
                    customSorting1(source,filelist,uiMetadata)                     
                #? Custom
                case "7":
                    randphrase=Randphrase()
                    print(f'Please input the naming pattern of the photos(This will be the name and it will be followed with a number)\n\nIf you want to go back please type"'+Fore.GREEN+randphrase+Style.RESET_ALL+'"')                    
                    uiName=input("--> ")
                    match uiName:
                        case _ if uiName == str(randphrase):
                            print("Going back!")
                            sleep(0.2)
                        case _:
                            if massflag == True:
                                for Dir in dirlist:
                                    better_dir=Dir.split("\\")
                                    better_dir=better_dir[-1]
                                    print("\nSubfolder: "+Fore.GREEN+f"{better_dir}"+Style.RESET_ALL)
                                    subsource=f"{source}/{better_dir}"
                                    subfilelist = [os.path.join(subsource, item) for item in os.listdir(subsource) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]

                                    customsorting2(subsource,subfilelist,uiName)
                            
                            customsorting2(source,filelist,uiName)
                case "break":
                   print("Going back!")
                   sleep(0.2)                  
        case "3":
            source =""    
            source = askdirectory()
            flagdir=os.path.isdir(str(source))
            while flagdir !=True: 
                print(Fore.RED+"ERROR"+Style.RESET_ALL+f", you either didnt select a directory or the directory doesnt exist")
                source = askdirectory()
                flagdir=os.path.isdir(str(source))
            source = source.rstrip(os.path.sep)

            filelist=os.listdir(source)
            filelist = [os.path.join(source, item) for item in os.listdir(source) if item.lower().endswith((".jpg", ".png", ".nef", ".jpeg","cr2",'nef'))]
            dirlist = [os.path.join(source, item) for item in os.listdir(source) if os.path.isdir(os.path.join(source, item))]
                    
            print("Would you like to do a"+Fore.RED+" M4SS "+Style.RESET_ALL+"organize again?\n")
            print("y/n")
            massui=userInput(ynlist)
            match massui:
                case "y":
                    massflag=True
                case "n":
                    massflag=False
        case "kill":
            exit()


