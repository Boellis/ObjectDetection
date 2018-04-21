import os

path = input("Enter the path or folder name: ") #This is the path relative to the directory this script is stored on (use / instead of  \)
updatedFilename  = input("Enter the updated name: ")

files = os.listdir(path)

print("Are sure you want to rename the following files?")
print(files)
awns = input("(y/n): ").lower()
if awns == "y" or awns == "yes" or awns == "yeah" or awns == "probably" or awns == "yup" or awns == "you bet":
    i = 1
    for file in files:
        root, ext = os.path.splitext(file) #ext will get the file extension of the file
        os.rename(os.path.join(path,file), os.path.join(path, updatedFilename+str(i)+ext))
        i+=1
