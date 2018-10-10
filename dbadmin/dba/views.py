#  ____  _      ____  _
# | __ )(_) ___| __ )(_) ___
# |  _ \| |/ __|  _ \| |/ __|
# | |_) | | (__| |_) | | (__
# |____/|_|\___|____/|_|\___|
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.timezone import localdate
from django import template
from datetime import datetime 
from .models import SQLpy
from .models import log
from .models import configfile
# from .forms import PostForm

DEBUG = True

# register = template.Library()
# @register.filter(prod=True)

## import pdb; pdb.set_trace()

# Create your views here.
def index(request):
    # """Exibe a pagina principal da aplicacao."""
    # context = {
    #     'hide_new_button': True,
    #     #'priorities': Event.priorities_list,
    #     'today': localdate(),
    # if request.method == "POST":
    if request.POST:        
        if request.POST.get('cc_prod') != None:
            if 'on' in request.POST.get('cc_prod'):
                request.session['cc_prod'] = 1
            else:
                request.session['cc_prod'] = 0
        else:
            request.session['cc_prod'] = 0

        if request.POST.get('cc_dth') != None:
            if 'on' in request.POST.get('cc_dth'):
                request.session['cc_dth'] = 1
            else:
                request.session['cc_dth'] = 0
        else:
            request.session['cc_dth'] = 0

        # print (str(request.session.get('cc_prod')), str(request.session.get('cc_dth')))

    context = {
        'prod': request.session.get('cc_prod',1),
        'dth': request.session.get('cc_dth',1),
    }

    return render(request, 'index.html', context)
    # return render(RequestContext(request), 'index.html')
    # return render(request, 'index.html', {'form': form})

def checkbackup(request):
  #return render_to_response('check-backup.html')
  return render(request, 'check-backup.html')

def verBloqueio(request):
    results = []
    total = 0

    # prod = 1, dth = 2, all = 3
    ambiente = '3'
    if request.session.get('cc_prod',1) == 1 and request.session.get('cc_dth',1) == 0: 
        ambiente = '1'
    if request.session.get('cc_prod',1) == 0 and request.session.get('cc_dth',1) == 1: 
        ambiente = '2'
    if request.session.get('cc_prod',1) == 1 and request.session.get('cc_dth',1) == 1: 
        ambiente = '3'

    settings = configfile()
    host = settings.item('DB_HOST')
    db = settings.item('DB_NAME')
    usr = settings.item('DB_USER')
    passwd = settings.item('DB_PASSWORD')

    tsql = 'select  s.name, se.IP + \',\' + convert(varchar, Port) as [IP] ' + \
           'from    [msdb].[dbo].[sysmanagement_shared_registered_servers_internal] s ' + \
           'join	DBA.dbo.SERVIDOR se on s.name = se.nome ' + \
           'where   s.server_group_id = 1 ' + \
           'and		se.Ativo = \'S\' ' + \
           'and     se.Ambiente = ' + ('1' if ambiente == '1' else '2' if ambiente == '2' else 'se.Ambiente') + \
           ' order by s.name'

    connServers = SQLpy(host, db, usr, passwd) #conexao 172.19.1.132=SV2KSQLPRD2
    servers = connServers.execute(tsql)
    tsql = 'sp_bloqueio'
    for server in servers:
        # s = server.name
        # if s.find('\\') > 0:
        #     s = server.IP + '\\' + s[s.find('\\')+1:]
        # else:
        #     s = server.IP
        conn = SQLpy(server.IP, 'DBA', usr, passwd) #conexao
        rows = conn.execute(tsql)
        for r in rows:
            if r.login != 'sem bloqueios':
                results.append(r)
                total += 1
        conn.close()
    connServers.close()

    context = {
        'events': results,
        'total': total,
        'today': datetime.now(),
        'ambiente': ambiente,
    }
    
    return render(request, 'verBloqueios.html', context)

