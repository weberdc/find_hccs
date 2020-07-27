@echo off

if "%4"=="" goto bad

set COMPARE=python %LCN_BIN%\nodes_in_common.py -p label

set CORPUS=%1
set BEHAVIOUR=%2
set FSA_V=fsa_v_%3
set THRESHOLD=t_%4
set KNN=knn
if not "%5"=="" set ALPHA=-%5

rem set OPTS=-v
set OPTS=--layout 2

@echo Started: %date% %time% 1>&2

rem echo corpus %CORPUS%
rem echo behaviour %BEHAVIOUR%
rem echo hcc %HCC%
rem echo alpha %ALPHA%
rem goto :eof

set HCCS_DIR=%BEHAVIOUR%\hccs-%FSA_V%-%THRESHOLD%

set FILEBASE=%HCCS_DIR%\%CORPUS%-%BEHAVIOUR%
set WINDOW=15m
@echo %WINDOW%%ALPHA%
@echo %WINDOW%%ALPHA% %date% %time% 1>&2
%COMPARE% %FILEBASE%-%WINDOW%%ALPHA%-hccs-%FSA_V%.graphml  ^
          %FILEBASE%-%WINDOW%%ALPHA%-hccs-%KNN%.graphml  ^
          %FILEBASE%-%WINDOW%%ALPHA%-hccs-%THRESHOLD%.graphml %OPTS%
@echo.

set WINDOW=60m
@echo %WINDOW%%ALPHA%
@echo %WINDOW%%ALPHA% %date% %time% 1>&2
%COMPARE% %FILEBASE%-%WINDOW%%ALPHA%-hccs-%FSA_V%.graphml  ^
          %FILEBASE%-%WINDOW%%ALPHA%-hccs-%KNN%.graphml  ^
          %FILEBASE%-%WINDOW%%ALPHA%-hccs-%THRESHOLD%.graphml %OPTS%
@echo.

set WINDOW=360m
@echo %WINDOW%%ALPHA%
@echo %WINDOW%%ALPHA% %date% %time% 1>&2
%COMPARE% %FILEBASE%-%WINDOW%%ALPHA%-hccs-%FSA_V%.graphml  ^
          %FILEBASE%-%WINDOW%%ALPHA%-hccs-%KNN%.graphml  ^
          %FILEBASE%-%WINDOW%%ALPHA%-hccs-%THRESHOLD%.graphml %OPTS%
@echo.

set WINDOW=1440m
@echo %WINDOW%%ALPHA%
@echo %WINDOW%%ALPHA% %date% %time% 1>&2
%COMPARE% %FILEBASE%-%WINDOW%%ALPHA%-hccs-%FSA_V%.graphml  ^
          %FILEBASE%-%WINDOW%%ALPHA%-hccs-%KNN%.graphml  ^
          %FILEBASE%-%WINDOW%%ALPHA%-hccs-%THRESHOLD%.graphml %OPTS%
@echo.


goto :cleanup

:bad

echo Usage: %0 CORPUSNAME BEHAVIOUR FSA_V_param THRESHOLD_param [ALPHA]
echo e.g. %0 sapol retweets 0.3 0.1 0.7
echo e.g. %0 sapol retweets 0.3 0.1

:cleanup

set CORPUS=
set BEHAVIOUR=
set ALPHA=
set HCC=
set WINDOW=
set FSA_V=
set KNN=
set THRESHOLD=

@echo End: %date% %time% 1>&2
