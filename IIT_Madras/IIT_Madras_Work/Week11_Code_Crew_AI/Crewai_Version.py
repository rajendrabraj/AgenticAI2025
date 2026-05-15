import pkg_resources
# ----------------------------------------
# 1. Detect LangChain version
# ----------------------------------------
def get_crew_ai_version():
    try:
        return pkg_resources.get_distribution("crewai").version
    except:
        return None

lc_version = get_crew_ai_version()
print("Detected crewai version:", lc_version)
print("-" * 90)
# Helper to compare versions
def version_tuple(v):
    return tuple(int(x) for x in v.split("."))


print("-" * 90)