# *********************************
# ***********JobsRunning***********
# *********************************
def JobsRunning(request):

    # prod = 1, dth = 2, all = 3
    ambiente = '3'
    if request.session.get('cc_prod',1) == 1 and request.session.get('cc_dth',1) == 0: 
        ambiente = '1'
    if request.session.get('cc_prod',1) == 0 and request.session.get('cc_dth',1) == 1: 
        ambiente = '2'
    if request.session.get('cc_prod',1) == 1 and request.session.get('cc_dth',1) == 1: 
        ambiente = '3'

    results = []
    total = 0
    tsql = 'select  s.name, se.IP + \',\' + convert(varchar, Port) as [IP] ' + \
           'from    [msdb].[dbo].[sysmanagement_shared_registered_servers_internal] s ' + \
           'join	DBA.dbo.SERVIDOR se on s.name = se.nome ' + \
           'where   s.server_group_id = 1 ' + \
           'and		se.Ativo = \'S\' ' + \
           'and     se.Ambiente = ' + ('1' if ambiente == '1' else '2' if ambiente == '2' else 'se.Ambiente') + \
           ' order by s.name'

    settings = configfile()
    host = settings.item('DB_HOST')
    db = settings.item('DB_NAME')
    usr = settings.item('DB_USER')
    passwd = settings.item('DB_PASSWORD')

    connServers = SQLpy(host, db, usr, passwd) #conexao
    servers = connServers.execute(tsql)
    tsql = 'sp_jobs_running'
    for server in servers:
        conn = SQLpy(server.IP, 'DBA', usr, passwd) #conexao
        rows = conn.execute(tsql)
        for r in rows:
            results.append(r)
            total += 1
        conn.close()
    connServers.close()

    context = {
        'events': results,
        'total': total,
        'today': datetime.now(),
        'ambiente': ambiente,
    }
    
    return render(request, 'JobsRunning.html', context)

# *********************************
# ***********verErrorlog***********
# *********************************
def verErrorlog(request):
    results = []
    total = 0

    # prod = 1, dth = 2, all = 3
    ambiente = '3'
    if request.session.get('cc_prod',1) == 1 and request.session.get('cc_dth',1) == 0: 
        ambiente = '1'
    if request.session.get('cc_prod',1) == 0 and request.session.get('cc_dth',1) == 1: 
        ambiente = '2'
    if request.session.get('cc_prod',1) == 1 and request.session.get('cc_dth',1) == 1: 
        ambiente = '3'

    tsql = 'sp_sql_erro 500, ' + ambiente
    if (DEBUG): log('verErrorlog ' + tsql)

    settings = configfile()
    host = settings.item('DB_HOST')
    db = settings.item('DB_NAME')
    usr = settings.item('DB_USER')
    passwd = settings.item('DB_PASSWORD')

    conn = SQLpy(host, db, usr, passwd) #conexao
    rows = conn.execute(tsql)
    
    for row in rows:
        results.append(row)
        total += 1

    conn.close()

    context = {
        'events': results,
        'total': total,
        'today': datetime.now(),
        'ambiente': ambiente,
    }
    
    return render(request, 'errorlog.html', context)

