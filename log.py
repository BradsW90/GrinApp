import subprocess

with open('.\Logs\log.txt','w') as output_file:
    subprocess.call(['python', '-m', 'flask', '--app', 'grinapp', 'run', '--debug'], stdout=output_file, stderr=subprocess.STDOUT)
