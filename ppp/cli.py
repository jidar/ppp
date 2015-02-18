import argparse
from pppengine import engine

DATAFILE_PATH = '~/.ppp'

# Commands
class CLI(object):

    @classmethod
    def process(self, cmd, datafile, args):
        """Processes command arguments and calls the proper function"""

        #for token in args
        #replace dashes with underscores (to support -- names with - in them)
        cmd = cmd.replace('-', '_')

        #Return proper function
        return getattr(CLI, cmd, 'help')

    def __init__(self):
        pass

    def new(datafile, args):
        entry = engine.Entry(args.project, args.ppp_type, args.text)
        datafile.append_entry(entry)

    def edit(datafile, args):
        new_entry = engine.Entry(args.project, args.ppp_type, args.text)
        datafile.replace_entry(args.entry_id, new_entry)

    def list(datafile, args):
        if args.item == 'entries':
            datafile.print_entries()
        elif args.item == 'projects':
            info = datafile.get_all_project_names()
            for n, dn in info:
                print "%s (%s)" % (str(dn), str(n))

    def delete(datafile, args):
        r = datafile.delete_entry(args.entry_id)
        if r:
            print 'Entry %s deleted successfully' % str(args.entry_id)
        else:
            print 'Entry %s not deleted (not found)' % str(args.entry_id)

    def new_project(datafile, args):
        datafile.add_project_name(args.project_name, args.project_display_name)

    def delete_project(datafile, args):
        if datafile.delete_project_name(args.project):
            print 'Project %s deleted.' % str(args.project)
        else:
            print 'There are entries currently using this project name.\
                   Delete those entries before removing the project name'

    def report_days(datafile, args):
        if args.project_list == ['all'] or args.project_list == 'all':
            args.project_list = datafile.get_project_names()
        datafile.report_days(int(args.days), args.project_list)


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
    parser = argparse.ArgumentParser(description=desc)
    subparsers = parser.add_subparsers(help='commands', dest='command')

    #Entry Management
    new_entry_parser = subparsers.add_parser('new', help='Create new PPP entry')
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
    list_parser.add_argument('item', action='store', choices=('entries', 'projects'), help='List all entries or proijects')

    #Project Name Management
    add_project_parser = subparsers.add_parser('new-project', help='Create new project name')
    add_project_parser.add_argument('project_name', metavar='project-name', action='store', help='Name to reference project on command line')
    add_project_parser.add_argument('project_display_name', metavar='project-display-name', action='store', help='Print name of project')

    del_proj_parser = subparsers.add_parser('delete-project', help='Delete specific project name if no entries are currently using it')
    del_proj_parser.add_argument('project', action='store', choices=projects, help='Project tag to delete.')        

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

    run(args, datafile)

    # This should always be run last
    engine.save_datafile(datafile, DATAFILE_PATH)
