@echo off

if "%4"=="" goto :eof

rem set CORPUS=sapol
set CORPUS=%1
rem set BEHAVIOUR=retweets
set BEHAVIOUR=%2
rem set FSA_V=fsa_v_0.3
set FSA_V=fsa_v_%3
rem set THRESHOLD=t_0.1
set THRESHOLD=t_%4
set KNN=knn


rem set FSA_V=fsa_v_0.3
rem set THRESHOLD=t_0.1
rem set KNN=knn
rem set CORPUS=sapol
rem set BEHAVIOUR=retweets
set HCCS_DIR=%BEHAVIOUR%\hccs-%FSA_V%-%THRESHOLD%
set REPORTS_DIR=%HCCS_DIR%\reports

set REPORT=python %LCN_BIN%\run_hccs_reports.py

@echo Started: %date% %time% 1>&2

if not exist "%REPORTS_DIR%" mkdir %REPORTS_DIR%

rem ------ 15m ------
set WINDOW=15m
set KEY=%WINDOW%
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


rem ------ 60m ------
set WINDOW=60m
set KEY=%WINDOW%
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


rem ------ 360m ------
set WINDOW=360m
set KEY=%WINDOW%
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


rem ------ 1440m ------
set WINDOW=1440m
set KEY=%WINDOW%
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set FILEBASE=%REPORTS_DIR%\%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
%REPORT% -i %FILEBASE%-analysis.json -o %FILEBASE%-report.csv


@echo Ended:   %date% %time% 1>&2