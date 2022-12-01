import os
import subprocess
import time
import hashlib
from colorama import Fore
from colorama import init
from termcolor import colored
from FileOps import read_file
from FileOps import add_content_file
from FileOps import search_str_file
from FileOps import unzip_files
from FileOps import check_sha
from FileOps import check_dir
from FileOps import check_file
from FileOps import copy_data_win

################################
ES_PORT = 9200
TARGETDIR = "C:\\"
UPDATEDIR = "C:\\impowin\\newversions"
ES_OLD_INSTALL = "C:\\Program Files\Elastic\Elasticsearch\\7.11.2"
ES_OLD_DATA = "C:\ProgramData\Elastic\ElasticSearch\data"
ES_OLD_PROGDATA = "C:\\ProgramData\\Elastic"
ES_OLD_VER = "Elasticsearch 7.11.2"
ES_OLD_INSTALLED_BIN = "C:\Program Files\Elastic\ElasticSearch\7.11.2\bin"
ES_INSTALLED_DIR = "C:\\Elasticsearch-7.17.5"
ES_INSTALLED_DATA = "C:\\Elasticsearch-7.17.5\data"
ES_INTERM_FILE = "elasticsearch-7.17.5-windows-x86_64.zip"
ES_INTERM_VER = "elasticsearch-7.17.5"
ES_INTERM_SHA = "93cf3cb4f7a6de22a7457f706292f8103ed21f43bfe1db24913d5394857b0f37e765f68ebddcc7576f822c3b051a26f6565aef9a14c6265ec63a2e351b320fd6"
ES_FINAL_FILE = "elasticsearch-8.3.3-windows-x86_64.zip"
ES_FINAL_VER = "elasticsearch-8.3.3"
ES_FINAL_SHA = "6b0456f78c30375911ea9b1fc61ad25ef7a7a69104fd4daf86a3e0a0d707d069b4106ceeebad2a5a7bef5c38c4f77a71f637ca1a1e8796b88be48b3a8377611c"
################################
RESCHECK = 1
INSTALLCONFIG = 0
INSTALLATIONINTERM = 0
INSTALLATIONFINAL = 0
INSTALLUPDATE = ""
INSTALLDIR = ""
TIMEOUT = 120
ES_INTERM_INSDIR = "C:\\" + ES_INTERM_VER
ES_FINAL_INSDIR = ""
ES_FINAL_CONFDIR = ""
OPC = 0

