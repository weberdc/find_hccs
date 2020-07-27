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

set HCC=%FSA_V%
set FILEBASE=%HCCS_DIR%\%CORPUS%-%BEHAVIOUR%
@echo FSA_V%ALPHA%
@echo FSA_V%ALPHA% %date% %time% 1>&2
%COMPARE% %FILEBASE%-15m%ALPHA%-hccs-%HCC%.graphml  ^
          %FILEBASE%-60m%ALPHA%-hccs-%HCC%.graphml  ^
          %FILEBASE%-360m%ALPHA%-hccs-%HCC%.graphml ^
          %FILEBASE%-1440m%ALPHA%-hccs-%HCC%.graphml %OPTS%
@echo.

set HCC=%KNN%
set FILEBASE=%HCCS_DIR%\%CORPUS%-%BEHAVIOUR%
@echo kNN%ALPHA%
@echo kNN%ALPHA% %date% %time% 1>&2
%COMPARE% %FILEBASE%-15m%ALPHA%-hccs-%HCC%.graphml  ^
          %FILEBASE%-60m%ALPHA%-hccs-%HCC%.graphml  ^
          %FILEBASE%-360m%ALPHA%-hccs-%HCC%.graphml ^
          %FILEBASE%-1440m%ALPHA%-hccs-%HCC%.graphml %OPTS%
@echo.

set HCC=%THRESHOLD%
set FILEBASE=%HCCS_DIR%\%CORPUS%-%BEHAVIOUR%
@echo THRESHOLD%ALPHA%
@echo THRESHOLD%ALPHA% %date% %time% 1>&2
%COMPARE% %FILEBASE%-15m%ALPHA%-hccs-%HCC%.graphml  ^
          %FILEBASE%-60m%ALPHA%-hccs-%HCC%.graphml  ^
          %FILEBASE%-360m%ALPHA%-hccs-%HCC%.graphml ^
          %FILEBASE%-1440m%ALPHA%-hccs-%HCC%.graphml %OPTS%
@echo.

goto :cleanup

:bad

echo Usage: %0 CORPUSNAME BEHAVIOUR FSA_V_param THRESHOLD_param [ALPHA]
echo e.g. %0 sapol retweets 0.3 0.1 -0.7

:cleanup

set CORPUS=
set BEHAVIOUR=
set ALPHA=
set HCC=

@echo End: %date% %time% 1>&2
