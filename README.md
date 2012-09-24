ppp
===
Stores entries based on project name and entry type (problem, plan, progress.)

Generates reports for projects (either all or specific) from current day
to any number of days in the past.

Data is stored in a python pickle file at ~/.ppp/datafile

First Run
=========
On first run, you should create one project to start with via:
ppp new-project <project-shortname> <project-display-name>
the project shortname is what you'll use to reference it on the cli,
whereas the project-display-name is what will show up in the reports.
(Make sure to put the project display name in quotes if it contains spaces)

Usage
=====

PPP (Progress, problems, plans) style report aggregator.

ppp --help

    positional arguments:
                            commands
        new                 Create new PPP entry
        delete              Delete old PPP entry
        list                List all projects or entries
        new-project         Create new project name
        delete-project      Delete specific project name if no entries are
                            currently using it
        report-days         Create a PPP report from X days ago until now
    
    optional arguments:
      -h, --help            show this help message and exit

ppp new

    positional arguments:
    
      project-name  Project tag for entry.
      ppp-type      PPP Type tag for entry.
      text          PPP Type tag for entry.

ppp delete

    positional arguments:
    
      entry-id    Project tag for entry.

ppp list

    positional arguments:
    
      {entries,projects}  List all entries or proijects

ppp new-project

    positional arguments:
    
      project-name          Name to reference project on command line
      project-display-name  Print name of project
      
ppp delete-project

    positional arguments:
      {<projects><...>}     Project tag to delete.
ppp report-days

    positional arguments:
      days          Days in past from today to report
      project-list  PPP Type tag for entry.
