
set DIR=f:\apps\mysql\mysql-8.0.28-winx64

@REM we will put the mysql files in the directory of the script
set DATADIR="%~dp0mysqldata"


@rem 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: 1(mdycGnKsOB
%DIR%\bin\mysqld --basedir "%DIR%" --datadir=%DATADIR% --secure_file_priv="" %*