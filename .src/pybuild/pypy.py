import os, logging

logging.basicConfig(level=logging.INFO)
def _copy_file(dir, file):
    import shutil
    try:
        shutil.copy2('settings.py', os.path.join(dir, f'py-srv/bin/{file}'))
    except:
        shutil.copy2('settings.py', os.path.join(dir, f'bin/{file}'))

def _findfile(name, path):
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)

def settings(dir):
    import shutil
    file = _findfile('setting.py', dir)
    if file not None:
        os.remove(file)
        _copy_file(dir, 'settings.py')
    else
        file = _findfile('db_settings.py', dir)
        os.remove(file)
        _copy_file(dir, 'db_settings.py')

def requirements(dir):
    FILE = _findfile('requirements.txt', dir)
    content = None
    with open(FILE, 'r') as fi:
        content = fi.read()
    
    content = content.replace('pymysql', 'mysql-connector-python')

    with open(FILE, 'w') as fo:
        fo.write(content)

def replace_app(content: str, new_content: dict):
    for old in new_content.keys():
        content = content.replace(old, new_content[old])
    return content

def app(dir):
    FILE = _findfile('app.py', dir)
    if FILE is None:
        FILE = _findfile("main.py", dir)
        
    with open(FILE, 'r') as fi:
        content = fi.read()
    
    new_content = {
        'MYSQL':'DOLT',
        "mariadb+pymysql":'mysql+mysqlconnector',
        ":{password}": ''
    }
    content = replace_app(content, new_content)

    content = content.replace(':pass', '').replace('maria', 'root')
    
    with open(FILE, 'w') as fo:
        fo.write(content)

def main():
    import sys
    dir = sys.argv[1]
    if dir is None:
        for x in sys.argv:
            logging.info(x)
        logging.error('No directory sent, exiting.')
        exit(1)
    
    app(dir)
    settings(dir)
    requirements(dir)

if __name__ == "__main__":
    main()