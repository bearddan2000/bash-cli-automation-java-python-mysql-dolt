import os
import logging

logging.basicConfig(level=logging.INFO)
def remove_file(dir, file_path):
    try:
        path = os.path.join(dir, file_path)
        os.remove(path)
    except:
        logging.warning(f'{file_path} not found')

def redo_docker_compose(dir):
    import yaml as yml
    with open(os.path.join(dir, 'docker-compose.yml'), 'r') as fi:
        compose = yml.safe_load(fi)

        services = compose['services']

        if "db" not in services:
            logging.warning('No database service found')
            return 

        # point to db service
        db_service = compose['services']['db']

        # change the image
        db_service['image'] = 'dolthub/dolt-sql-server'

        # check that the port is listed
        if "ports" in db_service:
            if 3306 not in db_service['ports']:
                db_service['ports'].append(3306)
        else:
            ports_lst = [3306]
            db_service['ports'] = ports_lst

        # remove enviroment leaf
        if "environment" in db_service:
            del db_service['environment']

        # remove volumes leaf and rebuild it
        if "volumes" in db_service:
            del db_service['volumes']
        
        volumes_lst = ['./db/sql:/docker-entrypoint-initdb.d']
        db_service['volumes'] = volumes_lst

        compose['services']['db'] = db_service
    
    with open(os.path.join(dir, 'docker-compose.yml'), 'w') as fo:
        yml.dump(compose, fo, sort_keys=False, indent=4, default_flow_style=False)

def redo_readme(dir):
    FILE = os.path.join(dir, 'README.md')
    content = None
    with open(FILE, 'r') as fi:
        content = fi.read()
    
    content = content.replace('mysql', 'dolt')
    content = content.replace('- maria', '- dolthub/dolt-sql-server')
    content = content.replace('--', '-')

    with open(FILE, 'w') as fo:
        fo.write(content)

def replace_install_script(dir):
    import shutil
    remove_file(dir, 'install.sh')
    shutil.copy2('install.sh', os.path.join(dir, 'install.sh'))

def del_grant_user_sql(dir):
    remove_file(dir, 'db/sql/*-grant-user.sql')

def main():
    import sys
    dir = sys.argv[1]
    if dir is None:
        for x in sys.argv:
            logging.info(x)
        logging.error('No directory sent, exiting.')
        exit(1)
    
    redo_readme(dir)
    redo_docker_compose(dir)
    replace_install_script(dir)
    del_grant_user_sql(dir)

if __name__ == "__main__":
    main()