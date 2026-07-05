##Python Program to show the packages installed in the current environment along with their versions.


from importlib import metadata

for dist in metadata.distributions():
    print(f"Package Name : Version :  {dist.name}=={dist.version}")


# import pkg_resources

# installed_packages = pkg_resources.working_set

# for pkg in installed_packages:
#     print(f"{pkg.project_name}=={pkg.version}")



import importlib.metadata

for pkg in importlib.metadata.distributions():
    print(f"{pkg.metadata['Name']}=={pkg.version}")