def verbackup(request):

    # prod = 1, dth = 2, all = 3
    ambiente = '3'
    if request.session.get('cc_prod',1) == 1 and request.session.get('cc_dth',1) == 0: 
        ambiente = '1'
    if request.session.get('cc_prod',1) == 0 and request.session.get('cc_dth',1) == 1: 
        ambiente = '2'
    if request.session.get('cc_prod',1) == 1 and request.session.get('cc_dth',1) == 1: 
        ambiente = '3'

    results = {}
    res = []
    total = 0
    # tsql = 'select  s.name as [servidor], se.ip, se.Port as [porta] ' + \
    #        'from    [msdb].[dbo].[sysmanagement_shared_registered_servers_internal] s ' + \
    #        'join	DBA.dbo.SERVIDOR se on s.name = se.nome ' + \
    #        'where   s.server_group_id = 1 ' + \
    #        'and		se.Ativo = \'S\' ' + \
    #        'order by s.name'
    tsql = 'sp_list_servers ' + ambiente

    settings = configfile()
    host = settings.item('DB_HOST')
    db = settings.item('DB_NAME')
    usr = settings.item('DB_USER')
    passwd = settings.item('DB_PASSWORD')

    connServers = SQLpy(host, db, usr, passwd) #conexao
    servers = connServers.execute(tsql)
    columns = [column[0] for column in servers.description]
    for server in servers:
        s = server.ip + ',' + str(server.porta)
        # print (s)
        conn = SQLpy(s, 'DBA', usr, passwd) #conexao
        # tsql = 'sp_CheckBackup \'' + server.ip + '\', ' + str(server.porta)
        tsql = 'sp_CheckBackup'
        rows = conn.execute(tsql)
        for r in rows:
            results = dict(zip(columns, server))
            results['database_name'] = r.database_name
            results['backup_start'] = r.backup_start
            results['backup_finish'] = r.backup_finish
            results['total_backup'] = r.total_backup
            results['device_name'] = r.device_name
            res.append(results)
            # resuts.append(r)            

        total += 1
        conn.close()
    connServers.close()

    res = sorted(res, key=lambda x: ((x['backup_start']).strftime("%y/%m/%d"), x['row']))
    # results = sorted(results, key=lambda server: (server.backup_start, server.servidor))

    context = {
        'events': res,
        'total': total,
        'today': localdate(),
        'ambiente': ambiente,
    }
    
    return render(request, 'backup.html', context)

def backupDetails(request, servidor: str, ip: str, porta: int):
    results = []
    total = 0
    tsql = 'sp_CheckBackupDetail '

    settings = configfile()
    db = settings.item('DB_NAME')
    usr = settings.item('DB_USER')
    passwd = settings.item('DB_PASSWORD')

    s = ip + ',' + str(porta)
    conn = SQLpy(s, db, usr, passwd) #conexao
    rows = conn.execute(tsql)
    
    for row in rows:
        results.append(row)
        total += 1

    conn.close()

    context = {
        'events': results,
        'total': total,
        'today': localdate(),
        'nomeservidor': servidor
    }
    
    return render(request, 'backupDetails.html', context)

def DuplicateIndex(request):
    results = {}
    res = []
    total = 0
    tsql = 'select  s.name as [servidor], se.ip, se.Port as [porta] ' + \
           'from    [msdb].[dbo].[sysmanagement_shared_registered_servers_internal] s ' + \
           'join	DBA.dbo.SERVIDOR se on s.name = se.nome ' + \
           'where   s.server_group_id = 1 ' + \
           'and		se.Ativo = \'S\' ' + \
           'order by s.name'
    connServers = SQLpy('172.19.1.132', 'DBA') #conexao no SV2KSQLPRD2
    servers = connServers.execute(tsql)
    columns = [column[0] for column in servers.description]
    for server in servers:
        s = server.ip + ',' + str(server.porta)
        # print (s)
        conn = SQLpy(s, 'DBA') #conexao
        # tsql = 'sp_CheckBackup \'' + server.ip + '\', ' + str(server.porta)
        tsql = 'sp_CheckBackup'
        rows = conn.execute(tsql)
        for r in rows:
            results = dict(zip(columns, server))
            results['database_name'] = r.database_name
            results['backup_start'] = r.backup_start
            results['backup_finish'] = r.backup_finish
            results['total_backup'] = r.total_backup
            results['device_name'] = r.device_name
            res.append(results)
            # resuts.append(r)            

        total += 1
        conn.close()
    connServers.close()

    res = sorted(res, key=lambda x: ((x['backup_start']).strftime("%y/%m/%d"), x['row']))
    # results = sorted(results, key=lambda server: (server.backup_start, server.servidor))

    context = {
        'events': res,
        'total': total,
        'today': localdate(),
    }
    
    return render(request, 'backup.html', context)


def indextst(request):
    tsql = 'select	top 1 name from	dbo.Mensagens'
    conn = SQLpy('VM2K8SQLDEV1', 'DBA') #conexao
    rows = conn.execute(tsql)
    msg = ''
    for row in rows:
        msg += str(row.name)

    SQLpy.close

    return HttpResponse(msg)

