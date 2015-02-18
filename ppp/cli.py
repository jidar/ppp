import argparse
from ppp import engine

DATAFILE_PATH = '~/.ppp'

# Commands
class CLI(object):

    @classmethod
    def process(cls, cmd, datafile, args):
        """Creates an instance of the CLI with the current datafile and args,
        and returns the requested command method from that instance to be 
        executed by the caller"""

        #for token in args
        #replace dashes with underscores (to support names with - in them)
        cmd = cmd.replace('-', '_')
        cli = cls(datafile, args)
        return getattr(cli, cmd)

    def __init__(self, datafile, args):
        self.datafile = datafile
        self.args = args

    def new(self):
        entry = engine.Entry(
            self.args.project, self.args.ppp_type, self.args.text)
        self.datafile.append_entry(entry)

    def edit(self):
        new_entry = engine.Entry(
            self.args.project, self.args.ppp_type, self.args.text)
        self.datafile.replace_entry(self.args.entry_id, new_entry)

    def list(self):
        self.datafile.print_entries(self.args.project, self.args.ppp_type)

    def delete(self):
        r = self.datafile.delete_entry(self.args.entry_id)
        if r:
            print 'Entry %s deleted successfully' % str(self.args.entry_id)
        else:
            print 'Entry %s not deleted (not found)' % str(self.args.entry_id)

    def new_project(self):
        self.datafile.add_project_name(
            self.args.project_name, self.args.project_display_name)

    def delete_project(self):
        if self.datafile.delete_project_name(self.args.project):
            print 'Project %s deleted.' % str(self.args.project)
        else:
            print 'There are entries currently using this project name.\
                   Delete those entries before removing the project name'

    def list_projects(self):
        info = self.datafile.get_all_project_names()
        for n, dn in info:
            print "%s (%s)" % (str(dn), str(n))

    def report_days(self):
        if self.args.project_list == ['all'] or \
                self.args.project_list == 'all':
            self.args.project_list = self.datafile.get_project_names()
        self.datafile.report_days(int(self.args.days), self.args.project_list)


#if __name__ == '__main__':
def entry_point(*args, **kwargs):
    desc = 'PPP Report aggregator'

    #Load data file
    datafile = engine.load_datafile(DATAFILE_PATH)

    #load data from datafile
    '''@TODO: implement non-lame (eg, 'all') workaround for argparse
       bug (http://bugs.python.org/issue9625) where default, choices and nargs=*
       don't play well together
    '''
    projects = datafile.get_project_names()
    projects.append('all')
    ppptypes = engine.PPPTYPES

    #Argparsers
    class MyHelpFormatter(argparse.HelpFormatter):
        pass
    parser = argparse.ArgumentParser(description=desc, usage=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(help='', dest='command', metavar='')

    #Entry Management
    new_entry_parser = subparsers.add_parser('new', help='Create new PPP entry', usage=argparse.SUPPRESS)
    new_entry_parser.add_argument('project', metavar='project-name', action='store', choices=projects, help='Project tag for entry.')
    new_entry_parser.add_argument('ppp_type', metavar='ppp-type', action='store', choices=ppptypes, help='PPP Type tag for entry.')
    new_entry_parser.add_argument('text', action='store', help='PPP Type tag for entry.')

    del_entry_parser = subparsers.add_parser('delete', help='Delete old PPP entry')
    del_entry_parser.add_argument('entry_id', metavar='entry-id', action='store', help='Project tag for entry.')

    edit_entry_parser = subparsers.add_parser('edit', help='Edit current PPP entry')
    edit_entry_parser.add_argument('entry_id', metavar='entry-id', action='store', help='Project tag for entry.')
    edit_entry_parser.add_argument('--ppp_type', metavar='--type', action='store', choices=ppptypes, help='Change entry ppp type')
    edit_entry_parser.add_argument('--project', action='store', choices=projects, help='Change entry project')
    edit_entry_parser.add_argument('--text', action='store', help='Change entry text')

    list_parser = subparsers.add_parser('list', help='List all projects or entries')
    list_parser.add_argument('project', metavar='project-name', action='store', choices=projects, help='Which project to list entries for.')
    list_parser.add_argument('--ppp_type', metavar='ppp-type', action='store', choices=ppptypes, help='Which PPP Types to list for project.')

    #Project Name Management
    add_project_parser = subparsers.add_parser('new-project', help='Create new project name')
    add_project_parser.add_argument('project_name', metavar='project-name', action='store', help='Name to reference project on command line')
    add_project_parser.add_argument('project_display_name', metavar='project-display-name', action='store', help='Print name of project')

    del_proj_parser = subparsers.add_parser('delete-project', help='Delete specific project name if no entries are currently using it')
    del_proj_parser.add_argument('project', action='store', choices=projects, help='Project tag to delete.')

    list_proj_parser = subparsers.add_parser('list-projects', help='List all projects')

    #Reporting
    report_days_parser = subparsers.add_parser('report-days', help='Create a PPP report from X days ago until now')
    report_days_parser.add_argument('days', action='store', default=7, help='Days in past from today to report')
    report_days_parser.add_argument('project_list', metavar='project-list', nargs='*', action='store', default='all', choices=projects, help='PPP Type tag for entry.')

    #report_from_date_parser = subparsers.add_parser('report-from-date', help='Create a PPP report from a starting date until now')
    #report_from_date_parser.add_argument('start_year', action='store', help='Starting year for report range')
    #report_from_date_parser.add_argument('start_month', action='store', help='Starting year for report range')
    #report_from_date_parser.add_argument('start_day', action='store', help='Starting year for report range')
    #report_from_date_parser.add_argument('project_list', metavar='project-list', nargs='*', action='store', default='all', choices=projects, help='PPP Type tag for entry.')    
    #
    #report_date_range_parser = subparsers.add_parser('report-date-range', help='Create a PPP report from a starting date to an ending date')
    #report_from_date_parser.add_argument('start_year', action='store', help='Starting year for report range')
    #report_from_date_parser.add_argument('start_month', action='store', help='Starting year for report range')
    #report_from_date_parser.add_argument('start_day', action='store', help='Starting year for report range')    
    #report_date_range_parser.add_argument('end_year', action='store', help='Ending year for report range')
    #report_date_range_parser.add_argument('end_month', action='store', help='Ending year for report range')
    #report_date_range_parser.add_argument('end_day', action='store', help='Ending year for report range')
    #report_date_range_parser.add_argument('project_list', metavar='project-list', nargs='*', action='store', default='all', choices=projects, help='PPP Type tag for entry.')    

    args = parser.parse_args()

    if datafile.get_project_names == [] and args.command != 'new-project':
        print 'No Projects Found.'
        print 'Add a new project using: ppp add-project <project-name> <project-diplay-name>'

    CLI.process(args.command, datafile, args)()

    # This should always be run last
    engine.save_datafile(datafile, DATAFILE_PATH)