def program():
    global RESCHECK
    global INSTALLCONFIG
    global UPDATEDIR
    global ES_INSTALLED_DIR
    global ES_OLD_INSTALL
    global INSTALLUPDATE
    global ES_INTERM_FILE
    global ES_FINAL_FILE
    global ES_FINAL_INSDIR
    global INSTALLATIONINTERM
    global INSTALLATIONFINAL
    global OPC

    if check_awk():

        init()

        while RESCHECK == 1:
            print(Fore.WHITE + "..................................")
            print(Fore.WHITE + "FS ElasticSearch Updater          ")
            print(Fore.WHITE + "..................................")
            print(Fore.WHITE + "1. PREVIOUS STEPS TO UPDATE.......")
            print(Fore.WHITE + "2. ES INTERM UPDATE PROCESS.......")
            print(Fore.WHITE + "3. ES FINAL UPDATE PROCESS ......")
            print(Fore.WHITE + "4. REMOVE OLD INSTALL.............")
            print(Fore.WHITE + "5. REMOVE ES FINAL................")
            print(Fore.WHITE + "6. ES FINAL CLEAN INSTALLATION ......")
            print(Fore.WHITE + "7. EXIT...........................")
            print(Fore.WHITE + "..................................")
            print(Fore.WHITE + "")

            OPC = input("Which is your selection (1-7):? \n")
            if OPC.isdigit():
                OPC = int(OPC)
                if OPC == 1:
                    first_steps()
                    print("")
                    input(Fore.GREEN + "Variables cleaned. Exit program and restart it again in a new terminal. Press enter to continue.\n")
                    RESCHECK = 0
                    os.system('exit')
                elif OPC == 2:
                    INSTALLUPDATE = ES_INTERM_VER
                    if INSTALLATIONINTERM == 1:
                        print("Upgrade has be done already.\n")
                        break
                    else:
                        check_process()
                        if INSTALLCONFIG == 1 and INSTALLATIONINTERM == 0:
                            checkon = 0
                            while checkon == 0:
                                resContinue = input("Do you want to continue with " + ES_INTERM_VER + "? (y/n) ")
                                if resContinue == 'y' or resContinue == 'Y':
                                    update_process_first(ES_INTERM_FILE, ES_INTERM_VER)
                                    checkon = 1
                                    if INSTALLCONFIG == 1:
                                        input("First step of update process has finished. Press enter to continue, launch again the program and continue with step 3.\n")
                                        first_steps()
                                        RESCHECK = 0
                                        os.system('exit')
                                    else:
                                        print("There is an error with installation.\n")
                                elif resContinue == 'n' or resContinue == 'N':
                                    checkon = 1
                                    print("Ending program...\n")
                                else:
                                    print("Wrong selection.")

                        else:
                            print("")
                            print("Can't proceed with installation, a previous configuration must be done.\n")

                elif OPC == 3:
                    INSTALLUPDATE = ES_FINAL_VER
                    INSTALLATIONFINAL = 0
                    if INSTALLATIONFINAL == 1:
                        print("Upgrade has be done already.\n")
                        break
                    else:
                        check_process()
                        if INSTALLCONFIG == 1 and INSTALLATIONFINAL == 0:
                            checkon = 0
                            while checkon == 0:
                                resContinue = input("Do you want to continue with " + ES_FINAL_VER + "? (y/n)")
                                if resContinue == 'y' or resContinue == 'Y':
                                    update_process_first(ES_FINAL_FILE, ES_FINAL_VER)
                                    final_steps(ES_FINAL_INSDIR)
                                    checkon = 1
                                elif resContinue == 'n' or resContinue == 'N':
                                    checkon = 1
                                    print("Ending program...\n")
                                else:
                                    print("Wrong selection.")
                        else:
                            print("")
                            print(Fore.WHITE + "Can't proceed with installation, a previous configuration must be done.\n")
                            print(Fore.WHITE + "")

                elif OPC == 4:
                    remove_oldins(ES_OLD_INSTALL,ES_OLD_DATA,ES_OLD_VER,ES_INSTALLED_DIR,ES_FINAL_VER,ES_FINAL_CONFDIR)


                elif OPC == 5:
                    remove_final()


                elif OPC == 6:
                    INSTALLCONFIG = 1
                    INSTALLUPDATE = ES_FINAL_VER
                    RESCHECK = 1
                    install_final()


                elif OPC == 7:
                    print("OK, goodbye...\n")
                    RESCHECK = 0

                else:
                    print(Fore.WHITE + "Wrong selection.\n")
                    print(Fore.WHITE + "")
            else:
                print(Fore.WHITE + "Wrong selection.\n")
                print(Fore.WHITE + "")
    else:
        print("awk.exe file is not inside this folder. Please copy it.\n")

### Steps functions ####################################################################################################

def first_steps():
    print("")
    print("Setting environment variables.\n")

    es_killing(ES_OLD_VER)

    dq = '""'
    cmd1 = "setx " + "ES_HOME " + dq
    print(cmd1)
    try:
        os.system(cmd1)
    except:
        print(Fore.WHITE + "Can't Unset ES_HOME.")
        print(Fore.WHITE + "")

    cmd2 = "setx " + "ES_PATH_CONF " + dq
    print(cmd2)
    try:
        os.system(cmd2)
    except:
        print(Fore.WHITE + "Can't Unset ES_PATH_CONF.")
        print(Fore.WHITE + "")

    cmd3 = "powershell -Command [Environment]::SetEnvironmentVariable(" + "\'ES_HOME\', $null ," + "\'Machine\')"
    print(cmd3)
    try:
        os.system(cmd3)
    except:
        print(Fore.WHITE + "Can't Unset ES_HOME.")
        print(Fore.WHITE + "")

    cmd4 = "powershell -Command [Environment]::SetEnvironmentVariable(" + "\'ES_PATH_CONF\', $null ," + "\'Machine\')"
    print(cmd4)
    try:
        os.system(cmd4)
    except:
        print(Fore.WHITE + "Can't Unet ES_PATH_CONF.")
        print(Fore.WHITE + "")

    cmd5 = "powershell -Command [Environment]::SetEnvironmentVariable(" + "\'ES_HOME\', $null ," + "\'User\')"
    print(cmd5)
    try:
        os.system(cmd5)
    except:
        print(Fore.WHITE + "Can't Unset ES_HOME.")
        print(Fore.WHITE + "")

    cmd6 = "powershell -Command [Environment]::SetEnvironmentVariable(" + "\'ES_PATH_CONF\', $null ," + "\'User\')"
    print(cmd6)
    try:
        os.system(cmd6)
    except:
        print(Fore.WHITE + "Can't Unset ES_PATH_CONF.")
        print(Fore.WHITE + "")


