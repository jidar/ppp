import ConfigParser
import pickle
import os
import sys
import time
import datetime
from uuid import uuid4

PROBLEM='problem'
PROGRESS='progress'
PLAN='plan'
PPPTYPES = (PROBLEM, PROGRESS, PLAN)

#Datafile Management
def load_datafile(datafile_path):
    datafile = None
    fh = None
    
    try:
        datafile_path = os.path.expanduser(datafile_path)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.write('Error expanding path to datafile for load')
        sys.stderr.flush()

    try:
        if not os.path.exists(datafile_path):
            os.mkdir(datafile_path)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.write('Error verifying existance fo datafile path for load')
        sys.stderr.flush()

    datafile_path = os.path.join(datafile_path, 'datafile')

    try:
        fh = open(datafile_path, 'r')
    except:
        sys.stderr.write('No datafile found, starting from scratch')
    
    if fh is not None:
        try:
            datafile = pickle.load(fh)
        except Exception as e:
            sys.stderr.write(str(e))
            sys.stderr.write('Error unpickling datafile')

    if datafile is None:
        #Initialize datafile if this is the first run
        datafile = DataFile()

    if fh is not None:
        fh.close()

    return datafile

def save_datafile(datafile, datafile_path):
    fh = None

    try:
        datafile_path = os.path.expanduser(datafile_path)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.write('Error expanding path to datafile for dump')
        sys.stderr.flush()
    
    datafile_path = os.path.join(datafile_path, 'datafile')
        
    try:
        fh = open(datafile_path, 'w+')
    except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.write('Error opening datafile for dump: %s' % str(datafile_path))        

    if fh is not None:
        try:
            pickle.dump(datafile, fh)
        except Exception as e:
            sys.stderr.write(str(e))
            sys.stderr.write('Error dumping datafile')
        
        fh.close()

class Entry(object):
    def __init__(self, project_name, classification, text):
        self.id = uuid4()
        self.timestamp = time.time()
        self.datetimestamp = datetime.datetime.now()
        self.project = project_name
        self.classification = classification
        self.text = text
        
    def __repr__(self):
        s = ''
        s += 'id: %s\n' % (str(self.id))
        s += 'date: %s\n' % (str(self.datetimestamp))
        s += 'project: %s\n' % (str(self.project))
        s += 'type: %s\n' % (str(self.classification))
        s += 'text: %s\n' % (str(self.text))
        return s
        
class Project(object):
    def __init__(self, name, display_name):
        self.name = name
        self.display_name = display_name

class DataFile(object):
    def __init__(self):
        self._entries = []
        self._project_names = []

    #Entry Management        
    def print_entries(self):
        if self._entries == []:
            print 'No entries listed.'
        for e in self._entries:
            print str(e)

    def append_entry(self, entry_object):
        self._entries.append(entry_object)
        
    def delete_entry(self, entry_id):
        for e in self._entries:
            if str(e.id).lower() == str(entry_id).lower():
                self._entries.remove(e)
                return True
    
    #Project Name Management
    def get_all_project_names(self):
        '''returns a lis of tuples'''
        return [(p.name, p.display_name) for p in self._project_names]
    
    def get_project_names(self):
        return [p.name for p in self._project_names]
    
    def add_project_name(self, name, display_name):
        if str(name).lower() not in [str(pn.name).lower() for pn in self._project_names]:
            self._project_names.append(Project(name, display_name))
            return True
        else:
            return False
    
    def delete_project_name(self, project_name):
        #offending_p = None
        for p in self._project_names:
            if str(project_name).lower() == str(p.name).lower():
                self._project_names.remove(p)
                return True
        else:
            return False
        
    def _report(self, entries, projects=None):
        #Make a list of the projects to include in the report
        req_projects = []
        if projects is not None:
            for req_pname in projects:
                for p in self._project_names:                
                    if str(req_pname).lower() == (p.name).lower():
                        req_projects.append(p)
        else:
            req_projects = self._project_names

        #Create the report on a per-project, per-type basis
        report_dict = {}
    
        for p in req_projects:
            pdict = p.display_name
            pname = p.name
            report_dict[pdict] = {}
            for t in PPPTYPES:
                ttype = t
                report_dict[pdict][ttype] = []
                for e in entries:
                    ename = e.project
                    etype = e.classification
                    etext = e.text
                    if (ename == pname) and (etype == ttype):
                            report_dict[pdict][ttype].append(etext)

        for p in report_dict:
            if report_dict[p] != {} or report_dict[p] != None:
                print p
            else:
                print 'Empty: %s' % str(e)
            for t in report_dict[p]:
                if report_dict[p][t] != []:
                    print '    ' + t
                for e in report_dict[p][t]:
                    print '        ' + e + '\n'

    #note: then < now
    def report_days(self, days, projects=None):
        then = datetime.datetime.now() - datetime.timedelta(days=days)
        then = datetime.datetime(then.year, then.month, then.day)
        requested_entries = []
        for e in self._entries:
            if e.datetimestamp > then:
                requested_entries.append(e)

        self._report(requested_entries, projects)
        
    def report_range(self, sy, sm, sd, ey=None, em=None, ed=None):
        start = datetime.datetime(sy, sm, sd)
        end = None
        requested_entries = []
        if ey and em and ed:
            try:
                end = datetime.datetime(ey, em, ed)
            except Exception as e:
                sys.stderr.write(str(e))
                sys.stderr.write('Improper date format given to range reporter')

        for e in self._entries:
            if e.datetimestamp > start and e.datetimestamp < end:
                requested_entries.append(e)
        
        self._report(requested_entries, projects)                