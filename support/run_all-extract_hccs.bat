@echo off

rem extract HCCs from the 15m, 60m, 360m and 1440m combined LCNs, including
rem alpha = 0.5, 0.7 and 0.9

rem Usage: %0 CORPUS BEHAVIOUR THETA THRESHOLD

@echo Started: %date% %time% 1>&2

rem parameterise this
rem set BEHAVIOUR=retweets
rem set CORPUS=saelec
set CORPUS=%1
set BEHAVIOUR=%2
set THETA=%3
set THRESHOLD=%4
set OUT_DIR=%BEHAVIOUR%\hccs-fsa_v_%THETA%-t_%THRESHOLD%
set OUT_PREFIX=%CORPUS%-%BEHAVIOUR%

if not exist "%OUT_DIR%" mkdir -p %OUT_DIR%

set EXTRACT_HCCS=python %LCN_BIN%\extract_hccs.py

rem set OPTS=-v
set OPTS=

rem set THRESHOLD=0.3
set T_OPTS=--strategy THRESHOLD -t %THRESHOLD% 

set KNN_OPTS=--strategy KNN

rem set THETA=0.5
set FSA_V_OPTS=--strategy FSA_V --theta %THETA%

set WINDOW=15m
set KEY=%WINDOW%
echo %KEY%:     THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%:     KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%:     FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.5
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.7
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.9
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%

set WINDOW=60m
set KEY=%WINDOW%
echo %KEY%:     THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%:     KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%:     FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.5
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.7
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.9
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%

set WINDOW=360m
set KEY=%WINDOW%
echo %KEY%:     THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%:     KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%:     FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.5
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.7
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.9
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%

set WINDOW=1440m
set KEY=%WINDOW%
echo %KEY%:     THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%:     KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%:     FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.5
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.7
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%
set KEY=%WINDOW%-0.9
echo %KEY%: THRESHOLD %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-t_%THRESHOLD%.graphml %T_OPTS% %OPTS%
echo %KEY%: KNN       %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-knn.graphml %KNN_OPTS% %OPTS%
echo %KEY%: FSA_V     %date% %time% 1>&2
%EXTRACT_HCCS% -i %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml -o %OUT_DIR%\%OUT_PREFIX%-%KEY%-hccs-fsa_v_%THETA%.graphml %FSA_V_OPTS% %OPTS%


@echo Ended:   %date% %time% 1>&2