def check_process():
    global ES_INSTALLED_DIR
    global UPDATEDIR
    global INSTALLCONFIG
    global INSTALLUPDATE
    global RESCHECK
    global ES_INSTALLED_DATA
    global ES_OLD_INSTALLED_BIN
    global ES_INSTALLED_DIR
    global ES_INTERM_INSDIR
    global ES_INTERM_FILE
    global ES_FINAL_FILE
    global OPC

    if INSTALLUPDATE == ES_FINAL_VER:
        ES_INSTALLED_DIR = ES_INTERM_INSDIR
    else:
        ES_INSTALLED_DIR = ES_OLD_INSTALL

    check_initial(ES_FINAL_VER, ES_INTERM_INSDIR, ES_OLD_DATA, INSTALLUPDATE)


    if check_dir(UPDATEDIR):
        print(UPDATEDIR + " directory exists.\n")

        if INSTALLUPDATE == ES_INTERM_VER:
            UPDATEDIR = UPDATEDIR + "\\"
            if check_file(UPDATEDIR, ES_INTERM_FILE):
                print(ES_INTERM_FILE + " is inside IMPOWIN folder\n")
                ressha = UPDATEDIR + ES_INTERM_FILE
                ressha = check_sha(ressha)
                print("ressha: " + ressha + "\n")
                if ressha == ES_INTERM_SHA:
                    print("Right SHA\n")
                else:
                    print("Wrong SHA\n")
                    RESCHECK = 0
            else:
                print(Fore.WHITE + ES_INTERM_FILE + " is not inside IMPOWIN folder.")
                print(Fore.WHITE + "")
                RESCHECK = 0

        elif INSTALLUPDATE == ES_FINAL_VER:
            UPDATEDIR = UPDATEDIR + "\\"
            if check_file(UPDATEDIR, ES_FINAL_FILE):
                print(ES_FINAL_FILE + " is inside IMPOWIN folder.\n")
                ressha = UPDATEDIR + ES_FINAL_FILE
                ressha = check_sha(ressha)
                print("ressha: " + ressha + "\n")
                if ressha == ES_FINAL_SHA:
                    print("Right SHA\n")
                else:
                    print("Wrong SHA\n")
                    RESCHECK = 0
            else:
                print(Fore.WHITE + ES_FINAL_FILE + " is not inside.")
                print(Fore.WHITE + "")
                RESCHECK = 0
    else:
        print(Fore.WHITE + UPDATEDIR + " doesn't exists.")
        print(Fore.WHITE + "")
        RESCHECK = 0


    if RESCHECK == 0:
        print(Fore.WHITE + "Something went wrong on installation. Please fix the problem and restart it again.")
        print(Fore.WHITE + "")

    else:
        print("The configuration of the installation has be done successfully.\n")
        print("The current values are: ")
        print("..................................")
        print(Fore.GREEN + "ElasticSearch source directory: " + ES_INSTALLED_DIR)
        print(Fore.GREEN + "ElasticSearch source data directory: " + ES_INSTALLED_DATA)
        print(Fore.GREEN + "Update source directory: " + UPDATEDIR)
        if INSTALLUPDATE == ES_INTERM_VER:
            print(Fore.GREEN + "ElasticSearch " + ES_INTERM_VER + " compressed file path: " + ES_INTERM_FILE)
        elif INSTALLUPDATE == ES_FINAL_VER:
            print(Fore.GREEN + "ElasticSearch " + ES_FINAL_VER + " compressed file path: " + ES_FINAL_FILE)
        print(Fore.WHITE + "")

    if RESCHECK == 1:
        INSTALLCONFIG = 1


