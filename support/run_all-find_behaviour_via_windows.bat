@echo off

rem produce all CSVs from raw

@echo Started: %date% %time% 1>&2

rem parameterise this
set BEHAVIOUR=retweets
set CORPUS=sapol
set DURATION_OPTS=-s 20180303_000000 -e 20180320_133000
set T_COL_OPT=--target ot_id

if not exist "%BEHAVIOUR%" mkdir %BEHAVIOUR%
if not exist "%BEHAVIOUR%\15m" mkdir %BEHAVIOUR%\15m
if not exist "%BEHAVIOUR%\60m" mkdir %BEHAVIOUR%\60m
if not exist "%BEHAVIOUR%\360m" mkdir %BEHAVIOUR%\360m
if not exist "%BEHAVIOUR%\1440m" mkdir %BEHAVIOUR%\1440m

set FIND_BEHAVIOUR=python %LCN_BIN%\find_behaviour_via_windows.py -i %CORPUS%-%BEHAVIOUR%.csv %DURATION_OPTS% %T_COL_OPT%

echo 15m
%FIND_BEHAVIOUR% -o %BEHAVIOUR%\15m   -w   15m -v 
echo 60m
%FIND_BEHAVIOUR% -o %BEHAVIOUR%\60m   -w   60m -v 
echo 360m
%FIND_BEHAVIOUR% -o %BEHAVIOUR%\360m  -w  360m -v 
echo 1440m
%FIND_BEHAVIOUR% -o %BEHAVIOUR%\1440m -w 1440m -v 

@echo Ended:   %date% %time% 1>&2
