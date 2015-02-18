ppp
===

Stores entries based on project name and entry type (problem, plan, progress.)

Generates reports for projects (either all or specific) from current day
to any number of days in the past.

Data is stored in a python pickle file at ```~/.ppp/datafile```

Quick-Start Usage Exmaple
===============

###First Run

On first run, you should create one project to start with via:
```
ppp new-project <project-shortname> <project-display-name>
```

You'll  use the ```project-shortname``` to reference the project on the cli,
whereas the ```project-display-name``` is what will show up in the reports.
(Make sure to put the project display name in quotes if it contains spaces)

To create a project add a problem and progress to it, do the following:
```
ppp new-project myproj "My Important Project!"
ppp new myproj problem 'This is a bad project name :('
ppp new myproj progress 'Hey, at least I got everything setup with ppp ;)'
ppp new myproj plan 'Come up with a better project name'
ppp new myproj plan 'Make ppp feature request to persist the project that's being worked on!'
```

Creating reports is easy too:
```
ppp report-days 1 myproj
```
produces:
```
My Important Project!
    progress
        Hey, at least I got everything setup with ppp ;)

    problem
        This is a bad project name :(

    plan
        Come up with a better project name

        Make ppp feature request to persist the project that's being worked on!
```

Usage
=====

PPP (Progress, Problems, Plans) style report aggregator.
    
    ppp --help
            positional arguments:
                            
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