def check_initial(ES_FINAL_VER,ES_INTERM_INSDIR,ES_OLD_DATA,INSTALLUPDATE):
    global ES_INSTALLED_DATA
    global ES_INSTALLED_DIR
    global ES_OLD_INSTALLED_BIN
    global UPDATEDIR
    global RESCHECK


    print("")
    print("The current installed Elasticsearch location is " + ES_INSTALLED_DIR)
    resInstalled = input("Is this directory OK? (Y/n): ")
    if resInstalled == 'n' or resInstalled == 'N':
        ES_INSTALLED_DIR = input("Write the path for installed Elasticsearch: ")
    else:
        print("")
        if INSTALLUPDATE == ES_FINAL_VER:
            ES_INSTALLED_DATA = ES_INTERM_INSDIR + "\\" + "data"
        else:
            ES_INSTALLED_DATA = ES_OLD_DATA
        print("The current installed Elasticsearch data location is " + ES_INSTALLED_DATA)
        resInstalled = input("Is this directory OK? (Y/n): ")
        if resInstalled == 'n' or resInstalled == 'N':
            ES_INSTALLED_DATA = input("Write the path for Elasticsearch data: ")
        else:
            print("")
            print("The current directory for using the update files is: " + UPDATEDIR)
            choiceDir = input("Is this directory OK? (Y/n): ")
            if choiceDir == 'n' or choiceDir == 'N':
                UPDATEDIR = input("Write the path for update directory: ")

            if check_dir(ES_INSTALLED_DIR):
                ES_OLD_INSTALLED_BIN = "\\bin\\elasticsearch.exe"
                if check_file(ES_OLD_INSTALL, ES_OLD_INSTALLED_BIN):
                    print("ElasticSearch Installation found.")
                else:
                    ES_OLD_INSTALLED_BIN = ES_OLD_INSTALL + ES_OLD_INSTALLED_BIN
                    print(ES_OLD_INSTALLED_BIN + " doesn't exists.\n")
            else:
                print(ES_INSTALLED_DIR + " doesn't exists")
                RESCHECK = 0

def update_process_first(es_file, es_dir):
    global RESCHECK
    global ES_INTERM_INSDIR
    global INSTALLCONFIG

    choiceok = 0
    while choiceok == 0:
        print("")

        if INSTALLUPDATE == ES_INTERM_VER:
            resCopy = input("Do you want to make a copy of data before proceeding? (y/n)\n")
            if resCopy == 'y' or resCopy == 'Y':
                resFolder = input("Write your target folder: \n")
                if check_dir(resFolder):
                    print(resFolder + " exists, please choose another.\n")
                else:
                    cmd = copy_data_win(ES_INSTALLED_DATA, resFolder)
                    try:
                        os.system(cmd)
                    except:
                        print(Fore.WHITE+ "Something wrong happen when backup data.")
                        print(Fore.WHITE + "")
                        RESCHECK = 0

                    choiceok = 1

            elif resCopy == 'n' or resCopy == 'N':
                choiceok = 1

            else:
                print(Fore.WHITE + "Wrong choice.")
                print(Fore.WHITE + "")

        if RESCHECK == 1:
            update_process_final(es_file, es_dir)
            choiceok = 1
        else:
            INSTALLCONFIG = 0

