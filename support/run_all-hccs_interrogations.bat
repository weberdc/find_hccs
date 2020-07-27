@echo off

if "%5"=="" goto :eof

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
rem set TWEETS=-t sapol_tweets.json.gz
set TWEETS=-t %5
rem set BOTS=-b ..\saelec\all_the_botornot_results.json
set BOTS=
if not "%6"=="" set BOTS=-b %6



set EXTRACT=python %LCN_BIN%\interrogate_hccs.py %TWEETS% %BOTS% 
rem set OPTS=-v
set OPTS=

@echo Started: %date% %time% 1>&2

if not exist "%REPORTS_DIR%" mkdir %REPORTS_DIR%

rem ------ 15m ------
set WINDOW=15m
set KEY=%WINDOW%
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


rem ------ 60m ------
set WINDOW=60m
set KEY=%WINDOW%
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


rem ------ 360m ------
set WINDOW=360m
set KEY=%WINDOW%
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


rem ------ 1440m ------
set WINDOW=1440m
set KEY=%WINDOW%
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%KNN%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%

set HCC=%THRESHOLD%
echo %KEY% %HCC%: %date% %time% 1>&2
set HCCS_BASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set LCN=%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml
%EXTRACT% --lcn %BEHAVIOUR%\%LCN% --hccs %HCCS_DIR%\%HCCS_BASE%.graphml -o %REPORTS_DIR%\%HCCS_BASE%-analysis.json %OPTS%


@echo Ended:   %date% %time% 1>&2
