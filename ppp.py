import argparse
import engine

class MyAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print "parser: %s" % str(parser)
        print "namespace: %s" % str(namespace)
        print "values: %s" % str(values)
        print "option_string: %s" % str(option_string)
    
    pass

if __name__ == '__main__':
    desc = 'PPP Report aggregator'
    #Load data file
    #load project names from
    projects = ('cloudfiles', 'blockstorage')
    ppptypes=('problem','progress','plan')
    parser = argparse.ArgumentParser(description=desc)
    #pppgroup = parser.add_mutually_exclusive_group()
    #pppgroup.add_argument('progress', help="Add progress report.", optional )
    #pppgroup.add_argument('problem', help="Add progress report.")
    #pppgroup.add_argument('plan', help="Add progress report.")
    
    parser.add_argument('--list', nargs=1, action='store', )
        
    subparsers = parser.add_subparsers(help='commands')

    create_parser = subparsers.add_parser('add', help='Add a PPP entry')
    create_parser.add_argument('project', action='store', choices=projects, help='Project tag for entry.')
    create_parser.add_argument('ppp-type', action='store', choices=ppptypes, help='PPP Type tag for entry.')
    create_parser.add_argument('text', action='store', help='PPP Type tag for entry.')
    
    create_parser = subparsers.add_parser('report', help='Create a PPP report')
    create_parser.add_argument('days', action='store', default=7, help='Days in past from today to report')
    create_parser.add_argument('--projects', nargs='+', action='store', default='all', choices=projects, help='PPP Type tag for entry.')
    
    args = parser.parse_args()
    print args