import os, logging

logging.basicConfig(level=logging.INFO)

def hibernate(dir):
    content = None
    FILE = os.path.join(dir, 'java-srv/bin/src/main/resources/hibernate.cfg.xml')
    content = spring_path(FILE, content)
    content = content.replace('maria', 'root').replace('pass','')
    with open(FILE, 'w') as fo:
        fo.write(content)

def normal(dir):
    content = None
    FILE = os.path.join(dir, 'java-srv/bin/src/main/java/example/Main.java')
    content = spring_path(FILE, content)
    content = content.replace('=maria', '=root').replace('=pass','=').replace('ToFile','ToConsole')
    with open(FILE, 'w') as fo:
        fo.write(content)

def docker(dir):
    content = None
    FILE = os.path.join(dir, 'java-srv/Dockerfile')
    try:
        with open(FILE, 'r') as fi:
            content = fi.read().splitlines()
    except:
        logging.warning(f'{FILE} not found')
        return 
    
    if 'ENV WAIT_VERSION 2.7.2' in content:
        logging.info("Dockerfile already has WAIT defined")
        return

    lst = [
        'ENV WAIT_VERSION 2.7.2',
        'ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait',
        'RUN chmod +x /wait'
    ]

    content[len(content)-3:2] = lst

    with open(FILE, 'w') as fo:
        fo.write('\n'.join(content))

def spring_path(file, content):
    try:
        with open(file, 'r') as fi:
            content = fi.read()
    except:
        logging.warning(f'{file} not found')
    return content

def spring(dir):
    content = None
    FILE = os.path.join(dir, 'java-srv/bin/src/main/resources/application.properties')
    content = spring_path(FILE, content)

    if content is None:
        FILE = os.path.join(dir, 'java-srv/bin/src/main/resources/application.yml')
        content = spring_path(FILE, content)

    content = content.replace('=maria', '=root').replace('=pass','=')
    with open(FILE, 'w') as fo:
        fo.write(content)

def docker_compose(dir):
    import yaml as yml
    with open(os.path.join(dir, 'docker-compose.yml'), 'r') as fi:
        compose = yml.safe_load(fi)
        # point to db service
        java_service = compose['services']['java-srv']

        java_service['command'] = 'sh -c "/wait && gradle run"'
        lst = [
            'WAIT_HOSTS=db:3306',
            'WAIT_HOSTS_TIMEOUT=300',
            'WAIT_SLEEP_INTERVAL=30',
            'WAIT_HOST_CONNECT_TIMEOUT=30',
        ]
        java_service['environment'] = lst


        compose['services']['java-srv'] = java_service
    
    with open(os.path.join(dir, 'docker-compose.yml'), 'w') as fo:
        yml.dump(compose, fo, sort_keys=False, indent=4, default_flow_style=False)

def main():
    import sys
    dir = sys.argv[1]
    if dir is None:
        for x in sys.argv:
            logging.info(x)
        logging.error('No directory sent, exiting.')
        exit(1)
    
    docker(dir)
    docker_compose(dir)

    if "hibernate" in dir:
        hibernate(dir)
    elif "spring" in dir:
        spring(dir)
    else:
        normal(dir)


if __name__ == "__main__":
    main()