def update_process_final(es_file, es_dir):
    global TARGETDIR
    global RESCHECK
    global INSTALLDIR
    global INSTALLCONFIG

    print("Checking if there is a ES running process...")
    es_killing(es_dir)
    print("")
    print(Fore.GREEN + "Installation process of " + es_dir + " started...")
    print(Fore.WHITE + "")
    choiceok = 0
    print("Current target is: " + TARGETDIR)
    es_install_dir = TARGETDIR
    while choiceok == 0:
        dirok = input("Is this destination ok? (y/n)? \n")
        if dirok == 'y' or dirok == 'Y':
            unzipdir = es_install_dir + es_dir
            if check_dir(unzipdir):
                print("The target directory " + unzipdir + " exists, please select another one.")
                es_install_dir = input("Write the new target directory: \n")
                print("Current target is: " + es_install_dir)
            else:
                choiceok = 1
        elif dirok == 'n' or dirok == 'N':
            es_install_dir = input("Write the new target directory: \n")
            print("Current target is: " + es_install_dir)
        else:
            print(Fore.WHITE + "Wrong choice.")
            print(Fore.WHITE + "")
            print("Current target is: " + es_install_dir)
    INSTALLDIR = es_install_dir
    print("")
    print("Unzipping " + es_file + " ....")
    print("")
    es_file = UPDATEDIR + es_file
    try:
        unzip_files(es_file, es_install_dir)
    except:
        print(Fore.WHITE + "Something went wrong, can't unzip to the target directory.")
        print(Fore.WHITE + "")
        RESCHECK = 0

    if RESCHECK == 1:
        install_es(es_install_dir,es_dir)
    else:
        print("Can't continue with installation, something was wrong\n")
        input("Press enter to continue\n")
        INSTALLCONFIG = 0

def install_es(es_install_dir, es_dir):
    global RESCHECK
    global ES_INSTALLED_DATA
    global ES_INTERM_INSDIR
    global ES_INTERM_VER
    global ES_FINAL_INSDIR
    global ES_FINAL_CONFDIR
    global ES_FINAL_VER
    global INSTALLATIONINTERM
    global INSTALLATIONFINAL
    global INSTALLCONFIG
    global OPC

    es_install_dir = es_install_dir + es_dir
    es_config_dir = es_install_dir + "\\" + "config"
    set_variables(es_install_dir,es_config_dir)
    if es_dir == ES_FINAL_VER and OPC != 6:
        ES_FINAL_INSDIR = es_install_dir
        ES_FINAL_CONFDIR = es_config_dir
        configfile = ES_FINAL_CONFDIR + "\\elasticsearch.yml"
        configoptsfile = ES_FINAL_CONFDIR + "\\jvm.options.d\\jvm.options"
        print(configoptsfile)
        datadir = es_install_dir + "\data"
        add_content_file(configfile, "xpack.security.enabled: false")
        add_content_file(configoptsfile, "-Xms1g\n")
        add_content_file(configoptsfile, "-Xmx1g")
        cmd = copy_data_win(ES_INSTALLED_DATA, datadir)
        try:
            os.system(cmd)
        except:
            print("There was a problem copying data from " + ES_FINAL_VER + " installation to the new one")
    if es_dir == ES_INTERM_VER:
        ES_INTERM_INSDIR = es_install_dir
        datadir = es_install_dir + "\data"
        cmd = copy_data_win(ES_INSTALLED_DATA,datadir)
        try:
            os.system(cmd)
        except:
            print("There was a problem copying data from " + ES_INTERM_VER +" installation to the new one")

    if es_dir == ES_FINAL_VER and OPC == 6:
        ES_FINAL_INSDIR = es_install_dir
        ES_FINAL_CONFDIR = es_config_dir
        configfile = ES_FINAL_CONFDIR + "\\elasticsearch.yml"
        configoptsfile = ES_FINAL_CONFDIR + "\\jvm.options.d\\jvm.options"
        add_content_file(configfile, "xpack.security.enabled: false")
        add_content_file(configoptsfile, "-Xms1g\n")
        add_content_file(configoptsfile, "-Xmx1g")

    runbat = "START /B CMD.EXE /C " + es_install_dir + "\\BIN\\" + "ELASTICSEARCH.BAT >NUL"
    print("")
    print(Fore.GREEN + "Launching ElasticSearch....")
    print(Fore.WHITE + "")
    try:
        os.system(runbat)
    except:
        print(Fore.WHITE + "There was a problem launching Elasticsearch.bat.")
        print(Fore.WHITE + "")
        RESCHECK = 0

    if RESCHECK == 1:
        logdir = es_install_dir + "\\" + "logs" + "\\"
        resLogfile = False
        logfile = "elasticsearch.log"
        logTimeout = 10
        count = 0
        while resLogfile == False or logTimeout > count:
            RESCHECK = 0
            resLogfile = check_file(logdir, logfile)
            count += 1
            if check_file(logdir, logfile):
                RESCHECK=1

        if RESCHECK == 1:
            logfile = logdir + logfile
            resFound = find_started(logfile)
            if resFound == 1:
                print(Fore.GREEN + "ElasticSearch has finished its starting.")
                print(Fore.WHITE + "")
                datadir = es_install_dir + "\data"
                resES = es_running(es_dir)
                if int(resES) > 0:
                    if check_dir(datadir):
                        print(Fore.GREEN + "The Data dir is also created.\n")
                        print("Ending now ElasticSearch after a good starting.")
                        print(Fore.WHITE + "")
                        es_killing(es_dir)
                        INSTALLCONFIG = 1
                    else:
                        print(Fore.WHITE + es_dir + " is not working as expected.")
                        print(Fore.WHITE + "")
                        RESCHECK = 0
                else:
                    print(Fore.WHITE + es_dir + " is not running.")
                    print(Fore.WHITE + "")
                    RESCHECK = 0

                if INSTALLUPDATE == ES_FINAL_VER:
                    INSTALLATIONFINAL = 1

                else:
                    INSTALLATIONINTERM = 1

            else:
                print(Fore.WHITE + "Elasticsearch log is no working.")
                print(Fore.WHITE + "")
                RESCHECK = 0
                if INSTALLUPDATE == ES_FINAL_VER:
                    INSTALLATIONFINAL = 0
                else:
                    INSTALLATIONINTERM = 0

        else:
            print(Fore.WHITE + "Elastic log directory isn't created.")
            print(Fore.WHITE + "")
            RESCHECK = 0
            if INSTALLUPDATE == ES_FINAL_VER:
                INSTALLATIONFINAL = 0
            else:
                INSTALLATIONINTERM = 0
    else:
        print(Fore.WHITE + "ELasticSearch couldn't start.")
        print(Fore.WHITE + "")

