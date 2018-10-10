# About the image
* Docker container com Django 2.x, python 3.6.x, bootstrap e bibliotecas de conexão ao SQL Server in a Linux container.

# Tags
docker pull bicbic/webdba:0.3

0:3 [dockerfile](https://hub.docker.com/r/microsoft/mssql-server-linux/).

# How to use this image
Pull the Docker image:
>``docker pull bicbic/mssqldba:1.1``

Run a container in interactive mode:
>``docker run -it mcr.microsoft.com/mssql-tools``

Try out sqlcmd/bcp:
> ``root@1396d2e50672:/# sqlcmd``

```shell
Microsoft (R) SQL Server Command Line Tool
Version 13.1.0007.0 Linux
Copyright (c) 2012 Microsoft. All rights reserved.

usage: sqlcmd [-U login id] [-P password]<br>
[-S server or Dsn if -D is provided]``
[-H hostname] [-E trusted connection]
[-N Encrypt Connection][-C Trust Server Certificate]
[-d use database name] [-l login timeout] [-t query timeout]
[-h headers] [-s colseparator] [-w screen width]
[-a packetsize] [-e echo input] [-I Enable Quoted Identifiers]
[-c cmdend]
[-q "cmdline query"] [-Q "cmdline query" and exit]
[-m errorlevel] [-V severitylevel] [-W remove trailing spaces]
[-u unicode output] [-r[0|1] msgs to stderr]
[-i inputfile] [-o outputfile]
[-k[1|2] remove[replace] control characters]
[-y variable length type display width]
[-Y fixed length type display width]
[-p[1] print statistics[colon format]]
[-R use client regional setting]
[-K application intent]
[-M multisubnet failover]
[-b On error batch abort]
[-D Dsn flag, indicate -S is Dsn]
[-X[1] disable commands, startup script, environment variables [and exit]]
[-x disable variable substitution]
[-? show syntax summary]
```

Example:

``# sqlcmd -S 127.0.0.1 -U sa -P MyPassword100``

>``select @@version``

>``go``

# Dockerfile

Check out the [Dockerfile](https://github.com/BicBic/mssql-python3x-docker/Dockerfile) on GitHub. Help us maintain/extend it by sending in your pull requests.

Documentation
To learn more about sqlcmd and bcp, check out
+ [sqlcmd](https://docs.microsoft.com/en-us/sql/tools/sqlcmd-utility?view=sql-server-2017)
+ [bcp](https://docs.microsoft.com/en-us/sql/tools/bcp-utility?view=sql-server-2017)

# Related Images
SQL Server for Linux Containers: [microsoft/mssql-server-linux](https://hub.docker.com/r/microsoft/mssql-server-linux/)
