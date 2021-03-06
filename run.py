import sys
import os
from mysql_fetch import dump
from processor import nodes, rels
from importer.import_db import run as run_import
import config

def fetch():
  print "Fetching..."
  if dump.run():
    print "sqlite created!"
  else:
    print "Fetch failed"

def process_nodes():
  nodes.run()

def process_rels():
  rels.run()

def process():
  process_nodes()
  process_rels()

def neo4j_import():
  run_import()

def neo4j(arg = False):
  try:
    cmd = sys.argv[2]
    os.system(config.neo4j['bin_path'] + " " + cmd)
  except:
    if not arg:
      print "Please pass an additional command to run - e.g. python run.py neo4j console"
      sys.exit(1)
    else:
      os.system(config.neo4j['bin_path'] + " " + arg)

def run_all():
  fetch()
  process()
  neo4j_import()
  compress()

def run_after_fetch_and_start():
  process()
  neo4j_import()
  neo4j('console')

def clean_processed_data():
  os.system('rm ' + config.data['processed_path'] + '/*')

def install_neo4j():
  os.system('curl -O http://dist.neo4j.org/neo4j-community-2.0.1-unix.tar.gz')
  os.system('tar -zxvf neo4j-community-2.0.1-unix.tar.gz')
  os.system('mv neo4j-community-2.0.1 ' + config.neo4j.path)
  os.system('rm neo4j-community-2.0.1-unix.tar.gz')

def compress():
  os.system('tar -cvf USPTO_graph.tar neo4j && gzip USPTO_graph.tar')

commands = {
  'fetch': fetch,
  'process_nodes': process_nodes,
  'process_rels': process_rels,
  'process': process,
  'import': neo4j_import,
  'all': run_all,
  'neo4j': neo4j,
  'run_after_fetch_and_start': run_after_fetch_and_start,
  'clean_processed': clean_processed_data,
  'install_neo4j': install_neo4j,
  'compress': compress
}

try:
  cmd = sys.argv[1]
  # Run command out of dictionary...so python run.py fetch will call fetch(), for example
  commands[cmd.lower()]()
except ImportError:
  print "Remember to have pandas installed!"
  sys.exit(1)
except:
  print "Please try running `python run.py [arg]` one of the following:"
  print "\n".join(map(lambda x: "  - " + str(x), commands.keys()))
  sys.exit(1)