def adding_services(es_install_dir):
    global ES_FINAL_VER

    print("Adding " + ES_FINAL_VER + " to Windows Service")
    runbat = "START /B CMD.EXE /C " + es_install_dir + "\BIN\ELASTICSEARCH-SERVICE.BAT install "
    try:
        os.system(runbat)
    except:
        print(Fore.WHITE + "Can't add elasticsearch-service-x64 to Windows Services.")
        print(Fore.WHITE + "")

    time.sleep(10)
    print("Changing " + ES_FINAL_VER + " Windows Service to automatic")
    runbat = "Powershell -command Set-Service -Name 'elasticsearch-service-x64' -StartupType auto >NUL"

    try:
        os.system(runbat)
    except:
        print(Fore.WHITE + "Can't change elasticsearch-service-x64 service to automatic.")
        print(Fore.WHITE + "")

    print("")

def final_steps(es_install_dir):
    global ES_FINAL_VER
    global ES_INSTALLED_DIR
    global ES_OLD_INSTALL
    global ES_FINAL_INSDIR
    global ES_FINAL_CONFDIR
    global ES_OLD_INSTALL
    global ES_OLD_DATA

    adding_services(es_install_dir)

    remove_oldins(ES_OLD_INSTALL,ES_OLD_DATA,ES_OLD_VER,ES_INSTALLED_DIR,ES_FINAL_VER,ES_FINAL_CONFDIR)

    set_variables(ES_FINAL_INSDIR, ES_FINAL_CONFDIR)
    runbat = "START /MIN CMD.EXE /C " + ES_INSTALLED_DIR + "\BIN\ELASTICSEARCH-SERVICE.BAT start"
    try:
        os.system(runbat)
    except:
        print(Fore.WHITE + "There was a problem adding the elasticsearch-service-x64 in Windows Service")
        print(Fore.WHITE + "")
    print("Finished installation. Don't forget to start ElasticSearch service and then restart ImpoWin!!\n")


