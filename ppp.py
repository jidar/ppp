import argparse
import engine

DATAFILE_PATH='~/.ppp'

class MyAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print "parser: %s" % str(parser)
        print "namespace: %s" % str(namespace)
        print "values: %s" % str(values)
        print "option_string: %s" % str(option_string)

def run(args, datafile):
    
    #Entry Management
    if args.command == 'new':
        entry = engine.Entry(args.project, args.ppp_type, args.text)
        datafile.append_entry(entry)
    
    if args.command == 'list':
        datafile.print_entries()

    if args.command == 'delete':
        r = datafile.delete_entry(args.entry_id)
        if r:
            print 'Entry %s deleted successfully' % str(args.entry_id)
        else:
            print 'Entry %s not deleted (not found)' % str(args.entry_id)
    
    #Project Management
    if args.command == 'add-project':
        datafile.add_project_name(args.project_name, args.project_display_name)
    
    if args.command == 'list-projects':
        info = datafile.get_all_project_names()
        for n, dn in info:
            print "%s (%s)" % (str(dn), str(n))
            
    if args.command == 'remove-project':
        if datafile.delete_project_name(args.project):
            print 'Project %s deleted.' % str(args.project)
        else:
            print 'There are entries currently using this project name.\
                   Delete those entries before removing the project name'

    if args.command == 'report-days':
        datafile.report_days(int(args.days), args.project_list)
        pass


    #This should always be the last thing
    engine.save_datafile(datafile, DATAFILE_PATH)
        

if __name__ == '__main__':
    desc = 'PPP Report aggregator'
    
    #Load data file
    datafile = engine.load_datafile(DATAFILE_PATH)
    
    #load data from datafile
    projects = datafile.get_project_names()
    ppptypes = engine.PPPTYPES
    if projects == []:
        print 'No Projects Found.'
        print 'Add a new project using: ppp add-project <project-name> <project-diplay-name>'
    
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
    
    list_entries_parser = subparsers.add_parser('list', help='List all entries')

    #Project Name Management    
    add_project_parser = subparsers.add_parser('add-project', help='Add new project name')
    add_project_parser.add_argument('project_name', metavar='project-name', action='store', help='Name to reference project on command line')
    add_project_parser.add_argument('project_display_name', metavar='project-display-name', action='store', help='Print name of project')

    list_proj_parser = subparsers.add_parser('list-projects', help='List all added projects')
    
    del_proj_parser = subparsers.add_parser('remove-project', help='Delete specific project name if no entries are currently using it')
    del_proj_parser.add_argument('project', action='store', choices=projects, help='Project tag to delete.')        
    
    #Reporting
    report_days_parser = subparsers.add_parser('report-days', help='Create a PPP report from X days ago until now')
    report_days_parser.add_argument('days', action='store', default=7, help='Days in past from today to report')
    report_days_parser.add_argument('--project-list', metavar='project_list', nargs='+', action='store', default=projects, choices=projects, help='PPP Type tag for entry.')

    report_from_date_parser = subparsers.add_parser('report-from-date', help='Create a PPP report from a starting date until now')
    report_from_date_parser.add_argument('start_year', action='store', help='Starting year for report range')
    report_from_date_parser.add_argument('start_month', action='store', help='Starting year for report range')
    report_from_date_parser.add_argument('start_day', action='store', help='Starting year for report range')
    report_from_date_parser.add_argument('--project-list', metavar='project_list', nargs='+', action='store', default=projects, choices=projects, help='PPP Type tag for entry.')    

    report_date_range_parser = subparsers.add_parser('report-date-range', help='Create a PPP report from a starting date to an ending date')
    report_from_date_parser.add_argument('start_year', action='store', help='Starting year for report range')
    report_from_date_parser.add_argument('start_month', action='store', help='Starting year for report range')
    report_from_date_parser.add_argument('start_day', action='store', help='Starting year for report range')    
    report_date_range_parser.add_argument('end_year', action='store', help='Ending year for report range')
    report_date_range_parser.add_argument('end_month', action='store', help='Ending year for report range')
    report_date_range_parser.add_argument('end_day', action='store', help='Ending year for report range')
    report_date_range_parser.add_argument('--project-list', metavar='project_list', nargs='+', action='store', default=projects, choices=projects, help='PPP Type tag for entry.')    

    args = parser.parse_args()
    run(args, datafile)