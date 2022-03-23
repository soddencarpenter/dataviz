@echo off
set DIR=f:\apps\mysql\mysql-8.0.28-winx64

@REM we will put the mysql files in the directory of the script
set DATADIR="%~dp0mysqldata"
@REM set DATADIR="%CD%mysqldata"


%DIR%\bin\mysqld --basedir "%DIR%" --datadir=%DATADIR% --secure_file_priv="" %*