def remove_oldins(old_install,old_data,ES_OLD_VER,es_installed_dir,es_FINAL_insdir,es_FINAL_confdir):
    global ES_OLD_PROGDATA
    choiceok = 0
    while choiceok == 0:
        resRemove = input("Final steps: removing older installations. Do you want to proceed? (y/n)")
        if resRemove == 'y' or resRemove == 'Y':
            print("Removing old installations\n")
            set_variables(old_install, old_data)
            runbat = "powershell -command uninstall-package -force  " + "\'" + ES_OLD_VER + "\'"
            try:
                os.system(runbat)

            except:
                print(Fore.WHITE + "Can't remove installed " + ES_OLD_VER+ ". Maybe is not installed already.")
                print(Fore.WHITE + "")

            cmd1 = "rmdir /s /q " + ES_OLD_PROGDATA
            print("Removing " + ES_OLD_PROGDATA + ".\n")
            print("Removing: " + cmd1)
            try:
                os.system(cmd1)
            except:
                print(
                    Fore.WHITE + "There was a problem removing " + ES_OLD_PROGDATA + " in the new ElasticSearch installation")
                print(Fore.WHITE + "")

            cmd2 = "rmdir /s /q " + es_installed_dir
            print("Removing " + es_installed_dir + ".\n")
            print("Removing: " + cmd2)
            try:
                os.system(cmd2)
            except:
                print(Fore.WHITE + "There was a problem removing data of " + es_installed_dir + " in the new ElasticSearch installation")
                print(Fore.WHITE + "")

            set_variables(es_FINAL_insdir, es_FINAL_confdir)

            choiceok = 1
        elif resRemove == 'n' or resRemove == 'N':
            print("Removal of old installation skipped. Don't forget to remove them later.\n")
            choiceok = 1
        else:
            print(Fore.WHITE + "Wrong selection.\n")
            print(Fore.WHITE + "")

def remove_final():
    es_remove_dir = "C:\\" + ES_FINAL_VER
    choiceok = 0
    while choiceok == 0:
        es_killing(ES_FINAL_VER)
        print("Removing elasticsearch-service-x64 from Windows Service")
        runbat = "sc.exe delete elasticsearch-service-x64"
        try:
            os.system(runbat)
        except:
            print(Fore.WHITE + "There was a problem removing the elasticsearch-service-x64 in Windows Service")
            print(Fore.WHITE + "")
        cmd = "rmdir /s /q " + es_remove_dir
        print("Removing " + es_remove_dir + ".\n")
        try:
            os.system(cmd)
        except:
            print(Fore.WHITE + "There was a problem removing" + es_remove_dir + " in the new ElasticSearch installation")
            print(Fore.WHITE + "")
        choiceok = 1

def install_final():
    global RESCHECK
    global UPDATEDIR
    global ES_FINAL_FILE
    global ES_FINAL_VER
    global INSTALLDIR

    resCheck = check_es_variables()

    if resCheck == 1:
        print("ES_HOME and ES_PATH_CONF variables are configured on the system.")
        print("")
        print(Fore.GREEN + "WARNING!! Can't proceed.")
        print(Fore.GREEN + "Could be temporary variables so better close the program and start it again.")
        print(Fore.GREEN + "You can also proceed with point 1. to clean any temporary variables.\n")
    elif resCheck == 0:
        print("The current directory for using the update files is: " + UPDATEDIR)
        choiceDir = input("Is this directory OK? (Y/n): ")
        if choiceDir == 'n' or choiceDir == 'N':
            UPDATEDIR = input("Write the path for update directory: ")

        UPDATEDIR = UPDATEDIR + "\\"
        if check_file(UPDATEDIR, ES_FINAL_FILE):
            print(ES_FINAL_FILE + " is inside IMPOWIN folder.\n")
            ressha = UPDATEDIR + ES_FINAL_FILE
            ressha = check_sha(ressha)
            print("ressha: " + ressha + "\n")
            if ressha == ES_FINAL_SHA:
                print("Right SHA\n")
                update_process_final(ES_FINAL_FILE,ES_FINAL_VER)
                print("Installdir is " + INSTALLDIR)
                adding_services(INSTALLDIR + "\\" + ES_FINAL_VER)
            else:
                print("Wrong SHA\n")
                RESCHECK = 0
        else:
            print(Fore.WHITE + ES_FINAL_FILE + " is not inside.")
            print(Fore.WHITE + "")
            RESCHECK = 0

    else:
        print("Unknown error.")

