##Python Program to show the packages installed in the current environment along with their versions.


from importlib import metadata

for dist in metadata.distributions():
    print(f"Package Name : Version :  {dist.name}=={dist.version}")
