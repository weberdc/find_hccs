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

set HCCS_DIR=%BEHAVIOUR%\hccs-%FSA_V%-%THRESHOLD%
set REPORTS_DIR=%HCCS_DIR%\reports
set VIS_DIR=%HCCS_DIR%\figures

if not exist "%VIS_DIR%" mkdir %VIS_DIR%

set N=%5
if "%N%"=="" set N=5
set EXT=pdf
rem always use -u|--user, n = 5
set DTM_VIS=python %LCN_BIN%\build_hccs_docsim_vis.py -u -n %N% --normalise-lower-bound --no-title

rem set OPTS=-v
set OPTS=%5 %6 %7 %8 %9



@echo Started: %date% %time% 1>&2

rem 15m

set WINDOW=15m
set KEY=%WINDOW%
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%



set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%



rem 60m

set WINDOW=60m
set KEY=%WINDOW%
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%



set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%



rem 360m

set WINDOW=360m
set KEY=%WINDOW%
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%



set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%



rem 1440m

set WINDOW=1440m
set KEY=%WINDOW%
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%


set KEY=%WINDOW%-0.5
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%


set KEY=%WINDOW%-0.7
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%



set KEY=%WINDOW%-0.9
set HCC=%FSA_V%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
rem goto :eof
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%KNN%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%

set HCC=%THRESHOLD%
set FILEBASE=%CORPUS%-%BEHAVIOUR%-%KEY%-hccs-%HCC%
set C_TITLE=%CORPUS% %KEY% %HCC% (%N% chars)
@echo %KEY% %HCC% (%N% chars): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-chars.%EXT% -t "%C_TITLE%" %OPTS%
set W_TITLE=%CORPUS% %KEY% %HCC% (%N% words)
@echo %KEY% %HCC% (%N% words): %date% %time% 1>&2
%DTM_VIS% -i %REPORTS_DIR%\%FILEBASE%-analysis.json -o %VIS_DIR%\%FILEBASE%-dtm-%N%-words.%EXT% -t "%W_TITLE%" -w %OPTS%



@echo Ended:   %date% %time% 1>&2