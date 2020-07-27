@echo off

rem (election) C:\Users\derek\Documents\PhD\local_analysis\coordination\sapol-tmp>python %LCN_BIN%\nodes_in_common.py retweets\hccs\sapol-retweets-15m-hccs-fsa_v_0.5.graphml retweets\hccs\sapol-retweets-60m-hccs-fsa_v_0.5.graphml retweets\hccs\sapol-retweets-360m-hccs-fsa_v_0.5.graphml retweets\hccs\sapol-retweets-1440m-hccs-fsa_v_0.5.graphml

if "%5"=="" goto bad

set COMPARE=python %LCN_BIN%\nodes_in_common.py -p label

set CORPUS=%1
set BEHAVIOUR=%2
set FSA_V=fsa_v_%3
set THRESHOLD=t_%4
set WINDOW=%5
set KNN=knn
rem set ALPHA=
rem if not "%6"=="" set ALPHA=-%6

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
@echo FSA_V %WINDOW%
@echo FSA_V %WINDOW% %date% %time% 1>&2
%COMPARE% %FILEBASE%-%WINDOW%-hccs-%HCC%.graphml  ^
          %FILEBASE%-%WINDOW%-0.5-hccs-%HCC%.graphml  ^
          %FILEBASE%-%WINDOW%-0.7-hccs-%HCC%.graphml ^
          %FILEBASE%-%WINDOW%-0.9-hccs-%HCC%.graphml %OPTS%
@echo.

set HCC=%KNN%
set FILEBASE=%HCCS_DIR%\%CORPUS%-%BEHAVIOUR%
@echo kNN %WINDOW%
@echo kNN %WINDOW% %date% %time% 1>&2
%COMPARE% %FILEBASE%-%WINDOW%-hccs-%HCC%.graphml  ^
          %FILEBASE%-%WINDOW%-0.5-hccs-%HCC%.graphml  ^
          %FILEBASE%-%WINDOW%-0.7-hccs-%HCC%.graphml ^
          %FILEBASE%-%WINDOW%-0.9-hccs-%HCC%.graphml %OPTS%
@echo.

set HCC=%THRESHOLD%
set FILEBASE=%HCCS_DIR%\%CORPUS%-%BEHAVIOUR%
@echo THRESHOLD %WINDOW%
@echo THRESHOLD %WINDOW% %date% %time% 1>&2
%COMPARE% %FILEBASE%-%WINDOW%-hccs-%HCC%.graphml  ^
          %FILEBASE%-%WINDOW%-0.5-hccs-%HCC%.graphml  ^
          %FILEBASE%-%WINDOW%-0.7-hccs-%HCC%.graphml ^
          %FILEBASE%-%WINDOW%-0.9-hccs-%HCC%.graphml %OPTS%
@echo.

goto :cleanup

:bad

echo Usage: %0 CORPUSNAME BEHAVIOUR FSA_V_param THRESHOLD_param WINDOW
echo e.g. %0 sapol retweets 0.3 0.1 15m

:cleanup

set CORPUS=
set BEHAVIOUR=
rem set ALPHA=
set HCC=
set WINDOW=
set FSA_V=
set KNN=
set THRESHOLD=

@echo End: %date% %time% 1>&2
