import os
import sys
import getopt


def transfer(dir_pref):
    ret = os.system('cython -%s %s.py;'
                    'gcc -c -fPIC -I%s %s.c -o %s.o'
                    % (py_ver, dir_pref, lib_dir, dir_pref, dir_pref))
    if ret == 0:
        ret = os.system('gcc -shared %s.o -o %s.so' % (dir_pref, dir_pref))
    if ret != 0:
        if ret == 2:
            print("Stop compile by ctrl-c")
        else:
            print("Compilie error, please check you have installed cython or the lib_dir is right")
        sys.exit(1)
    os.system('rm -f %s.c %s.o %s.py' % (dir_pref, dir_pref, dir_pref))
    print("Completed %s" % dir_pref)


if __name__ == '__main__':
    help_show = '''
py2so is tool to change the .py to .so, you can use it to hide the source code of py
It can be called by the main func as "from module import * "
py2so needs the environment of python2

Usage: python py2so.py [options] ...

Options:
  -h,  --help       Show the help info
  -p,  --py         Python version, default value is 3
                    Example: -p 2  (means you use python2)
  -l,  --lib        python libray for compile, must be offered
  -d,  --directory  Directory of your project (if use -d, you change the whole directory)
  -e,  --exclude    Directories or files that you do not want to sync to output file
                    dirs __pycache__, .vscode, .git, .idea will always not be synced
  -f,  --file       File to be transfered (if use -f, you only change one file)
  -o,  --output     Directory to store the compile results, default "./output"
  -m,  --maintain   List the file or the directory you don't want to transfer
                    Note: The directories should be surrounded by '[]', and must be the relative path to -d's value
                    Example: -m __init__.py,setup.py,[poc,resource,venv,interface]
Example:
  python py2so.py -f test_file.py
  python py2so.py -d test_dir -m __init__.py,setup.py,[poc/,resource/,venv/,interface/]
    '''
    py_ver       = '3'
    source_dir   = ''
    file_name    = ''
    m_list       = ''
    lib_dir      = ''
    exclude_list = []
    output_dir   = './output'
    try:
        options, args = getopt.getopt(sys.argv[1:], "hp:l:o:d:f:m:e:", ["help", "py=", "lib=", "file=", "output=", "directory=", "maintain=", "exclude="])
    except getopt.GetoptError:
        print('Get options Error')
        print(help_show)
        sys.exit(1)

    for key, value in options:
        if key in ['-h', '--help']:
            print(help_show)
            sys.exit(0)
        elif key in ['-p', '--py']:
            p_subv = value
        elif key in ['-l', '--lib']:
            lib_dir = value
        elif key in ['-o', '--output']:
            output_dir = value
        elif key in ['-d', '--directory']:
            source_dir = value
        elif key in ['-f', '--file']:
            file_name = value
        elif key in ['-e', '--exclude']:
            exclude_list = value.split(",")
        elif key in ['-m', '--maintain']:
            m_list = value
            file_flag = 0
            dir_flag = 0
            if m_list.find(',[') != -1:
                tmp = m_list.split(',[')
                file_list = tmp[0]
                dir_list = tmp[1:-1]
                file_flag = 1
                dir_flag = 1
            elif m_list.find('[') != -1:
                dir_list = m_list[1:-1]
                dir_flag = 1
            else:
                file_list = m_list.split(',')
                file_flag = 1
            if dir_flag == 1:
                dir_tmp = dir_list.split(',')
                dir_list = []
                for d in dir_tmp:
                    if d.startswith('./'):
                        dir_list.append(d[2:])
                    else:
                        dir_list.append(d)
    exclude_list = set(['.git', '.vscode', '.idea', '__pycache__'] + exclude_list)
    exclude_list = "'" + "', '".join(exclude_list) + "'"

    if lib_dir[-1] == r'/':
        lib_dir = lib_dir[:-1]

    if not os.path.isdir(lib_dir):
        print('lib_dir must be given, useing -l or --lib')
        sys.exit(1)

    if source_dir[-1] == r'/':
        source_dir = source_dir[-1]

    if output_dir[-1] == r'/':
        output_dir = output_dir[-1]

    if os.path.abspath(source_dir) == os.path.abspath(output_dir):
        print("Source dir equals output dir!")
        sys.exit(1)

    if py_ver not in ['2', '3']:
        print('python version must be 3 or 2')
        sys.exit(1)

    if source_dir:
        if not os.path.exists(source_dir):
            print('No such Directory, please check or use the Absolute Path')
            sys.exit(1)
        if not os.path.exists(output_dir):
            try:
                os.system('mkdir -p %s' % output_dir)
            except Exception:
                print("Cannot mkdir -p %s" % output_dir)
                sys.exit(1)
        os.system("rsync -azP ",
                  "--exclude={%s} " % exclude_list,
                  "--delete %s/ %s/" % (source_dir, output_dir))
        try:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    if m_list != '':
                        skip_flag = 0
                        if dir_flag == 1:
                            for each_dir in dir_list:
                                if (root+'/').startswith(output_dir + '/' + each_dir):
                                    skip_flag = 1
                                    break
                            if skip_flag:
                                continue
                        if file_flag == 1:
                            if file in file_list:
                                continue
                    pref = file.split('.')[0]
                    dir_pref = root + '/' + pref
                    if file.endswith('.pyc'):
                        os.system('rm -f %s' % dir_pref+'.pyc')
                    elif file.endswith('.so'):
                        pass
                    elif file.endswith('.py'):
                        transfer(dir_pref)
        except Exception as err:
            print(err)
            if "Python.h" in err:
                print("Please check out the Python version You use, and use option -p to specify the definite version")
                sys.exit(1)
        else:
            print('All finished')
    if file_name != '':
        try:
            dir_pref = file_name.split('.')[0]
            transfer(dir_pref)
        except Exception as err:
            print(err)
        else:
            print('All finished')
