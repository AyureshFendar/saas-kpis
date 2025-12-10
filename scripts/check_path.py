import os

path = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\data\subscriptions.csv"

print("Does the file exist? →", os.path.exists(path))

print("\nAbsolute path being read:")
print(os.path.abspath(path))

print("\nReal contents of file:")
with open(path, "r") as f:
    for i in range(5):
        print(f.readline().rstrip())
