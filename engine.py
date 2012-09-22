import ConfigParser
PROBLEM='problem'
PROGRESS='progress'
PLAN='plan'

class Entry(object):
    def __init__(self):
        self.timestamp = None
        self.project = None
        self.classification = None
        self.text = None        

#Datafile Management
def load_datafile(datafile_path):
    pass

def save_datafile(datafile_path):
    pass
        
class DataFile(object):
    def __init__(self):
        self._entries = []
        self._project_names = []

    #Entry Management
    def append_entry(entry_object):
        self._entries.append(entry_object)
    
    def get_project_names():
        return self._project_names
    
    #Project Name Management
    def add_project_name(new_project_name):
        if str(new_project_name).lower() not in [str(pn).lower() for pn in self._project_names]:
            self._project_names.append(new_project_name)
            return True
        else:
            return False
    
    def delete_project_name(project_name):
        if str(project_name).lower() not in [str(e.project).lower() for e in self._entries]:
            self._project_names.remove(project_name)
            return True
        else:
            return False

#    
#def archive_entry():
#    #Append entry to archive entry list
#    #remove entry from entries list
#    pass
#
#def 
#
#def save_report():
#    pass
#
#def open_report():
#    pass
#
#def est():
#    scp = ConfigParser.SafeConfigParser()
#    
#    scp.add_section()