### Auxiliary functions ################################################################################################


def run(cmd):
    ERROR = 0
    completed = 1
    cmd = "Powershell -Executionpolicy byPass -Command " + cmd
    try:
        completed = str(subprocess.check_output(cmd))
    except:
        print(Fore.WHITE + "Can't get pid of ES, maybe is not running.")
        print(Fore.WHITE + "")
        ERROR = 1

    if ERROR == 1:
        completed = 0

    return completed


def find_started(fil):
    global TIMEOUT
    print(Fore.GREEN + "Waiting for starting ElasticSearch...")
    print(Fore.WHITE + "")
    count = 0
    while TIMEOUT > count:
        found = 0
        with open(fil, 'r') as f:
            data = f.read()
            if "] started" in data:
                found = 1
                count = TIMEOUT
            f.close()
            time.sleep(1)
            count += 1

    return found


def set_variables(es_install_dir,es_config_dir):
    print("")
    print("Setting environment variables.\n")

    cmd3 = "powershell -command [System.Environment]::SetEnvironmentVariable('ES_HOME'," + "\'" + es_install_dir + "\'" + ",'Machine')"

    try:
        os.system(cmd3)
    except:
        print(Fore.WHITE + "Can't Set ES_HOME environment variable.")
        print(Fore.WHITE + "")

    cmd4 = "powershell -command [System.Environment]::SetEnvironmentVariable('ES_PATH_CONF'," + "\'" + es_config_dir + "\'" + ",'Machine')"

    try:
        os.system(cmd4)
    except:
        print(Fore.WHITE + "Can't Set ES_PATH_CONF environment variable.")
        print(Fore.WHITE + "")

    print("")

def es_killing(es_dir):
   rescmd = es_running(es_dir)
   if int(rescmd) > 0:
       print(Fore.GREEN + "Killing existing ES process.")
       print(Fore.WHITE + "")
       cmd = "TASKKILL /F /PID " + str(rescmd) + " >NUL"
       try:
           os.system(cmd)
       except:
           print(Fore.WHITE + "Can't kill ES process")
           print(Fore.WHITE + "")


def es_running(es_dir):
   global ES_PORT
   global ES_INTERM_VER
   global ES_FINAL_VER

   TMP_FILE = "tmp_file.txt"
   cmd= ""
   rf = ""

   cmd = "netstat -anbo | findstr LISTEN | findstr 127.0.0.1:" + str(ES_PORT) + "| .\\awk.exe " + '\"{print $5}\"' + " > " + TMP_FILE

   try:
       os.system(cmd)
   except:
       print(Fore.WHITE + "Can't see any ES process running.")
       print(Fore.WHITE + "")

   try:
       rf = read_file(TMP_FILE)
   except:
       print("Error with temporary file, check permissions to write on this folder.")

   if rf:
       rescmd = int(rf)
   else:
       rescmd = 0
   cmd = "del /F /Q " + ".\\" + TMP_FILE
   os.system(cmd)
   return rescmd


def check_awk():
    return check_file(".\\", "awk.exe")

def check_es_variables():
    TMP_FILE = "tmp_file.txt"
    found = 0
    print("")
    cmd1 = "set | findstr ES_HOME > " + TMP_FILE
    os.system(cmd1)
    resFind1 = read_file(TMP_FILE)
    cmd2 = "set | findstr ES_PATH_CONF > " + TMP_FILE
    os.system(cmd2)
    resFind2 = read_file(TMP_FILE)
    print(str(resFind1))
    print(str(resFind2))
    if "ES_HOME" in resFind1 or "ES_PATH_CONF" in resFind2:
        found = 1
    return found


if __name__ == '__main__':
    try:
        program()
    except KeyboardInterrupt:
        print("Bye\n")
        pass

